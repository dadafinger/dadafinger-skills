> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: kr-manual-format-review
description: >
  한국어 Product 매뉴얼(.docx)의 서식 일관성을 검수하고 원본에서 바로 수정한다.
  신규 섹션 추가 후 "서식 검수해줘", "매뉴얼 서식 안 맞는 거 있는지 봐줘",
  "서식 통일해줘", "이미지 크기 맞춰줘", "표 크기 통일해줘" 등을 언급하거나,
  매뉴얼 docx와 함께 서식/스타일/이미지·표 크기 점검 요청이 오면 이 스킬을 사용한다.
  검수 전용(MODE A)과 검수+수정(MODE B), 이미지·표 폭 크기 일관성 정규화를 지원한다.
metadata:
  type: skill
  status: active
  script: scripts/format_check.py
  script_size: scripts/size_normalize.py
  origin_session: 3.0.6 HA 관리 섹션 서식 검수 (2026-06-11)
---

> Sharing scope: Internal
> Share policy: caution
> Notes: 한글 매뉴얼 서식; 사내 서식 규칙

# 한국어 매뉴얼 서식 검수/수정 스킬

신규 섹션이 추가된 매뉴얼 docx에서 **문서 전체 관례와 어긋나는 서식**을 찾아내고,
요청 시 원본 파일에서 바로 수정한다. (수정 전 `.bak.docx` 백업 필수)

## 실행 모드

```
서식 안 맞는 거 있는지 검수해줘        →  MODE A (검수 리포트만)
수정할 게 있으면 바로 원본에서 수정해줘  →  MODE B (백업 → 수정 → 검증)
```

## 필수 입력 (Intake Gate)

| 입력 | 기본값 | 비고 |
|---|---|---|
| 매뉴얼 docx 경로 | 사용자 첨부 경로 | 없으면 질문 |
| 검수 범위 | 전체 | "OO 섹션 추가했어"라고 하면 해당 H1 섹션 우선 |

## MODE A — 검수 (read-only)

```bash
python3 scripts/format_check.py --file "매뉴얼.docx"            # 전체
python3 scripts/format_check.py --file "매뉴얼.docx" --section "HA 관리"
```

스크립트가 잡지 못하는 항목은 아래 **검수 체크리스트**를 기준으로 에이전트가 직접
paragraph 덤프를 떠서 확인한다.

## 검수 체크리스트 (문서 관례 기준)

### 1. 제목(Heading) 서식
- [ ] 제목 번호는 **텍스트로 수동 입력** (`1.1 HA 조회`). 자동 번호 매기기(numPr)가
      제목에 붙어 있으면 제거하고 수동 번호로 교체
- [ ] 번호 깊이와 Heading 레벨 일치: `1.` = H2, `1.1` = H3, `1.1.1` = H4
      (예: `1.4 …`가 Heading 2로 지정된 오류)
- [ ] H1 제목 표기가 본문 표기와 일치 (`HA관리` vs `HA 관리`)
- [ ] 상세 탭 제목은 `상세 정보 - …` 형식 (`상세 - …` 금지)
- [ ] 수정·삭제 제목은 `수정/삭제` 순서 (`삭제/수정` 금지 — 문서 전체 24 vs 2 관례)

### 2. 폰트
- [ ] 본문/제목에 `Pretendard JP Variable` 등 비표준 폰트 금지
      (일본어 매뉴얼에서 복사 시 유입됨) → 본문은 `Pretendard`, 제목은 rFonts
      제거 후 스타일 상속

### 3. 문자/공백
- [ ] 특수 공백(nbsp, `\xa0`) 금지 → 일반 공백 (웹/타문서 복사 흔적)
- [ ] `선택후` → `선택 후`, `] 에서` → `]에서`, `] 를` → `]를`
- [ ] 문장 끝 마침표 누락 (`…가능합니다` → `…가능합니다.`)

### 4. 본문 목록 번호
- [ ] 절차 목록 형식은 `1) 2) 3)` (numFmt `%1)`) — `1. 2. 3.` 금지
- [ ] 한 절차는 **하나의 numId로 연속** — 항목마다 다른 numId(start override로
      1,2,3,4를 흉내내는 패턴) 금지. 중간에 이미지가 끼어도 같은 numId 유지

### 5. 콜아웃(주의/참고 사항)
- [ ] `주의 사항`/`참고 사항`은 일반 문단이 아니라 **콜아웃 표**
      (1x1, 회색 배경 `F3F3F3`, 좌측 파란 테두리 `1155CC`)로 작성.
      기존 콜아웃 표(`5GiB` 주의 사항 등)를 deepcopy해서 텍스트만 교체

### 6. 내용 복사 흔적
- [ ] 타 섹션 잔재 단어 (`스택`, `인스턴스` 등 해당 메뉴와 무관한 대상어)
- [ ] 본문 메뉴 경로가 실제 LNB와 일치 (`[HA 관리 > HA 설정]`)

### 7. 이미지·표 크기 일관성 (전용 스크립트 `size_normalize.py`)
- [ ] 넓은 스크린샷 폭이 페이지마다 제각각(6.18/6.22/6.27/6.32in…)이면 **단일 정본 폭**으로 통일.
      마우스로 대충 드래그해 넣은 흔적 → 본문 좌우 가장자리가 들쭉날쭉해 보이는 원인
- [ ] 표 폭도 같은 정본 폭으로 통일하면 이미지·표 가장자리가 한 줄로 정렬됨
- [ ] **비율/열 비율은 보존**하고 폭만 스냅 (이미지=가로세로비 유지, 표=열 비율 유지)
- [ ] 아이콘·작은 인라인 이미지, auto(내용맞춤) 표, 들여쓰기 표는 **의도적 크기라 제외**

## 이미지·표 크기 정규화 (size_normalize.py)

폭 드리프트를 정본 폭 하나로 스냅한다. **비율 유지**(이미지=가로세로비, 표=열 비율),
3층 동기(이미지 `wp:extent`+xfrm `a:ext` / 표 `tblW`+`gridCol`+셀 `tcW`).

```bash
# 1) analyze — 읽기전용 분포·정본폭 권고 (수정 없음)
python3 scripts/size_normalize.py --file "매뉴얼.docx"

# 2) apply — 백업(.bak.docx) 후 정본폭으로 통일 (이미지+표)
python3 scripts/size_normalize.py --file "매뉴얼.docx" --apply
#   정본폭 자동 = 이미지 최빈 폭. 표는 같은 inch를 twip으로 환산해 이미지와 정렬.

# 옵션
python3 scripts/size_normalize.py --file "M.docx" --apply --width-in 6.2701  # 폭 명시
python3 scripts/size_normalize.py --file "M.docx" --apply --scope images     # 이미지만
python3 scripts/size_normalize.py --file "M.docx" --apply --scope tables --table-scope 2col
```

기본 정책(스크립트 내장):
- 이미지: `--min-img-in`(기본 5.5in) 이상만 스냅. 미만은 아이콘/인라인으로 보고 제외.
  스냅 결과 높이가 `--max-img-in`(기본 9.5in) 초과면 페이지 넘침으로 보고 제외.
- 표: 고정폭(dxa)·비들여쓰기만 스냅. `auto`(내용맞춤)·`tblInd>0`(들여쓰기) 표는 제외+리포트.
  열 비율은 표별로 보존하고 전체폭만 스냅(열폭 합계 = 전체폭 정확 일치).
- 단위: 이미지 EMU(914400/in) · 표 twip(1440/in) · 1 twip=635 EMU. 이미지 정본폭 inch를
  표 twip으로 환산해 **이미지와 표를 같은 폭**으로 맞춤(문서 전체 가장자리 정렬).
- **가정**: 표 중첩 없음(비탐욕 `<w:tbl>` 매칭). 적용 전 analyze로 분포 확인 권장.
- **멱등**: 이미 정본폭인 항목은 건드리지 않음(재실행 안전).

## MODE B — 수정 절차

1. **백업**: `cp 원본.docx 원본.bak.docx` (같은 폴더, `.bak.docx` 접미사)
2. 기계적 수정은 스크립트로:
   ```bash
   python3 scripts/format_check.py --file "매뉴얼.docx" --fix [--section "HA 관리"]
   # nbsp→공백, JP 폰트→Pretendard, 이중 공백 정리만 자동 수정
   ```
3. 구조적 수정(제목 레벨/번호, 목록 numId 통합, 콜아웃 표 변환, 어순 교체)은
   python-docx로 직접 수행. **주의사항**:
   - 제목 텍스트 교체 시 run만 갈아끼우고 **bookmarkStart/End는 보존** (TOC 링크용)
   - `수정/삭제` 어순 교체는 run이 `삭제`+`/`+`수정…`으로 쪼개져 있을 수 있음 —
     인접 run 3개 패턴(`…삭제`, `/`, `수정…`)을 찾아 양끝만 스왑
   - 목록 통합 시 같은 numId 재사용은 카운터가 이어지므로, 새 리스트가 필요하면
     numbering.xml에 `w:num`(abstractNumId 참조 + `startOverride=1`)을 새로 추가
   - 콜아웃 표 삽입은 `anchor.addprevious(new_tbl)` 후 기존 문단 제거
4. **검증**: 저장 후 다시 열어 섹션 덤프 — nbsp 0, JP 폰트 run 0, 금지 표기 0,
   제목 레벨/번호 정합 확인
5. **보고**: 수정 내역을 분류별로 사용자에게 보고 + TOC 업데이트 안내

## 후속 안내 (필수)

- 목차(TOC)는 Word 필드라 스크립트로 재생성하지 않는다 — 사용자에게
  **Word에서 목차 클릭 → F9 → "목차 전체 업데이트"** 안내
- `.bak.docx`는 사용자 확인 후 삭제하도록 안내

## 완료 기준

- [ ] 검수 리포트 제출 (MODE A) 또는 수정+검증 완료 (MODE B)
- [ ] MODE B 시 백업 파일 존재
- [ ] 검증 덤프에서 체크리스트 위반 0건
- [ ] TOC 업데이트 안내 전달
