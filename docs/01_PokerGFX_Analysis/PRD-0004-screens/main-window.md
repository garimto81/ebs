---
parent: PRD-0004-EBS-Server-UI-Design.md
screen_id: main-window
element_range: M-01 ~ M-20
---

# Main Window -- Screen Specification

## Quick Reference

- 단축키: 없음 (기본 화면)
- 요소: 20개 (P0: 11, P1: 7, P2: 2)
- 스크린샷: `images/mockups/ebs-main.png`
- HTML 원본: [ebs-server-ui.html](../mockups/ebs-server-ui.html)

![메인 윈도우](../images/mockups/ebs-main.png)

## Design Decisions

1. Dual Canvas 모니터링이 Preview Panel(M-02)에 집중되는 이유: 운영자가 방송 중 80% 이상 바라보는 화면이다. Live Canvas와 Delay Canvas의 상태 차이를 한 곳에서 확인할 수 있어야 Hidden Information Problem(홀카드 지연 공개)이 정상 작동하는지 즉시 판단 가능하다.

2. Quick Actions(M-11~M-16)가 메인에 노출되는 이유: 라이브 방송 중 탭 전환 없이 즉시 조작 가능해야 하는 기능이다. Reset Hand(M-11), Register Deck(M-13), Launch AT(M-14)는 초 단위 반응이 필요하므로 메인 화면에 상주한다.

3. Lock Toggle(M-07)이 전역 동작인 이유: 라이브 중 실수로 설정을 변경하면 방송 사고로 이어진다. Lock은 모든 탭의 설정 변경을 일괄 비활성화하며, Ctrl+L 단축키로 언제든 토글 가능하다.

## Workflow

앱 실행 시 기본 화면. Preview로 출력 상태 모니터링 → 상태 표시로 시스템 건강 확인 → 긴급 시 Quick Actions 사용 → 탭 전환으로 상세 설정 접근.

## Element Catalog

### 상태 표시 그룹 (시스템 건강 상태 한눈에 파악)

| # | 요소 | 타입 | 설명 | PGX 대응 | 우선순위 |
|:-:|------|------|------|:--------:|:--------:|
| M-01 | Title Bar | AppBar | 앱 이름 + 버전 + 윈도우 컨트롤 | #1 | P2 |
| M-02 | Preview Panel | Canvas | 16:9 비율 고정, Chroma Key Blue 배경, GFX 오버레이 실시간 렌더링 | #2 | P0 |
| M-03 | CPU Indicator | ProgressBar | CPU 사용률 + 색상 코딩 (Green < 60%, Yellow < 85%, Red >= 85%) | #3 | P1 |
| M-04 | GPU Indicator | ProgressBar | GPU 사용률 + 색상 코딩 | #3 | P1 |
| M-05 | RFID Status | Icon + Badge | Green=Connected, Red=Disconnected, Yellow=Calibrating | #3 | P0 |
| M-06 | Error Icon | IconButton | 에러 카운트 뱃지, 클릭 시 로그 팝업 | #3 | P1 |
| M-17 | Hand Counter | Badge | 현재 세션 핸드 번호 (Hand #47) | 신규 | P0 |
| M-18 | Connection Status | Row | AT/Overlay/DB 각각 Green/Red 표시 | 신규 | P0 |

### 보안 제어 그룹 (Hidden Information Problem 직접 대응)

| # | 요소 | 타입 | 설명 | PGX 대응 | 우선순위 |
|:-:|------|------|------|:--------:|:--------:|
| M-07 | Lock Toggle | IconButton | Lock 활성 시 설정 변경 불가, 오조작 방지 | #3 | P0 |
| M-08 | Secure Delay | Checkbox | Dual Canvas의 Delay 파이프라인 On/Off | #4 | P0 |
| M-09 | Preview Toggle | Checkbox | Preview 렌더링 On/Off (CPU 절약) | #4 | P0 |
| M-10 | Delay Progress | LinearProgressIndicator | Secure Delay 남은 시간 프로그레스바 + 텍스트 | 신규 | P0 |

### Quick Actions 그룹 (라이브 중 가장 빈번한 조작)

| # | 요소 | 타입 | 설명 | PGX 대응 | 우선순위 |
|:-:|------|------|------|:--------:|:--------:|
| M-11 | Reset Hand | ElevatedButton | 현재 핸드 초기화, 확인 다이얼로그 | #5 | P0 |
| M-12 | Settings | IconButton | 전역 설정 다이얼로그 (테마, 언어, 단축키) | #5 | P1 |
| M-13 | Register Deck | ElevatedButton | 52장 RFID 일괄 등록, 진행 다이얼로그 | #6 | P0 |
| M-14 | Launch AT | ElevatedButton | Action Tracker 실행/포커스 전환 | #7 | P0 |
| M-15 | Split Recording | ElevatedButton | 핸드별 분할 녹화 토글 | #9 | P1 |
| M-16 | Tag Player | Dropdown + Text | 플레이어 선택 + 태그 입력 | #10 | P1 |
| M-19 | Quick Lock | Keyboard Shortcut | `Ctrl+L` 즉시 Lock 토글 | 신규 | P1 |
| M-20 | Fullscreen Preview | IconButton | Preview 전체 화면 (F11) | 신규 | P2 |

## Interaction Patterns

| 조작 | 시스템 반응 | 피드백 |
|------|-----------|--------|
| M-07 Lock 클릭 | 모든 설정 변경 비활성화 | 자물쇠 아이콘 변화 + 탭 그레이아웃 |
| M-08 Secure Delay 토글 | Delay Canvas 파이프라인 On/Off | M-10 프로그레스바 표시/숨김 |
| M-11 Reset Hand | 확인 다이얼로그 → 핸드 초기화 | Preview 초기화, Hand# 리셋 |
| M-13 Register Deck | 52장 순차 스캔 다이얼로그 | 1/52~52/52 진행 표시 |

## Navigation

| 목적지 | 방법 | 조건 |
|--------|------|------|
| Sources~System 탭 | Ctrl+1~6 또는 탭 클릭 | M-07 Lock 해제 시 |
| Skin Editor | GFX 탭 > 스킨 선택 영역 | 별도 창 |
| ActionTracker | F8 또는 M-14 | 별도 앱 실행 |
| Preview 전체 화면 | F11 또는 M-20 | ESC로 복귀 |
