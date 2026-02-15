---
parent: PRD-0004-EBS-Server-UI-Design.md
screen_id: system
element_range: Y-01 ~ Y-24
---

# System Tab -- Screen Specification

## Quick Reference

- 단축키: Ctrl+6
- 요소: 24개 (P0: 7, P1: 11, P2: 6)
- 스크린샷: `images/mockups/ebs-system.png`
- HTML 원본: [ebs-server-ui.html](../mockups/ebs-server-ui.html)

![System 탭](../images/mockups/ebs-system.png)

## Design Decisions

1. RFID 캘리브레이션이 방송 준비 첫 단계인 이유: 카드 인식의 정확도가 이 탭에서 결정된다. 캘리브레이션 없이 다른 설정을 진행하면 테스트 핸드에서 카드 오인식이 발생하고, 모든 설정을 다시 확인해야 한다. 따라서 방송 준비 프로세스(Part III 섹션 7)에서 하드웨어 점검(1단계) → RFID 캘리브레이션(2단계)을 최우선으로 배치했다.

2. AT 접근 정책(Y-13~Y-15)이 이 탭에 있는 이유: ActionTracker는 딜러가 사용하는 별도 장치이므로 보안 설정이 필요하다. Kiosk Mode(Y-15)는 딜러가 불필요한 기능에 접근하지 못하도록 제한하고, Predictive Bet(Y-14)는 딜러의 입력 속도를 높인다. 이 설정은 시스템 관리 범주이므로 System 탭에 배치했다.

3. Advanced 그룹(Y-16~Y-23)이 별도 섹션인 이유: MultiGFX(다중 테이블), Stream Deck 매핑, Auto Start 같은 설정은 대부분의 방송에서 변경하지 않는다. 자주 사용하는 RFID/Diagnostics 설정과 시각적으로 분리하여 실수로 변경하는 것을 방지한다.

## Workflow

RFID 리셋/캘리브레이션 → 안테나 설정 → AT 접근 정책 → 진단 확인 → 고급 설정.

## Element Catalog

| # | 그룹 | 요소 | 설명 | PGX# | 우선순위 |
|:-:|------|------|------|:----:|:--------:|
| Y-01 | Table | Name | 테이블 식별 이름 | #2 | P1 |
| Y-02 | Table | Password | 접속 비밀번호 | #3 | P1 |
| Y-03 | RFID | Reset | RFID 시스템 초기화 | #4 | P0 |
| Y-04 | RFID | Calibrate | 안테나별 캘리브레이션 | #5 | P0 |
| Y-05 | RFID | UPCARD Antennas | UPCARD 안테나로 홀카드 읽기 | #22 | P0 |
| Y-06 | RFID | Disable Muck | AT 모드 시 muck 안테나 비활성 | #23 | P0 |
| Y-07 | RFID | Disable Community | 커뮤니티 카드 안테나 비활성 | #24 | P0 |
| Y-08 | System Info | Hardware Panel | CPU/GPU/OS/Encoder 자동 감지 | #11 | P1 |
| Y-09 | Diagnostics | Table Diagnostics | 안테나별 상태, 신호 강도 (별도 창) | #10 | P1 |
| Y-10 | Diagnostics | System Log | 로그 뷰어 | #12 | P1 |
| Y-11 | Diagnostics | Secure Delay Folder | 딜레이 녹화 폴더 | #13 | P1 |
| Y-12 | Diagnostics | Export Folder | 내보내기 폴더 | #14 | P1 |
| Y-13 | AT | Allow AT Access | AT 접근 허용 | #26 | P0 |
| Y-14 | AT | Predictive Bet | 베팅 예측 입력 | #27 | P0 |
| Y-15 | AT | Kiosk Mode | AT 키오스크 모드 | #28 | P0 |
| Y-16 | Advanced | MultiGFX | 다중 테이블 운영 | #16 | P2 |
| Y-17 | Advanced | Sync Stream | 스트림 동기화 | #17 | P2 |
| Y-18 | Advanced | Sync Skin | 스킨 동기화 | #18 | P2 |
| Y-19 | Advanced | No Cards | 카드 비활성화 | #19 | P1 |
| Y-20 | Advanced | Disable GPU | GPU 인코딩 비활성화 | #20 | P1 |
| Y-21 | Advanced | Ignore Name Tags | 네임 태그 무시 | #21 | P1 |
| Y-22 | Advanced | Auto Start | OS 시작 시 자동 실행 | 신규 | P2 |
| Y-23 | Advanced | Stream Deck | Elgato Stream Deck 매핑 | #15 | P2 |
| Y-24 | Updates | Version + Check | 버전 표시 + 업데이트 | #7,#8 | P2 |

## Interaction Patterns

| 조작 | 시스템 반응 | 피드백 |
|------|-----------|--------|
| Y-03 Reset 클릭 | RFID 시스템 재초기화 | M-05 상태 변화 (Yellow → Green/Red) |
| Y-04 Calibrate 클릭 | 안테나별 캘리브레이션 시작 | 진행률 + 안테나별 결과 |
| Y-09 Table Diagnostics | 별도 창 열림 | 안테나 신호 강도 실시간 표시 |

## Navigation

| 목적지 | 방법 | 조건 |
|--------|------|------|
| Table Diagnostics | Y-09 클릭 | 별도 창 열림 |
| Main Window | 탭 영역 외 클릭 | RFID 설정 완료 후 |
| Sources 탭 | Ctrl+1 | RFID 후 비디오 설정으로 이동 |
