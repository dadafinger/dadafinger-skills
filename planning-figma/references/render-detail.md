# Figma 렌더 상세 — planning-figma 참조 문서

> `planning-figma` SKILL.md가 참조하는 **Figma 새 프레임 렌더 메커니즘 SoT**(precheck·노드 룩업·3단·정합). SKILL.md의 절차가 진입점, 이 파일은 디테일. 기존 노드 incremental 수정은 **figma-change-flow**(이 스킬은 신규 생성 전용).

입력은 `planning-html`이 만든 html(또는 `planning-md`의 spec md). 산출은 **Figma 새 프레임(3단 완본)**.

## 경로/대상
- **Figma**: Roadmap 4.0 Product, fileKey `[fileKey-removed]`.
- 입력 html: `…/4.0/<기능>/html/vN/<화면>.html` · 입력 md: `…/4.0/<기능>/md/vN/명세서(최신)/<화면>.md` (버전 폴더 아래 `명세서(최신)` 하위가 정본).

## Intake (쓰기 전 확정)
1. **대상 화면**(html/md)·기능·vN.
2. **출력 위치** — 빈 영역(위치는 사용자가 나중에 조정 전제).
3. Figma 쓰기는 **side-effect** → 실제 생성 전 대상 확인.

## Stage 1 — 연결 precheck (먼저)
> ⚠️ `use_figma` 쓰기 전 **figma-change-flow Stage 0(연결 precheck 게이트)** 수행 — 연결 OK면 진행, OAuth 만료/불안정이면 **html/md까지만 + 반영 플랜 보존**(가용성에 매번 막히지 않게).
> ⚠️ `use_figma` 호출 전 **반드시** figma-use 가이드 로드: `/figma-use` 스킬 또는 `skill://figma/figma-use/SKILL.md`. 생략 시 흔한 실패. MCP hang·폰트·리스트 서식 우회는 **figma-change-flow** "MCP 읽기 hang 우회" 절.

## Stage 2 — clone 기준 룩업
> 🔑 clone 대상·기준 노드는 [figma-change-flow `references/node-registry.md`](../../figma-change-flow/references/node-registry.md)에서 **룩업**(검색 아님). 포맷 예시 `[node-id]`·화면별 SoT·in-file DS 인스턴스 전부 거기 정리됨. 헤더 텍스트로 재확인 후 clone.
>
> 🔑 **Figma 전용 DS 컴포넌트 정본 = `(v1.1) CCDS Components`** — fileKey **`[fileKey-removed]`**, 진입 노드 `[node-id]` (URL `[figma-design-removed]`). 폼/표/버튼/필드/필터/페이지네이션 등 **모든 컴포넌트의 원본**. 목업은 이 파일 컴포넌트를 `importComponentByKeyAsync`로 가져오거나(cross-file) 인스턴스 clone해 구성한다. ⚠️ 구 `design-system.md`의 DS 라이브러리 키 `[fileKey-removed]`는 **outdated** — CCDS v1.1이 정본.

## Stage 3 — 3단 완본 신규 생성
새 프레임을 **빈 영역에 신규 생성**(위치 임시 — 사용자 조정). 처음 만드는 프레임이라 기존 크롬이 없으므로 **3단을 전부 그린다**(헤더·Description도 md에서 최대한 채움):

> 🔒 **확정 규칙 (2026-06-29 · 집계 검수 반영) — 고정 적용**
> 1. **필터 영역 순서 = 조회 조건(기간) 첫 번째** → 대상 → 지표. 목업·거터·Description 모두 같은 순서(기존 ①대상→②지표→③조회 화면은 재배치 대상).
> 2. **서식 = 문서 공통 기준** — 공통템플릿 디자인 DNA(`planning-html/assets/공통템플릿/`) + Figma 표준 3단. 화면별 임의 서식 금지.
> 3. **Description = 거터 ↔ Wireframe 통일** — 거터 번호가 목업 마커와 1:1(동일 번호·동일 순서). ①②③ 마커 ≠ `1/1-1` 거터 같은 이중 번호 스킴 금지.
1. **헤더행** (마스터 `[node-id]` 패턴, ~1920×50) — Screen ID / Page Title / Author / Version을 frontmatter에서.
2. **본문 목업** (1920px mockup column / Content Root ~1688폭) — ⚠️ **실제 DS 컴포넌트 인스턴스를 clone해 구성(연동 에셋 우선) — 손으로 프레임/텍스트 그리기 금지(손그림 금지).** 클론 소스 우선순위: ① node-registry §1-2 화면별 SoT(같은 기능 기존 화면, 예: 알람 생성 Step `3144:*`) ② §1-3 in-file DS 인스턴스(Field/Button/Search Filter/parts·cell/pagination 등) ③ design-system.md `importComponentByKeyAsync`. HTML은 **배치·내용 참고용**(컴포넌트 대체 아님). **LNB/GNB 크롬**은 DS 블루 대신 `wf-lnb`/`wf-header` 문서형 회색+잉크 — [`wireframe-chrome.md`](../../figma-change-flow/references/wireframe-chrome.md). **각 기능 블록 옆 빨간 ①②③ 마커**(HTML `.area-no` 동일) — `[node-id]`/`[node-id]`에서 clone. **내용 치기(A) 중 마커 누락 OK → 서식 일괄(B)에서 반드시 배치**([`format-batch-pass.md`](../../figma-change-flow/references/format-batch-pass.md)).
3. **Description 컬럼**(704폭, 길면 2개로 분할) — md 영역별 명세를 `Section n`(num 50폭 + body 654폭) 블록으로, html/본문 번호와 1:1 매칭. **거터 번호 = 목업(Wireframe) 마커와 동일 번호·동일 순서로 통일**(이중 번호 스킴 금지 — 확정 규칙 3). 상단 `Description` 헤더 + 개요(Intro), 하단 Appendix/Changelog는 md 변경사항으로.

- 프레임 이름: `<화면>_<탭>` 관례(예: `집계 보고서_호스트`). 기준 마스터 구조: `[node-id]`.
- **fidelity 기본 = DS 컴포넌트 클론**(연동 에셋 우선, 메모리 *Figma 디자인 에셋 재사용* / *node-registry*). 손그림 네이티브(createFrame/createText로 카드·필드 직접 그리기)는 **금지** — 클론 소스가 정말 없을 때만 한정 폴백하고 그 사실을 보고에 명시. clone > 드로잉 화면 clone > import > (최후)손그림.

## Stage 4 — 검증 & 보고
- 생성 node ID 보고.
- **4중 정합(섹션 계약)**: md `### N` 수 = html `.area-no` 수 = Figma Description `Section n` 수 = 목업 ①②③ 마커 수. **거터 번호 = Wireframe 마커 번호 통일**(동일 번호·동일 순서, 별도 스킴 금지). 한 곳이라도 어긋나면 누락 신호 → 멈추고 점검.
- 핵심 정책 문구 반영 점검. 미반영·추정은 분리 보고(추측 채움 금지, 모호하면 「확인 필요」).

## Side-effect 가드
- Figma 쓰기(엔터프라이즈 Roadmap 파일)는 **대상 확인 후** 진행. 새 프레임은 빈 곳, 위치는 사용자 조정 전제.
- 기존 노드 덮어쓰기/삭제 금지(**신규 생성 전용**). 기존 프레임 수정은 figma-change-flow.

## 관련
- 입력: **planning-html**(html) / **planning-md**(섹션 계약).
- **figma-change-flow** — Figma 메커니즘(스켈레톤 재구성·MCP hang 우회·DS 클론)·node-registry.
- 메모리: *Figma 디자인 에셋 재사용*, *Figma 표준 포맷*(3단·예시 노드 클론), *[internal-path-removed]
