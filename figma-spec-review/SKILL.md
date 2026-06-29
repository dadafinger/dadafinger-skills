> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: figma-spec-review
description: Product Product 4.0 Figma 상세 명세 페이지를 읽기 전용으로 검수한다. 한 노드(또는 노드 목록)를 4개 기준 ① 포맷 준수 ② 용어 일관성 ③ Description 표준 ④ 노드 구조 무결성 으로 점검하고, 각 위반을 SoT 룰 근거와 함께 PASS/WARN/FAIL로 판정한 구조화 리포트를 낸다. 노드 단위로 독립 실행되므로 다건을 루프/워크플로로 돌리기 좋다. "figma 검수", "상세 명세 검수", "노드 검수", "포맷 맞는지 봐줘", "용어 일치 점검", "검수 루프", "spec review"가 트리거. 쓰기(use_figma) 금지 — 검수만 한다. 실제 수정은 figma-change-flow가 담당.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: Figma 상세 명세 검수; node-registry 참조

# Figma Spec Review (검수자)

Product 4.0 Figma **상세 명세 페이지를 읽기 전용으로 검수**하는 룰 SoT. 한 노드를 **4개 기준**으로 점검해 위반을 근거와 함께 판정한다.

> **🔴 읽기 전용 — 절대 쓰지 않는다.** 이 스킬은 `use_figma`(쓰기·JS 실행)를 호출하지 않는다. `get_metadata`/`get_screenshot`/`get_design_context`(+ 읽기 전용 순회)만 쓴다. 위반을 **고치지 않고 보고만** 한다 → 수정은 [`figma-change-flow`](../figma-change-flow/SKILL.md), Description 내용 보강은 [`figma-desc-spec`](../figma-desc-spec/SKILL.md)로 넘긴다.

## 역할 분담

| 스킬 | 역할 |
|---|---|
| **figma-spec-review (이 스킬)** | **검수(READ)** — 룰 대비 위반 탐지·판정·리포트. 안 고침. |
| figma-desc-spec | Description **내용 표준(WHAT)** SoT — ③의 근거(무엇이 맞는지). |
| planning-md · -html | **포맷·섹션계약 SoT** — ①의 근거(섹션계약 `planning-md/assets/명세서_템플릿.md` + 공통템플릿 디자인 DNA `planning-html/assets/공통템플릿/` + 4중 정합 `### N`=①②③=`.area-no`=`Section N`. 상세 `planning-html/references/render-detail.md`). |
| figma-change-flow | Figma **렌더·수정(HOW/WRITE)** — 검수에서 나온 위반을 실제로 반영 + 노드구조 함정·node-registry. |
| critique-reviewer | 산출물 **전략·정책 공백** 비판(상위) — 화면 외 회의록·거버넌스까지. |

이 스킬은 critique-reviewer와 달리 **단일 Figma 노드의 포맷/용어/Description/구조 적합성**만 본다(좁고 기계적·반복 가능). critique-reviewer는 회의록·전략까지 보는 넓은 비판.

## 언제 쓰나

트리거: `figma 검수`, `상세 명세 검수`, `노드 검수`, `포맷 맞는지 봐줘`, `용어 일치 점검`, `검수 루프`, `spec review`, `/figma-spec-review`.

쓰지 말 것:
- 위반을 **고쳐달라** → figma-change-flow / figma-desc-spec.
- 회의록·전략·동작 정책 공백 비판 → critique-reviewer.
- 매뉴얼 docx 서식/이미지 검수 → kr-manual-format-review / manual-image-review.

## Intake Gate (검수 시작 전 필수)

1. **대상 노드 확정** — Figma URL 또는 `fileKey` + `node-id`. 없으면 질문(`피그마 경로는 매번 모르면 물어봐주세요.`). 다건이면 노드 목록.
2. **기준 세대 확인** — 기본 **4.0.0** 기준(전역 history 페이지 운영 → 개별 페이지 Changelog/버전 마커 없음). 구세대 검수 시 사용자가 명시.
3. **검수 범위 확인 (4.0 통일 대상만)** — 4.0 Figma 기획서 통일 대상은 **신규 5종(미터링·집계·알람·IP·GPU)뿐**이다. **볼륨백업 등 "고도화" 항목은 검수 범위 밖** → 검수하지 않고 "범위 제외"로 표기(SoT: `proprium/4.0_Figma_기획서_관리.md`). `[node-id]` 알람센터 기존화면도 참고용 절대 제외. 대상이 통일 범위인지 먼저 확인.
4. **(선택) 용어 SoT 경로** — 알람 용어집 등. 미지정 시 design-system.md·node-registry.md 라벨을 기준으로 검사하고, 외부 용어 SoT 미확인은 리포트에 명기.

**노드가 정말 상세 명세인지 헤더로 먼저 확인** — 레이어명 ≠ 내용. 한 파일에 같은 Screen ID가 현행/마스터/구버전으로 중복 존재한다. 헤더(Screen ID·Page Title·Author)를 읽어 검수 대상이 맞는지 확정(→ node-registry.md §사용 규칙).

## 읽기 절차 (쓰기 없음)

1. `get_metadata`로 노드 트리(id/name/type/위치/크기) 회수. hang 시 `use_figma` **읽기 순회**로 `return JSON.stringify(...)`(console.log 회수 안 됨).
2. `get_screenshot`으로 **시각 확인**(목업 ①②③ 마커, 빈 영역, 깨진 폰트, 잘림).
3. 본문 텍스트는 `get_design_context` 또는 읽기 순회로 `characters` 회수. hang하면 스크린샷으로 갈음하고 리포트에 "시각 판독" 명기.
   - **🔴 거터(번호 칼럼) 셀을 반드시 따로 읽는다** — 섹션 거터(num 50px 셀, 예: `Frame 17`)의 텍스트를 순서대로 회수해 `1,2,3,…` 시퀀스를 직접 나열한다. 본문만 읽고 거터를 건너뛰면 거터 넘버링 오류(건너뜀·중복·누락·마커 불일치)를 못 잡는다(실제 미검출 사례 2026-06-24, node `[node-id]`). 거터 번호 ↔ 목업 ①②③ 마커 ↔ 섹션 위치를 **나란히 표로 대조**한다.
4. **검수 대상 텍스트를 인용**해 근거로 남긴다(추측 금지).

## 4대 검수 기준

각 항목은 `references/checklist.md`에 기계 점검용 체크리스트로 분해돼 있다. **검수 시 반드시 펼쳐 전수 확인**한다. 요약:

### ① 포맷 준수 (Format)
근거 SoT: **`planning-md/assets/명세서_템플릿.md` 섹션 계약 + `planning-html/assets/공통템플릿/`(tokens/base/template = 디자인 DNA 정본)** + figma-change-flow "상세 명세 페이지 해부" + 메모리 *Figma 기획서 표준 포맷*·*포맷 준수 피드백*.
- **🔑 섹션 계약 = 4중 정합의 권위 출처**: `### N · 기능요소명 <!-- marker=① screen=… -->` 으로 **md `### N` = 목업 ①②③ = HTML `.area-no` = Figma `Section N`(거터 번호)** 가 1:1로 박제된다. 거터·마커·섹션 정합(③ D1·G1–G6)은 이 계약을 기준으로 판정.
- 3단 골격(헤더행 / 좌 1920 목업 칼럼 / 우 Description 칼럼 2개) 존재.
- 검은 풀폭 타이틀 바(Description/Appendix) + 섹션 = 거터(번호) + title-bar + 불릿 노드들.
- **포맷은 예시 노드 클론으로 보장** — 손그림/임의 레이아웃이면 FAIL.
- **덩어리 단일 텍스트 노드 금지**(가독성 1순위 지적) → 섹션·불릿이 노드 단위로 쪼개졌는가.
- **빈 Changelog 금지**(개별 페이지가 자체 Changelog 운영하는 경우). 4.0.0 전역 history 운영 시엔 반대로 **개별 페이지에 Changelog/버전 마커가 있으면 FAIL**.

### ② 용어 일관성 (Terminology)
근거 SoT: 메모리 *알람 용어집 v3.3* + design-system.md.
- 라벨 표기 = **"Product 엔진"**(엔진 라벨 통일).
- 심각도 = 전 화면 `{Severity1/2/3…}` 토큰(고객사 커스텀, 기본 예시 Critical/Warning/Info **3단계**). "2단계" 등 옛 표기 잔존 시 FAIL.
- 같은 개념이 화면 내/화면 간 다른 라벨로 쓰이면 WARN+위치 인용.
- 버튼·상태·필드 라벨이 design-system / 상태값 SoT와 어긋나면 FAIL.

### ③ Description 표준 (Description)
근거 SoT: **figma-desc-spec (WHAT의 SoT)** — 검수 전 그 스킬 + `references/screen-type-checklists.md`를 펼친다.
- **목업 ①②③ 마커 N개 = Description 섹션 N개**(1:1). 불일치 = 누락 신호(FAIL).
- 섹션 본문 구성·순서 = **UI 요소(라벨 없이 넘버링) → 상태·케이스 → 제약 → 동작 정책(맨 뒤)**.
- 번호 규칙: 거터 있는 섹션은 거터가 번호 → 제목·본문 넘버링 금지 / 거터 없는 설명란은 온점 넘버링(`1. 2.`).
- **거터 넘버링 무결성(checklist G1–G6, FAIL)**: 거터 셀 번호가 `1,2,3,…` **연속**인가(건너뜀/역순 X) · **중복** 없는가 · **목업 ①②③ 마커와 1:1** 정렬인가 · 빈 칸/번호 **누락** 없는가 · `3-1/3-2` **하위 분할이 부모·마커와 정합**인가 · 거터 마지막 번호 = **섹션 개수** 인가. 거터 셀을 순서대로 읽어 시퀀스를 명시 대조(읽기 절차 3 참조).
- 문체 = **명사형(개조식) 종결**(`~함/~음/~없음`), 경어체·`~한다` 본문 종결 금지. AI 정형구(`또한`·`뿐만 아니라`) 검출 시 WARN.
- 제약 표기: `단,`=예외 / `유효성:`=검증 / `~할 경우`=조건.
- 이모지·장식 글리프(`💾 ▷ ✓ ● ▼` 등) 검출 시 FAIL(캡처 깨짐). 허용 표기만: `[버튼]`·`「라벨」`·`→`·`·`·`①②③`.
- 미결: 본문에 `(미결)` 인라인이 섞이면 WARN(맨 아래 「미결 사항」 블록으로 분리해야 함). `[OI-N]` 신규 넘버링 도입 시 FAIL(기존 토큰 `U-10/T-11/V-12/F-16` 유지).
- 전수 서술: 화면 4종(목록/생성/수정/상세) 유형별 필수 항목 누락 점검(checklist.md).

### ④ 노드 구조 무결성 (Structure)
근거 SoT: node-registry.md + figma-change-flow "auto-layout/텍스트 함정".
- **중복/마스터/구버전 혼입** 점검: 같은 Screen ID의 현행 외 잔존본을 잘못 검수/참조하고 있지 않은가(헤더 대조).
- 이중 불릿(`• ·`), 숨김 stray 텍스트 노드(옛 `· `/`— ` 잔재 visible=false), 깨진 폰트(Roboto 한글 공백·더블클릭해야 보임) 검출.
- 높이 정합: Description 콘텐츠가 카드 밖으로 흐르거나 `clip`으로 잘림.
- **Description ↔ 좌측 와이어프레임 정합**: 한쪽만 바뀐 모순 검출(스펙=화면 불일치).
- PII: 목업 샘플에 실직원 이메일(`@example.com`)·실명·고객사명·공인 IP 잔존 시 FAIL(제출 워싱 위반).
- 4.0.0: 개별 페이지에 일정/검증 워킹노트·Changelog·버전 마커 잔존 시 FAIL.

## 판정 등급

| 등급 | 의미 |
|---|---|
| **FAIL** | SoT 명시 룰 위반. 제출/반영 전 반드시 수정. |
| **WARN** | 룰 위반은 아니나 권고 이탈·일관성 흔들림·확인 필요. |
| **PASS** | 해당 기준 충족. |
| **N/A** | 그 노드에 해당 항목 없음(사유 명기). |

- **추측 금지·인용 필수**: 모든 FAIL/WARN은 노드 id + 인용 문구/스크린샷 근거를 단다.
- **고치지 않는다**: 수정안은 "권고 조치" 한 줄로만 남기고 실제 반영은 figma-change-flow에 위임.
- **읽기 실패 명기**: hang/접근 불가로 못 본 항목은 점검 누락으로 표시(PASS로 단정 금지).

## 산출물 — 노드별 구조화 리포트

리포트 포맷·필드는 `references/report-template.md` 참조. **루프 친화**를 위해 노드당 한 블록, 머리에 요약 한 줄(SCORE)을 둔다.

```
## {Screen ID} · {node-id} — 검수 결과
SCORE: FAIL 2 · WARN 3 · PASS 9  (verdict=FAIL)

| # | 기준 | 등급 | 근거(인용/노드) | 권고 조치 |
|---|---|---|---|---|
| 1 | ③ Description | FAIL | 목업 마커 4개 vs 섹션 3개 (node [node-id]) | 누락 섹션 1개 추가 |
| 2 | ② 용어 | FAIL | "2단계 심각도" 잔존 (node …) | Severity 토큰 3단계로 |
...
```

`verdict` = FAIL이 1개 이상이면 `FAIL`, 아니면 WARN 있으면 `WARN`, 그 외 `PASS`.

### 루프/워크플로 실행 (다건 검수)
서브에이전트 **figma-spec-reviewer**(`.claude/agents/figma-spec-reviewer.md`)가 이 룰로 **노드 1건을 독립 검수**해 위 블록을 반환한다. 다건은:
- 노드 목록을 주고 서브에이전트를 노드당 1개씩 병렬/순차 호출(Workflow `pipeline`/`parallel`).
- 각 결과 블록을 모아 **종합 리포트**(verdict별 집계 + FAIL 우선 정렬)로 합친다.
- 노드 단위로 상태가 독립이므로 캐시/재실행·부분 재검수에 안전.

## 산출물 저장 (선택)

다건 종합 시 한 파일로 저장:
- 경로 우선순위: ① 사용자 지정 → ② `~/Desktop/{버전}/검수/{YYYY-MM-DD}_figma-spec-review.md`
- 저장 후 절대 경로 보고.

## 실행 로그 (선택)
`runs/log.md`에 한 줄 append:
```
YYYY-MM-DD | file={fileKey} nodes={n} | verdict={pass/warn/fail 집계} | out={경로 or -}
```

## 참고 파일
- `references/checklist.md` — 4대 기준 기계 점검 체크리스트(전수 확인용).
- `references/report-template.md` — 노드별/종합 리포트 마크다운 템플릿.

## 관련 스킬 · 메모리
- figma-desc-spec(③의 SoT) · planning-md·-html(①포맷·섹션계약 SoT: 명세서_템플릿·공통템플릿) · figma-change-flow(수정 위임·노드구조 함정) · critique-reviewer(상위 비판) · status-state-change-review(상태값 SoT).
- 메모리: *Figma 기획서 표준 포맷*, *Figma 포맷 준수 피드백*, *알람 용어집 v3.3*, *Description 작성 표준 스킬*, *Figma 디자인 에셋 재사용 원칙*, *Figma Description 표기 관용·강조 피드백(오탐 금지)*, *4.0 Figma 기획서 통일 트래커(범위)*.
</content>
</invoke>
