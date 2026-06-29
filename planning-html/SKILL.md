> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: planning-html
description: 완성된 Product 기획 spec md를 공통템플릿 기반 HTML(본문영역)로 렌더하는 워크플로우(planning 3종 중 HTML). `assets/공통템플릿/`(tokens/base/template)을 복제해 md의 영역별 명세 `### N`을 `.area`(`.area-no N`)로 1:1 변환한다. **한 번 실행에 ① 정적본(Figma 입력용) + ② 인터랙티브 standalone 프로토(사람 리뷰·데모용) 두 파일을 같이 떨군다.** 'html 뽑아', '공통템플릿으로 그려', '본문영역 그려', 'spec md html', 'md→html', '인터랙티브로', '실제 동작하게', '탭 눌리게' 등이 트리거. 단독 실행 가능하며, 실행 오케스트레이션은 planning-flow.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: 공통템플릿 HTML; 사내 디자인 토큰·레이아웃

# Planning — HTML

완성된 기획서 md 한 장 → **공통템플릿 HTML(본문영역) 2종 동시 산출**. 입력은 `planning-md`가 작성한 spec md(없어도 md 경로만 있으면 **단독 실행**).

## 산출물 (한 번에 두 개)
| | ① 정적본 `<화면>.html` | ② 인터랙티브본 `<화면> (인터랙티브).html` |
|---|---|---|
| 용도 | **planning-figma 입력**(네이티브 변환) | 사람 리뷰·데모·사용성 확인 |
| JS | 없음(죽은 화면) | vanilla JS 인라인(탭·세그·토글·리스트·유효성·라이브 요약) |
| 공통 | 같은 공통템플릿 토큰/컴포넌트·같은 `.area` 구조·1440px·standalone 1파일 | 동일 + 동작 부착 |

**Figma에는 ①만 넣는다**(②의 JS는 변환 불가/노이즈). 두 파일은 같은 `html/vN/` 폴더에 형제로 둔다.

## Intake (쓰기 전 확정)
1. **입력 md** 경로·버전 — 어느 화면, 어느 vN.
2. **테마** — `hifi`(기본) / `wire`.
3. **출력 버전** — html/vN (보통 md와 동일 vN).
불명확하면 묻는다.

## 절차
1. **md 판독** — 메타(Screen ID·Title·Author·Version), 변경사항·진입경로·Description, **영역별 명세** `### N · 기능요소명 <!-- marker=… -->`를 추측 없이 읽는다. 섹션 경계는 md에서 이미 확정 — 여기서 다시 나누지 않음.
2. **공통템플릿 복제** — 디자인 SoT `assets/공통템플릿/`(`tokens.css`·`base.css`·`template.html`)을 복제해 채운다. **색/폰트/그림자 하드코딩 금지** → 토큰 변수만.
3. **본문영역만 채움** — `.screen > .screen-head + .screen-body > .area`. `.topbar`/`.info-banner`는 쓰지 않음(헤더·메뉴는 Figma 담당). md 영역 N → `.area`(`.area-no N`)와 **1:1**. 컴포넌트는 base.css 클래스 재사용.
4. **정적본 저장** — `…/<기능>/html/vN/<화면>.html`(md와 같은 vN). **단일 파일(standalone)**: `tokens.css`+`base.css`를 `<style>`에 **인라인**, 별도 CSS 파일 금지(명시 분리 요청 시만 외부 링크). 캔버스 1440px. 개발용 테마 토글 미포함(납품물).
5. **인터랙티브본 저장** — **같은 정적본을 토대로** `<화면> (인터랙티브).html`을 형제로 떨군다. CSS/토큰/`.area` 구조 **그대로 보존**, `<script>` 인라인으로 동작만 부착(외부 런타임 0 → 더블클릭 동작). 표준 패턴: 단일 `state` + 이벤트 위임으로 탭/스텝·세그먼트·토글·동적 리스트(추가/삭제)·유효성(`.err`)·라이브 요약·저장 토스트. 상세 스니펫·훅 규약은 **`references/interaction-patterns.md`**. 목업값(채널명 등)은 확정 사실로 단정 금지.
6. **보고 & 정합** — 두 산출 경로 + **md `### N` 수 = 정적본 `.area-no` 수 = 인터랙티브본 `.area-no` 수** 점검(어긋나면 멈추고 확인). Figma 트랙에는 **정적본만** 넘어간다고 명시.

상세(공통템플릿 파일 역할·경로 규약·컴포넌트 클래스)는 **`references/render-detail.md`**, 동작 부착은 **`references/interaction-patterns.md`**.

## Side-effect 가드
- [internal-path-removed]

## 관련 스킬
- **planning-flow** — md→html→figma 연속 실행 오케스트레이터(컨펌 게이트).
- **planning-md** — 입력 spec md 생산자(`명세서_템플릿.md` 섹션 계약).
- **planning-figma** — 다음 단계. 이 HTML을 네이티브 변환해 새 프레임 생성.
- **figma-change-flow** — Figma 메커니즘·node-registry.
