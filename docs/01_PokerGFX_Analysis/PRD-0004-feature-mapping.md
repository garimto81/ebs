---
parent: PRD-0004-EBS-Server-UI-Design.md
doc_type: reference
---

# PRD-0004: Feature Checklist Mapping (149개)

> PokerGFX-Feature-Checklist.md의 149개 기능이 PRD-0004의 어느 요소에 대응하는지 전체 매핑한다.

## Action Tracker (26개: AT-001 ~ AT-026)

AT는 별도 앱이므로 직접 설계 범위가 아니다. GfxServer와의 상호작용 지점을 매핑한다.

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| AT-001 | Network 연결 상태 | M-18 Connection Status |
| AT-002 | Table 연결 상태 | Y-01 Table Name, Y-02 Password |
| AT-003 | Stream 상태 | O-16 Streaming Platform |
| AT-004 | Record 상태 | O-15 Recording Mode, M-15 Split Recording |
| AT-005 | 게임 타입 선택 | Game Engine (내부) |
| AT-006 | Blinds 표시 | G-45 Show Blinds |
| AT-007 | Hand 번호 추적 | M-17 Hand Counter, G-46 Show Hand # |
| AT-008 | 10인 좌석 레이아웃 | G-02 Player Layout |
| AT-009 | 플레이어 상태 | G-15 How to Show Fold |
| AT-010 | Action-on 하이라이트 | G-19 Indent, G-20 Bounce |
| AT-011 | 포지션 표시 | Player Overlay H (Position) |
| AT-012 | 기본 액션 버튼 | Server GameState 반영 |
| AT-013 | UNDO | Server 상태 롤백 |
| AT-014 | 키보드 단축키 | AT 자체 UI |
| AT-015 | 베팅 금액 입력 | Server Pot 계산 |
| AT-016 | +/- 조정 | AT 자체 UI |
| AT-017 | Quick Bet | Server Pot 계산 |
| AT-018 | Min/Max 범위 | Rules R-02 Limit Raises |
| AT-019 | Community Cards | Preview 보드 표시 |
| AT-020 | 보드 카드 업데이트 | RFID 자동 / AT 수동 |
| AT-021 | HIDE GFX | Display Domain 전체 |
| AT-022 | TAG HAND | Hand History |
| AT-023 | ADJUST STACK | Server Player 데이터 |
| AT-024 | CHOP | Server Pot 분배 |
| AT-025 | RUN IT 2x | Outputs Dual Board |
| AT-026 | MISS DEAL | M-11 Reset Hand |

## Pre-Start Setup (13개: PS-001 ~ PS-013)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| PS-001 | Event Name | G-13 Vanity Text |
| PS-002 | Game Type | Game Engine (내부) |
| PS-003 | Min Chip | G-50 Chipcount Precision |
| PS-004 | 플레이어 이름 | Player Overlay C (Name) |
| PS-005 | 칩 스택 | Player Overlay G (Stack) |
| PS-006 | 포지션 할당 | Player Overlay H (Position) |
| PS-007 | RFID 카드 감지 | M-05 RFID Status, Y-03~Y-07 |
| PS-008 | Ante/SB/BB | G-45 Show Blinds |
| PS-009 | Straddle | R-04 Straddle Sleeper |
| PS-010 | Dealer 위치 | G-02 Player Layout |
| PS-011 | Board Count | Outputs Dual Board |
| PS-012 | TRACK THE ACTION | M-14 Launch AT |
| PS-013 | AUTO 모드 | RFID 자동 감지 |

## Viewer Overlay (14개: VO-001 ~ VO-014)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| VO-001 | Event Logo | G-10~G-12 Sponsor Logo |
| VO-002 | Blinds 정보 | G-45 Show Blinds |
| VO-003 | Chip Counts | G-50 Chipcount Precision |
| VO-004 | Broadcaster Logo | G-10~G-12 Sponsor Logo |
| VO-005 | Hole Cards | G-14 Reveal Players, G-16 Reveal Cards |
| VO-006 | Player Name + Stack | Player Overlay C, G |
| VO-007 | 마지막 액션 | G-35 Clear Previous Action |
| VO-008 | Equity % | G-37 Show Hand Equities |
| VO-009 | Board Cards | G-01 Board Position |
| VO-010 | Pot Display | G-50 Chipcount Precision (Pot) |
| VO-011 | Event Info | G-13 Vanity Text |
| VO-012 | Street 표시 | Game State Machine |
| VO-013 | To Act 표시 | G-19 Indent, G-20 Bounce |
| VO-014 | Folded Player | G-15 How to Show Fold |

## GFX Console (25개: GC-001 ~ GC-025)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| GC-001~008 | VPIP/PFR/AGR/WTSD/WIN/3Bet/CBet/Fold | G-24 Show Player Stats |
| GC-009 | 순위 테이블 | G-22 Show Leaderboard |
| GC-010 | 순위 변동 그래프 | G-22 확장 기능 |
| GC-011 | 정렬 옵션 | G-36 Order Players |
| GC-012 | 필터링 | G-28 Show Eliminated |
| GC-013~016 | 필드 정보 | G-22 Leaderboard 내부 |
| GC-017 | LIVE Stats 토글 | Display Domain 제어 |
| GC-018 | Export CSV | Y-12 Export Folder |
| GC-019 | Print Report | Y-12 Export Folder |
| GC-020 | Reset Stats | M-11 Reset Hand 확장 |
| GC-021 | 티커 메시지 | G-43 Score Strip |
| GC-022 | 시스템 상태 | M-03 CPU, M-04 GPU |
| GC-023 | Preview 창 | M-02 Preview Panel |
| GC-024 | 다크/라이트 테마 | M-12 Settings |
| GC-025 | 다국어 지원 | SK-10 Language |

## Security (11개: SEC-001 ~ SEC-011)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| SEC-001 | 30초 딜레이 | O-08 Delay Time |
| SEC-002 | 카운트다운 | O-10 Show Countdown, M-10 Delay Progress |
| SEC-003 | DB 조회 지연 | Delay Canvas 내부 로직 |
| SEC-004 | 즉시 카드 표시 | Live Canvas (M-02) |
| SEC-005 | 모드 표시 | M-08 Secure Delay |
| SEC-006 | RFID 통신 암호화 | System RFID 하위 시스템 |
| SEC-007 | Serial 암호화 | System RFID 하위 시스템 |
| SEC-008 | DB 암호화 | 설정 영속화 모델 |
| SEC-009 | WebSocket 암호화 | M-18 Connection Status (WSS) |
| SEC-010 | 모드 토글 | M-08 Secure Delay |
| SEC-011 | Delay 시간 설정 | O-08 Delay Time, O-09 Dynamic Delay |

## Equity & Stats (19개: EQ-001 ~ EQ-012, ST-001 ~ ST-007)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| EQ-001~004 | Street별 Equity | G-37 Show Hand Equities |
| EQ-005 | Multi-way Equity | G-37 (자동 지원) |
| EQ-006~007 | Outs 계산/확률 | G-40~G-42 Outs 설정 |
| EQ-008 | Win/Tie/Lose | G-37 확장 |
| EQ-009 | 핸드 레인지 | 고급 기능 (Phase 2) |
| EQ-010 | PLO Equity | Game Engine (내부) |
| EQ-011 | Short Deck Equity | Game Engine (내부) |
| EQ-012 | All-in Equity 애니메이션 | G-38 Hilite Winning Hand |
| ST-001~007 | 세션 통계 | G-24 Show Player Stats |

## Hand History (11개: HH-001 ~ HH-011)

| Feature ID | 기능 | PRD 연결 지점 |
|:----------:|------|---------------|
| HH-001~006 | 핸드 목록/필터/검색 | Hand History DB (hands.db) |
| HH-007 | 핸드 리플레이 | Preview Panel (M-02) 확장 |
| HH-008 | 핸드 상세 뷰 | 별도 다이얼로그 |
| HH-009~010 | Export | Y-12 Export Folder |
| HH-011 | 핸드 공유 | P2 기능 |

## Server 관리 (30개: SV-001 ~ SV-030)

| Feature ID | PRD 요소 | 매핑 |
|:----------:|:--------:|:----:|
| SV-001 | S-01 (Video Sources) | 직접 |
| SV-002 | S-06 (Auto Camera) | 직접 |
| SV-003 | S-14 (ATEM Control) | 직접 |
| SV-004 | S-15, S-16 (Sync) | 직접 |
| SV-005 | S-11, S-12 (Chroma Key) | 직접 |
| SV-006 | O-04, O-06 (Live/Delay) | 직접 |
| SV-007 | O-08~O-10 (Secure Delay) | 직접 |
| SV-008 | O-01, O-03 (Resolution) | 직접 |
| SV-009 | O-14 (Virtual Camera) | 직접 |
| SV-010 | O-02 (9x16 Vertical) | 직접 |
| SV-011 | O-16, O-17 (Streaming) | 직접 |
| SV-012 | G-01 (Board Position) | 직접 |
| SV-013 | G-02 (Player Layout) | 직접 |
| SV-014 | G-17, G-18 (Transition) | 직접 |
| SV-015 | G-20 (Bounce) | 직접 |
| SV-016 | G-10~G-12 (Sponsor) | 직접 |
| SV-017 | G-21 (Action Clock) | 직접 |
| SV-018 | G-50 (Precision) | 직접 |
| SV-019 | G-51 (BB Mode) | 직접 |
| SV-020 | G-47~G-49 (Currency) | 직접 |
| SV-021 | ~~C-01~C-03 (Commentary)~~ | **배제** (프로덕션 미사용) |
| SV-022 | ~~C-07 (PIP)~~ | **배제** (프로덕션 미사용) |
| SV-023 | M-13 (Register Deck) | 직접 |
| SV-024 | Y-04 (Calibrate) | 직접 |
| SV-025 | Y-16 (MultiGFX) | 직접 |
| SV-026 | Y-23 (Stream Deck) | 직접 |
| SV-027 | SK-01~SK-26 (Skin Editor) | 직접 |
| SV-028 | Graphic Editor 전체 | 직접 |
| SV-029 | SK-17~SK-20 (Photo/Flag) | 직접 |
| SV-030 | M-15 (Split Recording) | 직접 |

---

전체 커버리지: 147/149 (98.7%) — Commentary 2개(SV-021, SV-022) 배제