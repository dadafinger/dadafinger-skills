# Product 디자인시스템 레퍼런스 (Figma 작업 일관성 SoT)

> 목적: Product/솔루션 Figma 화면을 만들 때 **손그림 금지, 문서화된 디자인시스템 컴포넌트를 재사용**하기 위한 단일 기준. figma-change-flow는 화면 작성/수정 전 이 문서와 아래 원천을 먼저 확인한다.

## 0. 원천(SoT)
- **Confluence 스페이스 "솔루션 정책"** — cloudId `4013ae40-508f-45b0-a679-965c3c38ccbc`, space key `[fileKey-removed]`, id `1939046614`. 컴포넌트/토큰/화면 정책의 권위 문서. (Atlassian Rovo MCP `getConfluencePage` contentFormat:markdown 로 열람; 인증 필요 시 사용자 `/mcp`)
  - 인덱스: `공통 컴포넌트 정책 (Figma)` 1861255872 · `솔루션 컴포넌트 정책` 1942454273 · `솔루션본부 3.0.4 컴포넌트 정책` 2142109952 · `디자인 토큰 가이드` 1940619326 · `단위 표기` 2415591425 · `퍼블리싱 정책` 1940619286 · `React 컴포넌트(26년-Noh)` 2902523906
- **Figma DS 라이브러리(정본)**:
  - 🔑 **`(v1.1) CCDS Components` = fileKey `[fileKey-removed]`** — **Figma 전용 컴포넌트 정본**(진입 노드 `[node-id]`, URL `[figma-design-removed]`). 폼/표/버튼/필드/필터/페이지네이션 등 컴포넌트 원본은 **여기서** 가져온다(`importComponentByKeyAsync` / 인스턴스 clone).
  - ⚠️ (구) `25' Design System Policy Document` `[fileKey-removed]` · `25' Design System` `[fileKey-removed]` — **outdated**, §1 node-id는 이 구 파일 기준이라 **CCDS v1.1에서 재확인 필요**(node-id/key는 그대로 쓰지 말 것).
- 4.0 작업 파일 = `[fileKey-removed]`. 토큰은 Token Studio→style-dictionary→**CSS 변수**(예 `--palette-neutral-0:#000000`), 테마 CSS(`product-light.css` 등). 차트는 토큰 제외.

## 1. 컴포넌트 → Figma node-id (⚠️ 구 Policy Document `[fileKey-removed]` 기준 — 정본은 CCDS v1.1, 아래 node-id는 재확인 필요)
| 컴포넌트 | node-id | 비고 |
|---|---|---|
| GNB | `169-189722` | 최상단 로고·솔루션 전환 |
| LNB | `400-151672` | 좌측 메뉴 + 하단 기능(검색/알림/프로필/Cloud View) |
| Breadcrumbs | `138-51270` | LNB 구성 종속 |
| Header-form | `169-190544` | sticky, Breadcrumbs+Navigator+Cloud View |
| Button | `34-552` | Primary>Secondary>Tertiary>Ghost |
| Field (Input/Select/Number/TextArea) | `225-188276` | |
| Checkbox | `59-8511` | |
| Dropdown (& Filter) | `121-179618` | |
| Filter | `141-56499` | Search/Hybrid/Select-only |
| Pagination | `149-72231` | |
| List | `431-166362` | 1뎁스 |
| Listbox | `3828-99232` | 다뎁스/스텝 |
| Modal | `3001-205588` | |
| Nodata | `143-115368` | 대시보드 케이스는 DS 파일 `[fileKey-removed]` `17569-63636` |
| Alarm | `204-200556` | LNB 알림 패널 |
| Hierarchical Table | (DS 파일) `[fileKey-removed]` `14773-38087` | 앞쪽 전용 Arrow 셀 |

> Table은 Ant Table 기반(전용 마스터 node 미표기) — 패딩/스크롤 규칙은 §2 참조. 정밀 스펙은 위 node 직접 확인.

## 2. 핵심 스펙 (verbatim 수치 우선)
- **GNB**: 닫힘 트리거 = 로고/`unfold_more` 클릭·재클릭·외부 클릭·Close.
- **LNB**: 하단 기능 동시활성 — 검색↔알림·검색↔프로필 가능, **알림↔프로필 배타(둘 다 팝오버)**. 스크롤바 6px, 텍스트–화살표 4px, 마지막 메뉴 하단 8px 마진.
- **Breadcrumbs**: LNB 구성 종속, 없는/클릭불가 메뉴는 **Disabled(컬러 Subtler)**. 솔루션본부=**솔루션명 제외 1뎁스부터**. 상세/생성/수정 = `{직전 페이지명+동작}`.
- **Button**: 간격 **8px**(고스트 4px), 인풋+버튼 4px. 취소=고스트 고정. Danger=부정 동작만. 데이터 추가=Accent-link 상단. 버튼명 표준: 생성/수정/삭제/적용/해제/백업, 그 외 '확인'. With-Dropdown(Split, default형)=드롭다운 선택 즉시 실행.
- **Field**: 높이 M **32** / L **40**(예외 Small 24=콤보박스·열고정). 너비 m **608**/l **920**, Select·TextArea **588**. 인풋+버튼 간격 4px. InputNumber suffix 단위 사용금지(단위 표기는 별도 40px 공간, 290 내). 유효성 문구 한 줄. Placeholder/유효성 문구 표준 다수(§Confluence Field 참조).
- **Checkbox**: 수평 gap **16px**, 상하 8px, 2줄↑이면 트리거 상단 정렬.
- **Dropdown**: 단일=우측 체크 / 다중=좌측 체크박스+전체선택. 너비 부모 따름(예외 작업열 128~400, Search/열고정 200~400). 높이 34/36. 유효성은 메뉴 아닌 **선택 필드에 Invalid**.
- **Filter**: Search(돋보기·자연어)=Table 외 / Hybrid(필터+Select)=Table 내 기본 / Select-only. 목록에서만 우측 기능과 같은 행. '{n}개 선택됨' 기능은 좌상단(Filter 우측 금지). Select 목록 max-H **520px**.
- **Pagination**: 리스트 수 5/10/20/30/50, **목록 default 20**. 생성/모달 Large=5 고정 히든. 상세 테이블만 20 / 다중 섹션 10. 하이어라키 상위 20·하위 10.
- **3.0.4 Table**: Ant 기반, **헤더셀 말줄임 금지**(Sort가 셀 전체 점유). 너비=auto layout 기본 + 좌우 스크롤 시 **x-scroll 항상 추가**(1148/1500 내외). 헤더셀 특정 시 좌우 패딩 **12px**, 레이블↔아이콘 **4px**. **작업열 54px 고정**(다국어 작업/Task/作業).
- **Alarm**: 타이틀 **1줄**·본문 **2줄** 초과 말줄임. LNB 알림 클릭 토글, 재클릭/외부클릭 해제, **Close 버튼 금지**. 탭 우측 실시간 on/off 스위치.
- **Cloud View (Panel)**: 콘베 전용 독립 패널. 트리거 **Breadcrumb 우측**. 높이 Default=Max(브라우저 40%)/Min 160px. 기능 간격 4px. 서체 Pretendard JP body-02. v3.0.6 색=`text/default`, bg=`layer-02`.
- **Nodata**: 동사형 문구. 검색없음 `검색 결과가 없습니다`/`검색어나 검색 필터를 변경해 주세요.` · 데이터없음 `데이터가 없습니다`/`대상을 추가하거나 다시 확인해 주세요.` · 상위선택 c-1 · Listbox d-1. 테이블 Nodata 높이 = 셀수×**36px**(목록 720 / 모달 180 / 상세 720·360).
- **Modal**: 동시 1개, **Close 버튼 미사용(Esc/취소·확인)**, 푸터 버튼 ≤3. Small 400 / Medium 644 / Large 950 고정, 6열↑=Full-width(5% 마진). 컴포넌트 기본 너비 290px.
- **List/Listbox**: List=1뎁스(첫 항목 선택, KV 16px, Sider 320px) / Listbox=다뎁스·스텝(미선택 시작, 카테고리 필수, 588/886px, 전체 450px).
- **단위 표기**: 띄어쓰기 기본(`8 GiB`·`8 Core`·`8 W`·`8 °C`), 한글 단위명사는 붙임(`8개`·`8일`·`80,000원`), `%`는 붙임(`8%`). 영문 전체 띄어쓰기.

## 3. 리스트/테이블 화면 표준 조합 레시피 (예: 알람 센터)
1. **Header-form(sticky)** = Breadcrumbs(+Navigator, 콘베면 +Cloud View). 기능 아이콘 간격 4px.
2. LNB 하단: 검색=Global Search 레이어, **알림=Alarm 패널**(Close 없음).
3. 본문 = **Table(3.0.4)** — 헤더 패딩 12·레이블↔아이콘 4, x-scroll, 작업열 54 고정, Sort=헤더 전체. 계층이면 Hierarchical Table.
4. 필터 = **Filter(Hybrid)**(Table 내), 사이드 목록은 List/Listbox.
5. 빈 상태 = **Nodata**(높이 셀수×36).
6. 상세/액션 = **Modal**(Close 없음, ≤3 버튼), 콘베 상세뷰 = **Cloud View(Panel)**.
7. 페이지네이션 = **Pagination**(목록 20 default).

## 4. 작업 규칙
- Figma 화면 생성/수정 전 **이 문서 + 해당 Confluence 페이지를 먼저 확인**한다.
- 컴포넌트는 위 node-id의 DS 라이브러리 인스턴스를 재사용(`importComponentByKeyAsync` 또는 기존 인스턴스 clone). **박스+라벨 손그림 금지**(불가피할 때만, 사용자 고지 후).
- 정책표가 비어 있거나 이미지로만 있는 항목(Hierarchical Table 일부, Cloud View, Global Search)은 해당 Figma 노드를 직접 열어 확인.
