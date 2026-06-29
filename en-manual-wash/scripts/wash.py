"""
영문 매뉴얼 오픈스택 워싱 스크립트
구글 번역기 결과물을 오픈스택 표준 용어로 교체한다.

사용법:
  python wash.py --file "3.0.6_Product_Manual_en.docx"
  → 같은 폴더에 3.0.6_Product_Manual_en_washed.docx 생성
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

# ─────────────────────────────────────────────────────────
# 교체 사전 — 긴/구체적 패턴 먼저
# ─────────────────────────────────────────────────────────
REPLACEMENTS = [
    # ── 번역 오류 (긴 문구 먼저) ────────────────────────
    ("By Node pseudomorph Resources",         "Per-Node Virtual Resources"),
    ("Access authority Management",           "Access Permission Management"),
    ("Rack Configuration Diagram",            "Rack Diagram"),
    ("rack configuration diagram",            "Rack Diagram"),
    ("Physics network Configuration Diagram", "Physical Network Topology"),
    ("Virtual network Configuration Diagram", "Virtual Network Topology"),
    ("Physics network Configuration diagram", "Physical Network Topology"),
    ("Virtual network Configuration diagram", "Virtual Network Topology"),
    ("Availability John",                     "Availability Zone"),
    ("Gratitude Log",                         "Audit Log"),
    ("Role Buyeo",                            "Role Assignment"),
    ("Supplier Dashboard",                    "Admin Dashboard"),
    ("beginning Settings",                    "Default Settings"),
    ("Basics Settings",                       "Default Settings"),
    ("HA generated",                          "Create HA"),
    ("segment Agency",                        "Network Agent"),
    ("Alarm Center",                          "Alarm Channel Management"),
    ("alarm center",                          "alarm channel management"),
    ("Allowed IPs",                           "Allowed IP"),
    ("Block IP",                              "Blocked IP"),
    # ── OpenStack 표준 용어 ──────────────────────────────
    ("Instance Type (Flavor)",                "Flavor"),
    ("instances category",                    "Flavors"),
    ("Instance category",                     "Flavor"),
    ("instance category",                     "Flavor"),
    ("Instance Type",                         "Flavor"),
    ("Instance type",                         "Flavor"),
    ("instance Type",                         "Flavor"),
    ("instance type",                         "Flavor"),
    ("Dynamic IP",                            "Floating IP"),
    ("dynamic IP",                            "Floating IP"),
    ("dynamic ip",                            "Floating IP"),
    ("Layout Group",                          "Server Group"),
    ("Deployment group",                      "Server Group"),
    ("deployment group",                      "Server Group"),
    ("Batch Group",                           "Server Group"),
    ("batch Group",                           "Server Group"),
    ("Batch group",                           "Server Group"),
    ("batch group",                           "Server Group"),
    ("Sharing file",                          "Shared File"),
    ("sharing file",                          "Shared File"),
    ("Share File",                            "Shared File"),
    ("share file",                            "Shared File"),
    ("System Inspection",                     "System Maintenance"),
    ("system inspection",                     "system maintenance"),
    ("Physics network",                       "Physical Network"),
    ("physics network",                       "Physical Network"),
]

DOCX_SKILL = (
    "/Users/kimsoyoung/Library/Application Support/Claude/"
    "local-agent-mode-sessions/skills-plugin/"
    "261ee49d-3658-4b65-971d-93bf8eef810a/"
    "821aca0f-b389-46a4-b8d6-931d3ebefe26/skills/docx"
)


def wash_xml_files(xml_dir):
    """word/ 디렉터리의 모든 XML에서 w:t 안 텍스트를 교체"""
    stats = defaultdict(int)
    for fname in os.listdir(xml_dir):
        if not fname.endswith(".xml"):
            continue
        path = os.path.join(xml_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        def replace_in_wt(m):
            tag_open, text, tag_close = m.group(1), m.group(2), m.group(3)
            for old, new in REPLACEMENTS:
                if old in text:
                    stats[old] += text.count(old)
                    text = text.replace(old, new)
            return tag_open + text + tag_close

        content = re.sub(
            r"(<w:t[^>]*>)(.*?)(</w:t>)",
            replace_in_wt,
            content,
            flags=re.DOTALL,
        )
        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
    return stats


def print_report(stats):
    print("\n=== 교체 결과 ===")
    grand = 0
    for old, new in REPLACEMENTS:
        if stats[old]:
            print(f"  [{stats[old]:3d}회]  {old!r:45s} → {new!r}")
            grand += stats[old]
    print(f"\n총 {grand}개 교체 완료")
    return grand


def wash(input_path):
    input_path = os.path.abspath(input_path)
    base, ext = os.path.splitext(input_path)
    output_path = base + "_washed" + ext

    tmp_dir = tempfile.mkdtemp(prefix="en_wash_")
    try:
        # 1. 언팩
        print(f"언팩 중: {os.path.basename(input_path)}")
        result = subprocess.run(
            [sys.executable,
             os.path.join(DOCX_SKILL, "scripts/office/unpack.py"),
             input_path, tmp_dir],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("언팩 실패:", result.stderr)
            return

        # 2. 용어 교체
        xml_dir = os.path.join(tmp_dir, "word")
        stats = wash_xml_files(xml_dir)
        print_report(stats)

        # 3. 팩
        print(f"\n저장 중: {os.path.basename(output_path)}")
        result = subprocess.run(
            [sys.executable,
             os.path.join(DOCX_SKILL, "scripts/office/pack.py"),
             tmp_dir, output_path,
             "--original", input_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("팩 실패:", result.stderr[-500:])
            return

        print(f"\n완료: {output_path}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="영문 매뉴얼 오픈스택 워싱")
    parser.add_argument("--file", required=True, help="입력 docx 경로")
    args = parser.parse_args()
    wash(args.file)
