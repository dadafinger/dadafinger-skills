# 공통 템플릿 — Product HTML 기획서

`알람(Product)` · `복제` · `집계/미터링` 3개 프로토타입에서 디자인 DNA를 추출해
**한 벌의 토큰 + 스타일 + 템플릿**으로 통합한 것. 앞으로 HTML 기획서를 만들 때 이걸 토대로 쓴다.

## ⚠️ 작업 범위 = "본문영역"만
이 HTML 산출물은 **Product 명세 Figma 프레임의 1440px 본문영역에 들어갈 화면 목업**이다.
([Roadmap 4.0 Product]([figma-url-removed]
- **상단 메타 헤더**(Screen ID / Page Title / Author) → Figma 프레임 제공. **그리지 않음.**
- **우측 Description 컬럼**(영역별 설명) → Figma 프레임 제공. **그리지 않음.**
- 본문에는 `.area-no`(빨간 동그라미 번호)만 찍어 Description 의 번호와 연결한다.
- 독립 HTML 로 뽑을 때만 쓰는 `.topbar`/`.info-banner` 는 base.css 에 "standalone 전용"으로 남겨둠.

## 파일
| 파일 | 역할 |
|------|------|
| `tokens.css` | 디자인 토큰(색·폰트·spacing·radius·shadow). **Hi-fi ↔ Wireframe** 를 `data-theme` 로 분기 |
| `base.css` | 공통 컴포넌트 스타일(쉘·테이블·버튼·배지·모달 등). 전부 토큰 변수로만 동작 |
| `template.html` | 바로 채워 쓰는 기획서 HTML 골격 + 테마 미리보기 토글 |
| `명세서_템플릿.md` | Figma 명세 문서 포맷(Screen ID·변경이력·영역별 명세·QA) |

## 쓰는 법
1. `template.html` 을 복사 → 화면 단위로 `[대괄호]` 채우기.
2. 테마 선택: `<html data-theme="hifi">`(완성형) 또는 `data-theme="wire">`(설계도).
   개발 중엔 우상단 토글로 둘 다 미리보기 → 납품 시 `.theme-switch` 제거.
3. 제품별 브랜드색은 `tokens.css` 의 `--brand` 한 줄만 교체 (예: 복제 = `#f26c21`).
4. 명세서는 `명세서_템플릿.md` 로 작성하고 HTML 의 `data-screen-label` / `.area-no` 번호와 일치시킨다.

## 두 테마 차이 (토큰으로만 분기됨)
| | Hi-fi (알람·복제) | Wireframe (집계·미터링) |
|---|---|---|
| 폰트 | Pretendard | Monospace |
| 모서리 | 12 / 8px 둥금 | 0 (각짐), 칩만 999px |
| 테두리 | 1px 연회색 | 1.5~2px 검정 |
| 그림자 | soft blur | `4px 4px 0` offset |
| 강조 | 파랑/오렌지 | 잉크 검정 + 노란 하이라이트 |
| 용도 | 최종 목업 | 초안·구조 검토 |

## 공통 컴포넌트 (base.css)
본문 쉘(`.screen` `.screen-head` `.screen-body` `.area`+`.area-no`) · `.page-tabs` ·
`.card`/`.card-head` · `.toolbar`/`.search` · `.field`/`.input`/`.textarea`/`.select` ·
`.btn`(primary/dark/ghost/danger/sm) · `.seg` · `.tbl` · `.tag`/`.chip`/`.sev` ·
`.tg`(토글)/`.cbx`(체크) · `.note`(info/warn/danger) · `.pager` · `.modal` · `.area-no`

## 원칙
- **하드코딩 색·폰트·그림자 금지.** 전부 `tokens.css` 변수 재사용 → 테마 전환·제품 변형이 공짜.
- 새 컴포넌트가 필요하면 토큰으로 짜서 `base.css` 에 추가 (양 테마에서 검증).
- 캔버스는 항상 **1440px 고정**.
