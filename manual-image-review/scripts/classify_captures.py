#!/usr/bin/env python3
"""캡처 유형 자동 분류 (manual-image-review 사전 준비)

입력: extract_and_map.py + ocr_vision.swift 산출 폴더
출력: capture_types.csv (이미지별 유형 + 신뢰도 + 시그널)

분류 카테고리:
  FULL    화면 전체 (LNB+GNB+콘텐츠 모두)
  CONTENT 콘텐츠 영역만 (LNB/GNB 크롭)
  MODAL   모달/팝업 단독
  PANEL   부분 패널/탭/필터 영역
  INLINE  인라인 컴포넌트 (드롭다운/툴팁/뱃지)
  DIAGRAM 다이어그램/일러스트 (캡처 아닌 디자인 산출물)
  COVER   표지/머리말
  CLI     터미널/CLI 캡처
  TOAST   알림 메시지/토스트
  UNKNOWN 분류 실패 (수동 라벨 필요)
"""
from __future__ import annotations
import json, os, sys, csv, re
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/306_en_260617_review")
MEDIA = ROOT / "word" / "media"
OCR = ROOT / "ocr_results.jsonl"
REVIEW = ROOT / "review_list.txt"
OUT = ROOT / "capture_types.csv"

# LNB 시그널: 좌측 LNB의 표준 메뉴 토큰 (영문)
LNB_TOKENS = {"Product", "Cloud View", "Dashboard", "Basic settings", "Compute",
              "VPC", "Storage", "Monitoring", "HA Management", "Management",
              "Instance", "Volume", "Security Group", "Load Balancer", "Image",
              "Key Pair", "Flavor", "Server Group", "Project"}
# GNB 시그널: 우상단 글로벌 UI
GNB_TOKENS = {"Cluster name", "Project name", "Cloud view", "Logout",
              "My Page", "Notifications", "Search"}
# 모달 시그널
MODAL_TOKENS = {"Cancel", "Save", "Confirm", "Create", "Delete", "Apply", "Close",
                "Yes", "No", "OK"}
MODAL_PREFIX_TOKENS = {"Create ", "Edit ", "Modify ", "Delete ", "Add ", "Set "}
# CLI 시그널
CLI_TOKENS = {"$ ", "# ", "Last login", "[user@", "sudo ", "ssh-keygen", "kubectl",
              "Welcome to"}
# 토스트
TOAST_TOKENS = {"created successfully", "deleted successfully", "saved",
                "applied successfully", "completed", "failed"}

JPG_EXTS = {".jpg", ".jpeg"}


def load_ocr() -> dict[str, str]:
    out = {}
    if not OCR.exists():
        return out
    for line in OCR.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
            out[d["file"]] = d.get("text", "")
        except Exception:
            continue
    return out


def load_sections() -> dict[str, str]:
    """review_list.txt에서 image -> 섹션"""
    out = {}
    if not REVIEW.exists():
        return out
    current = None
    for line in REVIEW.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*\d+\.\s+(\S+\.\w+)", line)
        if m:
            current = m.group(1)
        elif current and line.strip().startswith("섹션:"):
            out[current] = line.split("섹션:", 1)[1].strip()
            current = None
    return out


def img_size(p: Path) -> tuple[int, int] | None:
    """PIL 없이 가벼운 헤더 파싱"""
    try:
        import struct
        with open(p, "rb") as f:
            head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h
        if head[:3] == b"\xff\xd8\xff":
            # JPEG: SOF0 마커까지 스캔
            with open(p, "rb") as f:
                data = f.read()
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    break
                marker = data[i + 1]
                if marker in (0xC0, 0xC1, 0xC2):
                    h = (data[i + 5] << 8) | data[i + 6]
                    w = (data[i + 7] << 8) | data[i + 8]
                    return w, h
                seg_len = (data[i + 2] << 8) | data[i + 3]
                i += 2 + seg_len
    except Exception:
        return None
    return None


def classify(name: str, text: str, section: str, size: tuple[int, int] | None) -> tuple[str, float, list[str]]:
    signals: list[str] = []
    score = {k: 0.0 for k in ("FULL", "CONTENT", "MODAL", "PANEL", "INLINE",
                              "DIAGRAM", "COVER", "CLI", "TOAST")}

    # --- 메타 휴리스틱 ---
    w, h = (size or (0, 0))
    ar = (w / h) if h else 0
    ext = Path(name).suffix.lower()

    # 표지/머리말
    if section and ("표지" in section or "머리말" in section):
        score["COVER"] += 5
        signals.append("section=cover")

    # 다이어그램: jpg + outline 또는 다이어그램 섹션
    if ext in JPG_EXTS:
        signals.append("ext=jpg")
        score["DIAGRAM"] += 1.5
        if section and ("outline" in section or "Configuration diagram" in section
                        or "Architecture" in section):
            score["DIAGRAM"] += 3
            signals.append("section=diagram")

    # CLI
    if any(tok in text for tok in CLI_TOKENS):
        score["CLI"] += 4
        signals.append("cli-tokens")

    # 토스트: 짧은 텍스트 + 성공/실패 문구
    if len(text) < 80 and any(tok in text.lower() for tok in TOAST_TOKENS):
        score["TOAST"] += 4
        signals.append("toast-tokens")

    # LNB/GNB
    lnb_hits = sum(1 for tok in LNB_TOKENS if tok in text)
    gnb_hits = sum(1 for tok in GNB_TOKENS if tok in text)
    if lnb_hits >= 4:
        score["FULL"] += 3
        signals.append(f"lnb={lnb_hits}")
    if gnb_hits >= 1:
        score["FULL"] += 2
        signals.append(f"gnb={gnb_hits}")
    if lnb_hits >= 4 and gnb_hits >= 1:
        score["FULL"] += 2
        signals.append("full-shell")
    if lnb_hits == 0 and gnb_hits == 0:
        score["CONTENT"] += 1
        signals.append("no-shell")

    # 모달: 모달 버튼 페어 + 폭이 풀스크린 아님
    modal_btn_hits = sum(1 for tok in MODAL_TOKENS if tok in text)
    modal_pref_hits = sum(1 for tok in MODAL_PREFIX_TOKENS if tok in text)
    if modal_btn_hits >= 2:
        signals.append(f"modal-btn={modal_btn_hits}")
        if w and w < 1300:
            score["MODAL"] += 4
        else:
            score["MODAL"] += 1.5
    if modal_pref_hits >= 1 and w and w < 900:
        score["MODAL"] += 2
        signals.append(f"modal-prefix={modal_pref_hits}")

    # 인라인: 매우 작은 사이즈
    if w and h:
        if max(w, h) < 700:
            score["INLINE"] += 2
            signals.append(f"small={w}x{h}")
        if w < 500 and h < 300:
            score["INLINE"] += 2
            signals.append("tiny")

    # 부분 패널: 폭은 본문급, 높이 짧음
    if w and h:
        if 800 <= w <= 1800 and h < w * 0.4:
            score["PANEL"] += 2
            signals.append("wide-short")

    # 콘텐츠 영역: 폭 1100~1900 + 헤더 텍스트 패턴 (페이지 타이틀)
    if w and 1100 <= w <= 1900 and ar > 1.1:
        score["CONTENT"] += 1.5
        signals.append("content-shape")

    # 화면 전체: 폭 매우 큼
    if w and w >= 2200:
        score["FULL"] += 1.5
        signals.append(f"wide={w}")

    # 결정
    label, conf = max(score.items(), key=lambda kv: kv[1])
    if conf < 1.5:
        label = "UNKNOWN"
        conf = 0.0
    return label, round(conf, 1), signals


def main() -> None:
    ocr = load_ocr()
    sections = load_sections()

    rows = []
    counts: dict[str, int] = {}
    for p in sorted(MEDIA.iterdir()):
        if not p.is_file():
            continue
        size = img_size(p)
        w, h = size or (0, 0)
        text = ocr.get(p.name, "")
        section = sections.get(p.name, "")
        label, conf, signals = classify(p.name, text, section, size)
        counts[label] = counts.get(label, 0) + 1
        rows.append({
            "file": p.name,
            "section": section,
            "w": w,
            "h": h,
            "type": label,
            "conf": conf,
            "signals": ";".join(signals),
        })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["file", "section", "w", "h", "type", "conf", "signals"])
        wr.writeheader()
        wr.writerows(rows)

    total = sum(counts.values())
    print(f"총 {total}장 분류 → {OUT}")
    for k in ("FULL", "CONTENT", "MODAL", "PANEL", "INLINE", "DIAGRAM", "COVER", "CLI", "TOAST", "UNKNOWN"):
        n = counts.get(k, 0)
        pct = (n / total * 100) if total else 0
        print(f"  {k:8s} {n:4d}장 ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
