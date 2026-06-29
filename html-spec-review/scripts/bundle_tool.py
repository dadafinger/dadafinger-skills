#!/usr/bin/env python3
"""
bundle_tool.py — Product HTML 번들 프로토타입(__bundler/manifest) 안전 조작 도구.

가시 HTML은 로더일 뿐이고, 실제 화면 로직은 manifest JSON 안의 gzip+base64 babel JSX
에셋에 들어있다. 손으로는 못 고친다. 이 도구가 그 에셋을 안전하게 디코드/검증/패치한다.

명령:
  list   <html>                      앱 JSX 에셋 목록(uuid·mime·길이·첫 줄)
  decode <html> [--match S] [--out F] 매칭 에셋 디코드 → stdout 또는 파일
  verify <html> [--match S] [--babel B] babel 문법 검증(쓰기 없음)
  patch  <html> --spec patches.json  스펙대로 패치(백업→치환/삽입→babel+라운드트립→쓰기)

patches.json 스키마:
  {
    "match": "function EditApp",          # 패치할 에셋을 특정하는 부분문자열(정확히 1개 매칭)
    "replacements": [["old","new"], ...],  # 각 old는 에셋 내 정확히 1회만 있어야 함(안전장치)
    "insertions":   [["anchor","anchor+추가"], ...],  # anchor도 1회만. 보통 anchor를 그대로 포함시켜 위치 삽입
    "assert_present": ["반영후 반드시 있어야 할 문자열", ...],
    "assert_absent":  ["반영후 반드시 사라져야 할 문자열", ...]
  }

설계 원칙: 매칭이 모호하면(0개/2개+) 즉시 중단. babel 실패면 쓰지 않음. 쓰기 전 백업,
쓰기 후 라운드트립(재디코드==기대값) 확인. 한 번에 에셋 1개만 건드린다(나머지 보존).
"""
import json, base64, gzip, re, os, sys, shutil, datetime, argparse, subprocess, glob, tempfile

MANIFEST_RE = r'(<script type="__bundler/manifest">)(.*?)(</script>)'


def load(html_path):
    html = open(html_path, encoding="utf-8").read()
    m = re.search(MANIFEST_RE, html, re.S)
    if not m:
        sys.exit("[중단] __bundler/manifest 스크립트 태그를 못 찾음 — 번들 standalone html이 맞나요?")
    return html, m, json.loads(m.group(2))


def decode_asset(val):
    raw = base64.b64decode(val.get("data") or val.get("content") or "")
    if val.get("compressed"):
        raw = gzip.decompress(raw)
    return raw.decode("utf-8")


def encode_asset(text):
    return base64.b64encode(gzip.compress(text.encode("utf-8"), 9)).decode("ascii")


def is_app_asset(val, text):
    """라이브러리(React/Babel/webpack) 에셋 제외 → 우리가 편집할 앱 JSX만."""
    if val.get("integrity"):
        return False
    head = text[:2000]
    if "react.development" in head or text.lstrip().startswith("!function") or "__webpack" in text[:500]:
        return False
    return True


def app_assets(man):
    out = []
    for uuid, val in man.items():
        if not isinstance(val, dict):
            continue
        if not any(x in val.get("mime", "") for x in ("javascript", "jsx", "ecmascript")):
            continue
        try:
            t = decode_asset(val)
        except Exception:
            continue
        if not is_app_asset(val, t):
            continue
        out.append((uuid, val, t))
    return out


def pick(man, match):
    a = app_assets(man)
    if match:
        a = [x for x in a if match in x[2]]
    return a


def find_babel(explicit=None):
    if explicit and os.path.exists(explicit):
        return explicit
    # standalone babel(3MB대) 탐색. cwd가 어디든 동작하도록 cwd + 프로젝트 루트(이 스크립트의
    # agent-shared 상위) 둘 다 훑는다. os.walk라 숨김(.alarm_*_work)도 포함.
    roots = [os.getcwd()]
    here = os.path.abspath(__file__)
    if "agent-shared" in here:
        roots.append(here.split(os.sep + "agent-shared")[0])  # 프로젝트 루트
    cands = []
    for base in dict.fromkeys(roots):  # 중복 제거, 순서 유지
        for root, dirs, files in os.walk(base):
            if "node_modules" in root:
                continue
            if "babel.min.js" in files:
                cands.append(os.path.join(root, "babel.min.js"))
    # alarm 작업폴더 우선 + 큰 파일 우선(react-dom 1MB와 혼동 방지)
    cands.sort(key=lambda p: ("alarm" not in p, -os.path.getsize(p)))
    for p in cands:
        if os.path.getsize(p) > 2_000_000:
            return p
    return None


def babel_check(text, babel_path):
    """(ok, msg). babel/node 없으면 ok=None(생략)."""
    if not babel_path:
        return None, "babel.min.js 미발견 — 문법검증 생략(--babel 로 지정 가능)"
    node = shutil.which("node")
    if not node:
        return None, "node 미설치 — 문법검증 생략"
    f = tempfile.NamedTemporaryFile("w", suffix=".jsx", delete=False, encoding="utf-8")
    f.write(text); f.close()
    script = ("const B=require(%s);const fs=require('fs');"
              "try{B.transform(fs.readFileSync(%s,'utf8'),{presets:['react']});console.log('OK')}"
              "catch(e){console.error(e.message);process.exit(1)}" % (json.dumps(babel_path), json.dumps(f.name)))
    r = subprocess.run([node, "-e", script], capture_output=True, text=True)
    os.unlink(f.name)
    return (r.returncode == 0), (r.stdout + r.stderr).strip()


def cmd_list(args):
    _, _, man = load(args.html)
    for i, (uuid, val, t) in enumerate(app_assets(man)):
        first = next((ln.strip() for ln in t.splitlines() if ln.strip()), "")
        print(f"[{i}] {uuid[:8]} {val.get('mime','')} len={len(t)} :: {first[:80]}")


def cmd_decode(args):
    _, _, man = load(args.html)
    hits = pick(man, args.match)
    if not hits:
        sys.exit(f"[중단] 매칭 에셋 0개 (match={args.match!r}). `list`로 후보 확인.")
    if args.out and len(hits) != 1:
        sys.exit(f"[중단] --out 은 정확히 1개 매칭 필요 (현재 {len(hits)}). match를 좁히세요.")
    if args.out:
        open(args.out, "w", encoding="utf-8").write(hits[0][2])
        print(f"wrote {args.out} (len {len(hits[0][2])})")
    else:
        for uuid, val, t in hits:
            sys.stdout.write(t if len(hits) == 1 else f"\n===== {uuid[:8]} =====\n{t}")


def cmd_verify(args):
    _, _, man = load(args.html)
    hits = pick(man, args.match)
    if len(hits) != 1:
        sys.exit(f"[중단] 정확히 1개 매칭 필요 (현재 {len(hits)}).")
    ok, msg = babel_check(hits[0][2], find_babel(args.babel))
    print({True: "BABEL OK", False: "BABEL FAIL", None: "BABEL SKIP"}[ok], "—", msg or "")
    sys.exit(0 if ok is not False else 1)


def cmd_patch(args):
    spec = json.load(open(args.spec, encoding="utf-8"))
    html, m, man = load(args.html)
    hits = pick(man, spec.get("match"))
    if len(hits) != 1:
        sys.exit(f"[중단] match가 정확히 1개여야 함 (현재 {len(hits)}, match={spec.get('match')!r}). `list`로 확인.")
    uuid, val, text = hits[0]
    new = text
    for old, rep in spec.get("replacements", []):
        c = new.count(old)
        if c != 1:
            sys.exit(f"[중단] replacement old가 {c}회 매칭(1이어야 안전): {old[:70]!r}")
        new = new.replace(old, rep)
    for anchor, inject in spec.get("insertions", []):
        c = new.count(anchor)
        if c != 1:
            sys.exit(f"[중단] insertion anchor가 {c}회 매칭(1이어야 안전): {anchor[:70]!r}")
        new = new.replace(anchor, inject)
    for s in spec.get("assert_present", []):
        if s not in new:
            sys.exit(f"[중단] assert_present 누락: {s[:70]!r}")
    for s in spec.get("assert_absent", []):
        if s in new:
            sys.exit(f"[중단] assert_absent 잔존: {s[:70]!r}")
    ok, msg = babel_check(new, find_babel(args.babel))
    if ok is False:
        sys.exit(f"[중단] BABEL FAIL — 쓰지 않음:\n{msg}")
    bak = args.html + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(args.html, bak)
    dk = "data" if "data" in val else "content"
    val[dk] = encode_asset(new); val["compressed"] = True
    new_man = json.dumps(man, ensure_ascii=True, separators=(",", ":"))
    open(args.html, "w", encoding="utf-8").write(html[:m.start(2)] + new_man + html[m.end(2):])
    # 라운드트립: 디스크에서 다시 디코드해 기대값과 동일한지
    _, _, man2 = load(args.html)
    rt = [a for a in app_assets(man2) if a[0] == uuid]
    if not rt or rt[0][2] != new:
        sys.exit(f"[중단] ROUNDTRIP MISMATCH — 백업에서 복구하세요: {bak}")
    print(f"PATCH OK · len {len(text)}→{len(new)} · babel={ {True:'OK',None:'skip'}.get(ok) } · "
          f"roundtrip=OK\n  backup: {bak}")


def main():
    p = argparse.ArgumentParser(description="Product HTML 번들 안전 조작 도구")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("list", "decode", "verify", "patch"):
        sp = sub.add_parser(name)
        sp.add_argument("html")
        if name in ("decode", "verify"):
            sp.add_argument("--match", default=None, help="에셋 특정용 부분문자열")
        if name == "decode":
            sp.add_argument("--out", default=None)
        if name in ("verify", "patch"):
            sp.add_argument("--babel", default=None, help="babel.min.js 경로(미지정 시 자동탐색)")
        if name == "patch":
            sp.add_argument("--spec", required=True, help="patches.json 경로")
    args = p.parse_args()
    {"list": cmd_list, "decode": cmd_decode, "verify": cmd_verify, "patch": cmd_patch}[args.cmd](args)


if __name__ == "__main__":
    main()
