---
name: doc-collect
description: >-
  신규 기획 또는 수정·고도화 작업 시작 전, [internal-path-removed]
  관련 문서를 수집하고 파일 인덱스 MD를 생성한다.
  Use when the user says "준비물 수집", "관련 문서 모아줘", "doc-collect",
  또는 작업 시작 시 참조 문서 목록이 필요할 때.
---

> Sharing scope: General
> Share policy: share
> Notes: 준비물 수집; 범용

# doc-collect

기획 작업 시작 전 참조 문서를 수집하고 인덱스 MD를 만드는 스킬.

## 경로 상수

```
ONEDRIVE_BASE = ~/Library/CloudStorage/[internal-path-removed]
DESKTOP_BASE  = ~/Desktop/
```

## Mandatory Intake Gate

작업 시작 전 반드시 확정한다. 불명확하면 질문한다.

1. **기능명** — 예) 알람 설정
2. **버전** — 예) 4.0
3. **모드** — `신규 기획` / `수정·고도화`

## 수집 대상

### 공통 (항상 수집)
| 대상 | 경로 |
|---|---|
| Desktop 작업 폴더 전체 | `DESKTOP_BASE/{버전}/{기능명}/` 하위 전체 |

### 신규 기획 추가 수집
| 대상 | 경로 | 조건 |
|---|---|---|
| 상위 기획 참고 자료 | `ONEDRIVE_BASE/0_기획 참고 자료/` | 파일 있을 때만 |
| 리서치 자료 | `ONEDRIVE_BASE/0_리서치/` | 파일 있을 때만 |
| 최신 기획서 (참조용) | `ONEDRIVE_BASE/2_기획서/{버전}/` 내 최신 PDF | 항상 |

### 수정·고도화 추가 수집
| 대상 | 경로 | 조건 |
|---|---|---|
| 기존 기획서 최신본 | `ONEDRIVE_BASE/2_기획서/{버전}/` 내 최신 PDF | 항상 |
| 최신 IA 구조도 | `ONEDRIVE_BASE/1_IA/{버전}/` 내 최신 XLSX | 항상 |
| 기획 리뷰·검증 이력 | `ONEDRIVE_BASE/4_기획 리뷰_검증/` 내 `{기능명}` 포함 폴더 | 있을 때만 |

## 실행 규칙

- 파일 **내용은 읽지 않는다.** 경로·파일명·확장자만 수집한다.
- 최신본 판단: 파일명 내 `v숫자` 가장 큰 것, 또는 날짜가 가장 최근인 것.
- 폴더/파일이 없으면 에러 없이 스킵하고 `미수집` 항목으로 기록한다.
- [internal-path-removed]

## 출력

저장 경로: `DESKTOP_BASE/{버전}/{기능명}/md/doc-collect_{기능명}_{YYYY-MM-DD}.md`

폴더 `md/`가 없으면 생성한다.

### 출력 포맷 템플릿

```markdown
# 수집 문서 인덱스 — {기능명} ({버전}) {YYYY-MM-DD}

모드: 신규 기획 / 수정·고도화

## 로컬 Desktop
| 파일명 | 경로 | 유형 |
|---|---|---|
| ... | ... | PDF / XLSX / MD / 기타 |

## [internal-path-removed]
| 파일명 | 경로 | 유형 | 비고 |
|---|---|---|---|
| ... | ... | ... | 최신본 / 참조용 |

## 미수집 (경로 없음 또는 파일 없음)
- `{경로}`: 사유
```
