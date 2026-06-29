> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: planning-figma
description: 완성된 Product 기획 html(또는 spec md)을 Figma 새 프레임(3단=헤더+본문목업+Description)으로 신규 생성하는 워크플로우(planning 3종 중 Figma). 연결 precheck → figma-use 로드 → node-registry 룩업 → 3단 생성 순. '피그마 새 프레임', 'spec md를 피그마에', 'figma로 그려', 'html→figma' 등이 트리거. 신규 생성 전용(기존 노드 incremental 수정은 figma-change-flow). 단독 실행 가능하며, 실행 오케스트레이션은 planning-flow.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: Figma 새 프레임 생성; 사내 wireframe chrome

# Planning — Figma

완성된 html(또는 spec md) → **Figma 새 프레임(3단 완본)** 신규 생성. **신규 생성 전용** — 기존 노드 덮어쓰기/삭제는 `figma-change-flow`. html/md만 있으면 **단독 실행**.

## Intake (쓰기 전 확정)
1. **대상 화면**(html/md)·기능·vN.
2. **출력 위치** — 빈 영역(위치는 사용자 조정 전제).
3. Figma 쓰기는 **side-effect** → 실제 생성 전 대상 확인.

## 절차
1. **연결 precheck** — `use_figma` 쓰기 전 `figma-change-flow` Stage 0(연결 precheck). OAuth 만료/불안정이면 **html/md까지만 + 반영 플랜 보존**.
2. **figma-use 로드** — `use_figma` 호출 전 **반드시** `/figma-use` 가이드 로드. MCP hang·폰트·리스트 서식 우회는 `figma-change-flow` "MCP 읽기 hang 우회".
3. **clone 기준 룩업** — clone 대상·기준 노드는 `figma-change-flow` `references/node-registry.md`에서 **룩업**(검색 아님). 헤더 텍스트로 재확인 후 clone.
   - 🔑 **Figma 전용 DS 컴포넌트 정본 = `(v1.1) CCDS Components` 파일 `[fileKey-removed]`**(진입 노드 `[node-id]`, URL `[figma-design-removed]`). 폼/표/버튼/필드 등 컴포넌트는 **이 파일에서** `importComponentByKeyAsync`로 가져오거나 인스턴스 clone. (구 `design-system.md`의 `[fileKey-removed]`는 outdated — CCDS v1.1이 정본.)
4. **3단 생성** — ① 헤더행(Screen ID/Title/Author/Version) ② 본문 목업 = **CCDS DS 컴포넌트로 구성**(위 `[fileKey-removed]` 컴포넌트 import/clone, 또는 같은 기능 기존 화면 clone) — **손그림(createFrame/createText로 직접 그리기) 절대 금지**, 좌측 거터 번호. **필터 영역 순서 = 조회 조건(기간) 첫 번째**(아래 「확정 규칙」). ③ Description 컬럼(md 영역별 명세 `Section n` 1:1 + Appendix) — **거터 번호 = 목업(Wireframe) 마커와 동일 번호·동일 순서로 통일**.
5. **보고 & 정합** — 생성 node ID + **4중 정합**(md `### N` = html `.area-no` = Figma `Section n` = 목업 마커, **거터=Wireframe 번호 통일**) 점검. **서식은 문서 공통 기준** 준수(아래 「확정 규칙」).

## 확정 규칙 (2026-06-29 · 집계 검수 반영)
> 화면 렌더·검수 시 아래 3건은 **고정 규칙**으로 적용(개별 화면 임의 변경 금지).
1. **필터 영역 순서** = **조회 조건(기간) 첫 번째** → 대상 → 지표. 목업·거터·Description **모두 같은 순서**. (기존 ①대상→②지표→③조회 순서로 그려진 화면은 이 순서로 재배치 대상.)
2. **서식 = 문서 공통 기준** — 공통템플릿 디자인 DNA(`planning-html/assets/공통템플릿/` tokens/base/template) + Figma 표준 3단 포맷. 화면별 임의 서식·임의 레이아웃 금지.
3. **Description = 거터 ↔ Wireframe 통일** — 거터 번호가 목업 마커와 **1:1(동일 번호·동일 순서)**. ①②③ 마커 ≠ `1/1-1/1-2` 거터 같은 **이중 번호 스킴 금지**. 이 통일이 4중 정합(md `### N`=`.area-no`=`Section n`=목업 마커)의 거터 축.
   - **플랫 카운팅 스킴(2026-06-29 집계 확정)**: **개요(진입경로·화면목적) = 무거터 Intro** · **1 = 카테고리 탭** · **2 = 조회 조건(기간)** · **3 = 집계 대상** · **4 = 지표** · **5 = 데이터 테이블** · **6 = 차트**. **sticky 액션바·필터 영역 그룹 설명은 별도 번호 없이** 필터 묶음(2~4) 내 보조 설명으로 둔다. 목업 헤더도 `▼ ② 조회 조건`처럼 같은 번호를 표기(탭 영역엔 `①` 마커), 본문 인라인 교차참조(`④/⑤ 스크롤`·`③ 참조` 등)도 재번호에 맞춰 보정.

## 조합(composition) 출처 — 부품 ≠ 배치
DS 정본(CCDS)은 **부품(Field/Select/Switch/Button/step-bar…)만** 정의하고 "어떤 순서·그룹·간격으로 배치하느냐"는 안 준다. 조합은 삼각측량한다:
- **부품(시각 fidelity)** = CCDS 컴포넌트 import/clone.
- **구조·내용**(영역·영역별 필드·2-Step 그룹) = **spec md + 같이 만든 HTML 목업**.
- **레이아웃 관례**(카드 구조·필드 행·스텝퍼 위치·3단) = **기존 유사 화면**(node-registry 화면별 SoT, 예: 알람 생성 step `3144:*`·포맷 예시 `[node-id]`).
- ⚠️ 기존 화면이 스켈레톤이면 *그룹핑·순서*만 참고, *fidelity*는 CCDS, *내용*은 spec로 채운다. DS 파일에 조합/템플릿 예시 페이지가 있으면 우선 참고.

상세(precheck·node-registry·3단 치수·작업 파일 `[fileKey-removed]`·마스터 `[node-id]`·**DS 정본 CCDS v1.1 `[fileKey-removed]`**·fidelity)는 **`references/render-detail.md`**.

## Side-effect 가드
- Figma 쓰기(엔터프라이즈 Roadmap 파일)는 **대상 확인 후** 진행. 새 프레임은 빈 곳, 위치는 사용자 조정 전제.
- 기존 노드 덮어쓰기/삭제 금지(**신규 생성 전용**). 기존 프레임 수정은 figma-change-flow.

## 🔴 기존 프레임 수정 시 — 내용(A) vs 서식(B)
- **신규 3단 생성**은 본 스킬. **이미 있는 알람 등 페이지**는 대부분 **figma-change-flow**.
- **내용 치기(A)** 와 **서식 일괄(B)** 분리 — [`figma-change-flow/references/format-batch-pass.md`](../figma-change-flow/references/format-batch-pass.md).
- A 중: 정책·필드만. **①②③ 빨간 마커·Description clone 구조·불릿 분리**는 B까지 미룸.
- B: `[node-id]` Description clone + 목업 **빨간 ①②③** 1:1 배치 + 4중 정합 검수.

## 관련 스킬
- **planning-flow** — md→html→figma 연속 실행 오케스트레이터(컨펌 게이트).
- **planning-html** / **planning-md** — 입력(html / 섹션 계약) 생산자.
- **figma-change-flow** — Figma 메커니즘(스켈레톤 재구성·MCP hang 우회·DS 클론)·node-registry.
- 메모리: *Figma 디자인 에셋 재사용*, *Figma 표준 포맷*(3단·예시 노드 클론).
