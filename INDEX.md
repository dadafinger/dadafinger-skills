# Skill Catalog (dadafinger-skills export)

모든 스킬의 **본문**은 이 디렉터리에 있다. AI 툴 공통 참조.  
공유 범위 분류: [scope-registry.yaml](scope-registry.yaml) · GitLab 배포: `./deploy.sh` → `dadafinger-skills`  
정비 절차·등록 불변식: [MAINTENANCE.md](MAINTENANCE.md) · 점검 `python3 scripts/check_registration.py`

## 1. 기획 파이프라인 (Planning pipeline)

| Skill | Scope | Share | SoT | 슬래시 커맨드 | 참조 문서 |
| planning-flow | Internal | caution | [SKILL.md](planning-flow/SKILL.md) | caution | [SKILL.md](planning-flow/SKILL.md) |
| planning-md | Internal | caution | [SKILL.md](planning-md/SKILL.md) | caution | [SKILL.md](planning-md/SKILL.md) |
| planning-html | Internal | caution | [SKILL.md](planning-html/SKILL.md) | caution | [SKILL.md](planning-html/SKILL.md) |
| planning-figma | Internal | caution | [SKILL.md](planning-figma/SKILL.md) | caution | [SKILL.md](planning-figma/SKILL.md) |
| figma-change-flow | Internal | caution | [SKILL.md](figma-change-flow/SKILL.md) | caution | [SKILL.md](figma-change-flow/SKILL.md) |
| figma-desc-spec | Internal | caution | [SKILL.md](figma-desc-spec/SKILL.md) | caution | [SKILL.md](figma-desc-spec/SKILL.md) |
| doc-collect | General | share | [SKILL.md](doc-collect/SKILL.md) | share | [SKILL.md](doc-collect/SKILL.md) |
| benchmark-research | General | share | [SKILL.md](benchmark-research/SKILL.md) | share | [SKILL.md](benchmark-research/SKILL.md) |
| ia-structure-update | Internal | caution | [SKILL.md](ia-structure-update/SKILL.md) | caution | [SKILL.md](ia-structure-update/SKILL.md) |

## 2. 검수 / 리뷰 (Review)

| Skill | Scope | Share | SoT | 슬래시 커맨드 | 참조 문서 |
| figma-spec-review | Internal | caution | [SKILL.md](figma-spec-review/SKILL.md) | caution | [SKILL.md](figma-spec-review/SKILL.md) |
| html-spec-review | Internal | caution | [SKILL.md](html-spec-review/SKILL.md) | caution | [SKILL.md](html-spec-review/SKILL.md) |
| status-state-change-review | Internal | caution | [SKILL.md](status-state-change-review/SKILL.md) | caution | [SKILL.md](status-state-change-review/SKILL.md) |
| critique-reviewer | General | share | [SKILL.md](critique-reviewer/SKILL.md) | share | [SKILL.md](critique-reviewer/SKILL.md) |

## 3. 매뉴얼 / 문서 (Manual & docs)

| Skill | Scope | Share | SoT | 슬래시 커맨드 | 참조 문서 |
| kr-manual-change-tracker | Internal | caution | [SKILL.md](kr-manual-change-tracker/SKILL.md) | caution | [SKILL.md](kr-manual-change-tracker/SKILL.md) |
| kr-manual-format-review | Internal | caution | [SKILL.md](kr-manual-format-review/SKILL.md) | caution | [SKILL.md](kr-manual-format-review/SKILL.md) |
| kr-manual-quickguide | Internal | caution | [SKILL.md](kr-manual-quickguide/SKILL.md) | caution | [SKILL.md](kr-manual-quickguide/SKILL.md) |
| en-manual-wash | General | share | [SKILL.md](en-manual-wash/SKILL.md) | share | [SKILL.md](en-manual-wash/SKILL.md) |
| openstack-glossary-en | General | share | [SKILL.md](openstack-glossary-en/SKILL.md) | share | [SKILL.md](openstack-glossary-en/SKILL.md) |
| manual-image-review | General | share | [SKILL.md](manual-image-review/SKILL.md) | share | [SKILL.md](manual-image-review/SKILL.md) |
| jp-capture-text-consistency | General | share | [SKILL.md](jp-capture-text-consistency/SKILL.md) | share | [SKILL.md](jp-capture-text-consistency/SKILL.md) |

## 트리거 키워드 (요약)

### 기획 파이프라인

- **planning-flow** (실행 오케스트레이터): `기획 전체 흐름`, `md부터 피그마까지`, `md→html→figma`, `요구사항 반영하고 그려`
- **planning-md**: `신규 기획`, `기획 초안`, `준비물 줄게`, `기획서 작성`, `요구사항/회의 메모 반영`, `이 md 고쳐줘`, `복합/combination`, `알람/이벤트 화면`, `화면 컬럼/필터`
- **planning-html**: `html 뽑아`, `공통템플릿으로 그려`, `본문영역 그려`, `spec md html`, `md→html`
- **planning-figma**: `피그마 새 프레임`, `spec md를 피그마에`, `figma로 그려`, `html→figma`
- **figma-change-flow**: Figma 반영, 노드 수정, 기획서→Figma
- **figma-desc-spec**: `Description 작성`, `상세 명세 써줘`, `설명 칼럼 검수`, `전수 서술 점검`, `4종 화면 누락`, `체크리스트로 검수`
- **doc-collect**: `준비물 수집`, `관련 문서 모아줘`, `doc-collect`
- **benchmark-research**: `벤치마킹 정리해줘`, `리서치 폴더 분석해줘`, `benchmark-research`
- **ia-structure-update**: `IA 업데이트`, `메뉴구조도 반영`, `메뉴IA구조도`, `IA에 반영`, `구조도에 화면 추가`, `IA 개정`, `Figma 신규 화면 IA 반영`

### 검수 / 리뷰

- **figma-spec-review**: `figma 검수`, `상세 명세 검수`, `노드 검수`, `포맷 맞는지 봐줘`, `용어 일치 점검`, `검수 루프`, `spec review` (읽기전용, 안 고침)
- **html-spec-review**: `html대로 md 됐는지`, `프로토타입이랑 기획서 맞아?`, `html ↔ md 정합`, `번들/프로토 검수`, `기획서랑 화면 차이`, `라이브 html 고쳐줘`, `최신본 맞는지` (1단계 읽기전용 트리아지 → 2단계 정해진 것만 안전 패치)
- **status-state-change-review**: `상태값 변경`, `상태 정의 검토`, `색상 검토`, `액세스 규칙 상태`
- **critique-reviewer**: `비판해줘`, `검수노트`, `약점 분석`, `부족한 점`, `리스크 정리`, `critique`, `좋은 점 빼고`, `날카롭게`

### 매뉴얼 / 문서

- **kr-manual-change-tracker**: `변경점 등록`, `체크리스트 YAML 추가`, `미등록 건 체크`, `커버리지 검증`, `변경 원장`
- **kr-manual-format-review**: `서식 검수`, `매뉴얼 서식 안 맞는 거`, `서식 통일`, `섹션 추가했어 검수해줘`, `이미지 크기 맞춰줘`, `표 크기 통일`, `이미지·표 크기 일관성`
- **kr-manual-quickguide**: `퀵가이드 완성`, `퀵 가이드`, `퀵가이드 캡처 목록`, `링크 삽입`, `링크 재생성`, `품질 검수`
- **en-manual-wash**: `영문 매뉴얼 검수`, `영문 워싱`, `오픈스택 기준으로 검수`, `구글 번역 결과 정리`, `영문 용어 교체`, `en manual wash`
- **openstack-glossary-en**: `영문 열 추가`, `영어열 채워`, `오픈스택 기준 번역`, `다국어 용어집`, `용어집 영어`, `영문 번역 파일`
- **manual-image-review**: `매뉴얼 이미지 검수`, `이미지도 검수`, `스크린샷 점검`, `캡처 확인`, `이미지 워싱`, `제출용 검사`, `한글 남았는지`, `image audit`
- **jp-capture-text-consistency**: 일본어 캡처 텍스트, UI 라벨 반영 검수

## 워크플로 (skills가 아닌 workflows/)

긴 SoT 워크플로는 [../workflows/INDEX.md](../workflows/INDEX.md) 참조.