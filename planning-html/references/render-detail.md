# HTML 렌더 상세 — planning-html 참조 문서

> `planning-html` SKILL.md가 참조하는 **HTML 렌더 메커니즘 SoT**(공통템플릿·경로 규약·md 판독·정합). SKILL.md의 절차가 진입점, 이 파일은 디테일.

완성된 기획서 md 한 장 → **공통템플릿 HTML(본문영역)**. 입력은 `planning-md`가 `명세서_템플릿.md` 포맷으로 작성한 spec md.

## 공통템플릿 (디자인 SoT)
`../assets/공통템플릿/` 에 정본이 있다. **하드코딩 금지, 항상 이걸 토대로** 쓴다.
| 파일 | 역할 |
|---|---|
| `tokens.css` | 디자인 토큰. `data-theme="hifi"`(완성형, Pretendard) ↔ `"wire"`(설계도, mono) |
| `base.css` | 공통 컴포넌트(본문 쉘·테이블·버튼·배지·폼·모달 등). 전부 토큰 변수로만 동작 |
| `template.html` | 본문영역 골격(`.screen` > `.screen-head` > `.screen-body` > `.area`+`.area-no`) |
| `README.md` | 사용법·테마 차이·컴포넌트 목록 |

출처: `알람(Product)`·`복제`=Hi-fi / `집계·미터링`=Wireframe 프로토타입에서 추출·통합.
(입력 md 포맷·섹션 계약 정본 `명세서_템플릿.md`는 **`planning-md/assets/`** 소유.)

## 경로 규약 (알람 4.0 기준)
- **입력 md**: `…/00.CONTRASS PLANNING/4.0/<기능>/md/vN/명세서(최신)/<화면>.md` (버전 폴더 아래 `명세서(최신)` 하위가 정본 · 최신 버전 폴더 우선, 예: `md/v7/명세서(최신)`)
- **출력 html**: `…/4.0/<기능>/html/vN/<화면>.html` (같은 vN으로 맞춤)
- 다른 기능이면 `<기능>`(알람/집계/미터링 등)만 바꾼다.

## Intake (쓰기 전 확정)
1. **입력 md** 경로/버전 — 어느 화면, 어느 vN.
2. **테마** — hifi(기본) / wire.
3. **출력 버전** — html/vN (보통 md와 동일 vN).
불명확하면 묻는다.

## Stage 1 — md 판독
입력 md에서 추출:
- **frontmatter/메타표**: Screen ID, Page Title, Author, Version → html `data-screen-label`(+ Figma 헤더행에서도 사용).
- **변경사항** 표, **진입 경로**, **Description**(개요).
- **영역별 명세** `### N · 기능요소명 <!-- marker=① screen=… -->` → 섹션 계약(`명세서_템플릿.md`)대로 번호 N·기능요소명·마커·screen 모드를 **추측 없이 읽는다.** 본문 구성(UI 요소 → 상태·케이스 → 제약 → 동작 정책, 동작 정책 맨 뒤) → html `.area`(`.area-no N`)와 1:1. (섹션 경계 판단은 md 작성 시 이미 끝 — 여기서 다시 나누지 말 것.)
- dirty/clean·유효성·QA 등 부가 섹션.

## Stage 2 — HTML 산출 (본문영역만)
**`../assets/공통템플릿/template.html` 을 복제**해 채운다.
- 범위 = **본문영역만**: `.screen` 안에 `.screen-head`(제목+액션) + `.screen-body`(영역들). **`.topbar`/`.info-banner` 는 쓰지 않는다**(헤더·메뉴정보는 Figma 프레임이 담당).
- md의 영역 N → `.area` 블록, 좌측 `.area-no` 번호를 md 번호와 일치. 컴포넌트는 base.css 클래스 재사용(`.card`/`.tbl`/`.btn`/`.field`/`.tag`/`.sev`/`.tg`/`.note`/`.pager` 등). 새 컴포넌트는 토큰으로 짜서 추가.
- 색/폰트/그림자 **하드코딩 금지** → tokens.css 변수만. 제품 변형은 `--brand` 한 줄.
- 테마: `<html data-theme="hifi">`(기본). 개발용 `.theme-switch` 토글은 납품/캡처 시 제거.
- **CSS = 단일 파일 인라인(기본)**: `tokens.css`+`base.css`를 `<style>`에 인라인해 **HTML 한 개**로 떨군다(별도 CSS 파일 생성 금지). 화면 고유 스타일도 같은 `<style>`에, 색/폰트/그림자는 토큰 변수만. 사용자가 명시적으로 "CSS 분리"를 요청할 때만 외부 파일+상대경로 링크.
- 저장: `html/vN/<화면>.html`(정적본). 캔버스 1440px 고정.

## Stage 2b — 인터랙티브본 산출 (형제 파일)
정적본을 토대로 `<화면> (인터랙티브).html`을 같은 폴더에 떨군다. CSS/토큰/`.area` 구조 보존, `<script>` 인라인으로 동작만 부착(외부 런타임 0). 표준 패턴·훅 규약은 **`interaction-patterns.md`**. **Figma 트랙에는 정적본만 넘긴다**(인터랙티브본 제외).

## Stage 3 — 검증 & 보고
- 산출 경로 **2개**(정적본 + 인터랙티브본) 보고.
- **정합**: md `### N` 수 = 정적본 `.area-no` 수 = 인터랙티브본 `.area-no` 수(어긋나면 누락 신호 → 멈추고 점검). Figma까지 가면 전체 4중 정합은 `planning-figma`에서 확인.
- 핵심 정책 문구(버전·지표·탭·상태·캘린더 등) 반영 여부 점검. 미반영·추정은 분리 보고(추측 채움 금지).

## Side-effect 가드
- [internal-path-removed]

## 관련
- 입력 md 생산: **planning-md**(`명세서_템플릿.md` 섹션 계약).
- 다음 단계 Figma: **planning-figma**.
- 메모리: *[internal-path-removed]
