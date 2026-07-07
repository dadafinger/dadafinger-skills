#!/usr/bin/env python3
"""
size_normalize.py — 매뉴얼 docx 안의 이미지·표 폭을 하나로 통일한다.

문제: 스크린샷/표를 마우스로 대충 드래그해 넣으면 폭이 6.18/6.22/6.27/6.32in …
      제각각이 되어 페이지마다 본문 좌우 가장자리가 들쭉날쭉해진다.
해법: "넓은 이미지"와 "고정폭 표"의 폭을 단일 정본 폭으로 스냅한다.
      - 이미지: 가로세로 비율 유지(높이는 비례 재계산). <wp:extent> + xfrm <a:ext> 동기.
      - 표: 각 표의 열 비율은 보존하고 전체폭만 스냅. tblW / gridCol / 셀 tcW 3층을
        같은 배율로 재계산(열폭 합계 = 전체폭 정확 일치).
      - 이미지와 표를 같은 정본 폭으로 맞추면 문서 전체 본문 가장자리가 정렬된다.

제외(의도적으로 건드리지 않음, 리포트만):
      - 작은 아이콘/인라인 이미지(--min-img-in 미만)
      - auto(내용맞춤) 표 — 고정폭이 없어 스냅하면 깨짐
      - 들여쓰기(tblInd>0) 표 — 의도적 하위 들여쓰기
      - 세로가 페이지를 넘칠(--max-img-in 초과) 이미지

단위: 이미지 extent=EMU(914400/in), 표 폭=twip(1440/in). 1 twip = 635 EMU.
가정: 표 중첩 없음(<w:tbl> 비탐욕 매칭). Product 매뉴얼군 기준 검증됨.

사용:
    python3 size_normalize.py --file M.docx                      # analyze(읽기전용 분포/권고)
    python3 size_normalize.py --file M.docx --apply              # auto 정본폭으로 적용(백업 후)
    python3 size_normalize.py --file M.docx --apply --width-in 6.2701
    python3 size_normalize.py --file M.docx --apply --scope images   # 이미지만
    python3 size_normalize.py --file M.docx --apply --scope tables --table-scope 2col
"""
import argparse, re, sys, shutil, zipfile, collections, os

EMU_PER_IN = 914400.0
TW_PER_IN  = 1440.0
EMU_PER_TW = 635.0

# ---------- docx io ----------
def read_document_xml(path):
    with zipfile.ZipFile(path) as z:
        return z.read('word/document.xml').decode('utf-8'), z.namelist()

def write_document_xml(path, new_xml):
    """word/document.xml 만 교체해 zip을 재작성(다른 엔트리·압축 보존)."""
    tmp = path + '.tmp_repack'
    with zipfile.ZipFile(path) as zin, \
         zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                data = new_xml.encode('utf-8')
            zout.writestr(item, data)
    os.replace(tmp, path)

# ---------- image analysis / transform ----------
def image_widths(xml):
    return [(int(cx), int(cy)) for cx, cy in
            re.findall(r'<wp:extent\s+cx="(\d+)"\s+cy="(\d+)"', xml)]

def dominant_image_cx(xml):
    """가장 흔한 폭 그룹(소수 2자리) 안에서 최빈 정확 EMU 값을 정본으로."""
    ext = image_widths(xml)
    if not ext:
        return None
    grp = collections.Counter(round(cx/EMU_PER_IN, 2) for cx, cy in ext)
    top = grp.most_common(1)[0][0]
    exact = collections.Counter(cx for cx, cy in ext if round(cx/EMU_PER_IN, 2) == top)
    return exact.most_common(1)[0][0]

def transform_images(xml, canon_cx, min_emu, max_emu, stats):
    def fix(m):
        block = m.group(0)
        me = re.search(r'<wp:extent\s+cx="(\d+)"\s+cy="(\d+)"', block)
        if not me:
            return block
        cx, cy = int(me.group(1)), int(me.group(2))
        if cx < min_emu:
            stats['img_untouched_small'] += 1
            return block
        if cx == canon_cx:
            stats['img_already'] += 1
            return block
        new_cy = round(canon_cx * cy / cx)
        if new_cy > max_emu:
            stats['img_skipped_tall'].append((round(cx/EMU_PER_IN, 2), round(new_cy/EMU_PER_IN, 2)))
            return block
        block = re.sub(r'(<wp:extent\s+cx=")\d+("\s+cy=")\d+(")',
                       rf'\g<1>{canon_cx}\g<2>{new_cy}\g<3>', block, count=1)
        b2 = re.sub(r'(<a:off\b[^>]*/>\s*<a:ext\s+cx=")\d+("\s+cy=")\d+(")',
                    rf'\g<1>{canon_cx}\g<2>{new_cy}\g<3>', block, count=1)
        if b2 == block:  # fallback: a:ext without preceding a:off
            b2 = re.sub(r'(<a:ext\s+cx=")\d+("\s+cy=")\d+(")',
                        rf'\g<1>{canon_cx}\g<2>{new_cy}\g<3>', block, count=1)
        stats['img_snapped'] += 1
        return b2
    return re.sub(r'<w:drawing\b.*?</w:drawing>', fix, xml, flags=re.DOTALL)

# ---------- table analysis / transform ----------
def _cols(t):
    return len(re.findall(r'<w:gridCol\b', t))

def _scale_cols(cols, total):
    s = sum(cols)
    if s == 0:
        return cols
    new = [round(c * total / s) for c in cols]
    d = total - sum(new)
    if new:
        i = max(range(len(new)), key=lambda k: new[k])
        new[i] += d
    return new

def transform_tables(xml, canon_tw, table_scope, stats):
    """table_scope: 'both'(2열+1열) | '2col' | '1col'."""
    def fix(m):
        t = m.group(0)
        mw = re.search(r'<w:tblW\s+w:w="(\d+)"\s+w:type="(\w+)"', t)
        if not mw:
            return t
        old, typ = int(mw.group(1)), mw.group(2)
        if typ != 'dxa':
            stats['tbl_excl_auto'] += 1
            return t
        if re.search(r'<w:tblInd\s+w:w="([1-9]\d*)"', t):
            stats['tbl_excl_indented'] += 1
            return t
        cols = _cols(t)
        if table_scope == '2col' and cols != 2:
            stats['tbl_out_of_scope'] += 1
            return t
        if table_scope == '1col' and cols != 1:
            stats['tbl_out_of_scope'] += 1
            return t
        if old == canon_tw:
            stats['tbl_already'] += 1
            return t
        f = canon_tw / old
        gc = [int(x) for x in re.findall(r'<w:gridCol\s+w:w="(\d+)"', t)]
        newgc = iter(_scale_cols(gc, canon_tw))
        t = re.sub(r'(<w:gridCol\s+w:w=")\d+(")',
                   lambda mm: mm.group(1) + str(next(newgc)) + mm.group(2), t)
        t = re.sub(r'(<w:tblW\s+w:w=")\d+("\s+w:type="dxa")',
                   lambda mm: mm.group(1) + str(canon_tw) + mm.group(2), t, count=1)
        t = re.sub(r'(<w:tcW\s+w:w=")(\d+)("\s+w:type="dxa")',
                   lambda mm: mm.group(1) + str(round(int(mm.group(2)) * f)) + mm.group(3), t)
        stats['tbl_snapped'] += 1
        return t
    return re.sub(r'<w:tbl>.*?</w:tbl>', fix, xml, flags=re.DOTALL)

# ---------- reporting ----------
def analyze(xml):
    print("=== 이미지 폭 분포 (넓은 순 상위) ===")
    ext = image_widths(xml)
    wc = collections.Counter(round(cx/EMU_PER_IN, 2) for cx, cy in ext)
    for w, c in sorted(wc.items(), key=lambda x: -x[1])[:12]:
        print(f"   {w:>5}in ({w*2.54:>5.2f}cm)  x{c}")
    print(f"   총 {len(ext)}개 배치 · {len(wc)}종 폭")
    dc = dominant_image_cx(xml)
    if dc:
        print(f"   → 최빈 정본 폭 후보: {dc} EMU = {dc/EMU_PER_IN:.4f}in")
    print("\n=== 표 폭 분포 (고정폭 dxa, 넓은 순 상위) ===")
    tbls = re.findall(r'<w:tbl>.*?</w:tbl>', xml, flags=re.DOTALL)
    dxa, auto, ind = [], 0, 0
    for t in tbls:
        mw = re.search(r'<w:tblW\s+w:w="(\d+)"\s+w:type="(\w+)"', t)
        if not mw:
            continue
        w, typ = int(mw.group(1)), mw.group(2)
        if typ != 'dxa':
            auto += 1
            continue
        if re.search(r'<w:tblInd\s+w:w="([1-9]\d*)"', t):
            ind += 1
            continue
        dxa.append((w, _cols(t)))
    twc = collections.Counter(round(w/TW_PER_IN, 2) for w, c in dxa)
    for w, c in sorted(twc.items(), key=lambda x: -x[1])[:12]:
        print(f"   {w:>5}in ({w*2.54:>5.2f}cm)  x{c}")
    n2 = sum(1 for w, c in dxa if c == 2)
    n1 = sum(1 for w, c in dxa if c == 1)
    print(f"   총 {len(tbls)}개 표 · 스냅대상(고정폭·비들여쓰기) {len(dxa)}개 "
          f"(2열 {n2} / 1열 {n1}) · 제외 auto {auto} / 들여쓰기 {ind}")

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="매뉴얼 docx 이미지·표 폭 일관성 정규화")
    ap.add_argument('--file', required=True)
    ap.add_argument('--apply', action='store_true', help='실제 수정(생략 시 analyze 전용)')
    ap.add_argument('--width-in', type=float, default=None,
                    help='정본 폭(inch). 생략 시 이미지 최빈폭 자동 감지')
    ap.add_argument('--scope', choices=['images', 'tables', 'both'], default='both')
    ap.add_argument('--table-scope', choices=['both', '2col', '1col'], default='both')
    ap.add_argument('--min-img-in', type=float, default=5.5,
                    help='이 폭 미만 이미지는 아이콘/인라인으로 보고 제외(기본 5.5in)')
    ap.add_argument('--max-img-in', type=float, default=9.5,
                    help='스냅 결과 높이가 이 값 초과면 페이지 넘침으로 보고 제외(기본 9.5in)')
    ap.add_argument('--no-backup', action='store_true')
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        sys.exit(f"파일 없음: {args.file}")

    xml, _ = read_document_xml(args.file)

    if not args.apply:
        analyze(xml)
        print("\n(analyze 전용. 실제 반영은 --apply)")
        return

    # 정본 폭 확정 (이미지 EMU · 표 twip 동기)
    if args.width_in is not None:
        canon_cx = round(args.width_in * EMU_PER_IN)
        canon_tw = round(args.width_in * TW_PER_IN)
    else:
        canon_cx = dominant_image_cx(xml)
        if canon_cx is None:
            sys.exit("이미지가 없어 자동 폭 감지 불가. --width-in 지정 필요")
        canon_tw = round(canon_cx / EMU_PER_TW)
    print(f"정본 폭: {canon_cx/EMU_PER_IN:.4f}in  (이미지 {canon_cx} EMU / 표 {canon_tw} twip)")

    # 백업
    if not args.no_backup:
        bak = re.sub(r'\.docx$', '.bak.docx', args.file)
        if not os.path.exists(bak):
            shutil.copy2(args.file, bak)
            print(f"백업 생성: {bak}")
        else:
            print(f"백업 이미 존재(보존): {bak}")

    stats = collections.defaultdict(int)
    stats['img_skipped_tall'] = []
    new = xml
    if args.scope in ('images', 'both'):
        new = transform_images(new, canon_cx,
                               args.min_img_in * EMU_PER_IN,
                               args.max_img_in * EMU_PER_IN, stats)
    if args.scope in ('tables', 'both'):
        new = transform_tables(new, canon_tw, args.table_scope, stats)

    write_document_xml(args.file, new)

    # 검증
    v, _ = read_document_xml(args.file)
    wide = [cx for cx, cy in image_widths(v) if cx >= args.min_img_in * EMU_PER_IN]
    tbl_snapped = len(re.findall(rf'<w:tblW\s+w:w="{canon_tw}"\s+w:type="dxa"', v))
    with zipfile.ZipFile(args.file) as z:
        integrity = 'OK' if z.testzip() is None else 'BAD'
        media = sum(1 for n in z.namelist() if n.startswith('word/media/'))

    print("\n=== 결과 ===")
    if args.scope in ('images', 'both'):
        print(f"이미지: 스냅 {stats['img_snapped']} / 이미정확 {stats['img_already']} / "
              f"작아서제외 {stats['img_untouched_small']} / 세로넘침제외 {len(stats['img_skipped_tall'])}")
        if stats['img_skipped_tall']:
            print(f"  넘침제외 목록(폭in,결과높이in): {stats['img_skipped_tall']}")
        print(f"  → 넓은 이미지 폭 종류: {len(set(wide))} (1이면 통일)")
    if args.scope in ('tables', 'both'):
        print(f"표: 스냅 {stats['tbl_snapped']} / 이미정확 {stats['tbl_already']} / "
              f"제외 auto {stats['tbl_excl_auto']} / 들여쓰기 {stats['tbl_excl_indented']} / "
              f"범위밖 {stats['tbl_out_of_scope']}")
        print(f"  → 정본폭 표: {tbl_snapped}개")
    print(f"zip 무결성: {integrity} · media {media}개 보존")
    print("\n※ Word에서 열어 확인 후 목차 F9(전체 업데이트) 권장. 이상 없으면 .bak.docx 삭제.")

if __name__ == '__main__':
    main()
