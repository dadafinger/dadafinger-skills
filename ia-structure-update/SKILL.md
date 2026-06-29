> **Scope: Internal** — 사내 기획에 묶인 특수 요구·명명은 일반화됨. 범용 방법론만 참고.

---
name: ia-structure-update
description: Author의 Product 메뉴IA구조도(.xlsx) 업데이트 워크플로. Figma Roadmap의 신규/변경 화면을 IA 메뉴구조도에 수렴 반영(신규 행 추가·표기 정정)하고, 원본 보존 v_next 신규본 + 개정이력으로 저장한다. "IA 업데이트", "메뉴구조도 반영", "메뉴IA구조도", "IA에 반영", "구조도에 화면 추가", "IA 개정", "Figma 신규 화면 IA 반영" 등이 언급되면 사용한다. planning-flow가 기획서까지의 흐름이라면, 이 스킬은 그 결과를 산출물 IA 엑셀에 안전하게 반영하는 단계다.
---

> Sharing scope: Internal
> Share policy: caution
> Notes: IA 메뉴구조도 .xlsx; 사내 IA

# Product IA 구조도 업데이트 (메뉴구조도 반영)

Figma Roadmap의 4.x 신규/변경 화면을 **Product 메뉴IA구조도 .xlsx**에 반영하는 반복 워크플로. 산출물 엑셀의 서식·병합·수식·개정이력을 깨지 않고 안전하게 행을 추가/정정하고, **원본을 보존한 채 v_next 신규본**으로 저장한다.

관련: [[planning-flow]] (기획서 단계), `figma-change-flow` (Figma 노드 반영), [[figma-spec-format]], [[figma-format-compliance-feedback]].

## When to use

- "이어서 IA 업데이트", "메뉴구조도에 반영", "메뉴IA구조도 수정/개정"
- Figma 4.x 신규 화면(보고서/미터링/집계 등)을 IA에 수렴 반영
- 기존 화면의 표기 통일·명칭 정정을 IA 전반에 적용
- 알람/메뉴 제거 등 구조 변경을 개정이력과 함께 기록

## ⚠️ Intake Gate (쓰기 전 반드시 확정)

1. **대상 변경분** — 어떤 Figma 노드(node-id)들을 반영할지. 각 노드가 **실제로 그 화면이 맞는지 판독으로 검증**(아래 "노드 불일치 함정" 참고).
2. **저장 방식** — 기본 = **v_next 신규본 + 개정이력 추가, 원본 보존**. (product SoT 원칙상 산출물 IA는 읽기전용이 기본 → 의도적 오버라이드 시 신규본으로 안전 처리)
3. **배치** — 신규 화면을 기존 LEVEL1 하위에 넣을지, 신규 LEVEL1을 신설할지. **Figma Description의 "진입 경로"가 1차 근거**. LNB 목업과 상충하면 사용자에게 확인.

## 소스 위치

- **IA 파일**: `~/Library/CloudStorage/[internal-path-removed]` (실장님 드라이브가 최신 → [[reference_onedrive]])
- **Figma**: `Roadmap 4.0 Product` = fileKey `[fileKey-removed]`. 판독 도구 = **공식 `claude.ai Figma` MCP** (`get_metadata` / `get_screenshot` / `get_design_context`). URL의 `node-ref-removed` → nodeId `2040-14706` 그대로 사용.
- get_metadata 출력이 토큰 한도를 넘으면 파일로 저장됨 → **서브에이전트(general-purpose)로 jq/python 파싱**해서 Screen ID·Page Title·진입 경로·Description 섹션·Changelog·Author만 verbatim 추출시켜 메인 컨텍스트를 아낀다.

## IA 파일 구조 (v4.0.0 기준)

시트: `0. 표지`, `0-1. 개정이력`, `0-2. 목차`, `1. 메뉴구조도`, `2. 역할 정의`

### 1. 메뉴구조도 컬럼 레이아웃 (1-indexed)
| 열 | 내용 | 정렬 |
|---|---|---|
| B(2) | 순번 | center · **수식 `=B{r-1}+1`** (B7=1) |
| C(3) | 시스템명(Product) | center |
| D(4) | LEVEL 1 | center |
| E(5) | LEVEL 2 | left |
| F(6) | LEVEL 3 | left |
| G(7) | 화면ID | center |
| H(8) | 화면명 | left |
| I~P(9~16) | 역할 8종 O/X | center |
| Q(17) | 비고 | - |

- 역할 8종: 솔루션 / Product 엔진 / 기본설정 / 물리 인프라 / 컴퓨트 / 네트워크 / 스토리지 / 프로젝트 관리자
- 헤더 5~6행, **데이터 7행~**. 범례: `O`=메뉴 제공(할당 자원 내 CRUD), `X`=숨김.
- **신규 추가 하이라이트 = solid `FFFFFF00`(노랑)**. 범례 스워치 = B2. 신규 행은 B..Q에 노랑 fill + 비고 "X.X.X 신규 추가".
- **데이터 셀은 LEVEL 값을 행마다 반복**(병합 아님). 병합은 헤더에만 존재 → 행 삽입이 데이터 병합을 깨지 않음.
- 폰트 Malgun Gothic 10, 전 셀 테두리.

## 워크플로

1. **Figma 판독** — 대상 노드들 get_metadata(필요시 서브에이전트 파싱) + 필요시 get_screenshot. 추출: Screen ID, Page Title, **진입 경로**, 탭/구조, Description 섹션, Changelog, Author.
2. **IA 현황 파악** — openpyxl로 메뉴구조도 dump: LEVEL1 행 범위, 삽입 위치, **대상 화면ID가 이미 존재하는지** 확인(중복 추가 방지), 미러링할 형제 블록의 역할 O/X, 개정이력·표지·목차 버전 셀.
3. **배치·번호 결정** — 진입 경로 따라 LEVEL1/2 결정. 화면ID는 **IA 자체 규칙 `CONT-NN_NN_NN`로 형제 연번 이어서 부여**(Figma의 `CON-0xx` 로드맵 내부 ID를 그대로 쓰지 않음). 화면 내 탭은 가상 네트워크 구성도 선례처럼 **탭 = LEVEL3 행**으로 모델링.
4. **역할 O/X** — 같은 LEVEL1 블록 행을 **미러링**(예: 모니터링 블록 = `O,O,X,O,X,X,X,X`).
5. **반영(openpyxl)** — 아래 구현 주의 준수.
6. **검증** — 저장본 reload 후: 신규 행 값·노랑 fill·테두리, 시프트된 기존 행 무손상, 순번 수식, 개정이력/표지/목차 갱신 확인.
7. **메모리/working doc 갱신** — 진행/완료 상태 기록.

## 구현 주의 (openpyxl 함정 — 반드시 지킬 것)

```python
import copy, datetime, openpyxl
from openpyxl.styles import PatternFill
YELLOW = PatternFill(fill_type="solid", fgColor="FFFFFF00")

wb = openpyxl.load_workbook(SRC)         # 원본 로드 → DST(v_next)로만 저장(원본 보존)
ws = wb["1. 메뉴구조도"]

INS, N, TEMPLATE = 315, 4, 310           # 삽입행, 행수, 스타일 클론용 동일블록 데이터행
tpl = {c: copy.copy(ws.cell(TEMPLATE, c)._style) for c in range(1, 18)}
tpl_h = ws.row_dimensions[TEMPLATE].height

ws.insert_rows(INS, N)                    # ⚠️ 새 행은 스타일 없음 + 수식 미번역
for i, (l1,l2,l3,sid,name) in enumerate(rows):
    r = INS + i
    ws.row_dimensions[r].height = tpl_h
    for c in range(1, 18):
        ws.cell(r, c)._style = copy.copy(tpl[c])     # 스타일 클론
    ws.cell(r,3,"Product"); ws.cell(r,4,l1); ws.cell(r,5,l2)
    ws.cell(r,6,l3); ws.cell(r,7,sid); ws.cell(r,8,name)
    for j,v in enumerate(['O','O','X','O','X','X','X','X']): ws.cell(r,9+j,v)
    ws.cell(r,17,"4.0.0 신규 추가")
    for c in range(2,18): ws.cell(r,c).fill = YELLOW

ws.cell(7,2,1)                            # 순번 수식 전면 재생성 (insert_rows가 수식 미번역)
for r in range(8, ws.max_row+1): ws.cell(r,2, f"=B{r-1}+1")
```

- **insert_rows는 ① 새 행을 무스타일로 두고 ② 수식 참조를 옮기지 않는다** → 스타일 클론 + 순번(B열) 수식 전면 재생성 필수.
- **개정이력(`0-1. 개정이력`)**: 빈 템플릿 행(8~10행)이 이미 서식과 함께 존재 → 값만 채움. `J3`(개정일)=오늘, `J4`(버전)=다음 버전, 새 행: `B8`=버전, `C8`=날짜, `E8`(병합 E:G)=개정내용(번호 목록, `\n` 구분), `H8`(병합 H:I)=작성자(Author), `J8`=승인자(`-`).
- **표지(`0. 표지`)**: `C28`=문서버전, `C27`=작성일자.
- **목차(`0-2. 목차`)**: `O3`=개정일, 해당 시트 행의 `제.개정일`(예 메뉴구조도=O10, 개정이력=O8). 단 `개정번호`(O4·L열)는 템플릿상 이미 불일치(예 4)할 수 있으니 무리하게 안 건드림 — 변경분만 갱신하고 사용자에게 언급.
- **저장은 항상 `..._v<N+1>.xlsx` 신규 파일**. 원본 v<N> 절대 덮어쓰지 않음.

## 자주 겪는 함정 (실제 사례)

- **노드 불일치**: 사용자가 "복제" 노드라며 준 `2288-27397`이 실제론 **볼륨 백업 스케줄**(CONT-04_06_xx)이었음. 반드시 판독으로 화면 정체를 확인하고, 의도와 다르면 사용자에게 되물어라. 추측으로 행을 만들지 말 것.
- **이미 존재하는 화면**: 볼륨 백업 스케줄 5개 화면(CONT-04_06_01~05)은 이미 IA에 있어 **구조 변경 불필요**였다. 추가 전 화면ID로 기존 행 존재 여부를 먼저 확인.
- **로드맵 ID ≠ IA 화면ID**: Figma는 `CON-006` 같은 내부 ID를 쓰지만 IA는 `CONT-NN_NN_NN`. IA 번호 체계로 변환해 부여.
- **표기 통일**: "스케쥴"→"스케줄"처럼 전 시트 일괄 치환 요청 가능. 데이터 셀만 바꾸고(개정이력의 정정 서술 문구는 의도된 표기이므로 유지), 개정이력에 정정 항목 추가.

## 산출 후

- working doc(`proprium/IA_4.0.0_UPDATE_WORKING.md` 류)과 프로젝트 메모리에 완료/잔여 항목 기록.
- 신규 행/개정이력/버전 갱신 요약을 표로 사용자에게 보고.
