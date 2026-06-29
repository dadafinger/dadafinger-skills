> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: kr-manual-quickguide
description: 3.0.6 한국어 Product 매뉴얼의 '퀵 가이드' 섹션 완성 및 유지보수. 퀵가이드는 상세 가이드의 요약이므로 이미지 중복 삽입 대신 내부 하이퍼링크를 사용한다. 링크 삽입 스크립트, 품질 검수, 링크 재생성 3가지 모드를 지원한다.
metadata:
  type: skill
  status: active
  target_doc: /Users/kimsoyoung/Desktop/manual/3.0.6매뉴얼/산출물/3.0.6_Product_Manual_260511_kr.docx
  spec_pdf: "/Users/kimsoyoung/Desktop/manual/3.0.6매뉴얼/명령용 306 압축 기획서/[3.0.6] Product_v8_20260421.pdf"
  repo: "[internal-repo-path] (레거시 소영)/매뉴얼"
  script: manual_pipeline/scripts/quickguide_add_hyperlinks.py
---

> Sharing scope: Internal
> Share policy: caution
> Notes: 퀵가이드 하이퍼링크; 사내 매뉴얼 구조

## 이 스킬이 하는 일 (한 줄 요약)

한국어 매뉴얼의 **퀵 가이드** 섹션을 관리합니다.  
퀵 가이드란 "기본 설정 → VPC 설정 → 인스턴스 생성" 흐름을 빠르게 안내하는 요약 페이지입니다.

---

## 어떻게 사용하나요? (초보자용)

### 상황별 선택

```
DOCX 파일이 새로 교체됐어요  →  MODE A (링크 재삽입)
내용이 기획서 v8 기준에 맞는지 검토하고 싶어요  →  MODE B (품질 검수)
퀵가이드에 새 섹션이 생겼어요  →  MODE C (링크 추가)
```

### 호출 예시

```
/kr-manual-quickguide 링크 재삽입해줘           ← MODE A
/kr-manual-quickguide 퀵가이드 검수해줘          ← MODE B
/kr-manual-quickguide "알람센터" 섹션 링크 추가해줘  ← MODE C
```

### 대상 파일

```
DOCX  ~/Desktop/manual/3.0.6매뉴얼/산출물/3.0.6_Product_Manual_260511_kr.docx
PDF   ~/Desktop/manual/3.0.6매뉴얼/명령용 306 압축 기획서/[3.0.6] Product_v8_20260421.pdf
```

---

## 설계 결정 이력

| 검토 순서 | 방안 | 결정 |
|---|---|---|
| 1안 | Playwright 신규 캡처 삽입 | ❌ 퀵가이드는 상세 가이드 요약이므로 중복 |
| 2안 | 상세 가이드 이미지 복사 재사용 | ❌ 내용 변경 시 두 곳 모두 수정 필요 → 정합성 문제 |
| **3안 (채택)** | **상세 가이드로 내부 하이퍼링크** | **✅ 단일 소스, 유지보수 용이** |

---

## 현재 상태 (2026-06-04 기준)

| 섹션 | 텍스트 | 하이퍼링크 |
|---|---|---|
| 1. 기본 설정 | ✅ 완료 | ✅ 삽입 완료 (2개) |
| 2. VPC 설정 | ✅ 완료 | ✅ 삽입 완료 (5개) |
| 3. 인스턴스 생성 | ✅ 완료 | ✅ 삽입 완료 (1개) |

**삽입된 링크 목록 (총 8개):**

```
[기본 설정] 끝
  ↗ 상세 가이드: 이미지 생성          → bookmark _Toc228369051
  ↗ 상세 가이드: 인스턴스 유형 생성    → bookmark _Toc228369060

[VPC 설정] 끝
  ↗ 상세 가이드: 세그먼트 생성         → bookmark _Toc228369087
  ↗ 상세 가이드: 라우터 생성           → bookmark _Toc228369092
  ↗ 상세 가이드: 유동 IP 생성          → bookmark _Toc228369097
  ↗ 상세 가이드: 보안 그룹 생성        → bookmark _Toc228369106
  ↗ 상세 가이드: 로드밸런서 생성        → bookmark _Toc228369101

[인스턴스 생성] 끝
  ↗ 상세 가이드: 인스턴스 생성         → bookmark _Toc228369076
```

---

## 실행 모드

### MODE A — 링크 재삽입 (DOCX 교체·재생성 후)

DOCX가 새로 교체되면 삽입된 링크가 사라진다. 스크립트를 다시 실행한다.

```bash
cd "[internal-repo-path] (레거시 소영)/매뉴얼"
.venv/bin/python manual_pipeline/scripts/quickguide_add_hyperlinks.py
```

- 자동으로 `.bak.docx` 백업 생성 후 수정
- 대상 파일: `Desktop/manual/3.0.6매뉴얼/산출물/3.0.6_Product_Manual_260511_kr.docx`

### MODE B — 품질 검수

기획서(v8 PDF) 기준으로 아래 항목을 점검한다.

```
2026-06-04 검수 결과:

[✅] 전체 — 하이퍼링크 8개 존재 확인 (_Toc 앵커 8개 정상 삽입)
[✅] 2. VPC 설정 — LB 리스너·풀 단계별 입력 흐름 반영됨

[❓] 1. 기본 설정 — GPU 관련 안내 필요 여부 (퀵가이드 범위인지 확인 필요)
[❓] 2. VPC 설정 — 세그먼트 외부 유형 안내 포함 여부 (현재 미언급)
[❓] 2. VPC 설정 — LB 임계치 설정 반영 여부 (현재 미언급, 퀵가이드 범위 확인)
[❓] 3. 인스턴스 생성 — 무중단 안내 문구 (현재 미언급, 퀵가이드 범위 확인)
[❓] 전체 — LNB 알람센터 퀵가이드 포함 여부 (스쿼드 검수 전 범위 결정)
[ ] 전체 — 하이퍼링크 8개 Ctrl+클릭 동작 (Word에서 직접 확인 필요)
```

### MODE C — 링크 추가/수정

퀵가이드에 새 섹션이 생기거나 링크 대상이 바뀔 경우 스크립트의 `SECTION_LINKS` 딕셔너리를 수정한다.

```python
# manual_pipeline/scripts/quickguide_add_hyperlinks.py
SECTION_LINKS: dict[str, list[tuple[str, str]]] = {
    "기본 설정": [
        ("_Toc228369051", "이미지 생성"),
        ("_Toc228369060", "인스턴스 유형 생성"),
    ],
    "VPC 설정": [
        ("_Toc228369087", "세그먼트 생성"),
        ("_Toc228369092", "라우터 생성"),
        ("_Toc228369097", "유동 IP 생성"),
        ("_Toc228369106", "보안 그룹 생성"),
        ("_Toc228369101", "로드밸런서 생성"),
    ],
    "인스턴스 생성": [
        ("_Toc228369076", "인스턴스 생성"),
    ],
}
```

북마크 이름은 `_Toc`로 시작하는 Word 자동 생성 북마크. DOCX가 새로 생성되면 북마크 이름이 바뀔 수 있으므로 재확인 필요.

#### 북마크 확인 명령

```bash
cd "[internal-repo-path] (레거시 소영)/매뉴얼"
.venv/bin/python3 - <<'EOF'
import zipfile
from xml.etree import ElementTree as ET
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
docx = "/Users/kimsoyoung/Desktop/manual/3.0.6매뉴얼/산출물/3.0.6_Product_Manual_260511_kr.docx"
with zipfile.ZipFile(docx) as z:
    root = ET.fromstring(z.read("word/document.xml"))
targets = ["이미지 생성", "인스턴스 유형 생성", "인스턴스 생성", "세그먼트 생성",
           "라우터 생성", "유동 IP 생성", "보안 그룹 생성", "로드밸런서 생성"]
for p in root.findall(".//w:p", NS):
    text = "".join(r.text or "" for r in p.findall(".//w:t", NS)).strip()
    for t in targets:
        if text == t or text.endswith(t):
            bms = [bm.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name","")
                   for bm in p.findall(".//w:bookmarkStart", NS)]
            if bms:
                print(f"{text!r:35s} → {bms}")
EOF
```

---

## 완료 기준

- [x] 텍스트 3섹션 작성 완료
- [x] 내부 하이퍼링크 8개 삽입 완료
- [ ] MODE B 품질 검수 통과
- [ ] 스쿼드 검수 완료
- [ ] 체크리스트 항목 `퀵가이드 추가 [작성중]` → `[완료]` 갱신
