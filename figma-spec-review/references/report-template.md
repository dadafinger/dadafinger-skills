# Figma Spec Review — 리포트 템플릿

## 노드별 블록 (루프 단위 · 서브에이전트 반환값)

```markdown
## {Screen ID} · {node-id} — 검수 결과
- 파일: {fileKey}
- 헤더 확인: Screen ID={…} / Page Title={…} / Author={…}  (현행본 확인 ✓ / 의심 ⚠)
- 읽기 방식: metadata+screenshot+characters (또는 "시각 판독만" 등 한계 명기)
- 기준 세대: 4.0.0 (전역 history 운영)
- 외부 SoT 확인: 용어집={확인/미확인} · 상태값={확인/미확인}

SCORE: FAIL {n} · WARN {n} · PASS {n} · N/A {n}   →   verdict={FAIL|WARN|PASS}

| # | 기준 | 점검ID | 등급 | 근거 (인용 / 노드) | 권고 조치 |
|---|---|---|---|---|---|
| 1 | ③ Description | D1 | FAIL | 목업 마커 4개 vs 섹션 3개 (node [node-id]) | 누락 섹션 1개 보강 |
| 2 | ② 용어 | T2 | FAIL | "2단계 심각도" 잔존: "…" (node …) | Severity 토큰 3단계 표기로 |
| 3 | ① 포맷 | F9 | WARN | Intro에 `v1.0` 버전 라인 (node …) | 전역 history 운영 → 제거 |
| … | | | | | |

### 미점검 / SoT 미확인
- (없으면 "없음")
```

> **verdict 규칙**: FAIL ≥ 1 → `FAIL` · 아니고 WARN ≥ 1 → `WARN` · 그 외 `PASS`.
> 권고 조치는 한 줄로만. 실제 수정은 figma-change-flow / figma-desc-spec에 위임(이 스킬은 안 고침).

## 종합 리포트 (다건 루프 합본)

```markdown
# Figma Spec Review — 종합 리포트
- 검수일: {YYYY-MM-DD}
- 파일: {fileKey}
- 대상: {n}개 노드
- 집계: FAIL {x}건 · WARN {y}건 · PASS {z}건

## 우선 조치 (FAIL 노드부터)
| 노드 | Screen ID | verdict | FAIL 요지 |
|---|---|---|---|
| … | … | FAIL | … |

## 노드별 상세
(위 노드별 블록을 verdict FAIL→WARN→PASS 순으로 나열)

## 반복 패턴 (여러 노드 공통 위반)
- 예: "전 노드에 Severity 옛 표기" → 용어 일괄 치환 1건으로 묶음.
```

> 종합 시 **반복 패턴**을 묶어 figma-change-flow 반영 단위(일괄 작업)로 변환하면 수정 왕복이 준다.
</content>
