# 외부 SoT 참조 (External Sources of Truth)

> Figma 화면 작성·수정 전 **반드시 먼저 확인**해야 할 외부 권위 문서 목록.
> 본 표를 무시하고 작업하면 컴포넌트·정책·상태값 정의가 어긋남 → 정합성 깨짐.

## 1. 디자인 시스템 (Design System)

| 항목 | 위치 | 비고 |
|---|---|---|
| **디자인 시스템 SoT 노트** | `references/design-system.md` | 본 스킬 내. 외부 원천을 정리한 운영 가이드 |
| Confluence 스페이스 "솔루션 정책" | space key `[fileKey-removed]` · id `1939046614` | Atlassian Rovo MCP `getConfluencePage` 사용. 컴포넌트/토큰/화면 정책의 권위 문서 |
| Figma DS 라이브러리 — Policy Document | fileKey `[fileKey-removed]` | 모든 공통 컴포넌트의 node-id |
| Figma DS 라이브러리 — 솔루션본부 전용 | fileKey `[fileKey-removed]` | Hierarchical Table 등 솔루션 파츠 |
| 4.0 작업 파일 | fileKey `[fileKey-removed]` | 현재 작업 대상 |

## 2. 공통 정책 (Common Policy) — 2026-06-18 신규 등록

| 항목 | 위치 |
|---|---|
| **공통 정책 Confluence 페이지** | `[wiki-url-removed]` |
| space key | `[fileKey-removed]` (디자인 시스템 SoT와 동일 스페이스) |
| 접근 방법 | Atlassian Rovo MCP `getConfluencePage` (인증 필요 시 `/mcp`) |

**사용 시점**:
- 화면 작성 전 — 적용되는 공통 정책 확인
- 컴포넌트 동작·상태·접근 권한 정의 시
- 새로 정책을 만들기 전 — 중복 정의 회피
- 권한 모델·통보 정책·검색 동작 등 도메인 횡단 정책 결정 시

**확인 순서**:
1. 스페이스 overview 접근 → 정책 인덱스 파악
2. 작업 도메인에 관련된 정책 페이지 검색
3. 정책 본문 확인 후 Description에 인용 (출처 명시: "공통 정책 §X")
4. 정책과 화면이 충돌하면 사용자(기획자)에게 확인 → 정책 갱신 또는 화면 변경 결정

## 3. 상태값 정의 시트 (Status Value Definition) — 2026-06-18 신규 등록

| 항목 | 위치 |
|---|---|
| **상태값 정의 시트** | `https://okekr-my.sharepoint.com/:x:/g/personal/is_park_okekr_onmicrosoft_com/IQAv4A7OK5NJQZS30__vGXPpAXmjmX2dCzh0vZGPbosmFKA?e=rPKWVQ&nav=MTVfe0IwQTM2NzZDLTNGOUQtNEUwRi04QTgxLUExQ0I0NUZGMEU4MH0` |
| 형식 | SharePoint Excel (xlsx) — 통합 상태값 사전 |
| 보유자 | is_park@okekr_onmicrosoft_com |

**사용 시점**:
- 자원 상태값(인스턴스 / 볼륨 / 네트워크 / 알람 / 작업 등) 라벨·색상·전이 정의
- 새 상태값 추가 검토
- 상태값 한·영·일 표기 결정
- 화면에 상태 칩·뱃지·아이콘 사용 시

**확인 순서**:
1. SharePoint 시트 열기 (브라우저 또는 다운로드)
2. 도메인별 시트 탭에서 해당 자원 상태값 찾기
3. canonical 상태값과 표기·색상이 시트와 일치하는지 검증
4. 시트에 없는 새 상태값이 필요한 경우:
   - 시트 보유자에게 추가 요청 → 시트 갱신 후 화면 반영
   - 시트가 SoT이므로 화면에서 임의 추가 금지

**관련 스킬**:
- `status-state-change-review` — Storage > Shared File > Access Rules 등 특정 도메인 상태값 검토 시 함께 사용
- 본 시트가 그 스킬의 baseline보다 더 광범위 → **전 도메인 상태값은 본 시트가 SoT**

## 4. 외부 SoT 사전 확인 워크플로

화면 작업 시 다음 순서로 외부 SoT를 확인:

```
1. 작업 도메인 식별 (예: 알람, 집계, 인스턴스)
   ↓
2. references/design-system.md 확인 — 쓸 수 있는 컴포넌트 node-id 파악
   ↓
3. 공통 정책 Confluence 확인 — 적용되는 정책 인용
   ↓
4. 상태값 정의 시트 확인 — 노출할 상태값·색상·라벨 결정
   ↓
5. 도메인별 명세 md (예: 알람 v6 명세) 확인
   ↓
6. 회의록 확인 (최신 결정 사항)
   ↓
7. Figma 작업 (use_figma) — 위 SoT 모두 부합하는지 검증 후 진행
```

## 5. 충돌 처리

외부 SoT 간 정의가 다르거나 명세와 SoT가 충돌할 때:

| 충돌 케이스 | 처리 |
|---|---|
| 디자인 시스템 vs 명세 | 디자인 시스템 우선. 명세 갱신 |
| 공통 정책 vs 도메인 명세 | 공통 정책 우선. 도메인 명세 갱신 |
| 상태값 시트 vs 화면 | 상태값 시트 우선. 화면 갱신 |
| 회의록 vs SoT | 회의록은 변경 의도. SoT 갱신 후 화면 반영 (SoT 갱신 책임자에게 요청) |
| SoT 자체가 어긋남 | 사용자(기획자·정책 담당)에게 알리고 SoT 정합 우선 |

> 충돌 발견 시 **임의 판단 금지**. 출처·차이점·권고안을 사용자에게 보고 후 결정.

## 6. 등록·갱신 이력

| 일자 | 항목 | 변경 |
|---|---|---|
| 2026-06-18 | 공통 정책 Confluence | 신규 등록 |
| 2026-06-18 | 상태값 정의 시트 (SharePoint) | 신규 등록 |
| (이전) | 디자인 시스템 SoT | references/design-system.md에 정리 완료 |
