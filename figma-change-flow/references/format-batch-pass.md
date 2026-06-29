# Figma 상세 명세 — 서식 일괄 적용 (Format Batch Pass)

> **용도**: 기획 **내용(정책·용어·필드)** 반영이 끝난 뒤, Description·목업 **서식만** `[node-id]` 표준에 맞추는 **별도 배치**.  
> **figma-desc-spec = WHAT**, **이 문서 + figma-change-flow HOW = 서식 렌더**.

---

## 🔴 2단계 워크플로 (사용자 확정 2026-06-25)

| 단계 | 이름 | 할 일 | 하지 말 것 |
|---|---|---|---|
| **A** | **내용 치기** | spec md 기준 Description·목업 UI·용어·정책 문구 반영 | 서식 재구성·덩어리 TEXT 분해·Appendix/Changelog 정리·①②③ 마커 배치 |
| **B** | **서식 일괄** | 아래 체크리스트 **기능 세트 단위 일괄**(예: 알람 step1~4 전부) | 내용·정책 추가 수정(발견 시 A로 되돌림) |

- **알람(2026-06)**: A 진행 중 — Description 덩어리 TEXT·구 「항목 (옵션 및 설명)」·Changelog 노출·**목업 빨간 ①②③ 미배치** = **B에서 처리**.
- B는 사용자 **「서식 일괄」「포맷 통일」** 명시 또는 A 완료 확인 후 시작.
- **IA node-id 조회**는 A·B 공통(§0 node-registry). **서식 clone 소스**는 B 전용 `[node-id]`.

---

## 4중 정합 (서식 B 완료 기준)

```
md ### N  =  html .area-no N  =  Figma Description Section N(거터)  =  목업 빨간 ①②③
```

- **목업 빨간 동그라미(①②③)** = 좌측 **1920px mockup column** 위에 올리는 **섹션 참조 마커**(와이어프레임 각 큰 기능 블록 옆). Description 거터(50px `1·2·3`)와 **번호는 1:1이지만 위치·역할이 다름**.
- **①②③은 제목·본문 넘버링에 쓰지 않음** — 목업·Description 연결 전용(`figma-desc-spec`).
- HTML `.area-no`(빨간 동그라미)와 **동일 의미** — Figma 목업에도 반드시 있어야 함. **없으면 B 미완료(FAIL)**.

### 목업 ①②③ 마커 (HOW)

- **참조 실물**: `[node-id]` · `[node-id]` (`CONT-03_01_01`) 목업 column 내 기존 마커 **clone**.
- **배치**: md `<!-- marker=① -->` · `### N` 순서대로, 해당 **와이어프레임 기능 블록** 좌측/상단에 1:1.
- **스타일**: 빨간 원형 + 흰 숫자(①②③ 또는 1·2·3 — **프로젝트 관례는 circled ①②③**, HTML `.area-no`와 시각 일치).
- **손그림 금지** — 예시 페이지에서 마커 컴포넌트/프레임 clone 후 위치만 조정.
- **변경 콜아웃 빨간 박스**(Rectangle stroke overlay) ≠ ①②③ 마커 — 혼동 금지(`figma-change-flow` 이전 버전 표시 정리 절).

---

## Description 서식 (B 체크리스트)

**clone 소스**: `[node-id]` → Description `[node-id]`(Sec 0–4) / `[node-id]`(Sec 5–7+). **구조 새로 그리지 말고 clone 후 텍스트·개수만 조정.**

| # | 항목 | PASS 조건 |
|---|---|---|
| F1 | 3단 골격 | 헤더행 + mockup 1920 + Desc 704(×2) |
| F2 | Description 구조 | 거터 50px + title-bar 44px + **불릿 TEXT 노드 분리** (400자+ 단일 노드 = FAIL) |
| F3 | 본문 블록 순서 | UI 요소(라벨 없이 `1.2.3.`) → 상태·케이스 → 제약 → **동작 정책(맨 뒤)** |
| F4 | 4.0 통일 | Appendix/Changelog/Intro 버전라인/**인라인 ⭐vN** 숨김 또는 제거(전역 history 운영) |
| F5 | 거터 G1–G6 | `1,2,3,…` 연속 · 중복 없음 · **목업 ①②③과 1:1** |
| F6 | 행간 | fs×1.5 (36px 목표, `4.0_Figma_기획서_관리.md`) |
| F7 | 좌우 정합 | Description 용어·필드 = 목업 Field 라벨 (S6) |
| F8 | 와이어 크롬 | LNB/GNB **문서형** — 파랑 active·블루그레이 배경 없음 · [`wireframe-chrome.md`](wireframe-chrome.md) |

**렌더 HOW**: `figma-change-flow` Description 렌더 기법(`setRangeListOptions`·font load·높이 hug).

---

## 알람 일괄 B 대상 (IA v5 · node-registry §0)

| Screen ID | 화면 | node-id |
|---|---|---|
| CONT-09_10_01 | 알람 센터 목록 | `[node-id]` |
| CONT-09_10_02 | 알람 이력 | `[node-id]` |
| CONT-09_10_03 | 알람 설정 | `[node-id]` |
| CONT-09_10_04~07 | 알람 생성 step1~4 | `[node-id]` … `18051` |
| CONT-09_10_08 | 알람 상세 | `[node-id]` |
| CONT-09_10_09 | 알람 상세_통보 설정 | `[node-id]` |
| CONT-09_12_01 | 알람 수정 | `[node-id]` |
| CONT-00_01_01 | Cloud View 알람 센터 | `[node-id]` |

> B 시작 전: A(내용) 완료 확인 · 헤더 Screen ID 재검증 · **[node-id]** 제외.

---

## 에이전트 행동 규칙

1. **A 중**: 사용자가 「서식」「포맷」「①②③」만 언급해도 **「내용 치기 끝난 뒤 B로 일괄」** 안내 — 부분 서식만 섞지 않음(깨짐 재발).
2. **B 시작**: 기능 단위(알람 전체 등) **한 세션에 몰아서** — clone·마커·분해·숨김을 화면별 작은 배치로.
3. **B 완료**: `figma-spec-review` 4기준 스캔(특히 F6·D1·G3·S6) → 노드별 PASS/WARN 보고.

---

## 관련 SoT

- `figma-desc-spec` — Description WHAT
- `figma-change-flow/SKILL.md` — Product Figma 기획서 표준 포맷 · Description HOW
- `node-registry.md` §1-1 `[node-id]` · §0 IA
- `4.0_Figma_기획서_관리.md` — 알람 ⬜ → B 후 ✅ 갱신
