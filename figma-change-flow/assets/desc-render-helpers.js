// =============================================================================
// desc-render-helpers.js — CONTRABASS 상세 명세 Description 렌더 검증 헬퍼 (SoT)
// =============================================================================
// 목적: 매 use_figma 호출마다 30줄 헬퍼를 재작성하던 왕복을 없앤다.
//       (FIGMA_BOTTLENECK_TRACKER Tier2 F1~F6 "write-helper 코드화" = 1순위)
//
// 사용법: use_figma `code`에 필요한 함수를 통째로 붙여넣고 호출한다.
//   - use_figma는 코드를 async로 감싸므로 top-level await/return 그대로 사용.
//   - 컨텍스트가 매 호출 초기화되므로 폰트 로드 블록을 매번 포함할 것.
//   - skillNames에 "figma-use"(리소스면 "resource:figma-use") 포함.
//
// 표준 (호스트 2112:57627 · 미터링 이력 2040:14706 실측 = 정본):
//   - 본문 폰트 = fs24 / lineHeight 36 (fs×1.5).  ⚠ figma-change-flow 해부의
//     "주불릿 fs12·서브 fs11"은 구 템플릿 값 — 4.0 집계/미터링 본문엔 fs24.
//   - 폰트 = Noto Sans Regular(라벨 Bold). Roboto/Inter는 한글 미렌더 → "더블클릭
//     해야 보이는" 버그(F1). characters= 전후로 Noto Sans 전체 강제 지정으로 회피.
//   - 네이티브 리스트 3-depth: depth0=블록 라벨(정책/상태·케이스/제약/동작 정책,
//     NONE·Bold) · depth1=항목(다건 ORDERED→1. / 단건 UNORDERED→•) · depth2=세부.
//   - 「UI 요소」 블록은 라벨 없이 depth1 넘버링부터 시작(label:null).
//   - setRangeListOptions 먼저 → setRangeIndentation 나중 (반대면 깨짐, F5).
//   - 본문 = textAutoResize='HEIGHT' + 고정폭 (폭 0 붕괴 회피, F4).
// =============================================================================

// ── 폰트 셋업 (매 호출 포함) ────────────────────────────────────────────────
let KF = { family: "Noto Sans", style: "Regular" };
try { await figma.loadFontAsync(KF); }
catch (e) { KF = { family: "Noto Sans KR", style: "Regular" }; await figma.loadFontAsync(KF); }
let KB = { family: KF.family, style: "Bold" };
try { await figma.loadFontAsync(KB); } catch (e) { KB = KF; }

// 기존 노드 세그먼트 폰트 전부 로드(덮어쓰기 전 필수, F2)
async function loadExisting(n) {
  for (const sg of n.getStyledTextSegments(['fontName'])) {
    try { await figma.loadFontAsync(sg.fontName); } catch (e) {}
  }
}

// ── setRich: 블록 모델 → 네이티브 3-depth 리스트로 본문 텍스트 노드 재작성 ──
// blocks: [{ label: string|null, items: [ { t: string, subs?: string[] } | "문자열" ] }]
//   - label=null  → 「UI 요소」 블록(라벨 줄 없이 depth1부터)
//   - items 다건 → ORDERED(1.2.3), 단건 → UNORDERED(•) / subs도 동일 규칙
// 반환: 재작성 후 노드 height (섹션 reflow 계산용)
async function setRich(id, blocks, opts) {
  const FS = (opts && opts.fs) || 24;
  const LH = (opts && opts.lh) || 36;
  const n = await figma.getNodeByIdAsync(id);
  await loadExisting(n);
  const lines = [];
  for (const b of blocks) {
    if (b.label != null) lines.push({ t: b.label, d: 0, o: false });
    const arr = b.items.map(it => typeof it === 'string' ? { t: it } : it);
    const ic = arr.length;
    for (const it of arr) {
      lines.push({ t: it.t, d: 1, o: ic > 1 });
      for (const s of (it.subs || [])) lines.push({ t: s, d: 2, o: it.subs.length > 1 });
    }
  }
  const text = lines.map(l => l.t).join('\n');
  n.fontName = KF; n.characters = text; n.fontName = KF;  // F1: 한글 폰트 강제 전후
  n.textAutoResize = 'HEIGHT';                            // F4
  let pos = 0;
  for (const l of lines) {
    const s = pos, e = pos + l.t.length;
    n.setRangeListOptions(s, e, { type: l.d === 0 ? 'NONE' : (l.o ? 'ORDERED' : 'UNORDERED') }); // 먼저
    n.setRangeIndentation(s, e, l.d);                                                            // 나중 (F5)
    n.setRangeFontSize(s, e, FS);
    n.setRangeLineHeight(s, e, { unit: 'PIXELS', value: LH });
    n.setRangeFontName(s, e, l.d === 0 ? KB : KF);
    pos = e + 1; // skip '\n'
  }
  return n.height;
}

// ── resizeFixedSection: lm=NONE 고정높이 섹션 reflow (04 DataZoom 구조) ──────
// 섹션 프레임은 고정높이+본문 텍스트만 HUG → 본문 재작성 후 섹션/body/num 높이를
// 직접 계산해 resize. 상위가 VERTICAL auto-layout이면 형제·카드가 자동 reflow.
//   섹션h = 본문텍스트.y(보통 56) + 본문h + botPad(~24)
// ※ 03 캘린더처럼 전 체인이 VERTICAL auto-layout HUG면 이 함수 불필요(setRich만).
async function resizeFixedSection(secId, bodyId, numId, bodyTextH, opts) {
  const topY = (opts && opts.topY) != null ? opts.topY : 56;
  const botPad = (opts && opts.botPad) != null ? opts.botPad : 24;
  const nh = Math.round(topY + bodyTextH + botPad);
  for (const id of [secId, bodyId, numId].filter(Boolean)) {
    const f = await figma.getNodeByIdAsync(id);
    f.resize(f.width, nh);
  }
  return nh;
}

// ── surgicalReplace: 큰 리스트 노드 안에서 한 문구만 서식 보존 치환 ──────────
// characters= 전체 재설정은 서식을 날리므로 delete+insert(스타일 BEFORE 상속) 사용.
// 동일 정의=동일 문구 원칙(여러 화면에 같은 문장 전파)에 사용.
async function surgicalReplace(id, oldStr, newStr) {
  const n = await figma.getNodeByIdAsync(id);
  await loadExisting(n);
  const i = n.characters.indexOf(oldStr);
  if (i < 0) return { id, notfound: true };
  n.deleteCharacters(i, i + oldStr.length);
  n.insertCharacters(i, newStr, 'BEFORE');
  return { id, i, ok: n.characters.indexOf(newStr) >= 0 };
}

// ── 빨강 변경 강조: "이미 완료된 기획서"의 갱신분만 빨강 글자 ────────────────
// (사용자 확정 2026-06-30) 완료 기획서를 수정하면 갱신 문장을 빨강으로 강조.
//   ⚠ 신규 기획 + 전역 history 페이지 운영 중인 페이지에는 적용하지 않음(현행만 흑).
//   인라인 (YYYY.MM.DD vN) 날짜 마커는 붙이지 않고 색상만(전역 history 원칙).
const SPEC_RED = { r: 0.886, g: 0.114, b: 0.149 }; // ~#E21D26 (파일 내 기존 빨강 없을 때 fallback)

// 파일 내 기존 빨강을 샘플링(톤 일치). 없으면 SPEC_RED 반환.
async function sampleRed(rootId) {
  figma.skipInvisibleInstanceChildren = true;
  const root = await figma.getNodeByIdAsync(rootId);
  for (const t of root.findAllWithCriteria({ types: ['TEXT'] })) {
    let segs; try { segs = t.getStyledTextSegments(['fills']); } catch (e) { continue; }
    for (const s of segs) {
      const f = (s.fills || [])[0];
      if (f && f.type === 'SOLID' && f.color && f.color.r > 0.6 && f.color.g < 0.35 && f.color.b < 0.35)
        return { r: f.color.r, g: f.color.g, b: f.color.b };
    }
  }
  return SPEC_RED;
}

// 특정 문구 범위만 빨강 fill (텍스트 변형 아님 → 폰트 로드 불필요).
async function reddenPhrase(id, phrase, red) {
  const n = await figma.getNodeByIdAsync(id);
  const i = n.characters.indexOf(phrase);
  if (i < 0) return { id, notfound: true };
  n.setRangeFills(i, i + phrase.length, [{ type: 'SOLID', color: red || SPEC_RED }]);
  return { id, i, applied: true };
}

// =============================================================================
// 사용 예시 (집계 보고서 4.0, 2026-06-30 검증)
// -----------------------------------------------------------------------------
// // (A) lm=NONE 고정높이 섹션 (04 DataZoom): setRich → resize
// const h = await setRich('3413:27603', [
//   { label: null, items: [
//     { t: "모달 헤더 — 「차트 확대」 타이틀 + 대상 지표(그룹 > 세부 지표) + [✕ 닫기]" },
//     { t: "조회 조건 표기 — STEP · 수집 기간 상단 읽기 전용 (본 화면 ③ 조회 조건 상속)" } ] },
//   { label: "제약", items: ["조회 조건은 모달에서 변경 불가 — 닫고 본 화면에서 재조회"] },
//   { label: "동작 정책", items: ["[확대] 클릭 시 풀스크린 오버레이로 진입 · 단일 지표 전용"] },
// ]);
// await resizeFixedSection('3413:27597', '3413:27600', '3413:27598', h);
//
// // (B) VERTICAL auto-layout HUG 섹션 (03 캘린더): setRich만 (자동 reflow)
// const subs = ["일자 단위 선택 · 시간 선택 UI 없음 · 수집 시작 00시 / 종료 23시 자동 고정"];
// await setRich('2142:21753', [
//   { label: null, items: ["RangePicker — 시작 요일 일요일(Sun)"] },
//   { label: "Step별 캘린더 정의", items: [
//     { t: "hourly/daily — YYYY-MM-DD ~ YYYY-MM-DD 형식", subs } ] },
//   { label: "동작 정책", items: ["기간 선택 완료 시에만 [조회] 활성"] },
// ]);
//
// // (C) 동일 문구 전파: 정본 문장을 여러 화면에 동일하게
// const NEW = "역순 선택(종료일을 시작일보다 빠르게 클릭) 시 클릭한 일자를 시작일로 갱신 · 동일 일자 선택 시 1일 기간으로 처리";
// await surgicalReplace('3380:101850', "종료일이 시작일보다 빠른 잘못된 순서일 경우 해당 셀 비활성", NEW);
//
// // (D) 완료 기획서 갱신분 빨강
// const RED = await sampleRed('2040:17468');
// await reddenPhrase('2142:21753', NEW, RED);
//
// // 모든 use_figma는 영향 노드 id를 return 으로 회수할 것.
// =============================================================================
