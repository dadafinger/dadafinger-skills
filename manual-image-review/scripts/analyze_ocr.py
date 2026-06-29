#!/usr/bin/env python3
"""매뉴얼 docx 이미지 검수 3단계: OCR 결과 분석 -> 트리아지 큐 생성.

사용법:
    python3 analyze_ocr.py <outdir> [--keywords kw1,kw2] [--no-jpg-flag]

입력(outdir): mapping.json, ocr_results.jsonl
출력(outdir):
    triage_queue.txt   육안 검수 대상(본문 순서) + 사유 + 섹션  <- 핵심 산출물
    ocr_flags.json     기계가독 플래그 전체
    ui_subtitles.txt   화면 타이틀-부제 쌍 (부제 오류 빠른 스캔용)
    findings_auto.md   자동 검출 리포트 스켈레톤

한글 노이즈 필터: OCR이 영문 UI를 한글 단일 글자('이','에' 등)로 오독하는 일이 많아
2글자 이상 연속 한글만 실제 잔존으로 취급한다.
"""
import argparse, json, re
from collections import OrderedDict, defaultdict

DEFAULT_KEYWORDS = ['product', 'company-a', '목동', '테스트클러스터', 'co_', 'operator-a']


def ip_class(ip):
    a = [int(x) for x in ip.split('.')]
    if any(x > 255 for x in a):
        return None
    if a[0] == 10 or (a[0] == 172 and 16 <= a[1] <= 31) or (a[0] == 192 and a[1] == 168):
        return 'private'
    if a[0] == 127:
        return 'loopback'
    if a[0] == 169 and a[1] == 254:
        return 'linklocal'
    if a[0] == 0 or a[0] >= 224:
        return 'special'
    return 'PUBLIC'


def typo_hint(ip):
    if ip.startswith('172.168.'):
        return ' (172.16 사설대역 오타 의심)'
    if ip.startswith('192.198.'):
        return ' (192.168 오타/OCR 오독 의심)'
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    ap.add_argument('--keywords', default='', help='추가 키워드 (쉼표 구분)')
    ap.add_argument('--no-jpg-flag', action='store_true',
                    help='jpg 전수 플래그 끄기 (jpg가 다이어그램·구버전 캡처가 아닌 문서일 때)')
    args = ap.parse_args()
    out = args.outdir
    keywords = DEFAULT_KEYWORDS + [k for k in args.keywords.split(',') if k]

    ocr = {}
    with open(f'{out}/ocr_results.jsonl', encoding='utf-8') as f:
        for line in f:
            o = json.loads(line)
            ocr[o['file']] = o['text']
    with open(f'{out}/mapping.json', encoding='utf-8') as f:
        images = json.load(f)

    # 고유 파일 -> 첫 등장 순서/섹션(들)
    uniq = OrderedDict()
    for r in images:
        h = r['heading']
        sec = ' > '.join(h[k] for k in sorted(h, key=int)) if h else '(표지/머리말)'
        u = uniq.setdefault(r['file'], {'order': r['order'], 'secs': [], 'px': r.get('px'),
                                        'eff_dpi': r.get('eff_dpi')})
        if sec not in u['secs']:
            u['secs'].append(sec)

    flags = defaultdict(list)   # file -> [사유,...]
    detail = defaultdict(dict)

    # 1) 한글 잔존 (2글자 이상 토큰만)
    for fn, t in ocr.items():
        toks = re.findall(r'[가-힣]{2,}', t)
        if toks:
            flags[fn].append('한글')
            detail[fn]['korean'] = list(dict.fromkeys(toks))[:12]

    # 2) IP (공인/오타 의심만)
    for fn, t in ocr.items():
        pubs = sorted({ip for ip in re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', t)
                       if ip_class(ip) == 'PUBLIC'})
        if pubs:
            flags[fn].append('공인IP')
            detail[fn]['public_ip'] = [ip + typo_hint(ip) for ip in pubs]

    # 3) 이메일/도메인
    for fn, t in ocr.items():
        emails = sorted(set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', t)))
        if emails:
            flags[fn].append('이메일')
            detail[fn]['emails'] = emails[:15]

    # 4) 키워드
    for fn, t in ocr.items():
        hit = [kw for kw in keywords if kw.lower() in t.lower()]
        if hit:
            flags[fn].append('키워드')
            detail[fn]['keywords'] = hit

    # 5) 형식 기반: jpg(다이어그램·구버전 캡처 단골), 초박형 크롭, 저DPI
    for fn, u in uniq.items():
        if not args.no_jpg_flag and re.search(r'\.jpe?g$', fn, re.I):
            flags[fn].append('jpg')
        px = u.get('px')
        if px and (px[1] < 60 or px[0] < 200):
            flags[fn].append('초소형크롭')
        if u.get('eff_dpi') and u['eff_dpi'] < 72:
            flags[fn].append('저해상도')

    # 6) 타이틀-부제 쌍 (부제 카피 오류 스캔용)
    subs = []
    for fn, t in ocr.items():
        lines = [l.strip() for l in t.split('\n') if l.strip()]
        if len(lines) >= 2 and lines[1].startswith('You can'):
            subs.append((lines[0][:40], lines[1][:80], fn))
    with open(f'{out}/ui_subtitles.txt', 'w', encoding='utf-8') as f:
        for title, sub, fn in sorted(subs):
            f.write(f'{title:42s} | {sub}  [{fn}]\n')

    # 트리아지 큐 (본문 순서)
    queue = [(u['order'], fn, u) for fn, u in uniq.items() if fn in flags]
    queue.sort()
    qlines = [f"육안 검수 대상: {len(queue)}장 / 고유 {len(uniq)}장 "
              f"({100 * len(queue) // max(1, len(uniq))}%)", ""]
    for order, fn, u in queue:
        px = f"{u['px'][0]}x{u['px'][1]}" if u['px'] else '?'
        qlines.append(f"#{order:3d} {fn} [{px}] — {', '.join(flags[fn])}")
        qlines.append(f"     섹션: {u['secs'][0]}" +
                      (f" (외 {len(u['secs']) - 1}곳)" if len(u['secs']) > 1 else ''))
        for k, v in detail[fn].items():
            qlines.append(f"     {k}: {v}")
    with open(f'{out}/triage_queue.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(qlines))

    with open(f'{out}/ocr_flags.json', 'w', encoding='utf-8') as f:
        json.dump({fn: {'reasons': flags[fn], **detail[fn]} for fn in flags},
                  f, ensure_ascii=False, indent=1)

    # findings_auto.md 스켈레톤
    md = ['# 이미지 검수 자동 검출 결과', '',
          f'- 고유 이미지 {len(uniq)}장 중 육안 검수 대상 {len(queue)}장', '',
          '| 순번 | 이미지 | 섹션 | 자동 검출 | 육안 판정 |',
          '|------|--------|------|-----------|-----------|']
    for order, fn, u in queue:
        det = '; '.join(f"{k}:{v}" for k, v in detail[fn].items())[:120]
        md.append(f"| #{order} | {fn} | {u['secs'][0][:50]} | {det} | (기록) |")
    with open(f'{out}/findings_auto.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print('\n'.join(qlines[:40]))
    print(f"\n-> {out}/triage_queue.txt, ocr_flags.json, ui_subtitles.txt, findings_auto.md")


if __name__ == '__main__':
    main()
