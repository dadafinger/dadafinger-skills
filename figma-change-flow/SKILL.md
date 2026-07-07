> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: figma-change-flow
description: Apply planning/prototype changes to existing Figma nodes with a repeatable workflow. Use when the user asks to reflect updated specs in Figma, revise specific node URLs, or create/update documentation frames in a Figma file.
disable-model-invocation: true
---

> Sharing scope: Internal
> Share policy: caution
> Notes: 기존 Figma 노드 수정; node-registry·내부 fileKey

# Figma Change Flow

## Goal

변경된 기획서/프로토타입 기준으로 지정된 Figma 경로를 수정 또는 신규 작성한다.

## Mandatory Intake Gate

작업 시작 전에 아래 2가지를 반드시 확인한다.

1. **피그마 경로 확인**
   - 사용자 요청에 Figma URL/노드 경로가 없거나 불명확하면 반드시 질문한다.
   - 사용자 문구(원문 유지): `피그마 경로는 매번 모르면 물어봐주세요.`

2. **변경 기준 리소스 요청**
   - 어떤 변경안을 기준으로 반영할지 반드시 요청한다 (md/spec, 프로토타입, 회의노트, 스크린샷 등).
   - 사용자 문구(원문 유지): `기준으로 삼을 변경점 리소스를 요청하세요.`

3. **🔴 목업(와이어프레임) 작업이면 — "레이아웃 소스" vs "검토 소스"를 분리한다 (필수)**
   - **목업/와이어프레임의 1차 레이아웃 소스 = 해당 화면의 최신 HTML 프로토타입.** 명세(md/spec)는 **검토·정합 기준**이지 **드로잉 소스가 아니다.**
   - 쓰기 전에 반드시: (a) 해당 화면의 **최신 HTML 프로토타입을 먼저 찾는다**(`html/vN/`). (b) 있으면 그 HTML 화면을 옮겨온다(캡처→네이티브 재구성 / DS 클론). (c) **그 다음** 명세 delta로 검토·보정한다.
   - **명세 텍스트만 보고 목업을 손으로 그리지 않는다** — 그러면 "실제 화면"이 아니라 **주석 덩어리(정책 문장 나열)** 가 나온다(사용자 지적 사례 2026-07-06 "명세만 봤구나… 엉망"). 명세 본문은 우측 Description으로만 간다.
   - **HTML 프로토타입이 없거나 명세보다 구버전이면** → 그 사실을 **먼저 사용자에게 알리고**, HTML을 소스로 옮긴 뒤 명세 delta를 "검토 반영"으로 표기한다(HTML=레이아웃, 명세=정본).
   - **신규 vs 기존 화면 수정으로 방법이 갈린다 (사용자 확정 2026-07-06)**:
     - **신규 화면 = HTML 역반영**(위 (a)(b)(c)). 
     - **기존 화면 수정 = 방법이 다르다 — 아직 미확정.** 함부로 HTML을 통째로 재이식하지 말고(기존 편집·정합이 깨짐), **사용자에게 방법을 확인**한다. 확정 전엔 기존 노드에 대한 대규모 재작성 금지.
   - **"신규인데 HTML이 없는 요소"(예: 새 모달)** → 명세만 손그림(=엉망) 금지. **DS 컴포넌트를 클론**(예 Modal `3001-205588`, `references/design-system.md`)해 **실제 UI**(폼·테이블·트랜스퍼·버튼)로 구성하고 명세(예 §7.5)로 **검토**한다. 정책 문장이 아니라 실 UI를 그린다.
   - **🔴 대상 페이지의 목업 스타일에 맞춘다** — 페이지 목업이 **`wf-` 회색 스켈레톤**이면 새 요소도 wf 회색으로, **DS 컴포넌트 목업**이면 DS로. wf 페이지에 DS-blue를 얹는 등 혼용하면 정합이 깨진다(먼저 `get_metadata`로 기존 목업이 wf냐 DS냐 확인).

입력이 모두 확정되기 전에는 Figma 쓰기 작업(`use_figma`)을 하지 않는다. **목업 작업은 3번(HTML 소스 확보 / 신규·기존 방법 확정)까지 끝나기 전에는 그리지 않는다.**

## Required Inputs

- Figma 파일 URL 또는 `fileKey`
- 수정/신규 대상 노드 URL 목록 (`node-id`)
- 변경 기준 리소스 경로/URL (최신본 우선)
- (선택) 반영 우선순위, 완료 정의

## Execution Workflow

0. **Figma 연결 precheck 게이트 (쓰기 전 필수)**
   - `use_figma` 쓰기 작업을 시작하기 **전에** 연결 상태를 가볍게 확인한다 — `whoami` 또는 대상 파일 `get_metadata` 1회.
   - 결과에 따라 분기한다:

   | 상태 | 신호 | 처리 |
   |---|---|---|
   | **정상** | whoami/metadata 응답 OK | 진행 (아래 4번 — 작은 멱등 배치). |
   | **OAuth 만료/해지** | `connection invalidated. The user needs to reconnect it` | 재시도·포커스로 **복구 불가**. 사용자에게 커넥터 재연결 요청. 그 전까지 **반영 보류** → 아래 "보류 시 산출" 수행. |
   | **브리지 불안정** | `connection lost` | 읽기는 살아있을 수 있음. 작은 배치 + 클라우드 검증으로 진행 (→ "쓰기 브리지 불안정 대응" 절). |

   - **보류 시 산출 (반영 못 할 때도 손해 0):** HTML/md 산출물은 그대로 내고, **반영 플랜(노드별 변경 체크리스트)을 로컬 md로 보존** → 연결 복구 후 그대로 실행. (과거 사례: 알람 SMTP — 세션에 use_figma 없어 직접 반영 보류, 명세까지만 산출.)
   - **배치 모드:** 여러 화면을 반영할 땐 연결 확인된 **한 세션에 몰아서** 처리한다(매 세션 가용성에 휘둘리지 않게).

1. **입력 정규화**
   - Figma URL에서 `fileKey`, `node-id`를 추출한다.
   - 변경 대상 노드를 `수정`/`신규`로 분류한다. **clone/기준 노드는 [`references/node-registry.md`](references/node-registry.md)에서 먼저 조회**(검색 아닌 룩업), 헤더 텍스트로 재확인 후 확정.

2. **기준 리소스 분석**
   - 지정된 최신 md/spec/prototype를 읽고 변경 포인트를 목록화한다.
   - 기존 버전과 충돌되는 구버전 정책 문구를 식별한다.

3. **Figma 현황 파악**
   - 대상 노드의 `get_metadata`/`get_design_context`/`get_screenshot`로 현재 상태를 확인한다.
   - 변경 포인트를 노드별 체크리스트로 매핑한다.

4. **반영 (incremental)**
   - `use_figma`로 작은 단위로 수정한다.
   - 텍스트 수정 시 폰트 로드 규칙을 지킨다.
   - 탭/섹션 제거 요청은 텍스트 치환이 아닌 프레임 구조 변경(삭제/재배치)까지 수행한다.

5. **검증**
   - 변경 노드별 스크린샷 재확인.
   - 핵심 정책 문구(버전/지표/탭/캘린더/차트 등) 반영 여부를 점검한다.

6. **결과 보고**
   - 수정된 노드 ID 목록
   - 삭제/생성된 프레임 목록
   - 남은 확인 필요 항목(있으면)

## Product Figma 기획서 표준 포맷

신규 기획서 작성 또는 기존 기획서 수정 시 아래 3단 구조를 표준으로 따른다.  
참고 파일: [figma-url-removed]

### 1. 표지 (Cover)
- 배경: 진한 네이비/다크블루
- 상단: `CONTENTS` 라벨
- 중앙: 문서 제목(기능명, 신규/수정 여부 표기) + 문서 번호 (예: FY25-CONT-XXXX)
- 하단: PRODUCT 로고 + 기밀 문구

### 2. 기능 명세 요약 (0. 세부 기능 명세)
- 흰 배경 페이지
- 제목: `0. 세부 기능 명세`
- 테이블 컬럼: 추가일자 / WIP 기능 (변경 내용 요약) / 참고 화면(Screen ID) / 비고(N/A 등)
- PRODUCT 로고 + 기밀 문구 하단 배치

### 3. 상세 명세 (Detailed Spec)
- **헤더 행**: Screen ID | 번호(예: CON-006) | Page Title | 페이지명 | Author | 작성자
- **본문 2단 구성**:
  - 좌(Description): UI 스크린샷(또는 와이어프레임) + 기능 설명 bullet
  - 우(Appendix): 보충 설명, 예외 케이스, 정책 상세
- **하단**: Changelog 테이블 (날짜 / 변경 내용 / 작성자)

#### 상세 명세 페이지 해부 — 4.0 파일 기준 포맷 예시 (사용자 지정 SoT)

4.0 파일(`[fileKey-removed]`)의 **`[node-id]` "집계 보고서_호스트"** 가 상세 명세의 포맷 예시다 (사용자가 직접 지정). 신규/재정비 시 구조를 새로 그리지 말고 **이 페이지의 Description 프레임을 `clone()` 후 텍스트만 교체**한다 (`[node-id]` Sections 0–4 / `[node-id]` Sections 5–7+Appendix+Changelog).

- **페이지 골격**: Background+Shadow(3440) > [헤더 Container 3400×86(GRID)] + [콘텐츠 Container 3400(HORIZONTAL, gap 36): `1920px mockup column` + Desc 칼럼 704 + Desc 칼럼 704]
- **Desc 칼럼 스타일**: 검은 풀폭 타이틀 바(Description/Appendix/Changelog, 흰 글자) · Intro 단락 + 버전 라인(`vX.X (YY'MM/DD) — 요약`)
- **섹션** = [num 거터 50px: fs22 Inter Bold] + [body 654px: title-bar 44px(fs14 Inter Bold + 선택적 노란 배지 "NEW vX.X") + 불릿 TEXT 노드들]
  - ⚠ 이 "노드 단위 불릿·fs12/서브 fs11"은 **구 3.0.x 템플릿 값** — 4.0 Description 본문 정본은 **플랫 인코딩 B(`setFlat`: 섹션 본문 1 TEXT 노드·fs24/lh36)**. 이 해부는 페이지 골격(3단·거터 50px·타이틀바 44px) 참고용이고 본문 서식은 setFlat을 따른다.
  - 섹션 번호·본문은 목업 내 ①②③… 마커와 상호 참조
- **Changelog 행(ch-row)** = [v 셀 130px: `vX.X · YYMMDD` Roboto Mono Bold 11 + `추가/변경 · 작성자` fs10] + [변경 불릿 fs11 550w] — 제목만 있는 빈 Changelog 금지, 스펙 md 변경 이력에서 최소 2–3행 채울 것
- 폰트: 예시 클론은 Inter/Roboto Mono 유지 (한글 fallback 렌더 정상 — 신규 생성 텍스트에만 Noto Sans KR 후보 로드 규칙 적용)

### 작성 순서
1. 표지 생성 (문서명·번호 확정 후)
2. 기능 명세 요약 테이블 작성
3. 상세 명세 페이지(들) 작성 — Screen ID 단위로 1페이지씩
4. 수정 시에는 상세 명세 본문만 업데이트하고 Changelog에 이력 추가

> **주 요청은 상세 명세 수정이 대부분임.** 표지/요약 수정은 사용자가 별도 언급할 때만 수행.

### 🔴 2단계: 내용 치기(A) → 서식 일괄(B) (사용자 확정 2026-06-25)

Figma 기획서 **정책·용어·필드 내용** 반영과 **Description·목업 서식 통일**은 **분리**한다.

| 단계 | 할 일 | 금지 |
|---|---|---|
| **A 내용** | spec 기준 Description·목업 UI 텍스트·용어 반영 | `[node-id]` 구조 clone·덩어리 TEXT 분해·①②③ 마커·Appendix/Changelog 정리 |
| **B 서식** | [`references/format-batch-pass.md`](references/format-batch-pass.md) 체크리스트 **기능 세트 일괄** | 정책·필드 내용 추가(필요 시 A로 복귀) |

- **알람(2026-06)**: A 진행 중. Description 덩어리·구 블록 순서·Changelog 노출·**목업 빨간 ①②③ 미배치** → **B에서 일괄**.
- B 트리거: 사용자 「서식 일괄」「포맷 통일」 또는 A 완료 확인.
- **목업 ①②③**: 좌 mockup column **빨간 동그라미** — md `marker=①` / `### N` / Description 거터 / HTML `.area-no` **1:1**. 예시에서 **clone**(`[node-id]`, `[node-id]`). 없으면 B 미완료.
- **와이어프레임 LNB 크롬**: 기획 목업은 **디자인과 구분** — LNB/GNB에 DS 블루 금지, `wf-lnb` 문서형 회색+잉크. 상세 토큰·HOW → [`references/wireframe-chrome.md`](references/wireframe-chrome.md).

---

## 페이지 하위 모달·팝업 = "in-page 가이드" (별도 페이지 아님, 사용자 확정 2026-07-06)

한 페이지에서 뜨는 **모달/팝업/드로어**는 별도 화면 프레임으로 빼지 않고 **해당 페이지 프레임 안에 시각 가이드로 함께** 그린다("페이지 하위 모달도 해당 페이지 내에서 함께 시각적으로 가이드를 제공").

- **배치**: 메인 목업 바로 **아래 여백**(예: `Background+Shadow` 카드 내 목록 스켈레톤 하단)에 `dim 배경 + 중앙 modal card` 형태로. 목록과 모달이 **동시에 보이게**(모달로 화면을 덮어 목록을 가리지 않음).
- **마커 1:1**: 모달 가이드에 **Description의 서브마커(예 `1-1`)** 와 같은 번호 배지를 붙여 우측 설명과 매칭. (섹션 1 = 액션 버튼 영역, `1-1` = 그 버튼이 띄우는 모달.)
- **모달 규격(DS, `references/design-system.md`)**: **Close 버튼 없음**(Esc/취소·확인) · 푸터 버튼 **≤3** · 폭 Small 400 / Medium 644 / Large 950 고정 · Nodata 문구 규칙. 트랜스퍼(후보↔선택) 피커는 Large.
- **스타일**: 페이지 목업이 `wf-` 회색이면 모달도 wf 회색으로(위 Intake Gate 3번 스타일 매칭).
- 검증 사례: 알람 설정 `[node-id]` 하단 `수신자 추가` 모달(트랜스퍼 피커) = `모달1-1-수신자추가-guide`, 명세 §7.5로 검토(2026-07-06).

## 프로토타입 → 와이어프레임 캡처 & Figma 삽입 워크플로우

상세 명세의 콘텐츠 영역에 와이어프레임(UI 스크린샷)을 얹어야 할 때 아래 절차를 따른다.

### Step 1. 로컬 서버 기동 (HTML 프로토타입인 경우)

`.claude/launch.json`에 서버 설정을 작성하고 `preview_start`로 기동한다.

```json
{
  "version": "0.0.1",
  "configurations": [{
    "name": "prototype",
    "runtimeExecutable": "python3",
    "runtimeArgs": ["-m", "http.server", "7788", "--directory", "<HTML이 있는 디렉토리>"],
    "port": 7788
  }]
}
```

### Step 2. Chrome 헤드리스 캡처

Chrome 익스텐션이 연결되지 않았거나 브라우저가 read-only 티어인 경우, Bash로 Chrome 헤드리스를 사용한다.

```bash
ENCODED_URL=$(python3 -c "import urllib.parse; print('http://localhost:7788/' + urllib.parse.quote('<파일명.html>'))")
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new --disable-gpu \
  --screenshot="/tmp/wireframe.png" \
  --window-size=1440,900 \
  "$ENCODED_URL"
```

- 캡처 해상도: 기본 1440×900 (프로토타입 캔버스 너비에 맞게 조정)
- 탭이 여러 개인 경우 각 탭별로 별도 캡처 (URL 파라미터 또는 별도 HTML 페이지 활용)

### Step 3. Figma 콘텐츠 영역에 Rectangle 생성

`use_figma`로 이미지를 담을 Rectangle을 콘텐츠 프레임 안에 생성한다.

```js
const rect = figma.createRectangle();
parent.appendChild(rect);
rect.name = 'wireframe-<화면명>';
rect.x = 40;
rect.y = 180; // 제목·기준 텍스트 아래
rect.resize(2580, Math.round(2580 * 900 / 1440)); // 비율 유지
// 기존 body text가 있으면 rect 아래로 이동
bodyText.y = rect.y + rect.height + 40;
```

### Step 4. 이미지 업로드 & fill 적용

`upload_assets` → `curl POST` 순서로 진행한다.

```bash
# 1) 업로드 URL 획득 (upload_assets 호출, nodeId = rect ID)
# 2) curl로 PNG 업로드
curl -X POST "<submitUrl>" \
  -F "file=@/tmp/wireframe.png;type=image/png"
```

- `scaleMode`: `FIT` (이미지 비율 유지)
- 업로드 성공 시 `placedOnNodeId`가 rect ID와 일치하는지 확인

### Step 5. 검증

`get_screenshot`으로 와이어프레임이 콘텐츠 영역에 올바르게 삽입됐는지 확인한다.

---

## 🔴 와이어프레임은 "직접 그리지 말고" 연동 에셋(디자인시스템 컴포넌트)으로 — 최우선 원칙

> **🔴🔴 0순위 — 목업의 소스는 "명세"가 아니라 "HTML 프로토타입"이다.** 목업/와이어프레임을 그리기·고치기 전에 **해당 화면의 최신 HTML 프로토타입(`html/vN/`)을 먼저 찾아 그 화면을 옮겨온다**(캡처→네이티브 재구성 또는 DS 클론). **명세(md)는 옮긴 뒤 검토·정합용**이지 드로잉 소스가 아니다. 명세만 보고 목업을 손으로 그리면 실제 화면이 아니라 정책 문장 나열이 나온다(2026-07-06 사용자 지적: "명세만 봤구나… 엉망"). → Intake Gate 3번 참조. HTML이 없거나 명세보다 구버전이면 먼저 사용자에게 알리고 진행한다(HTML=레이아웃 소스, 명세=정본 검토).

> **clone 대상 SoT = [references/node-registry.md](references/node-registry.md)** — 어떤 노드를 clone/참조할지(포맷 예시·화면별 SoT·드로잉 화면·in-file 인스턴스)는 여기서 **먼저 조회**(검색 아닌 룩업). 흩어진 인라인 node-id의 단일 출처.
> **디자인시스템 SoT = [references/design-system.md](references/design-system.md)** — 컴포넌트 마스터 스펙·정책. Figma 화면 생성/수정 전 반드시 먼저 확인. Confluence "솔루션 정책"(space `[fileKey-removed]`) + Figma DS 라이브러리(`[fileKey-removed]`·`[fileKey-removed]`) 컴포넌트 node-id·스펙·표준 조합 레시피가 정리돼 있다. 컴포넌트는 거기 명시된 node-id 인스턴스를 재사용한다.
>
> 역할: **node-registry = "무엇을 clone"(작업파일 내 node-id) · design-system = "컴포넌트 마스터"(라이브러리 key import).**

목업/와이어프레임을 새로 만들 때 **박스+라벨을 손으로 그리는 스켈레톤은 최후의 수단**이다. 그렇게 그리면 실제 화면과 헤더·LNB·테이블·세그먼트·토글 톤이 어긋나 **일관성이 깨진다(사용자 지적 사례)**. 반드시 아래 순서로 **기존 연동 에셋을 먼저 재사용**한다.

1. **이미 이 파일에 인스턴스로 박혀 있는 디자인시스템 컴포넌트를 clone해 재사용.** 4.0 파일의 기존 목업은 `header`, `newproduct/대시보드|컴퓨트|…`(LNB), `component/breadcrumb`, `parts/header`·`parts/cell`(테이블), `Search Filter`, `pagination` 등 **연동 컴포넌트 인스턴스**로 구성돼 있다. 숨기기 전에 이 인스턴스들을 `clone()`해서 새 화면 크롬으로 재사용하라(공유 인스턴스 원본은 수정 금지, override만).
2. **사용자가 이미 그려 둔 고충실 화면을 참조/클론.** 예: `full 3.0.6 Product`(fileKey `[fileKey-removed]`, 예 node `[node-id]` "임계치 알람 생성")에 헤더·breadcrumb·기본정보·대상 선택(3-pane)·임계치 정책 테이블·채널 토글이 **실 컴포넌트로 완성**돼 있다. 같은 기능 화면은 이걸 기준 에셋으로 삼는다.
3. **published 라이브러리 컴포넌트는 `search_design_system`으로 찾아 `importComponentByKeyAsync(key)`로 인스턴스화** (figma-generate-design 스킬 워크플로 참조). cross-file이라도 팀 라이브러리면 키로 import 가능.
4. **위 1~3이 모두 불가능할 때만** 아래 "네이티브 스켈레톤"으로 박스+라벨을 그린다 — 그리고 이 경우에도 사용자에게 "연동 에셋이 없어 스켈레톤으로 그린다"를 먼저 알린다.

> 정리: **clone(기존 인스턴스) > 사용자 드로잉 화면 클론 > import(라이브러리 키) > (최후) 손그림 스켈레톤.** "기존 피그마에 연동된 에셋을 쓰라"가 기본값이다.

## 평면 스크린샷 → 편집 가능 스켈레톤 재구성 (위 1~3이 불가능할 때만)

사용자가 "와이어프레임 예시"로 넣어둔 것이 **평면 PNG 스크린샷**(`RECTANGLE` + `IMAGE` fill, 보통 이름이 `스크린샷 ...`)인 경우가 많다. Figma는 래스터 픽셀을 텍스트/도형 레이어로 **자동 분해하지 못하므로**, "수정 가능하게 만들어달라"는 요청은 **스펙 기준으로 네이티브 레이어 스켈레톤(박스+라벨)을 새로 그리는 것**이 유일한 방법이다. **단, 위 '연동 에셋 우선' 원칙을 먼저 시도한 뒤**의 폴백이다.

> "컴포넌트로 등록"(`createComponentFromNode`)은 편집성을 더해주지 않는다(오히려 인스턴스는 구조가 잠김). 목표가 "수정 가능"이면 컴포넌트화가 아니라 **네이티브 재구성**이다.

### Step 1. 타입 판단 먼저 (read-only)

`use_figma`로 대상 노드를 순회해 **IMAGE fill 노드**가 있는지 확인한다.

```js
function hasImageFill(n){ return Array.isArray(n.fills) && n.fills.some(f => f && f.type === 'IMAGE'); }
// IMAGE fill RECTANGLE / 단일 이미지 → 평면 스크린샷 = 재구성 필요
// FRAME/GROUP + TEXT/도형 자식      → 이미 편집 가능 = 재구성 불필요
```

### Step 2. 재구성 수준 합의

- "수정 가능하게만" = **가벼운 스켈레톤**(필터바·결과표를 박스+라벨로). 픽셀 정밀 재현은 별도 요청 시에만.
- 모호하면 [가벼운 스켈레톤 / v_X 충실 재구성 / 스크린샷 유지] 중 택1로 물어본다.

### Step 3. 원자적·멱등 생성

- **작은 단위로 멱등하게** 생성한다. 노드 수가 적으면 1회 호출로 원자적 생성, **많으면(수십+ 노드) 작은 배치로 분할**(스켈레톤 → 행 묶음 ~3개씩 → 푸터·리사이즈). 큰 단일 호출은 커밋 전 끊겨 반영이 안 되는 경우가 잦다 → 아래 **'쓰기 브리지 불안정 대응'** 참조.
- 생성 전 동일 이름(`{화면}-skeleton-vX.X`) 기존 노드를 제거 → **재시도해도 중복 안 생김**.
- 원본 스크린샷은 **삭제 대신 `visible=false`(숨김)** — 되돌릴 수 있게. 스켈레톤은 원본의 `x/y/parent`를 그대로 받아 같은 자리에 배치.
- 폰트: 한글은 후보를 try/catch로 순차 로드(**Noto Sans KR / Pretendard / Apple SD Gothic Neo**; `Inter`는 한글 미렌더). 계층은 한 폰트 + `fontSize` 차등으로 단순화.

```js
async function pickFont(){
  const c=[{family:"Noto Sans KR",style:"Regular"},{family:"Pretendard",style:"Regular"},
           {family:"Apple SD Gothic Neo",style:"Regular"},{family:"Inter",style:"Regular"}];
  for(const f of c){ try{ await figma.loadFontAsync(f); return f; }catch(e){} }
}
```

### Step 4. 검증

`get_screenshot`(URL → `curl` 다운로드 → Read)으로 스켈레톤과 주변 컬럼이 정합한지 확인한다.

### 형제 화면 재사용 (같은 기능의 다른 탭/화면)

같은 기능의 형제 화면(예: 미터링 ① 이력 데이터 ↔ ② 집계)은 처음부터 새로 그리지 말고 **이미 만든 컬럼을 `clone()` → 대상 화면 프레임에 배치 → 평면 스크린샷은 `visible=false`** 로 두고 **다른 부분만 교체**한다.

- 교체 대상: 활성 탭 상태 / 필터 영역 / 결과 테이블 / 타이틀·푸터 라벨.
- 유지: 디자인 시스템 인스턴스 크롬(헤더·LNB·브레드크럼·탭 틀). **공유 인스턴스 자체는 수정 금지** — active 등 화면별 차이만 인스턴스 prop/텍스트로 조정.
- 효과: 두 화면 구조 일관 + 컴포넌트 동기화 유지.

### 형제 스펙 페이지 일괄 반영 (여러 화면을 같은 MD 세트로)

같은 기능군의 여러 스펙 페이지(센터·이력·설정·생성/수정·상세·CloudView 등)를 한 번에 최신화할 때.

- **대상 노드부터 확정 — 절대 이름·위치로 추측 금지.** 한 파일에 같은 Screen ID가 **현행 프레임 + 마스터 행 + 구버전**으로 중복 존재한다(예: '알람' 섹션의 현행본 vs 별도 `CONT-09_10_xx` 마스터(=구 기능, 다른 작성자/버전) vs 표지·3.0.x 잔존본). **각 후보의 헤더 텍스트(Screen ID·Page Title·Author)를 `use_figma`로 읽어 검증**한 뒤 매핑을 사용자에게 확인받고 진행한다. 잘못 건드리면 다른 산출물을 덮어쓴다.
- **통합 폼 주의**: 생성/수정/복제는 보통 **1개 통합 프레임**(`?mode=`)이다 → MD 2개가 Figma 1개에 매핑.
- **레이어명 ≠ 내용**: 레이어명이 "알람 수정"이어도 헤더가 "상세"면 상세 페이지다. 헤더 기준으로 판단.
- **스펙 페이지가 없고 표지만 있을 때**: 표준 포맷을 새로 그리지 말고 **형제 스펙 페이지를 `clone()` → 헤더(Screen ID/Title)·Description·Changelog 텍스트만 교체 → Main Area의 레거시 자식(숨김 목업·이전 스켈레톤) 전부 `remove()` 후 해당 화면용 스켈레톤 재구성.** 클론은 480+ 텍스트(레거시 인스턴스 포함)를 끌고 오므로, 편집 대상은 **내용 매칭(`characters` prefix)** 으로 노드 id를 찾는다(클론은 id가 전부 새로 부여됨).
- **본문 폰트 삼분(스펙 페이지 관행)**: Intro=Noto Sans Light, 섹션 본문=Roboto Regular, Appendix/Changelog=Inter Regular. 단정하지 말고 **노드별 현재 폰트(`getStyledTextSegments(['fontName'])[0].fontName`)를 로드 후 덮어쓴다** — Inter도 이 환경에선 한글 fallback 렌더됨.
- **이중 불릿**: 본문에 `\n`로 줄을 나눠 쓰면 노드의 기존 unordered-list 옵션과 리터럴 `· ` 마커가 겹쳐 "• ·"가 된다 → `node.setRangeListOptions(0, len, {type:'NONE'})`로 리스트 옵션 제거.
- **Changelog는 prepend**: 기존 `characters`를 읽어 새 버전 줄을 맨 앞에 붙이고(중복 삽입 가드: 버전 토큰 indexOf 체크), 빨강 fill·Inter는 그대로 보존.

### MCP 읽기 hang 우회 (Figma 서버 불안정 대응)

`get_metadata`와 텍스트 노드의 `.characters`/`.fontName` **읽기**가 간헐적으로 타임아웃될 수 있다.

- **구조 파악**: `get_metadata` 대신 `use_figma`로 순회해 `id/name/type/x/y/size`만 회수. 반드시 `return JSON.stringify(...)` (console.log은 회수 안 됨).
- **본문 내용 확인**: `.characters`가 hang하면 `get_screenshot`으로 **시각 확인** 후 매핑.
- **기존 텍스트 덮어쓰기**: 옛 폰트를 읽지 않고 `node.fontName = 로드된폰트` 먼저 → `node.characters = "..."` 순서.
- **이중 불릿**: 원본 리스트 서식이 리터럴 마커와 겹치면 `node.setRangeListOptions(0, len, {type:'NONE'})`로 제거.
- **레이아웃 안전성**: 덮어쓰기 전 `layoutMode` 확인 — VERTICAL auto-layout이면 본문 길이가 바뀌어도 자동 reflow(겹침 걱정 없음).

### 쓰기 브리지 불안정 대응 (`use_figma` connection lost 우회)

`use_figma`(쓰기·JS 실행)는 Figma **데스크톱 앱 플러그인 런타임**을 경유한다. 이 연결이 자주 끊겨 **"Anthropic proxy: MCP server connection lost"** 가 뜬다. 반면 `get_screenshot`·`get_metadata`(클라우드 REST)는 보통 정상 → **읽기는 살아도 쓰기만 죽을 수 있다.**

- **"connection invalidated. The user needs to reconnect it" = 다른 장애** (브리지 불안정이 아니라 **커넥터 OAuth 만료/해지**). 재시도·데스크톱 포커스로 복구 불가 — **사용자가 커넥터 설정에서 Figma를 재연결해야만 풀린다.** 이때 보조 서버 `mcp__Figma__*`(데스크톱, 읽기 전용: get_metadata/get_screenshot/get_design_context)는 살아있을 수 있으니 **커밋 여부 검증과 읽기는 계속 가능**. 쓰기 직전이었다면 검증 후 작업 계획을 로컬 md로 보존하고 사용자에게 재연결을 요청한다.

- **"connection lost" ≠ 실패**: 응답 채널만 끊기고 **실제로는 커밋되는 경우가 많다**. 에러를 곧장 실패로 단정하지 말고 **클라우드로 검증**한다.
- **검증은 `use_figma` 리턴이 아니라 `get_screenshot`(JSON의 `original_height`) / `get_metadata`(자식 구조)** 로. 단 **클라우드 렌더는 지연**될 수 있어 쓰기 직후 스크린샷이 stale일 수 있다 → `get_metadata`와 교차 확인하거나 잠시 후 재확인.
- **작은 호출이 잘 커밋된다**: 큰 빌드는 커밋 전 끊김 → **작은 멱등 배치로 분할**. 각 배치는 **이름으로 존재 확인 후 없을 때만 추가**(`drow-<i>` 등), stray는 배치 시작 시 `findAll(name).remove()`로 정리(부분 커밋 대비 재실행 안전).
- **데스크톱 앱 포그라운드가 브리지를 되살린다**: 대상 파일을 데스크톱 앱에서 열고 **실제로 클릭/포커스**(computer-use `open_application` + 캔버스/툴 클릭)하면 복구되는 경우가 있다. `open_application`만으로는 부족할 때가 있음.
- **형제/연속 배치 순서**: auto-layout append 순서가 꼬이지 않게 **인덱스 오름차순으로, 앞 배치 커밋 확인 후 다음 배치**.

### auto-layout / 텍스트 함정

- **`resize()`가 auto-layout primary축을 FIXED로 강제** → hug가 풀려 프레임이 자식만큼 안 커진다. 자식 추가 후 `primaryAxisSizingMode="AUTO"`를 다시 세팅하거나, 높이를 **자식 높이 합으로 명시 계산**해 컨테이너·푸터를 재배치.
- **`textTruncate` 프로퍼티 없음** → `textAutoResize="NONE"` + 고정폭 + 셀 `clipsContent=true`로 overflow 클립.
- **폰트는 매 `use_figma` 호출마다 `loadFontAsync`** 필요(실행 컨텍스트가 매번 새로 시작). Pretendard 미가용 환경 → Noto Sans KR 치환(SemiBold→Bold, ExtraBold→Black 등), mono는 Roboto Mono.
- **Roboto 한글 fallback 누락(간헐적)**: Roboto 런의 한글이 일부 노드에서만 렌더 안 됨(라틴·숫자만 보이고 한글 글리프 공백). 같은 문자("백업")가 어떤 섹션은 되고 어떤 섹션은 안 되는 노드 단위 글리치 — stale 렌더 아님(`node.screenshot()` 인라인 렌더로도 동일). **해결 = 해당 텍스트 노드 fontName을 `Noto Sans`(한글 확실 렌더)로 교체 후 characters 재설정.** 신규 텍스트 다수 작성 시 본문은 처음부터 Noto Sans로 가는 것도 안전.
- **텍스트 노드 autoRename**: characters를 넣으면 노드 name이 내용으로 자동 변경됨. 클론 후 자식 텍스트를 name으로 찾으면 깨짐 → **위치(자식 인덱스) 기반 접근**으로 num/title/desc 회수.
- **Changelog/본문 텍스트 폭 붕괴**: 가변 텍스트에 `layoutSizingHorizontal='FILL'`만 주면 폭이 0으로 붕괴해 세로로 1글자씩 wrap됨 → `textAutoResize='HEIGHT'` + **명시 폭(`layoutSizingHorizontal='FIXED'` + `resize(w, h)`)**.
- **상세 명세 화면 높이 정합**: Description 프레임이 FIXED 높이면 섹션 추가 시 콘텐츠가 넘침 → 내부 콘텐츠 높이 측정 후 Description·화면(node)·Background+Shadow를 `max(mockup bottom, desc bottom)+여백`으로 resize.
- **높이 정합 검증 레시피(검증된 순서)**: v5 텍스트가 길어지면 페이지 프레임이 콘텐츠를 자르거나(`clipsContent=true`) 흰 카드 밖으로 흘러 보인다. 다음 순서로 해소한다 — ① Description 컬럼 프레임 `primaryAxisSizingMode='AUTO'`(VERTICAL) **+ 그 자식 콘텐츠 프레임 `layoutSizingVertical='HUG'`**(이걸 안 하면 부모가 hug 안 되고 stale 높이가 읽힘), ② 행 컨테이너(좌 목업+우 Description를 담는 HORIZONTAL) `counterAxisSizingMode='AUTO'`, ③ Paper가 VERTICAL hug면 자동 확장, ④ 페이지 프레임이 `layoutMode==='NONE'`(직접 resize)이면 `page.resize(w, paperBottom+여백)`, auto-layout이면 `counterAxisSizingMode='AUTO'`. **주의: AUTO 설정 직후 같은 스크립트에서 읽은 `.height`는 stale일 수 있다** → 시각 검증(`get_screenshot`)으로 확정. 좌 목업 카드가 우 Description보다 짧으면 `Background+Shadow`를 desc 높이에 맞춰 resize해 좌/우 카드 높이를 맞춘다.
- **목 데이터 PII 회피**: 스켈레톤 샘플의 조치자/작성자는 실직원 이메일(`operator@example.com`) 금지 → `운영자A/B/C` 같은 일반 라벨 사용(제출·캡처 워싱 안전).
- **⚠️ Description ↔ 와이어프레임 정합(필수)**: Description(우측 설명)을 변경하면 **좌측 와이어프레임도 같은 모델로 반드시 수정**한다. 한쪽만 바꾸면 스펙=화면 모순 → 개발자가 옛 모델로 구현하거나 clarification 재작업. 와이어프레임이 **컴포넌트 인스턴스**(예 `list-horizon-item`)면 평면 스크린샷이 아니라 **수정 가능** → "참조용"이라며 누락 금지. 인스턴스 내부 텍스트는 `I<instId>;<subId>` 노드에 `characters` override로 수정. 빨강 변경 박스/마커는 실제 바뀐 행에 정렬.
- **미가용 폰트(Pretendard JP Variable 등) → Noto Sans KR 대체**: 기존 인스턴스 텍스트 폰트가 플러그인 미가용이면 `loadFontAsync` 실패("font family does not exist"). `figma.listAvailableFontsAsync()`로 확인 후 `node.fontName={family:'Noto Sans KR',style:'Regular'}` 교체 → characters 설정(한글 안전). Pretendard 미가용 환경 흔함.
- **변경 이력 마커 표기 = `(YYYY.MM.DD vn 변경/삭제/추가)`**: description 내 변경/신규 기록은 이 형식으로 통일(예 `(2026.06.15 v1 추가)`, `(2026.06.15 v1 변경)`). 빨강 글자색 유지, 마커 텍스트만 이 형식. 구버전 색상 수정이력 딱지는 검정 통일 또는 제거(삭제 컬럼 dimmed는 유지). 자세히는 메모리 [[feedback-desc-change-marker-format]].

---

## 이전 버전 표시서식(버전 마커·딱지·콜아웃) 정리 — 파괴적, 안전 절차 필수

"이전 버전 업데이트 표시서식을 지워라" 요청 시. **권위 파일이므로 keep-baseline을 먼저 확인하고, 대상을 정확히 식별한 뒤, 시범(숨김)·스크린샷 검증 후 진행.** 절대 휴리스틱으로 일괄 삭제하지 말 것.

**KEEP(절대 보존):** 현행/최신 항목, **v1·2026 등 현행 버전**, 현행 Changelog 섹션, **목업 위 ①②③ 섹션 번호 마커**(=설명 섹션 연결, 버전 아님), `(삭제)` 의미(삭제 항목은 마커 보존 또는 dimmed 유지), 실제 UI 컴포넌트(`badge`·`tabs`·`btn`·`alert` 등 **의미있는 이름**), 콘텐츠성 블록(예: `table-container` 안의 `version: 3.0.6` 메타).

**정리 대상 3종 + 절차:**
1. **인라인 버전 마커** — 설명 텍스트 안 `(YYYY.MM.DD vN 추가/변경/수정/현행화)`·`(26.x.x …)`. 텍스트 노드에서 **`(...)` 중 "숫자 + 동작어(추가/변경/수정/현행화)"를 모두 포함한 괄호만** regex 제거(내용 보존). `삭제`·`(CONT-09_…)`·`(예: 192.168…)`·`(Prometheus)`는 **보존**. 반드시 **드라이런(읽기 전용)으로 before/after 확인 후** 적용. 폰트는 노드 현재 폰트 로드 후 `characters` 재설정.
2. **목업 위 변경 콜아웃 박스** — **제네릭 이름**(`Rectangle 7299`·`Rectangle 1468`·`Vector` 등) + **stroke 색상(빨강/파랑/보라) 오버레이**만 대상. 제외: 의미있는 컴포넌트 이름, `Frame 633xxx`(changelog), instance-internal id(`I…;…`), ①②③ 마커. **삭제 대신 `visible=false`로 먼저 숨김 → `get_screenshot` 검증(콜아웃만 사라지고 UI·①②③ 정상인지) → 확정**(복원불가라 숨김 우선 권장).
3. **구버전 changelog 딱지** — `Frame 633303/633306/633302/633307/633308`·`26086359`(버전 배지 + 변경사항 행). **주의: 깔끔한 단일 테이블이 아니라 페이지 곳곳(페이지 직속·Description·`table-container`)에 흩어지고 콘텐츠와 엉켜 있는 경우가 많다.** 기계적 "최신만 남기고 삭제"는 콘텐츠/레이아웃 손상 위험 → **자동 삭제 보류, 수동 정리 권장**. 단 **이미 hidden인 stray 구버전 딱지**(v3/v4/v8 배지 등)는 `visible===false` 가드로 안전 삭제 가능.

마커 표기 형식 표준은 [[feedback-desc-change-marker-format]] 참조(현행 `(YYYY.MM.DD vN 변경)` 빨강 유지, 구버전 딱지만 제거/검정 통일).

## Description(상세 명세) "내용" 작성 = figma-desc-spec (SoT)

> Description에 **무엇을 어떻게 쓸지**(섹션 단위 = 와이어프레임 큰 레이아웃 기능 요소, 섹션 본문 구성(UI 요소 → 상태·케이스 → 제약 → 동작 정책, 동작 정책 맨 뒤), 화면 4종 전수 서술, 분기·예외·Validation·동작·안내 4영역, 변경 마커·Changelog 규칙)는 **[figma-desc-spec](../figma-desc-spec/SKILL.md)** 스킬이 SoT다. 작성·검수 전 반드시 그 스킬 + `references/screen-type-checklists.md`를 펼친다.
>
> 이 절은 그 내용을 **Figma 노드에 실제로 그려넣는 렌더 기법(HOW)** 만 다룬다.

### Description 렌더 기법 (🔒 플랫 인코딩 B = 정본)

> **🔧 검증된 헬퍼 코드 = [`assets/desc-render-helpers.js`](assets/desc-render-helpers.js) (붙여넣기용 SoT).** 매 호출마다 재작성하지 말고 이 파일에서 **`setFlat`(정본 B)**·`resizeFixedSection`·`surgicalReplace`·`sampleRed`+`reddenPhrase`를 use_figma `code`에 붙여넣어 쓴다. `setFlat`은 계층·강조를 진짜 글자/공백으로만 표현하고 노드 전체를 NONE/indent0/Noto Sans Regular로 1회 정규화 → `characters=` 덮어써도 무손상. ⚠ 구 `setRich`(네이티브 리스트 A)는 LEGACY(깨짐 위험, 신규 금지).
>
> **🔴 본문 폰트 = fs24 / lineHeight 36 (정본 표준, 호스트 `[node-id]`·미터링 이력 `[node-id]` 실측).** 아래 "상세 명세 페이지 해부"의 "주불릿 fs12·서브 fs11"은 **구 템플릿 값** — 4.0 집계/미터링 본문엔 fs24를 쓴다(fs12로 쓰면 같은 페이지의 다른 섹션과 크기 불일치 → 재작업).
>
> **🔴 완료 기획서 갱신분 = 빨강 글자 (사용자 확정 2026-06-30).** 이미 완료된 기획서를 수정하면 **갱신한 문장만** `setRangeFills`로 빨강(`sampleRed`로 파일 내 기존 빨강 톤 일치, 없으면 `#E21D26`). 인라인 `(YYYY.MM.DD vN)` 날짜 마커는 붙이지 않고 **색상만**(전역 history 페이지 운영 원칙). 신규 기획·전역 history 페이지 본문에는 빨강 적용 안 함(현행만 흑).
>
> **섹션 reflow 분기**: ① `lm=NONE` 고정높이 섹션(04 DataZoom 구조) = `setRich` 후 `resizeFixedSection`(섹션/body/num 높이 = 56+본문h+24)로 직접 resize → 상위 VERTICAL auto-layout이 형제·카드 reflow. ② 전 체인 VERTICAL auto-layout HUG(03 캘린더 구조) = `setRich`만 하면 자동 reflow(resize 불필요).

**계층(와이어프레임 기준):** 최상위 = **섹션 = 페이지 내 큰 레이아웃/기능 요소 단위**(목업 ①②③ 마커 = 이 단위 · 섹션 제목 = 거터 번호 + title-bar 텍스트 노드, 리스트 아님). 섹션 **본문**은 플랫 인코딩 마커로 한 TEXT 노드에 담는다(`setFlat`이 생성):
- **L0 소제목** `■ `(공백0) · **L1** 열거 `1. `/진술 `• `(공백2) · **L2** 열거 `a. `/진술 `• `(공백5) · **L3** `• `(공백8).
- **컴포넌트·분기 = 번호(`1.`/`a.`), 정책·제약·세부 = 글머리 `•`.** 들여쓰기는 U+0020만, 폭 0/2/5/8 고정. `a.`는 그룹마다 리셋. 마커 규약 상세 = [figma-desc-spec](../figma-desc-spec/SKILL.md) + `setFlat` 상수표.
- ⚠ 계층을 진짜 글자/공백으로만 표현하므로 `setRangeListOptions`/`setRangeIndentation`(구 A)는 **쓰지 않는다**(노드 리셋 시 평면화돼 깨지던 원인 제거).

**🔴 폰트 버그(더블클릭해야 보이는 현상) — 반드시 회피:**
- 원인: `node.characters=` 로 덮어쓰면 **첫 글자 스타일이 전체에 적용**된다. 첫 세그먼트가 `Roboto`(라틴 전용·한글 글리프 없음)면 한글이 빈 글리프로 렌더돼 **정적 화면에선 안 보이고, 더블클릭(편집모드 OS 폴백)에서만 보임**.
- 해결: `characters=` **전후로 한글 가능 폰트를 전체 범위에 강제 지정**. 이 파일에서 로드 가능 확인된 폰트 = **`Noto Sans` Regular**(폴백 `Noto Sans KR` Regular). `Roboto`/`Inter`/`Noto Sans CJK KR`/`Pretendard`는 부적합/로드불가.
- 표준 헬퍼(검증됨):
  ```js
  let KF={family:"Noto Sans",style:"Regular"};
  try{await figma.loadFontAsync(KF);}catch(e){KF={family:"Noto Sans KR",style:"Regular"};await figma.loadFontAsync(KF);}
  // setFlat(id, blocks): blocks=[{label?, ol?, items:[{t, ol?, subs?}|"str"]}]  (정본 B)
  // 본문 노드의 기존 세그먼트 폰트 전부 loadFontAsync → n.fontName=KF → n.characters=flatText → n.fontName=KF 재지정
  // 계층은 ■/1./a./• 마커 + 공백(0/2/5/8) 글자로만 표현 (범위 서식 미의존 = 안 깨짐)
  // 노드 전체 1회 setRangeListOptions(NONE)+setRangeIndentation(0)+fs24/lh36 · n.textAutoResize='HEIGHT'
  ```
- 제목 텍스트도 같은 버그 대상 → `fixFont(id)`로 전체 범위 `Noto Sans` 재지정.
- (구 A 전용 주의 — `setRangeIndentation` 스케일 드리프트 — 은 **플랫 B에서 폐기**: 들여쓰기가 실제 공백(0/2/5/8)이라 노드별 스케일 차이·드리프트가 없다.)

**기타 렌더 규칙:**
- 제목 텍스트엔 번호(①) 붙이지 않음 — 번호는 좌측 거터(Frame 17) 셀이 표시. 제목은 컴포넌트명만.
- 본문 노드 `textAutoResize='HEIGHT'` + 섹션 프레임 VERTICAL hug → 작성 후 Description·Paper·페이지 높이 재정합(아래 "auto-layout / 텍스트 함정" 참조).
- **섹션 reflow 레시피(`lm=NONE` 섹션이 VERTICAL auto-layout Description 프레임의 자식일 때 — 4.0 집계 페이지 구조, 2026-06-18 검증):** 섹션 프레임은 고정높이+`clip=true`이고 본문 텍스트만 HUG다 → 본문 재작성 후 **섹션 프레임 높이를 직접 계산해 resize**해야 reflow된다. `섹션h = 본문텍스트.y(=56) + 본문텍스트.height + (표 있으면 16+표h) + pad(~24)`; 같은 값으로 body 프레임도 resize. 그러면 부모 Description 프레임(`pri=AUTO`)이 자동 hug → 나머지 섹션·Appendix가 따라 내려옴. 좌측 목업/표 같은 비텍스트 자식은 본문 아래 `y`를 다시 계산해 배치.
- **숨김 중복 노드 정리:** 구 본문을 `setFlat`으로 재작성하면 옛 stray 줄들이 `visible=false`로 남을 수 있다 → body 프레임에서 `findAll(n=>n.type==='TEXT'&&n.visible===false)`로 제거(단 `NEW` 배지 프레임 내부 텍스트는 제외). 가시 stray 노드는 먼저 `visible=false` 후 같은 패스로 삭제.
- 변경 마커는 본문, 이력은 Changelog 섹션(형식·내용 규칙은 figma-desc-spec).
- **행간 = 폰트 크기 × 1.5 (사용자 확정 2026-06-23)**: 본문·Appendix 텍스트 `lineHeight={value: fontSize*1.5, unit:'PIXELS'}` (예: fs24 → 36px). 고정높이+`clip=true` 프레임은 행간 키운 뒤 잘리므로 **`clipsContent=false` + 본문 높이 재계산 reflow**(위 "섹션 reflow 레시피")로 전체 노출.
- **거터 없는 설명란 = 온점 넘버링 (figma-desc-spec 번호 규칙)**: Intro 등 거터(번호 칼럼) 없는 설명 노드는 리터럴 `1. 2. ` 접두로 시작(플랫 B). 거터 있는 섹션은 거터 셀이 번호 표시 → 제목·본문 넘버링 없음.
- **Appendix Title 바 = `#999999` 배경 + 텍스트 `#212121` (standalone 집계 표준)**: 바(프레임) fill `rgb(153,153,153)`, 텍스트 fill `rgb(33,33,33)`. 텍스트를 #999로 두면 바에 묻히는 사고 주의.
- **미결 사항 블록 = 페이지 맨 아래 (figma-desc-spec 미결 분리 규칙)**: `(미결)`을 섹션 본문에서 제거하고 Appendix 다음(Changelog 앞) 「미결 사항」 블록에 모은다. 기존 토큰(`U-10`/`T-11`/`V-12`/`F-16` 등) 유지, `[OI-N]` 신규 넘버링 금지. 블록도 본문과 동일 reflow 규칙 적용.

**참고 예시 노드**: node-id 단일 목록은 [`references/node-registry.md`](references/node-registry.md) §1-2에서 조회(여기 중복 나열 안 함). ⚠ 알람·미터링 등 **과거 A(네이티브 리스트)로 친 노드는 정본 전환 시 `setFlat`으로 재렌더 대상**. (폰트 버그의 진짜 원인은 수동 접두가 아니라 첫 세그먼트 `Roboto` 폰트 재사용 — `setFlat`은 Noto Sans 강제로 회피하므로 수동 접두 자체는 정상.)

## 외부 SoT 사전 확인 — 필수 (2026-06-18 보강)

> Figma 작업 시작 전 **반드시 다음 3개 외부 SoT를 먼저 확인**한다. 무시하고 작업하면 컴포넌트·정책·상태값 정의가 어긋나 정합성 깨짐.

| SoT | 위치 | 사용 시점 |
|---|---|---|
| **디자인 시스템** | `references/design-system.md` + Confluence space `[fileKey-removed]` + Figma DS 라이브러리 (`[fileKey-removed]`, `[fileKey-removed]`) | 컴포넌트 재사용 결정 시 (손그림 금지) |
| **공통 정책** | Confluence `[wiki-url-removed]` (space `[fileKey-removed]`) | 권한·통보·검색 동작 등 도메인 횡단 정책 결정 시 |
| **상태값 정의 시트** | SharePoint xlsx `https://okekr-my.sharepoint.com/:x:/g/personal/is_park_okekr_onmicrosoft_com/IQAv4A7OK5NJQZS30__vGXPpAXmjmX2dCzh0vZGPbosmFKA?e=rPKWVQ&nav=MTVfe0IwQTM2NzZDLTNGOUQtNEUwRi04QTgxLUExQ0I0NUZGMEU4MH0` | 자원 상태값 라벨·색상·전이 정의 시 |
| **IA 노드 매핑 (Screen ID)** | [internal-path-removed]`[internal-path-removed]` (**최신**, L열 `로드맵 노드경로`) · 알람 등 node-id 표 = [`node-registry.md` §0](references/node-registry.md) | Figma 반영·rename·Intake Gate **1차 SoT** — node-id 여기서 먼저 조회 (아래 절) |

세부 워크플로 + 충돌 처리 룰: **`references/external-sot.md`** 참조.

### 외부 SoT 위반 처리
- 화면이 외부 SoT와 충돌 → 화면 변경 (SoT 우선)
- SoT 자체가 어긋남 → 사용자에게 보고 후 결정 (임의 판단 금지)
- 회의록에 SoT와 다른 결정 → SoT 갱신 책임자에게 요청 후 SoT 갱신 → 화면 반영

## Figma 프레임 ↔ IA Screen ID rename (매핑 xlsx 기준, 사용자 확정 2026-06-19)

"figma 페이지(프레임) 이름을 Screen ID로 rename" 요청 시. **IA 노드 매핑 xlsx가 SoT** — 임의로 Screen ID를 추측하지 말 것.

- **매핑 소스**: 위 외부 SoT 표의 `figma 노드 매핑용_[4.0.0] … 메뉴IA구조도_vN.xlsx`.
  - 시트 **`1. 메뉴구조도`** 사용. 헤더는 5행: 컬럼 = `시스템명 | LEVEL 1 | LEVEL 2 | LEVEL 3 | 화면ID | 화면명 | 관리자 | 운영자 | 사용자 | 로드맵 노드경로`.
  - **`화면ID`**(예 `CONT-07_05_01`)가 rename 대상 값. `로드맵 노드경로`에 Figma URL이 있으면 노드 검증에 사용.
  - 읽기: `openpyxl.load_workbook(path, data_only=True)` → `ws['1. 메뉴구조도']`, 키워드 행 필터(메뉴명/노드id)로 대상 추출.
- **규칙**: 프레임 `node.name = 화면ID` (Screen ID **단독**, 화면명 미포함 — 참고 노드 `[node-id]` = `"CONT-09_12_01"` 컨벤션). 표지/요약 등 화면 아닌 프레임은 제외.
- **인페이지 헤더 Screen ID 정합 필수**: 헤더행의 `Screen ID` 값 텍스트도 같은 화면ID로 갱신(구 `CON-006` 등 잔존값 제거). 안 하면 프레임명과 헤더가 불일치.
- **검증**: rename 후 `node.name`·헤더 텍스트가 xlsx `화면ID`와 일치하는지 대조. 같은 Screen ID 중복 프레임(현행/마스터/구버전) 주의 — 헤더로 대상 확정 후 진행.
- 확정 매핑(2026-06-19, 모니터링): `CONT-07_04_01`=미터링 이력 · `CONT-07_04_02`=미터링 집계 · `CONT-07_05_01`=집계 호스트(`[node-id]`) · `CONT-07_05_02`=집계 인스턴스(`[node-id]`) · `CONT-07_05_03`=캘린더 동작 정책(`[node-id]`).

## MCP/Figma Tool Rules

- `CallMcpTool` 호출 전, 해당 MCP tool schema를 먼저 읽는다.
- `use_figma` 호출 시 `skillNames`에 `figma-use`를 포함한다.
- 멀티페이지 또는 다중 노드 반영은 노드 단위로 분리해 안전하게 적용한다.

## Response Style

- 진행 중에는 짧은 상태 업데이트를 제공한다.
- 완료 시에는 노드 기준으로 무엇이 바뀌었는지 명확히 보고한다.
- 사용자 추가 요청이 있으면 같은 흐름으로 반복 수행한다.

