---
name: en-manual-wash
description: >
  영문 매뉴얼(.docx)을 오픈스택 용어집 기준으로 검수·교체(워싱)할 때 사용한다.
  구글 번역기로 나온 영문 매뉴얼을 오픈스택 표준 용어로 정리하는 전체 흐름을 자동화한다.
  반드시 사용할 것: "매뉴얼 영문 검수", "영문 워싱", "오픈스택 기준으로 검수",
  "구글 번역 결과 정리", "영문 용어 교체", "en manual wash" 등을 언급할 때.
  docx 파일과 함께 요청이 오면 이 스킬을 우선 사용한다.
---

> Sharing scope: General
> Share policy: share
> Notes: 영문 매뉴얼 워싱; OpenStack 공개 기준

# 영문 매뉴얼 오픈스택 워싱 스킬

구글 번역기로 생성된 영문 매뉴얼을 오픈스택 표준 용어로 검수·교체한다.
원본은 보존하고 `_washed.docx` 파일을 새로 생성한다.

## 전체 흐름

```
국문 매뉴얼 → (구글 번역) → 영문 raw.docx
                                    ↓
                         [이 스킬] 오픈스택 용어로 워싱
                                    ↓
                         영문 washed.docx  +  용어집 교체 리포트
```

## 실행 방법

```bash
python scripts/wash.py --file "매뉴얼경로.docx"
# 출력: 같은 폴더에 *_washed.docx 생성
```

또는 Claude가 직접 아래 단계를 실행한다.

## 단계별 처리

### 1. 언팩

```python
SKILL_DOCX = "/Users/kimsoyoung/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/261ee49d-3658-4b65-971d-93bf8eef810a/821aca0f-b389-46a4-b8d6-931d3ebefe26/skills/docx"
python3 f"{SKILL_DOCX}/scripts/office/unpack.py" INPUT_DOCX /tmp/en_wash/
```

### 2. 용어 교체

`scripts/wash.py`의 `REPLACEMENTS` 기준으로 모든 XML 파일의 `<w:t>` 텍스트를 직접 교체한다.
(tracked changes 없음 — 바로 반영)

### 3. 팩

```python
python3 f"{SKILL_DOCX}/scripts/office/pack.py" /tmp/en_wash/ OUTPUT_DOCX --original INPUT_DOCX
```

### 4. 리포트

교체 건수를 항목별로 출력한다.

## 주의사항

- 원본 파일을 덮어쓰지 않는다 — 항상 `_washed.docx`로 저장
- `<w:t>` 태그 안 텍스트만 교체 (XML 구조 변경 없음)
- 번역 사전은 `scripts/wash.py`의 `REPLACEMENTS` 에서 관리
- 새 교체 용어 추가 시 `REPLACEMENTS` 에만 추가하면 됨

## 용어 사전 위치

```
scripts/wash.py  →  REPLACEMENTS 리스트
```

`openstack-glossary-en/scripts/translate.py`의 `TRANSLATIONS`와 동기화하여 관리한다.
