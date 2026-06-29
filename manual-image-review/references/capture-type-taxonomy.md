# 캡처 유형 분류 (Capture Type Taxonomy)

매뉴얼 이미지를 "어떤 화면을 어떻게 캡처했는가"로 분류한다.
용도: 향후 자동 캡처 워크플로(`screenshot` 스킬)와 1:1 매핑해 **소스 캡처 시점에 동일 유형으로 일관 출력**하기 위함.

## 분류 카테고리 (9 + 1)

| 코드 | 이름 | 정의 | 식별 시그널 | screenshot 워크플로 |
|---|---|---|---|---|
| **FULL** | 화면 전체 | LNB + GNB + 콘텐츠 모두 포함, 브라우저 풀스크린 캡처 | LNB 메뉴 토큰 ≥4개 + GNB 토큰 ≥1개 OR 폭 ≥2200 | `--mode=full --window=1920x1080` |
| **CONTENT** | 콘텐츠 영역만 | LNB/GNB 크롭, 본문 영역만 | 폭 1100~1900 + 종횡비 > 1.1 + 셸 시그널 없음 | `--mode=content --contentSelector="main"` |
| **MODAL** | 모달/팝업 단독 | 모달 다이얼로그만 잘라 표시 | Cancel/Save/Confirm 버튼 페어 ≥2 + 폭 < 1300 OR Create/Edit/Delete 접두 + 폭 < 900 | `--mode=modal --selector=".modal" --backdrop=hide` |
| **PANEL** | 부분 패널/탭/필터 | 콘텐츠 영역의 일부 영역만 (필터, 상세 패널, 사이드 패널) | 800 ≤ 폭 ≤ 1800 + 높이 < 폭×0.4 (wide-short) | `--mode=panel --selector="[data-panel]"` |
| **INLINE** | 인라인 컴포넌트 | 드롭다운/툴팁/뱃지/팝오버 같은 작은 UI 요소 | max(폭,높이) < 700 OR 폭<500 + 높이<300 | `--mode=inline --selector=":focus" --hover=keep` |
| **DIAGRAM** | 다이어그램/일러스트 | 캡처가 아닌 디자인 산출물 (PPT/SVG/Figma 추출) | jpg + outline/Configuration diagram/Architecture 섹션 | (캡처 X — 디자인 원본 export) |
| **COVER** | 표지/머리말 | 매뉴얼 디자인 요소 (표지, 챕터 표제) | 섹션 "(표지/머리말)" | (캡처 X — 매뉴얼 디자인) |
| **CLI** | 터미널/CLI | 텍스트 기반 셸 캡처 | `$ `, `# `, `Last login`, `[user@`, ssh/sudo 토큰 | `--mode=cli --terminal=iTerm --theme=light` |
| **TOAST** | 알림 메시지/토스트 | 우상단/하단 작은 알림 | 길이 < 80 + "created/deleted/saved/applied successfully" | `--mode=toast --capture-on=event` |
| UNKNOWN | 분류 실패 | 자동 분류 실패 — 수동 라벨 필요 | 최고 점수 < 1.5 | (수동) |

## 자동 분류 룰 (heuristic)

`scripts/classify_captures.py` 가 다음 입력으로 분류한다:
- `word/media/*.png|jpg` (이미지 메타로 폭/높이 추출)
- `ocr_results.jsonl` (텍스트 시그널)
- `review_list.txt` (섹션 정보)

산출: `capture_types.csv` (file, section, w, h, type, conf, signals).

신뢰도(`conf`) ≥ 1.5만 분류 확정. 그 미만은 UNKNOWN → 수동 라벨 권고.

## screenshot 워크플로 매핑

`workflows/screenshot.md` 의 캡처 옵션과 본 분류를 1:1로 묶는다.

```
FULL    → 풀스크린 캡처, LNB/GNB 모두 포함, 1920x1080 또는 1440x900
CONTENT → contentSelector="main" 또는 LNB/GNB 마스킹
MODAL   → 모달 셀렉터 + 외부 배경 dim 유지, 모달 그림자 포함 캡처
PANEL   → 특정 패널 셀렉터 (필터/사이드/탭 본문)
INLINE  → 호버/포커스 상태 유지 후 작은 셀렉터, 컴포넌트만
DIAGRAM → 캡처 X. 디자인 원본(SVG/PPT/Figma)에서 PNG export (≥1600px)
COVER   → 캡처 X. 매뉴얼 디자인에서 직접 작성
CLI     → 터미널 헤드리스 캡처, 폰트 통일(Menlo/Monaco), 라이트 테마
TOAST   → 이벤트 트리거 후 즉시 캡처 (트랜지션 후 1~2초)
```

## 정합성 룰

- 같은 페이지의 캡처는 **유형이 일관**되어야 함 (예: 인스턴스 목록 페이지의 5장이 FULL/CONTENT 섞이면 안 됨)
- DIAGRAM은 자동 캡처 워크플로의 산출물이 아님 → 매뉴얼 디자인 트랙
- 같은 컴포넌트의 다른 상태(image303/304 같은 화면 + 드롭다운 펼침)는 동일 유형 + 상태만 다름
- jpg 형식은 DIAGRAM 외엔 비권장 (PNG 통일 권고)
