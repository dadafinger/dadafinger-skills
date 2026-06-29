---
name: openstack-glossary-en
description: >
  다국어 용어집 Excel 파일(.xlsx)에 영어 번역 열을 추가하거나 채울 때 사용한다.
  반드시 아래 상황에서 이 스킬을 사용할 것:
  사용자가 "영문 열 추가", "영어열 채워", "오픈스택 기준으로 번역", "영어 번역 추가",
  "다국어 용어집", "영문 번역 파일", "용어집 영어" 등을 언급하거나,
  한국어/영어/일어 열이 있는 Excel 용어집 파일에서 영어 열이 비어있다고 하면 즉시 이 스킬을 사용한다.
  오픈스택 표준 용어(인스턴스 유형→Flavor, 유동 IP→Floating IP 등)와
  공통 UI 용어(작업→Actions, 생성일시→Created At 등), 역할 이름(최고관리자→Super Admin 등)을 자동 적용한다.
---

> Sharing scope: General
> Share policy: share
> Notes: OpenStack 용어집 번역; 공개 표준

# OpenStack 용어집 영어 번역 스킬

Excel 용어집 파일에서 한국어 열을 읽고, OpenStack 표준 용어 기준으로 영어 열을 채운다.
기존 번역이 있는 셀은 건드리지 않고, 빈 셀만 채운다.

## 전체 흐름

1. **파일 구조 파악** — openpyxl로 시트 목록과 열 구조 확인
2. **번역 대상 열 식별** — 헤더 행에서 `한국어` 셀을 찾고, 바로 오른쪽 열을 영어 열로 간주
3. **번역 적용** — `scripts/translate.py`의 `TRANSLATIONS` 사전으로 빈 영어 셀만 채움
4. **저장 후 검증** — 채운 수, 누락 항목 출력

## 열 구조 감지

헤더 행(1~5행 사이)에서 값이 `'한국어'`인 셀을 찾는다.
그 셀의 바로 오른쪽 열이 영어 열이다.
헤더가 없거나 구조가 다를 경우, 실제 셀 값을 보고 사용자에게 열 위치를 확인한다.

```python
for row in ws.iter_rows(min_row=1, max_row=5):
    for cell in row:
        if cell.value == '한국어':
            kor_col = cell.column
            eng_col = kor_col + 1
```

## scripts/translate.py 사용

번역 사전과 실행 로직이 모두 들어 있다. 다음 두 가지 방법으로 사용한다.

**CLI로 직접 실행:**
```bash
python scripts/translate.py --file "파일경로.xlsx"
# 특정 시트만:
python scripts/translate.py --file "파일경로.xlsx" --sheets "CON EN,Product"
```

**Python에서 import:**
```python
from scripts.translate import translate_file, TRANSLATIONS
translate_file("파일경로.xlsx", target_sheets=["CON EN"])
```

## 사전에 없는 항목 처리

스크립트 실행 후 "사전 미등록 항목" 목록이 출력된다.
이 항목들은 빈칸으로 남긴다 — 임의로 번역하지 않는다.
사용자에게 목록을 보여주고, 추가할 번역이 있으면 `TRANSLATIONS` 사전에 추가한 뒤 재실행한다.

## 제외 시트

**VIOLA 시트는 무조건 제외한다.** 한국어/영어 구조가 아니므로 번역 대상에서 항상 제외.
`scripts/translate.py`의 `EXCLUDED_SHEETS`에 등록되어 있으며, 별도 지시 없이 절대 처리하지 않는다.

## 주의사항

- 기존에 값이 있는 영어 셀은 절대 덮어쓰지 않는다
- VPC, HA, SSL, Product 등 영문 약어는 그대로 유지한다
- 셀 스타일(폰트, 정렬)은 인접 한국어 셀에서 복사한다
- 저장 전 백업이 필요하면 `import shutil; shutil.copy(원본, 백업경로)` 사용
