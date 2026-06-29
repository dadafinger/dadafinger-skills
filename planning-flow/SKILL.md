> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: planning-flow
description: Author의 Product Product 기획 워크플로우 **실행 오케스트레이터**. 3개 독립 스킬 — `planning-md`(spec md 신규/수정) · `planning-html`(공통템플릿 본문영역) · `planning-figma`(새 프레임 3단) — 을 한 진입점에서 분기·연결 실행한다. md 작성 후 HTML·Figma로 이어갈 때 **단계마다 컨펌**을 받고 자동 진행하지 않는다. '기획', '신규 기획', '기획서', '요구사항/회의 메모 반영', 'md부터 피그마까지', 'md→html→figma' 등이 트리거. 각 단계만 따로 할 거면 해당 하위 스킬을 직접 써도 된다.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: md→html→figma 오케스트레이터; 사내 프로젝트명·브랜드 포함

# Planning Flow (실행 오케스트레이터)

Product 4.0 기획을 **MD → HTML → Figma** 한 흐름으로 진행하는 진입점. 실제 작업은 3개 독립 스킬이 수행하고, 이 스킬은 **분기·연결·컨펌**만 담당한다(자산·렌더 상세 없음).

| 단계 | 담당 스킬 | 단독 호출 |
|---|---|---|
| MD | **planning-md** | `/planning-md` |
| HTML | **planning-html** | `/planning-html` |
| Figma | **planning-figma** | `/planning-figma` |

## Step 0 — 진입 분기 (필수)
호출되면 **무엇을 할지 먼저 확인**한다: ① MD(신규/수정) · ② HTML · ③ Figma · 또는 연속(MD→HTML→Figma). 명시돼 있으면 바로 해당 스킬로.

## 연속 실행 컨펌 게이트
한 단계가 끝나면 **다음 단계로 넘어가기 전 매번 계속할지 묻는다 — 자동 연속 금지.**
- MD 완료 → ⏸ "여기서 멈출까요 / HTML로 갈까요?" → 가면 **planning-html**.
- HTML 완료 → ⏸ "Figma 새 프레임도 만들까요?"(Figma 쓰기는 side-effect → 항상 별도 확인) → 가면 **planning-figma**.
- "끝까지 가" 식으로 전권을 미리 줘도, **Figma 쓰기 직전엔 한 번 더 확인**.

## 전체 정합 (연속 실행 시)
- **4중 정합(섹션 계약)**: md `### N` = html `.area-no` = Figma `Section n` = **목업 빨간 ①②③**. 한 곳이라도 어긋나면 멈추고 점검.
- 각 단계 산출(경로·node ID)과 핵심 정책 문구 반영 여부를 종합 보고.

## Figma 기존 페이지 — 내용(A) → 서식 일괄(B)
- **알람 등 이미 Figma에 치는 중인 화면**: MD/HTML/Figma **내용 반영(A)** 이 끝난 뒤 **`figma-change-flow` format-batch-pass(B)** 로 Description·목업 서식만 기능 세트 단위 일괄.
- A 중에는 서식 재구성·①②③ 마커·덩어리 TEXT 분해 **하지 않음** — [`figma-change-flow/references/format-batch-pass.md`](../figma-change-flow/references/format-batch-pass.md).

## Invocation
직접 호출: `/planning-flow` (연속 흐름) 또는 하위 스킬 직접:
> "신규 기획 만들거야." → planning-md (A)
> "이 md 고쳐줘. 대상=`<경로>`, 수정사항: …" → planning-md (B: 복제 후 버전업)
> "이 md로 html만 뽑아줘." → planning-html
> "이 화면 피그마 새 프레임으로." → planning-figma
> "수정하고 html·피그마까지 가줘." → md(B) → ⏸ → html → ⏸ → figma

## 관련 스킬
- **planning-md / -html / -figma** — 실제 워크플로우(각 단독 실행 가능).
- **doc-collect** — 준비물 수집.
- **figma-change-flow** — 기존 Figma 노드 incremental 수정·MCP hang 우회·DS 클론.
- **figma-desc-spec** — 상세 명세 Description 내용 표준.
- **figma-spec-review** — 작성된 명세 검수(읽기 전용).
