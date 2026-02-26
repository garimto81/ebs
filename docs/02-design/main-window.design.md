# Main Window 설계 스펙

## 변환 요약

- PokerGFX 10개 → EBS 13개
- RFID Status 독립 분리
- Recording·Secure Delay·Studio·Split Recording·Tag Player — EBS MVP 범위 외 (추후 개발 예정)
- Preview 상시 활성화 고정 (M-09 토글 제거)
- 2-column 레이아웃 계승
- Hand Counter(M-17)·Connection Status(M-18) Drop 확정

## UI 설계 원칙

- **Preview Panel**: 480px 고정폭, 16:9 비율 자동 높이 (480×270). Chroma Key Blue(#0000FF) 배경에 GFX 오버레이 실시간 렌더링. CSS `aspect-ratio:16/9` 적용.
- **Control Panel**: 나머지 320px. 상단: 필수 상태 인디케이터(CPU/GPU/RFID). 중단: 자동 spacer(flex:1, ~60px). 하단: 액션 버튼. 수직 스크롤 없이 모든 요소가 보여야 한다.
- **앱 윈도우**: 800×365px 기준 (Title Bar 28px + Preview 270px + Status Bar 22px + Shortcut Bar 24px + Watermark 22px).
- **Status Bar**: 하단 1행. 서버 연결 상태, 게임 타입, 블라인드 레벨 표시. RFID 연결 상태, 현재 핸드 번호, AT/Overlay/DB 연결 상태 (M-17/M-18 Drop 확정).
- **탭 없음**: Main Window는 독립 모니터링 화면. 각 설정 탭(System, Sources, Outputs, GFX 1, GFX 2, GFX 3)은 탭 클릭으로 전환.

## 레이아웃

Preview Panel(M-02, 좌) + Status Panel(M-03~M-06, 우상) + 액션 버튼(M-11~M-14, 우하).

## Element Catalog

### 상태 표시 그룹

| # | 요소 | 타입 | 설명 | PGX | 우선순위 |
|---|------|------|------|-----|---------|
| M-01 | Title Bar | AppBar | 앱 이름 + 버전 + 윈도우 컨트롤 | #1 | P2 |
| M-02 | Preview Panel | Canvas | 출력 해상도(O-01)와 동일한 종횡비 유지, Chroma Key Blue, GFX 오버레이 실시간 렌더링. 해상도 정책: 실제 출력은 Full HD(1920×1080) 기준 리사이징. 문서 표기(480×270)는 UI 공간 내 표시 크기로 가독성용 축약 표기. | #2 | P0 |
| M-03 | CPU Indicator | ProgressBar | CPU 사용률 + 색상 코딩 (Green<60%, Yellow<85%, Red>=85%). 매뉴얼: "The icons on the left indicate CPU and GPU usage. If they turn red, usage is too high for the Server to operate reliably." (p.34) | #3 | P1 |
| M-04 | GPU Indicator | ProgressBar | GPU 사용률 + 색상 코딩. 매뉴얼: "The icons on the left indicate CPU and GPU usage. If they turn red, usage is too high for the Server to operate reliably." (p.34) | #3 | P1 |
| M-05 | RFID Status | Icon+Badge | RFID 리더 상태 7색 표시. Green=정상 운용, Grey=보안 링크 수립 중, Blue=정상 운용+미등록 카드 감지, Black=정상 운용+동일 카드 중복 감지, Magenta=정상 운용+중복 카드 감지, Orange=연결됨+응답 없음(CPU 과부하/USB 문제), Red=미연결. 매뉴얼 p.34 | #3 | P0 |
| M-06 | RFID Connection Icon | Icon | RFID 연결 상태 표시 (연결 시 녹색 USB/WiFi 아이콘으로 변경, 미연결 시 경고 아이콘) | #3 | P1 |
| M-17 | Hand Counter | Badge | 현재 세션 핸드 번호 (Hand #47) | 신규 | P0 **[DROP]** |
| M-18 | Connection Status | Row | AT/Overlay/DB 각각 Green/Red 표시 | 신규 | P0 **[DROP]** |

### M-02 Preview Panel 해상도 스케일링 스펙

| 조건 | Preview 동작 |
|------|-------------|
| 출력 해상도(O-01) = 16:9 (기본) | Preview 캔버스 크기: UI_Panel_Width × 9/16 |
| 출력 해상도(O-01) = 9:16 (세로 모드) | Preview 캔버스 크기: UI_Panel_Height × 9/16 |
| 출력 해상도 변경 시 | 블랙아웃 없이 즉시 비율 재계산 및 리스케일 |
| 4K 출력 (3840×2160) | Preview는 UI 공간 내 최대 크기로 표시 (업스케일 없음, 고밀도 픽셀 그대로 표시) |
| SD 480p (854×480) 출력 | Preview는 실제 픽셀 크기 또는 2× 확대 표시 (픽셀이 너무 작아 식별 불가 방지) |

Preview는 항상 출력 해상도의 종횡비를 유지한다. Preview 캔버스 자체의 픽셀 밀도는 UI 공간 크기에 따라 결정되며, 출력 해상도와 1:1 대응하지 않는다.

### 보안 제어 그룹

| # | 요소 | 타입 | 설명 | PGX | 우선순위 |
|---|------|------|------|-----|---------|
| M-07 | Lock Toggle | IconButton | 설정 잠금/해제. 잠금 시 모든 탭 설정 변경 불가 (액션 버튼 제외, 본방송 중 실수 방지). 매뉴얼: "Click the Lock symbol next to the Settings button to password protect the Settings Window." (p.33) | #3 | P1 |
| M-09 | Preview Toggle | Checkbox | Preview 렌더링 On/Off (CPU 절약) | #4 | P0 |

### 액션 버튼 그룹

| # | 요소 | 타입 | 설명 | PGX | 우선순위 |
|---|------|------|------|-----|---------|
| M-11 | Reset Hand | ElevatedButton | 현재 핸드 초기화, 확인 다이얼로그 | #5 | P0 |
| M-12 | Settings | IconButton | 전역 설정 다이얼로그 (테마, 언어, 단축키) | #5 | P1 |
| M-13 | Register Deck | ElevatedButton | 52장 RFID 일괄 등록, 진행 다이얼로그 | #6 | P0 |
| M-14 | Launch AT | ElevatedButton | Action Tracker 실행/포커스 전환 | #7 | P0 |

---

**Version**: 1.0.0 | **Updated**: 2026-02-26
