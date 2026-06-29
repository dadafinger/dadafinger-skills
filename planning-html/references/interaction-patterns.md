# 인터랙션 패턴 — planning-html 참조 문서

> `planning-html` SKILL.md(절차 5 = 인터랙티브본 산출)가 참조하는 **동작 부착 SoT**. 정적 공통템플릿 HTML(절차 4)에 vanilla JS로 표준 상호작용을 붙여 형제 인터랙티브본을 만드는 스니펫·규약. SKILL.md가 진입점, 이 파일은 디테일. 정적본 렌더 메커니즘은 `render-detail.md`.

## 원칙
- **CSS/토큰 보존** — 정적본의 tokens/base를 그대로. 동작용 클래스(`.hidden`·`.err`·`.on`·`.show`)만 추가, 색/폰트/그림자는 토큰 변수.
- **단일 `state` 객체** — 화면 상태 1곳. 모든 렌더는 state→DOM 단방향.
- **이벤트 위임** — `document.addEventListener("click"/"change"/"input")` 한 곳에서 `closest()`로 분기(동적 노드 안전).
- **standalone** — `<script>` 인라인, 외부 런타임 0. 더블클릭 동작. 1파일.
- **목업값 단정 금지** — 외부 연동값(채널명 등)은 예시일 뿐 "설정에 따름"으로 일반화([[feedback-prototype-mock-values]]).

## 마크업 훅 규약 (data-속성)
| 훅 | 의미 |
|---|---|
| `data-panel="N"` | step N 패널(show/hide 대상) |
| `data-step-goto="N"` | stepper 직접 이동 |
| `data-act="next\|prev\|save\|cancel\|addX"` | 액션 버튼 |
| `data-seg="key"` + `button[data-val]` | 세그먼트 그룹·값 |
| `data-toggle` | `.tg` 토글 |
| `data-multi-only` | 특정 상태에서만 보이는 영역 |
| `data-chip-del="idx"` | 칩 삭제 |
| `.err` / `.err-msg.show` | 유효성 표시 |

## 표준 스니펫

### 1. 세그먼트(.seg) 단일 선택 + 분기
```js
var segBtn = t.closest(".seg button");
if (segBtn){
  var seg = segBtn.closest(".seg");
  seg.querySelectorAll("button").forEach(b=>b.classList.remove("on"));
  segBtn.classList.add("on");
  state[seg.dataset.seg] = segBtn.dataset.val;
  applyVisibility(); renderSummary(); return;
}
```

### 2. 토글(.tg)
```js
var tg = t.closest("[data-toggle]");
if (tg){ state.enabled=!state.enabled; tg.classList.toggle("on", state.enabled); return; }
```

### 3. Stepper / 패널
```js
function goStep(n){ state.step=n; applyVisibility(); renderSummary(); window.scrollTo({top:0,behavior:"smooth"}); }
function applyVisibility(){
  document.querySelectorAll("[data-panel]").forEach(p=>p.classList.toggle("hidden", p.dataset.panel!==String(state.step)));
  document.querySelectorAll(".stepper .step").forEach(s=>{
    var i=Number(s.dataset.stepGoto);
    s.classList.toggle("on", i===state.step); s.classList.toggle("done", i<state.step);
  });
  document.querySelectorAll('[data-act="prev"]').forEach(b=>b.disabled=state.step===1);
  document.querySelectorAll('[data-act="next"]').forEach(b=>b.classList.toggle("hidden", state.step===LAST));
  document.querySelectorAll('[data-act="save"]').forEach(b=>b.classList.toggle("hidden", state.step!==LAST));
}
```

### 4. 동적 리스트(조건/칩) 렌더 + 추가/삭제
- state 배열에서 매번 `innerHTML` 재구성. 최소(예: ≥1)·최대(예: ≤5) 가드.
- 삭제 가능 여부는 `arr.length>최소`로 버튼 노출 토글.

### 5. 유효성
```js
function validate(silent){
  var ok=true;
  function mark(id,errId,bad){ if(!silent){ q(id).classList.toggle("err",bad); q(errId).classList.toggle("show",bad);} if(bad)ok=false; }
  mark("ruleName","err-ruleName", !q("ruleName").value.trim());
  // 도메인 규칙: 복합 룰 조건 ≥2 등
  return ok;
}
```
- `next`/`save`에서 `validate(false)` 통과 실패 시 이동·저장 차단 + 토스트.

### 6. 라이브 요약
- `input`/`change`/세그먼트/리스트 변경마다 `renderSummary()` 호출 → 요약 `.sum` 셀에 state 반영.

## 체크리스트 (산출 전)
- [ ] `<script>` 인라인, 외부 런타임 의존 0 (폰트 CDN만 허용)
- [ ] 정적본 `.area-no` 수 = 프로토 `.area-no` 수 (영역 구조 보존)
- [ ] 모든 인터랙티브 컴포넌트가 실제 동작(클릭/입력 반영)
- [ ] 유효성 규칙이 단계 이동·저장을 실제 차단
- [ ] 목업값을 확정 사실로 단정하지 않음
- [ ] 정적본 미덮어쓰기(형제 파일 신규)

## 관련
- 정적본 렌더(절차 4): `render-detail.md`(같은 스킬).
- 다음 단계 Figma: **planning-figma** — **정적본만** 변환(인터랙티브본 제외).
- 메모리: *HTML 단일 파일 기본*, *프로토타입 목업값 임의단정 금지*.
