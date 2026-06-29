#!/usr/bin/env python3
"""매뉴얼 docx 이미지 검수 1단계: 이미지 추출 + 본문 위치 매핑 + 품질 메타.

사용법:
    python3 extract_and_map.py <manual.docx> <outdir>

출력(outdir):
    word/media/       원본 이미지 전체
    mapping.json      본문 참조 순서별 레코드 (file, 섹션, 앞뒤 문맥, px, eff_dpi)
    review_list.txt   육안 검수 체크리스트 (고유 이미지 첫 등장 순 + 재사용처)
    stats.txt         요약 (참조 수/중복/저해상도/미사용/재사용)
"""
import argparse, bisect, hashlib, json, os, re, struct, subprocess, sys, zipfile
from collections import Counter, OrderedDict, defaultdict
from xml.etree import ElementTree as ET

NS = {
    'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    'r': "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    'wp': "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    'a': "http://schemas.openxmlformats.org/drawingml/2006/main",
    'v': "urn:schemas-microsoft-com:vml",
}
W = lambda tag: f'{{{NS["w"]}}}{tag}'


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return struct.unpack('>II', data[16:24])


def img_size(path, data):
    s = png_size(data)
    if s:
        return s
    try:
        out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                             capture_output=True, text=True).stdout
        wm = re.search(r'pixelWidth: (\d+)', out)
        hm = re.search(r'pixelHeight: (\d+)', out)
        if wm and hm:
            return int(wm.group(1)), int(hm.group(1))
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('outdir')
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    zf = zipfile.ZipFile(args.docx)

    # 1) 이미지 추출
    media_names = [n for n in zf.namelist() if n.startswith('word/media/')]
    zf.extractall(args.outdir, members=media_names)

    # 2) rId -> media, 스타일 맵
    relroot = ET.fromstring(zf.read('word/_rels/document.xml.rels'))
    rid2target = {rel.get('Id'): rel.get('Target') for rel in relroot}
    sid2name = {}
    for st in ET.fromstring(zf.read('word/styles.xml')).findall(W('style')):
        nm = st.find(W('name'))
        sid2name[st.get(W('styleId'))] = nm.get(W('val')) if nm is not None else ''

    # 헤더/푸터에서 쓰는 media (미사용 판정 정확도용)
    header_media = set()
    for n in zf.namelist():
        if re.match(r'word/_rels/(header|footer)\d*\.xml\.rels', n):
            for rel in ET.fromstring(zf.read(n)):
                t = rel.get('Target') or ''
                if 'media/' in t:
                    header_media.add(t.split('media/')[-1])

    # 3) 본문 순회: 헤딩 체인 + 이미지 참조
    body = ET.fromstring(zf.read('word/document.xml')).find(W('body'))
    paras, images, heading_chain = [], [], {}
    for pi, p in enumerate(body.iter(W('p'))):
        txt = ''.join(t.text or '' for t in p.iter(W('t'))).strip()
        style_el = p.find(f'{W("pPr")}/{W("pStyle")}')
        sname = sid2name.get(style_el.get(W('val')), '') if style_el is not None else ''
        paras.append((pi, txt))
        m = re.match(r'(?:[Hh]eading|제목|見出し)\s*(\d)', sname or '')
        if m and txt:
            lvl = int(m.group(1))
            heading_chain[lvl] = txt
            for l in [l for l in heading_chain if l > lvl]:
                del heading_chain[l]
        embeds = [b.get(f'{{{NS["r"]}}}embed') for b in p.iter(f'{{{NS["a"]}}}blip')]
        embeds += [im.get(f'{{{NS["r"]}}}id') for im in p.iter(f'{{{NS["v"]}}}imagedata')]
        embeds = [e for e in embeds if e]
        if not embeds:
            continue
        extents = [(int(e.get('cx')), int(e.get('cy'))) for e in p.iter(f'{{{NS["wp"]}}}extent')]
        for i, rid in enumerate(embeds):
            images.append({
                'order': len(images) + 1,
                'para_idx': pi,
                'file': (rid2target.get(rid) or '?').replace('media/', ''),
                'extent_emu': extents[i] if i < len(extents) else None,
                'heading': dict(heading_chain),
            })

    # 앞/뒤 문맥
    nonempty = [(i, t) for i, t in paras if t]
    keys = [i for i, _ in nonempty]
    for rec in images:
        pos = bisect.bisect_left(keys, rec['para_idx'])
        rec['prev_text'] = nonempty[pos - 1][1][:120] if pos > 0 else ''
        nxt = next((t for i, t in nonempty[pos:] if i > rec['para_idx']), '')
        rec['next_text'] = nxt[:120]

    # 4) 픽셀 크기 / md5 / 유효 DPI
    dims, hashes = {}, {}
    for name in media_names:
        data = zf.read(name)
        fn = name.replace('word/media/', '')
        hashes[fn] = hashlib.md5(data).hexdigest()
        dims[fn] = img_size(os.path.join(args.outdir, name), data)
    for rec in images:
        s = dims.get(rec['file'])
        rec['px'] = list(s) if s else None
        rec['eff_dpi'] = None
        if s and rec['extent_emu'] and rec['extent_emu'][0]:
            rec['eff_dpi'] = round(s[0] / (rec['extent_emu'][0] / 914400))

    def sec(rec):
        h = rec['heading']
        return ' > '.join(h[k] for k in sorted(h, key=int)) if h else '(표지/머리말)'

    with open(f'{args.outdir}/mapping.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=1)

    # 5) review_list.txt (고유 첫 등장 순)
    seen = OrderedDict()
    for r in images:
        seen.setdefault(r['file'], {'first': r, 'locs': []})['locs'].append(sec(r))
    lines = []
    for i, (fn, v) in enumerate(seen.items(), 1):
        r = v['first']
        px = f"{r['px'][0]}x{r['px'][1]}" if r['px'] else '?'
        extra = f"  (재사용 {len(v['locs'])}회)" if len(v['locs']) > 1 else ''
        lines.append(f"{i:3d}. {fn}  [{px}]{extra}")
        lines.append(f"     섹션: {sec(r)}")
        if r['prev_text']:
            lines.append(f"     직전: {r['prev_text'][:90]}")
        if r['next_text']:
            lines.append(f"     직후: {r['next_text'][:90]}")
        for loc in v['locs'][1:]:
            lines.append(f"     재사용처: {loc}")
    with open(f'{args.outdir}/review_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # 6) stats.txt
    used = {r['file'] for r in images}
    allm = set(hashes)
    unused = sorted(allm - used - header_media)
    dup = defaultdict(list)
    for fn, h in hashes.items():
        dup[h].append(fn)
    dup_groups = [sorted(fs) for fs in dup.values() if len(fs) > 1]
    reuse = Counter(r['file'] for r in images)
    low = [r for r in images if r['eff_dpi'] and r['eff_dpi'] < 72]
    byh1 = Counter(r['heading'].get(1, '(없음)') for r in images)

    out = [
        f"docx: {args.docx}",
        f"본문 이미지 참조: {len(images)} / media 파일: {len(allm)} / 고유 사용: {len(used)}",
        f"헤더·푸터 전용: {sorted(header_media)}",
        f"본문·헤더 모두 미사용: {unused}",
        f"바이트 동일 중복 그룹: {len(dup_groups)} {dup_groups[:10]}",
        f"2회 이상 재사용: {len([c for c in reuse.values() if c > 1])}개 파일",
        f"유효 DPI<72: {len(low)}건 " + ', '.join(f"#{r['order']}{r['file']}" for r in low[:10]),
        "", "H1별 참조 수:",
    ] + [f"  {c:4d}  {h}" for h, c in byh1.items()]
    with open(f'{args.outdir}/stats.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print('\n'.join(out))
    print(f"\n고유 이미지 {len(seen)}장 -> {args.outdir}/review_list.txt")


if __name__ == '__main__':
    main()
