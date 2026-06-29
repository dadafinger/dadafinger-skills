# 와이어프레임 크롬 — 문서형 톤 (Design ≠ Wireframe)

> **목적**: 기획서 목업/와이어프레임은 **실제 Hi-fi 디자인과 시각적으로 구분**한다. DS LNB·GNB의 **브랜드 블루·액센트 컬러를 크롬(헤더·LNB)에 쓰지 않는다** — HTML `data-theme="wire"` 토큰과 동일 철학.

---

## 원칙

| | Hi-fi (제품 디자인) | Wireframe (기획서 목업) |
|---|---|---|
| LNB | DS `newproduct/*` 인스턴스 · 블루 active | **`wf-lnb` 네이티브 스켈레톤** · 잉크(검정)+회색 |
| 강조 | `#2f6df6` / `#2154c7` | `#1a1a1a` + 좌측 2px 검정 바(선택) |
| 배경 | `#f0f2f7` 등 블루그레이 | `#fafaf7` / `#f1efe9` (따뜻한 문서 회색) |
| DS 인스턴스 | 본문 Field·Table·Button 등 **재사용** | **LNB/GNB 영역은 숨김** — `wf-*` 크롬만 노출 |

- **본문 콘텐츠**는 DS clone 유지(필드·테이블·필터). **크롬만** 문서형.
- 파란 `#d9e5ff` active pill · `#2154c7` 텍스트 · `#f0f2f7` LNB 배경 = **금지**(디자인과 혼동).

---

## Figma `wf-*` 토큰 (4.0 알람 등)

HTML wire 테마 [`planning-html/assets/공통템플릿/tokens.css`](../../planning-html/assets/공통템플릿/tokens.css) `[data-theme="wire"]` 와 정렬:

| 레이어 | fill / stroke | 비고 |
|---|---|---|
| `wf-header` | fill `#f1efe9` · 하단 stroke `#1a1a1a` 1.5px | GNB 스켈레톤 |
| `wf-lnb` | fill `#fafaf7` | LNB 패널 |
| `wf-lnb-active` | fill `#f1efe9` · **좌 stroke `#1a1a1a` 2px** | 선택 메뉴 행 |
| `wf-lnb-active` TEXT | fill `#1a1a1a` · Semi Bold | |
| `wf-lnb` 일반 TEXT | fill `#4a4a4a` · Regular | |
| `wf-content` | fill `#ffffff` | 본문 |

**선택 하이라이트 대안**: active bg `#ffe79a`(wire `--c-accent-weak`) — 노란 형광 pen 느낌. 기본은 **`#f1efe9` + 검정 좌바**(더 문서형).

---

## 적용 HOW

1. 목업에 **`wf-lnb` + `wf-header` + `wf-content`** 3단 스켈레톤이 있으면 크롬은 이 규칙으로 통일.
2. 같은 화면에 **`newproduct/*` LNB 인스턴스**가 남아 있으면 **`visible=false`** (레거시 DS 크롬 — 파란 끼 유입).
3. **신규 화면**: DS LNB clone 대신 `wf-lnb` 텍스트 목록 + active 행 1개. 메뉴명만 spec 기준 override.
4. **일괄 적용 시점**: 서식 일괄(B) 또는 사용자 「LNB 파란 제거」「문서형 크롬」 요청 시 — **내용(A)과 독립** 가능(색만 바꿈).

### 검수

- LNB 영역에 **파랑 계열 fill/stroke/text** 없음 (`#d9e5ff`, `#2154c7`, `#2f6df6`, `#f0f2f7` 등).
- `get_screenshot`으로 LNB 열 시각 확인 — DS 컬러 아이콘·블루 active bar 없음.

---

## 관련

- `figma-change-flow/SKILL.md` — 와이어프레임 DS clone 원칙(본문)
- `format-batch-pass.md` — B 단계에서 크롬+Description+①②③ 일괄
- `planning-html` wire theme — HTML↔Figma 크롬 정합
