> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: kr-manual-change-tracker
description: Product 한국어 매뉴얼 변경점 추적 — 수기 체크리스트를 YAML 변경 원장에 등록하고, 기획서 PDF 대비 미등록 Screen ID를 체크하여 전체 커버리지를 검증한다. 버전 업 시 수기 체크리스트 또는 기획서 Document History를 받아 변경 원장을 완성하는 것이 목적.
metadata:
  type: skill
  status: active
  yaml_log: "[internal-repo-path] (레거시 소영)/매뉴얼/examples/change-request-log.3_0_5_to_3_0_6.yaml"
  validate_script: "[internal-repo-path] (레거시 소영)/매뉴얼/manual_pipeline/scripts/validate_manual_change_coverage.py"
  manual_docx: /Users/kimsoyoung/Desktop/manual/3.0.6매뉴얼/산출물/3.0.6_Product_Manual_260511_kr.docx
  spec_pdf: "/Users/kimsoyoung/Library/CloudStorage/[internal-path-removed]"
  repo: "[internal-repo-path] (레거시 소영)/매뉴얼"
---

> Sharing scope: Internal
> Share policy: caution
> Notes: 매뉴얼 변경 원장 YAML; 사내 버전(3.0.6 등)

## 이 스킬이 하는 일

Product 버전 업 시 발생하는 세 가지 작업을 일관되게 처리한다.

| 모드 | 트리거 | 결과 |
|---|---|---|
| **A — 체크리스트 등록** | 수기 체크리스트 텍스트 제공 | YAML에 CR 항목 추가 |
| **B — 미등록 건 체크** | 기획서 PDF 제공 | 기획서 Screen ID vs YAML 비교 표 |
| **C — 커버리지 검증** | 매뉴얼 docx 경로 확인 | 반영/미반영 현황 MD 생성 |

---

## 호출 예시

```
/kr-manual-change-tracker 체크리스트 등록해줘
/kr-manual-change-tracker 미등록 건 체크해줘
/kr-manual-change-tracker 커버리지 검증 실행해줘
/kr-manual-change-tracker 전체 다 해줘   ← A → B → C 순서 실행
```

---

## 필수 입력 (Mandatory Intake Gate)

작업 시작 전 아래를 반드시 확인한다. 없으면 질문한다.

| 모드 | 필수 입력 |
|---|---|
| A — 체크리스트 등록 | 수기 체크리스트 텍스트 (붙여넣기 또는 파일 경로) |
| B — 미등록 건 체크 | 기획서 PDF 경로 |
| C — 커버리지 검증 | 매뉴얼 docx 경로, YAML 경로 |

경로 기본값은 `metadata`의 경로를 사용하되, 버전이 바뀌면 반드시 사용자에게 확인한다.

---

## MODE A — 체크리스트 → YAML 등록

### Step 1. 마지막 CR 번호 확인

```python
import yaml, re
with open(yaml_path, encoding="utf-8") as f:
    data = yaml.safe_load(f)
cr_ids = [c["change_id"] for c in data["changes"]]
last_num = max(int(re.search(r'\d+', cid).group()) for cid in cr_ids)
# 다음 등록은 last_num + 1 부터
```

### Step 2. 기획서 Screen ID 목록 로드 (있으면)

```python
import fitz, re
doc = fitz.open(spec_pdf_path)
id_title_map = {}
for i in range(len(doc)):
    text = doc[i].get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for j, line in enumerate(lines):
        if line == 'Screen ID' and j+1 < len(lines):
            sid = lines[j+1]
            if re.match(r'CONT-\d{2}_\d{2}_\d{2,}', sid):
                for k in range(j+2, min(j+6, len(lines))):
                    if lines[k] == 'Page Title' and k+1 < len(lines):
                        id_title_map[sid] = lines[k+1]
                        break
```

### Step 3. 체크리스트 항목 파싱 규칙

수기 체크리스트는 자유 형식이므로 아래 패턴으로 항목 단위를 분리한다.

- 메뉴 경로(`>` 또는 `_` 구분), 변경 설명(`:` 이후), Screen ID 명시 여부 확인
- Screen ID가 명시된 항목(`CONT-XX_XX_XX` 포함): 그대로 사용
- Screen ID 미명시 항목: 기획서 `id_title_map`에서 메뉴명 키워드로 매칭, 없으면 `TBD`

### Step 4. YAML 항목 생성 규칙

```yaml
- change_id: CR-XXXXX          # last_num + 순번
  major_version: v3.0
  minor_version: v3.0.6        # 현재 작업 버전
  screen_id: CONT-XX_XX_XX     # 기획서 ID 또는 TBD
  screen_name: 메뉴_화면명
  change_type: 수정|신규|삭제|문구 변경|정책 변경|예외 케이스 추가|매뉴얼 보완
  title: 변경 내용 한 줄 요약
  before: 이전 버전 기준 정책/문구/동작
  after: 변경 후 내용
  reason: 수기 체크리스트 등록 항목
  requester: Product Planning Team
  assignee: Product Planning
  status: 요청됨                # 기본값. 완료 표시 있으면 기획반영
  approved_at: null
  figma_url: [figma-url-removed]
  manual_section: 'Screen ID: CONT-XX_XX_XX'
  include_release_note: true
  tags:
  - 3.0.5->3.0.6
  - product
  updated_at: 'YYYY-MM-DD'
```

**change_type 자동 분류 기준:**
- `신규 추가`, `추가 필요` → `신규`
- `삭제` → `삭제`
- `문구 추가`, `안내 문구` → `문구 변경`
- `정책`, `원복`, `역할` → `정책 변경`
- 나머지 → `수정`

**status 자동 분류 기준:**
- 체크리스트에 `[완료]` 표시 → `기획반영`
- `===> 여기까지 캡쳐 완료` 이전 구간 → `기획반영`
- `(ing)` → `검토중`
- 나머지 → `요청됨`

### Step 5. YAML 파일 append

기존 파일 마지막에 추가. `yaml.dump` 사용 시 한글 유지(`allow_unicode=True`).

---

## MODE B — 미등록 건 체크

기획서 Document History(p3~p6)에서 버전별 변경 Screen ID를 추출하고, 현재 YAML에 등록된 Screen ID와 비교한다.

### Step 1. 기획서 Document History 파싱

```python
import fitz, re
doc = fitz.open(spec_pdf_path)
# p3~p6: Document History (버전에 따라 페이지 수 다를 수 있음)
# "Document History" 텍스트가 있는 페이지를 자동 탐지
history_pages = []
for i in range(len(doc)):
    if "Document History" in doc[i].get_text():
        history_pages.append(i)

all_spec_ids = set()
for pi in history_pages:
    text = doc[pi].get_text()
    ids = re.findall(r'CONT-\d{2}_\d{2}[_-]\d{2,}', text)
    all_spec_ids.update(ids)
```

### Step 2. YAML 등록 Screen ID와 비교

```python
with open(yaml_path, encoding="utf-8") as f:
    data = yaml.safe_load(f)
yaml_ids = {c["screen_id"] for c in data["changes"] if c.get("screen_id")}

missing_in_yaml = sorted(all_spec_ids - yaml_ids)
extra_in_yaml = sorted(yaml_ids - all_spec_ids)  # TBD 등 추정값
```

### Step 3. 미등록 건 보고

```
## 기획서 대비 미등록 Screen ID

| Screen ID | 기획서 버전 | 추정 화면명 |
|---|---|---|
| CONT-03_01_01 | v1~v2 | 인스턴스_목록 |
...

→ 등록할까요? [Y] 일괄 등록 / [N] 스킵
```

사용자가 Y 선택 시: 미등록 건을 `change_type: 매뉴얼 보완`, `status: 요청됨`으로 YAML에 추가.

---

## MODE C — 커버리지 검증

```bash
cd "[internal-repo-path] (레거시 소영)/매뉴얼"
python3 manual_pipeline/scripts/validate_manual_change_coverage.py \
  --change-log "examples/change-request-log.3_0_5_to_3_0_6.yaml" \
  --manual-docx "<매뉴얼 docx 경로>" \
  --target-version "v3.0.6" \
  --out-dir "<output 디렉토리>"
```

결과 파일: `manual_change_coverage.md`, `manual_change_coverage.csv`

검증 후 요약을 사용자에게 보고한다:

```
## 커버리지 결과
- 전체: N건
- 반영: N건 (N%)
- 미반영: N건

미반영 항목 중 status가 '매뉴얼반영'/'승인완료'인 건이 있으면 경고.
```

---

## 버전 전환 시 체크리스트

새 버전(예: v3.0.7) 작업 시작 전:

1. YAML 파일명 복사: `change-request-log.3_0_6_to_3_0_7.yaml`
2. `metadata.yaml_log`, `manual_docx`, `spec_pdf` 경로 업데이트
3. 새 기획서 PDF에서 Document History 재파싱
4. CR 번호 시작점 확인 (기존 마지막 번호 + 1)

---

## 완료 기준

- [ ] 수기 체크리스트 전 항목 YAML 등록
- [ ] 기획서 Document History 대비 미등록 0건 (또는 의도적 스킵 명시)
- [ ] 커버리지 검증 실행 완료
- [ ] 미반영 항목 중 `매뉴얼반영`/`승인완료` 상태인 건 0건
