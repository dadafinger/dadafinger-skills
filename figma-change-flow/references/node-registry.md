# Figma 노드 레지스트리 (clone 대상 단일 룩업 SoT)

> **목적 — "검색"을 "조회"로.** Figma 작업마다 파일을 다시 뒤지며 clone 대상·기준 화면을 재탐색하는 게 자동화 최대 병목이었다. 이 표가 **의미 라벨 ↔ node-id ↔ 용도**의 단일 출처다. 신규 프레임·와이어프레임·Description을 만들 때 *먼저 여기서 조회*하고, 없을 때만 탐색한다.
>
> **역할 분담**
> - **IA Excel `로드맵 노드경로`** = **Screen ID ↔ Figma node-id 1차 SoT** (아래 §0). Figma 반영·rename·Intake Gate에서 **먼저 IA에서 node-id 조회**.
> - 이 문서(`node-registry.md`) = **작업 파일 안의 구체적 clone 대상**(node-id로 `clone()`). 포맷 예시·화면별 SoT·드로잉 화면·in-file DS 인스턴스·step 분할 등 **보조 룩업**.
> - [`design-system.md`](design-system.md) = **DS 라이브러리 마스터**(`importComponentByKeyAsync(key)`). 컴포넌트 스펙·정책.
> - clone(작업파일 인스턴스) > 드로잉 화면 clone > import(라이브러리 key) > (최후) 손그림. → figma-change-flow "연동 에셋 우선" 원칙.

## 0. IA Screen ID ↔ Figma node-id (1차 SoT — 사용자 확정 2026-06-25)

**파일 (최신)**: [internal-path-removed]`[internal-path-removed]`  
(구 `figma 노드 매핑용_…_v3.xlsx` — v5가 최신)

- **시트**: `1. 메뉴구조도`
- **헤더**: 6행 `화면ID`·`화면명` 등 / **L열(12번째) `로드맵 노드경로`** = Figma URL (`node-ref-removed`)
- **읽기**: Excel **읽기 전용** — IA xlsx 수정 금지(doc-collect·워크플로 공통). `openpyxl`로 `화면ID`·`로드맵 노드경로` 추출.
- **Figma 파일**: `[fileKey-removed]` (-Roadmap- 4.0 Product)

### 알람 (IA v5 ↔ node-id)

| 화면ID | 화면명 | node-id (IA) |
|---|---|---|
| CONT-00_01_01 | Cloud View_알람 센터 | `[node-id]` |
| CONT-09_10_01 | 알람 센터 목록 | `[node-id]` |
| CONT-09_10_02 | 알람 이력 | `[node-id]` |
| CONT-09_10_03 | 알람 설정 | `[node-id]` |
| CONT-09_10_04~07 | 알람 생성_step1~4 | `[node-id]` / `17751` / `17901` / `18051` |
| CONT-09_10_08 | 알람 상세 | `[node-id]` |
| CONT-09_10_09 | 알람 상세_통보 설정 | `[node-id]` |
| CONT-09_12_01 | 알람 수정 | `[node-id]` |

> **IA vs 본 레지스트리 Screen ID 차이 주의** — IA는 메뉴 기준 ID(예: 센터=`CONT-09_10_01`), §1-2 아래 행은 작업 중 헤더 검증값(예: 센터=`CONT-09_12_01`)이 섞일 수 있음. **node-id 확정 후 반드시 헤더(Screen ID·Page Title·Author) 재확인.** 알람 수정은 IA=`[node-id]`(통합 1프레임) vs step별 `[node-id]~18065` 병존 — 용도에 맞게 선택.

## 🔴 사용 규칙 (clone 전 필수)

1. **node-id는 후보다 — 헤더 텍스트로 재확인 후 사용.** 한 파일에 같은 Screen ID가 *현행 프레임 + 마스터 행 + 구버전*으로 중복 존재한다. clone/수정 직전 `use_figma`로 대상 노드의 헤더(Screen ID·Page Title·Author)를 읽어 검증한 뒤 매핑을 확정한다. **레이어명 ≠ 내용** (레이어명 "알람 수정"이어도 헤더가 "상세"면 상세 페이지).
2. **검증 상태 컬럼 확인.** `스킬기록`은 과거 세션에서 기록된 값 → 재확인 권장. `검증 YYYY-MM-DD`는 그 날짜에 직접 확인됨.
3. **공유 인스턴스 원본 수정 금지** — clone 후 override만. 구버전·마스터·정리대상 노드는 *건드리지 말 것* 표시 준수.
4. node-id 표기는 Figma 내부 `:` 형식(`[node-id]`)과 URL `-` 형식(`2112-57627`)이 같다.

---

## 1. 작업 파일 — 4.0 Product

**fileKey `[fileKey-removed]`** (Roadmap 4.0 Product). 신규 기획서·상세 명세는 이 파일에서 작업.

### 1-1. 상세 명세 페이지 포맷 예시 (clone 소스 = 표준 SoT)

| 의미 라벨 | node-id | 종류 | 용도 | 검증 |
|---|---|---|---|---|
| 집계 보고서_호스트 (포맷 예시 페이지) | `[node-id]` | clone 소스 | **상세 명세 표준 포맷의 정본.** 신규/재정비 시 구조를 새로 그리지 말고 이 페이지를 골격 기준으로 clone | 검증 2026-06-18 (루트명 `집계 보고서_호스트` ✓) |
| └ Description 프레임 ①(Sections 0–4) | `[node-id]` | clone 소스 | Description 칼럼(704) clone 후 텍스트만 교체 | 검증 2026-06-18 ⚠ 프레임 *이름*은 stale (`Description Frame 1 (Sections 1-3)`)이나 **자식 = Section 0~4** 실재 |
| └ Description 프레임 ②(Sections 5–7+Appendix) | `[node-id]` | clone 소스 | 두 번째 Description 칼럼(704) | 검증 2026-06-18 ⚠ 이름 stale (`...(Sections 4-5 + Appendix + Changelog)`)이나 **자식 = Section 5~7+Appendix** |
| 헤더행 (instance `header`, 1920×50) | `[node-id]` | 패턴 | Screen ID/Page Title/Author/Version 헤더행 | 검증 2026-06-18 (실제 = 컴포넌트 instance `header`, 1920×50 ✓) |

> 페이지 골격: Background+Shadow(3440) > [헤더 Container 3400×86 GRID] + [콘텐츠 Container 3400 HORIZONTAL gap36: `1920px mockup column` + Desc 704 + Desc 704]. 상세는 figma-change-flow "상세 명세 페이지 해부" 절.

### 1-2. 화면별 SoT 예시 노드 (신규 작성 시 clone · 본문 서식은 setFlat B 재렌더 대상)

> 같은 기능군 신규 화면은 해당 화면을 clone해서 시작(골격·크롬·거터 재사용). ⚠ 아래 노드의 **Description 본문은 구 A(네이티브 리스트)로 렌더돼 있어 정본 B `setFlat`으로 재렌더 대상**. (폰트 버그의 원인은 수동 접두가 아니라 첫 세그먼트 `Roboto` 재사용 — setFlat은 Noto Sans 강제로 회피하므로 수동 접두 마커가 정본.)

> 헤더 검증용 Screen ID 병기(clone 전 이 ID로 헤더 확인). 미터링은 페이지명이 루트.

| 기능군 | 화면 | node-id | Screen ID / 루트명 | 검증 |
|---|---|---|---|---|
| 알람 | 센터 | `[node-id]` | `CONT-09_12_01` | 검증 2026-06-18 ✓ |
| 알람 | 이력 | `[node-id]` | `CONT-09_13_01` (알람 이력) | 검증 2026-06-18 ✓ |
| 알람 | 설정 | `[node-id]` | `CONT-09_10_01` (알람 설정) | 검증 2026-06-18 ✓ |
| 알람 | 생성·수정 (구 통합 폼) | `[node-id]` | `CONT-09_10_02` (생성·수정·복제 통합 폼, `?mode=`) | 검증 2026-06-18 ✓ |
| 알람 | 생성 Step1 (기본 정보) | `[node-id]` | `CONT-09_10_03` (알람 생성_step1) | 검증 2026-06-19 ✓ |
| 알람 | 생성 Step2 (조건·조합·발생빈도·액션유예) | `[node-id]` | `CONT-09_10_03` (알람 생성_step2) | 검증 2026-06-19 ✓ |
| 알람 | 생성 Step3 (심각도·Action) | `[node-id]` | `CONT-09_10_03` (알람 생성_step3) | 검증 2026-06-19 ✓ |
| 알람 | 생성 Step4 (권장 사항) | `[node-id]` | `CONT-09_10_03` (알람 생성_step4) | 검증 2026-06-19 ✓ |
| 알람 | 수정 Step1 (기본 정보·잠금) | `[node-id]` | `CONT-09_10_06` (알람 수정_step1) | 검증 2026-06-19 ✓ |
| 알람 | 수정 Step2 (조건 설정·잠금) | `[node-id]` | `CONT-09_10_06` (알람 수정_step2) | 검증 2026-06-19 ✓ |
| 알람 | 수정 Step3 (심각도 잠금·Action 편집) | `[node-id]` | `CONT-09_10_06` (알람 수정_step3) | 검증 2026-06-19 ✓ |
| 알람 | 수정 Step4 (권장 사항) | `[node-id]` | `CONT-09_10_06` (알람 수정_step4) | 검증 2026-06-19 ✓ |
| 알람 | 상세 | `[node-id]` | `CONT-09_10_08` (알람 상세 — 라이브 헤더 실측 정정, 구 표기 CONT-09_10_04) | 검증 2026-06-30 ✓ |
| 알람 | CloudView | `[node-id]` | `CONT-09_12_02` (Cloud View 알람 센터) | 검증 2026-06-18 ✓ |
| 미터링 | 이력 데이터 | `[node-id]` | `미터링 보고서_이력 데이터` | 검증 2026-06-18 ✓ |
| 미터링 | 집계 | `[node-id]` | `미터링 보고서_집계` | 검증 2026-06-18 ✓ |

### 1-3. in-file DS 인스턴스 (4.0 파일 기존 목업 = clone할 화면 크롬)

> 4.0 파일 기존 목업은 아래 **연동 컴포넌트 인스턴스**로 구성돼 있다. 새 화면 크롬은 손으로 그리지 말고 이 인스턴스를 `clone()`해 재사용(공유 원본 수정 금지, override만). 정확한 node-id는 대상 목업에서 `use_figma` 순회로 회수 — 인스턴스 *이름*으로 식별.

| 인스턴스 이름 | 역할 |
|---|---|
| `header` | 상단 헤더 |
| `newproduct/대시보드\|컴퓨트\|…` | LNB (좌측 메뉴) |
| `component/breadcrumb` | 브레드크럼 |
| `parts/header` · `parts/cell` | 테이블 헤더/셀 |
| `Search Filter` | 필터바 |
| `pagination` | 페이지네이션 |

> DS 라이브러리 마스터 스펙·정책(GNB/LNB/Button/Field/Filter/Pagination node-id)은 [`design-system.md`](design-system.md) §1 참조. cross-file import는 `importComponentByKeyAsync`.

---

## 2. 사용자 드로잉 화면 (실 컴포넌트 완성본 = 같은 기능 기준 에셋)

**fileKey `[fileKey-removed]`** (`full 3.0.6 Product`). 디자인 에셋 출처의 권위 파일. 같은 기능 화면은 이걸 기준 에셋으로 clone/참조.

| 의미 라벨 | node-id | 종류 | 용도 | 검증 |
|---|---|---|---|---|
| 임계치 알람 생성 (modal) | `[node-id]` | 드로잉 화면 | 헤더·breadcrumb·기본정보·대상선택(3-pane)·임계치 정책 테이블·채널 토글이 **실 컴포넌트로 완성**. 알람 생성 계열 기준 에셋 | 검증 2026-06-18 ⚠ **루트명이 generic `Main Area`** — 내부 screen `A-VLA-002-67`·modal `A-CON-009-02`·자식 `임계치 상세 추가`로 식별. clone 전 내부 확인 |
| CONT-03_01_01 인스턴스_목록 | `[node-id]` | Description 양식 예시 | 헤더행·목업 ①②③ 마커·Description/Appendix/Changelog 실물 양식 | 검증 2026-06-18 (루트 `CONT-03_01_01`, 페이지명 인스턴스_목록 ✓) |

---

## 3. DS 라이브러리 (key import — 상세는 design-system.md)

| 라이브러리 | fileKey | 비고 |
|---|---|---|
| 🔑 **(v1.1) CCDS Components — 정본** | **`[fileKey-removed]`** | **Figma 전용 컴포넌트 원본**(진입 `[node-id]`). 폼/표/버튼/필드/필터/페이지네이션 import/clone 소스 |
| (구) 25' Design System Policy Document | `[fileKey-removed]` | ⚠️ outdated — design-system.md §1 node-id는 이 구 파일 기준, CCDS v1.1에서 재확인 필요 |
| (구) 25' Design System (솔루션본부 파츠) | `[fileKey-removed]` | ⚠️ outdated |
| Roadmap 3.0.5/3.0.6 (3단 포맷 참고) | `[fileKey-removed]` | 표지/요약/상세 3단 표준 포맷 원본 (node `[node-id]`) |

---

## 4. 정리·주의 대상 노드 (건드리지 말 것 / 정리 시에만)

> 아래는 clone 대상이 *아니다*. figma-change-flow "이전 버전 표시서식 정리" 절차로만, 검증 후 다룬다.

| 노드 | 성격 | 처리 |
|---|---|---|
| `Frame 633303` / `633306` / `633302` / `633307` / `633308` | 구버전 changelog 딱지 | 자동 삭제 보류 — 콘텐츠와 엉켜 있어 수동 정리. 이미 hidden인 것만 가드 후 삭제 |
| `26086359` | 구버전 버전 배지+변경행 | 위와 동일 |

---

## 갱신 규칙

- 새 화면을 만들거나 SoT 노드를 통일하면 **여기 행을 추가/갱신하고 검증일을 적는다.** 흩어진 인라인 node-id를 늘리지 말고 이 표로 모은다.
- node-id가 실제와 어긋난 것을 발견하면 즉시 `검증 YYYY-MM-DD`로 정정 (헤더 텍스트 확인 후).
- 관련 메모리: *Figma 표준 포맷*, *Figma 디자인 에셋 재사용*, *알람 Figma 명세 6화면*, *미터링 Figma 2화면*.
