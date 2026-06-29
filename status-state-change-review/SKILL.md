> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: status-state-change-review
description: Review proposed status value additions/changes for Storage > Shared File > Access Rules using the maintained baseline and OpenStack canonical states. Use when the user asks to validate status names, colors (especially orange), mappings, or wording such as 상태값 변경, 상태 정의 검토, 색상 검토, 액세스 규칙 상태.
disable-model-invocation: true
---

> Sharing scope: Internal
> Share policy: caution
> Notes: Storage 액세스 규칙 상태; 사내 제품 도메인

# Status State Change Review

## Goal

검토 요청된 상태값 변경안이 기존 기준선과 OpenStack 공식 정의에 맞는지 판단하고, 수정 권고안을 제시한다.

## Canonical References

1. 단일 기준/이력 파일(항상 먼저 확인):
   - `agent-shared/references/storage-share-access-rule-policy-history.md`
2. OpenStack 공식 문서:
   - `https://docs.openstack.org/api-ref/shared-file-system/#describe-share-access-rule`
   - 기준 섹션: `Response parameters > state`
   - 운영 원칙: 이 URL을 기본 참조로 고정하며, 사용자가 매번 재전달하지 않아도 된다.

## Workflow

1. 단일 기준/이력 파일에서 상태값/색상/라벨/이력을 읽는다.
2. 사용자 제안안(문서/표/이미지)에서 상태 목록을 추출한다.
3. 아래 항목을 순서대로 검토한다:
   - **값 정합성**: canonical 상태값과 1:1 대응되는가
   - **표기 정확성**: 오탈자(`QUEUED_*`)가 없는가
   - **색상 의미 일관성**: Red/Orange/Blue/Green 의미가 일치하는가
   - **한글 라벨 적합성**: 대기/진행/실패/완료 의미가 혼동 없는가
   - **국문화 근거 부합성**: `DENYING`/`QUEUED_TO_DENY` 용어가 선택 기준(거부 vs 삭제)과 맞는가
   - **쌍 일관성**: `QUEUED_TO_DENY`와 `DENYING` 라벨이 동일 계열(삭제/거부)로 맞춰졌는가
4. 판정 결과를 `적합`, `조건부 적합`, `수정 필요`로 분류한다.
5. 최종 답변에 즉시 적용 가능한 수정안을 포함한다.
6. 정책 변경이 확정되면 단일 기준/이력 파일에 아래를 반드시 추가한다:
   - `최종 추가 작성일` 갱신
   - 근거 확인 결과 업데이트
   - 변경 히스토리 항목 append

## Color Review Rule (Orange Focus)

- `Orange`는 실패 확정이 아닌 **경고성 전이/대기 상태**에 사용한다.
- `QUEUED_TO_DENY`에는 기본적으로 Orange를 허용한다.
- `QUEUED_TO_DENY`를 `기존 규칙 삭제 대기 중`으로 번역했다면 `DENYING`은 반드시 `기존 규칙 삭제 중`으로 맞춘다.
- `QUEUED_TO_DENY`를 `거부 대기 중`으로 번역했다면 `DENYING`은 반드시 `거부 중`으로 맞춘다.
- 필요 시 경고 아이콘/보조 텍스트를 함께 권고한다.

## Output Template

```markdown
- 기준: <기준선 파일 + OpenStack 문서>
- 판정: <적합 | 조건부 적합 | 수정 필요>

- 확인 결과
  - 상태값: <요약>
  - 오탈자: <있음/없음>
  - 색상: <요약>

- 수정 권고
  - <즉시 수정 항목>
  - <선택 개선 항목>
  - <대안 A: 삭제 계열 라벨 세트>
  - <대안 B: 거부 계열 라벨 세트>
```

## Guardrails

- OpenStack canonical 값과 충돌하는 새 내부 상태를 임의 확정하지 않는다.
- SharePoint 링크가 인증/타임아웃으로 읽히지 않으면:
  - 현재 기준선으로 1차 검토를 수행하고
  - 사용자에게 시트 내보내기본(csv/xlsx 캡처/텍스트) 제공을 요청한다.
- 색상은 접근성 관점에서 텍스트/아이콘과 함께 검토한다(색상 단독 판정 금지).
