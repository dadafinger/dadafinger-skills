> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: html-spec-review
description: Product HTML 번들 프로토타입(__bundler/manifest 안 gzip+base64 babel JSX)과 그 MD 기획서가 서로 맞는지 정합 검수하고, 정해진 차이만 정본(라이브 html)에 안전 패치한다. 1단계는 읽기전용 트리아지(번들 디코드 → MD 주장 vs 실제 빌드 1:1 대조 → 일치표+불일치N건+포크/구버전 footgun 점검 → 어느 쪽이 정답인지 결정 요청), 2단계는 사용자가 정답을 정한 것만 외과적 패치(백업→에셋만 재인코딩→babel+라운드트립 검증)하고 MD도 동기화. "html대로 md 됐는지", "프로토타입이랑 기획서 맞는지", "html ↔ md 정합", "번들/프로토 검수", "기획서랑 화면 차이", "라이브 html 고쳐줘", "최신본 맞는지 봐줘", "html spec review"가 트리거. 막 돌려서 난장판이 된 알람/집계/미터링 프로토타입을 기획자가 최소 노력으로 검수·정본화할 때 꼭 쓴다. Figma 노드 검수는 figma-spec-review, 이건 html 번들 ↔ md.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: html↔md 정합; 사내 번들·프로토 경로

# HTML Spec Review (번들 ↔ 기획서 정합 검수 + 안전 패치)

Product HTML **번들 프로토타입**(Figma Make류 툴 생성, `__bundler/manifest` 안에 gzip+base64로 박힌 babel JSX가 진짜 화면)과 그 **MD 기획서**가 일치하는지 검수하고, **확정된 차이만** 정본 html에 안전하게 반영한다.

> **왜 이 스킬이 필요한가** — 프로토타입을 AI로 막 돌리다 보면 같은 화면이 여러 파일로 갈라지고(포크), 빌드 스크립트가 구버전을 가리키고, MD 본문과 빌드가 슬그머니 어긋난다. 손으로 검수하려면 번들을 디코드하고 babel로 검증하고… 너무 귀찮아 결국 안 본다. 그 반복 작업을 `scripts/bundle_tool.py`로 박제하고, **검수는 5분 트리아지로, 수정은 정답 정한 것만**으로 쪼개 심리적 장벽을 없앤다.

## 역할 분담

| 스킬 | 대상 / 역할 |
|---|---|
| **html-spec-review (이 스킬)** | **html 번들 ↔ md** 정합 검수(READ) + 정본 html 안전 패치(WRITE). |
| figma-spec-review | **Figma 노드 ↔ 룰** 검수(READ 전용). 대상이 다름(번들 아님). |
| planning-html | 번들 **생성·렌더 기법**(공통템플릿 디자인 DNA). 이 스킬은 그 산출물을 검수/수정. |
| critique-reviewer | 화면 외 **전략·정책 공백** 비판(상위). |

**번들 내부 구조·재패킹·함정의 SoT는 메모리 [[reference_alarm-html-prototype-pipeline]]** — manifest 구조, JSX 중괄호 함정(`>{토큰}<` → ReferenceError), repack 인덱스 매칭, NFC/NFD 파일명 주의 등. 검수/패치 전 그 메모리를 펼쳐 맥락을 잡는다.

## 언제 쓰나

트리거: `html대로 md 됐는지`, `프로토타입이랑 기획서 맞아?`, `html ↔ md 정합`, `번들 검수`, `프로토 검수`, `기획서랑 화면 차이`, `라이브 html 고쳐줘`, `최신본 맞는지`, `/html-spec-review`.

쓰지 말 것:
- Figma 노드 포맷/Description 검수 → figma-spec-review.
- 번들을 **새로 생성/렌더** → planning-html / figma-change-flow.
- 매뉴얼 docx·이미지 검수 → kr-manual-format-review / manual-image-review.

## Intake Gate (시작 전 필수)

1. **대상 화면 확정** — 어떤 화면(예: 알람 생성)의 ① 라이브 html 경로 ② 대응 MD 기획서 경로. 모르면 묻는다(`html/md 경로 모르면 매번 물어봐주세요`). 라이브 html은 보통 [internal-path-removed]`…/4.0/<도메인>/html/v7/…`.
2. **"라이브 = 정본" 원칙** — 기획자는 파일 여러 벌이 아니라 **실제 배포되는 라이브 html 한 벌**만 본다. 작업폴더(`.alarm_v*_work/jsx_*`, `*_DEPLOYED.jsx` 등)는 포크/구버전일 수 있으니 **정본으로 단정하지 말 것**. 정본은 항상 라이브 html에서 디코드한 내용.
3. **검수 세대 확인** — v7/v7.1 등 최신만. 구버전 비교 시 사용자가 명시.

## 1단계 · 읽기전용 트리아지 (검수만, 쓰기 없음)

### A. 번들에서 진짜 화면 코드 꺼내기
```bash
python3 scripts/bundle_tool.py list   "<live.html>"                       # 앱 JSX 에셋 후보 확인
python3 scripts/bundle_tool.py decode "<live.html>" --match "function EditApp" --out /tmp/live.jsx
```
`--match`는 화면 진입 함수(`function EditApp`/`ListApp` 등)나 고유 문자열로 **정확히 1개** 에셋을 특정한다. (라이브러리 에셋은 자동 제외.)

### B. MD 주장 ↔ 빌드 1:1 대조
MD의 **변경 이력 항목**과 **섹션별 명세**를 하나씩 빌드(디코드한 JSX)에서 확인한다 — "반영 완료" 같은 자기선언을 믿지 말고 코드에서 직접 찾는다.
- 변경분 N개 → 각 항목이 빌드에 실제로 있는가(상태 토글·유효성·숨김 조건·라벨·문구).
- 섹션별: UI 요소·상태/케이스·제약(유효성)·동작정책 문구가 빌드 문자열과 일치하는가.
- **근거 인용 필수**(추측 금지): 어긋난 건 빌드의 실제 문자열/라인을 따온다.

### C. footgun 점검 (난장판의 실체)
- **포크 점검** — 라이브 html에서 디코드한 내용 ≠ 작업폴더 `*_DEPLOYED.jsx`/`jsx_*`이면 갈라진 것. `diff`로 실차이를 뽑아 **어느 쪽이 MD·과거 피드백과 맞는지**로 정본을 가린다(둘 다 일부만 맞을 수 있음).
- **재패킹 배선 점검** — `do_repack.py`/`repack.py`의 `override_safe`·파일명이 **구버전 에셋**(예: `jsx_*_v6_2`)을 가리키면, 무심코 실행 시 라이브가 퇴행한다. 발견 시 경고하고 **함부로 repack 실행 금지**.

### D. 트리아지 리포트 산출
`references/triage-report-template.md` 포맷. 머리에 한 줄 판정(일치 M/M · 불일치 N), 일치표 + 불일치표(각 항목에 **어느 쪽이 정답일지 추정 + 결정 요청**). 사용자는 accept/reject만 하면 되도록.

> 🔴 1단계에서 **고치지 않는다.** 차이를 보여주고 정답을 받는다. 검수와 수정을 섞으면 그게 바로 귀찮음의 원인.

## 2단계 · 안전 패치 (정답 정한 것만)

사용자가 항목별 정답(MD를 빌드에 맞출지, 빌드를 MD에 맞출지)을 정하면 반영한다.

### 방향 규칙
- 빌드가 정답 → **MD를 수정**(Edit 툴).
- MD가 정답 → **정본 html을 패치**(아래 도구) + MD도 필요 시 정정.
- 둘 다 틀림(예: 잘못된 안내문구) → **양쪽 다** 올바른 값으로.

### html 패치 = bundle_tool.py patch (백업·검증 내장)
`patches.json`을 만들고 도구에 넘긴다. 도구가 **백업 → 치환/삽입 → babel 문법검증 → 라운드트립(재디코드==기대값) → 쓰기**를 한 번에, 실패하면 쓰지 않는다.
```json
{
  "match": "function EditApp",
  "replacements": [["Action 설정과 수신자별 심각도", "Action 설정과 그룹별 심각도"]],
  "insertions": [["  )}\n  </div>\n</div>", "  )}\n  </div>\n  <NEW_BANNER/>\n</div>"]],
  "assert_present": ["그룹별 심각도"],
  "assert_absent":  ["수신자별 심각도"]
}
```
```bash
python3 scripts/bundle_tool.py patch "<live.html>" --spec /tmp/patches.json
```
- **각 `old`/`anchor`는 에셋 내 정확히 1회만** 매칭돼야 통과(모호하면 중단) → 안전.
- 삽입은 anchor를 그대로 포함시켜 위치를 박는다(JSX 형제 노드로, 균형 맞게).
- 패치 후 `verify`로 한 번 더 확인 가능. 백업은 `<live.html>.bak_타임스탬프`.

### 🔴 JSX 중괄호 함정 (메모리 SoT 재확인)
JSX 텍스트 노드에 리터럴 중괄호 토큰을 넣을 땐 `>{"{Severity1}"}<`(표현식 안 문자열). `>{Severity1}<`는 변수로 해석돼 `ReferenceError`로 화면이 깨진다. 따옴표 문자열 안(`"FATAL"`→`"{Severity1}"`)은 안전. → babel 검증이 1차로 잡지만 런타임 ReferenceError는 못 잡으니 토큰 삽입 시 특히 주의.

### MD 동기화
빌드를 정본으로 확정한 항목은 MD 본문·변경이력·모드정책 등 **모든 관련 위치**를 함께 고친다(한 군데만 고치면 다음에 또 어긋남). 라이브와 MD가 같은 사실을 말하게 만드는 게 목표.

## 마무리

- 라이브 html은 **하나의 정본**으로 수렴됐는가. 포크/구버전은 정본과 동기화하거나 폐기 권고.
- 재패킹 배선이 구버전을 가리키면 정리 권고(미정리 시 재빌드 회귀 위험을 명시).
- 패치한 화면은 babel+라운드트립 통과를 보고에 명시. 시각 렌더 확인이 필요하면 헤드리스 캡처(메모리 절차).
- 새로 알게 된 포크/footgun/정본 결정은 [[reference_alarm-html-prototype-pipeline]] 메모리에 한 줄 기록.

## 참고 파일
- `scripts/bundle_tool.py` — 번들 list/decode/verify/patch (백업·babel·라운드트립 내장).
- `references/triage-report-template.md` — 트리아지 리포트 포맷.

## 관련 메모리
- [[reference_alarm-html-prototype-pipeline]](번들 내부·재패킹·함정 SoT) · [[reference_alarm-html-prototype-pipeline]]의 v7 정본/footgun 기록 · [[feedback-prototype-mock-values]](목업값 단정 금지) · [[feedback-condition-type-not-ux]](조건유형 비강조) · [[project_alarm-figma-spec-pages]] · [[project_alarm-terminology]].
