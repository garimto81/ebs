# PRD-0003-Stage1: PokerGFX 완전 복제

**버전**: 1.0.0
**생성일**: 2026-01-28
**상위 문서**: [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md)
**참조 체크리스트**: [PokerGFX-Feature-Checklist.md](PokerGFX-Feature-Checklist.md)
**전제조건**: Stage 0 Gate 통과 (2026년 6월)
**목표 기간**: 2026년 하반기 (H2) - 약 6개월

---

## 1. Stage 1 개요

### 1.1 목표

> **"운영자가 PokerGFX와 EBS 사이에서 차이를 느끼지 못해야 한다"**

Stage 1은 PokerGFX의 모든 기능을 100% 동일하게 구현하는 것을 목표로 합니다.
새로운 기능 추가 없이, 검증된 워크플로우를 그대로 재현합니다.

### 1.2 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **1:1 복제** | PokerGFX 기능을 동일하게 구현 |
| **No Innovation** | Stage 1에서는 새 기능 추가 금지 |
| **운영자 친숙성** | 기존 워크플로우 유지 |
| **54개 기능 완성** | PokerGFX-Feature-Checklist.md 100% 완료 |

### 1.3 기간 및 마일스톤

**전체 기간**: 2026년 7월 - 12월 (6개월)

| 분기 | 마일스톤 | 목표 | 완료 기능 |
|------|----------|------|----------|
| Q3 (7-9월) | Alpha → Beta | RFID + Action Tracker | AT-001~026, PS-001~013 |
| Q4 (10-11월) | RC | 플레이어 관리 + 통계 + Overlay | VO-001~014, GC-001~025, EQ-001~019 |
| Q4 (12월) | Release | Trustless Mode + 테스트 + Gate | SEC-001~011, HH-001~011 |

---

## 2. 기능 매핑 (PokerGFX → EBS)

### 2.1 Action Tracker 기능 (26개)

#### 2.1.1 상태 표시 (Status Bar)

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-001 | Network 연결 상태 | ✓ | 동일 구현 | WebSocket ping/pong | ⬜ |
| AT-002 | Table 연결 상태 | ✓ | 동일 구현 | RFID Serial 상태 | ⬜ |
| AT-003 | Stream 상태 | ✓ | 동일 구현 | OBS WebSocket | ⬜ |
| AT-004 | Record 상태 | ✓ | 동일 구현 | OBS Recording API | ⬜ |

#### 2.1.2 게임 설정

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-005 | 게임 타입 선택 | HOLDEM/PLO/SHORT DECK | 동일 구현 | 토글 버튼 | ⬜ |
| AT-006 | Blinds 정보 표시 | SB/BB/Ante | 동일 구현 | State 관리 | ⬜ |
| AT-007 | Hand 번호 추적 | 카운터 표시 | 동일 구현 | DB auto_increment | ⬜ |

#### 2.1.3 플레이어 그리드

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-008 | 10인 좌석 레이아웃 | ✓ | 동일 구현 | CSS Grid 10칸 | ⬜ |
| AT-009 | 플레이어 상태 표시 | Active/Dealt/Folded/Empty | 동일 구현 | State enum | ⬜ |
| AT-010 | Action-on 하이라이트 | 현재 차례 강조 | 동일 구현 | CSS 클래스 | ⬜ |
| AT-011 | 포지션 표시 | DLR/SB/BB 버튼 | 동일 구현 | 아이콘 오버레이 | ⬜ |

#### 2.1.4 액션 입력

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-012 | 기본 액션 버튼 | FOLD/CHECK/CALL/BET/ALL-IN | 동일 구현 | 버튼 그룹 | ⬜ |
| AT-013 | UNDO 버튼 | 마지막 액션 취소 | 동일 구현 | Action Stack | ⬜ |
| AT-014 | 키보드 단축키 | F/C/B/A | 동일 구현 | addEventListener | ⬜ |

#### 2.1.5 베팅 입력

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-015 | 베팅 금액 직접 입력 | 숫자 키패드 | 동일 구현 | NumberInput | ⬜ |
| AT-016 | +/- 조정 버튼 | 금액 증감 | 동일 구현 | Step 버튼 | ⬜ |
| AT-017 | Quick Bet 버튼 | MIN/2xBB/3xBB/½POT/POT/ALL-IN | 동일 구현 | 사전 계산 버튼 | ⬜ |
| AT-018 | Min/Max 범위 표시 | 유효 베팅 범위 | 동일 구현 | 계산 로직 | ⬜ |

#### 2.1.6 보드 관리

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-019 | Community Cards 표시 | 5장 보드 | 동일 구현 | CardGrid 컴포넌트 | ⬜ |
| AT-020 | 보드 카드 업데이트 | Flop/Turn/River 진행 | 동일 구현 | State 업데이트 | ⬜ |

#### 2.1.7 하단 컨트롤

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| AT-021 | HIDE GFX | 오버레이 숨김/표시 | 동일 구현 | Visibility toggle | ⬜ |
| AT-022 | TAG HAND | 핸드 북마크 | 동일 구현 | DB tagged 필드 | ⬜ |
| AT-023 | ADJUST STACK | 칩 스택 수동 조정 | 동일 구현 | Input 모달 | ⬜ |
| AT-024 | CHOP | 팟 나누기 | 동일 구현 | N-way split 계산 | ⬜ |
| AT-025 | RUN IT 2x | 보드 2번 런 | 동일 구현 | 보드 복제 로직 | ⬜ |
| AT-026 | MISS DEAL | 미스딜 처리 | 동일 구현 | 핸드 무효화 | ⬜ |

### 2.2 Pre-Start Setup 기능 (13개)

#### 2.2.1 게임 설정

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-001 | Event Name 입력 | 이벤트명 설정 | 동일 구현 | TextInput | ⬜ |
| PS-002 | Game Type 선택 | NLHE/PLO/PLO5 | 동일 구현 | Select 드롭다운 | ⬜ |
| PS-003 | Min Chip 설정 | 최소 칩 단위 | 동일 구현 | NumberInput | ⬜ |

#### 2.2.2 플레이어 설정

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-004 | 플레이어 이름 입력 | 각 좌석별 이름 | 동일 구현 | 좌석별 TextInput | ⬜ |
| PS-005 | 칩 스택 입력 | 시작 칩 스택 | 동일 구현 | NumberInput | ⬜ |
| PS-006 | 포지션 할당 | DLR/SB/BB 배치 | 동일 구현 | 화살표 버튼 | ⬜ |
| PS-007 | 카드 감지 상태 | RFID 2장 감지 | 동일 구현 | WebSocket 실시간 | ⬜ |

#### 2.2.3 블라인드/앤티 설정

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-008 | Ante/SB/BB/3rd Blind | 입력 | 동일 구현 | NumberInput 그룹 | ⬜ |
| PS-009 | Straddle 추가 | 스트래들 활성화 | 동일 구현 | Checkbox + NumberInput | ⬜ |

#### 2.2.4 딜러 포지션

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-010 | Dealer/SB/BB 위치 조정 | 화살표로 변경 | 동일 구현 | 순환 로직 | ⬜ |

#### 2.2.5 보드 설정

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-011 | Board Count 선택 | SINGLE/DOUBLE/TRIPLE | 동일 구현 | Radio 버튼 | ⬜ |

#### 2.2.6 시작

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| PS-012 | TRACK THE ACTION 버튼 | 핸드 시작 | 동일 구현 | API 호출 | ⬜ |
| PS-013 | AUTO 모드 | RFID 자동 감지 시작 | 동일 구현 | WebSocket 트리거 | ⬜ |

### 2.3 Viewer Overlay 기능 (14개)

#### 2.3.1 상단 바 (Top Bar)

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| VO-001 | Event Logo 표시 | ✓ | 동일 구현 | Image 컴포넌트 | ⬜ |
| VO-002 | Blinds 정보 | SB/BB/Ante | 동일 구현 | WebSocket 동기화 | ⬜ |
| VO-003 | Chip Counts | 5-6명 플레이어 (스크롤) | 동일 구현 | Horizontal scroll | ⬜ |
| VO-004 | Broadcaster Logo 표시 | ✓ | 동일 구현 | Image 컴포넌트 | ⬜ |

#### 2.3.2 Player HUD (좌측 하단)

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| VO-005 | Hole Cards 표시 | HUD 위 겹치는 카드 2장 | 동일 구현 | absolute positioning | ⬜ |
| VO-006 | Player Name + Stack | 이름 및 칩 스택 | 동일 구현 | Text 오버레이 | ⬜ |
| VO-007 | 마지막 액션 표시 | CHECK/BET/RAISE | 동일 구현 | WebSocket 실시간 | ⬜ |
| VO-008 | Equity % 표시 | 실시간 승률 | 동일 구현 | Monte Carlo 계산 | ⬜ |

#### 2.3.3 우측 패널 (컴팩트 3-Grid)

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| VO-009 | Board Cards | 5장 커뮤니티 카드 | 동일 구현 | CardGrid | ⬜ |
| VO-010 | Pot Display | 현재 팟 금액 | 동일 구현 | WebSocket 동기화 | ⬜ |
| VO-011 | Event Info | 이벤트명 및 게임 타입 | 동일 구현 | Config 기반 | ⬜ |

#### 2.3.4 상태 표시 (좌측 상단)

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| VO-012 | Street 표시 | PREFLOP/FLOP/TURN/RIVER | 동일 구현 | State 기반 | ⬜ |
| VO-013 | To Act 표시 | 현재 차례 플레이어 | 동일 구현 | WebSocket 동기화 | ⬜ |

#### 2.3.5 Folded State

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| VO-014 | Folded Player 스타일 | 회색 처리 + Equity 숨김 | 동일 구현 | CSS filter: grayscale | ⬜ |

### 2.4 GFX Console (Production Dashboard) 기능 (25개)

#### 2.4.1 통계 표시 모드

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-001 | Seat 순서 | 좌석 순서대로 | 동일 구현 | Sort by seat | ⬜ |
| GC-002 | Stack 순위 | 칩 스택 순위 | 동일 구현 | Sort by stack | ⬜ |
| GC-003 | VPIP% | 자발적 참여율 | 동일 구현 | DB 집계 쿼리 | ⬜ |
| GC-004 | PFR% | 프리플랍 레이즈 | 동일 구현 | DB 집계 쿼리 | ⬜ |
| GC-005 | AGRfq% | 공격 빈도 | 동일 구현 | DB 집계 쿼리 | ⬜ |
| GC-006 | WTSD% | 쇼다운 도달률 | 동일 구현 | DB 집계 쿼리 | ⬜ |
| GC-007 | WIN | 순수익 | 동일 구현 | 팟 합산 | ⬜ |
| GC-008 | Payouts | 상금 | 동일 구현 | 입력 필드 | ⬜ |

#### 2.4.2 리더보드

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-009 | 플레이어 순위 테이블 | Stack/VPIP/PFR/AGR/WTSD | 동일 구현 | Table 컴포넌트 | ⬜ |
| GC-010 | Chip Bar 그래프 | 상대적 스택 크기 | 동일 구현 | SVG BarChart | ⬜ |
| GC-011 | Stat Bar 그래프 | 각 스탯 시각화 | 동일 구현 | SVG 수평 바 | ⬜ |
| GC-012 | 정렬 기능 | STACK/NAME/SEAT | 동일 구현 | Table 헤더 클릭 | ⬜ |

#### 2.4.3 필드 정보

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-013 | Total Field | 전체 참가자 수 | 동일 구현 | DB COUNT | ⬜ |
| GC-014 | Remaining | 남은 참가자 수 | 동일 구현 | 활성 플레이어 COUNT | ⬜ |
| GC-015 | Avg Stack | 평균 스택 | 동일 구현 | DB AVG | ⬜ |
| GC-016 | Total Chips | 전체 칩 | 동일 구현 | DB SUM | ⬜ |

#### 2.4.4 컨트롤

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-017 | LIVE Stats 토글 | 실시간 통계 업데이트 | 동일 구현 | WebSocket 구독 | ⬜ |
| GC-018 | Show Eliminated 토글 | 탈락자 표시/숨김 | 동일 구현 | Filter 조건 | ⬜ |
| GC-019 | PIP Display | Picture-in-Picture | 동일 구현 | Browser PIP API | ⬜ |
| GC-020 | Export CSV | 통계 CSV 내보내기 | 동일 구현 | File Download | ⬜ |

#### 2.4.5 티커

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-021 | Ticker Message 입력 | 우→좌 스크롤 | 동일 구현 | CSS animation | ⬜ |

#### 2.4.6 시스템 상태

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-022 | System Status Panel | RFID/WebSocket/DB/OBS | 동일 구현 | Health Check API | ⬜ |
| GC-023 | Quick Actions | New Table/Add Player/Reset/Test Card | 동일 구현 | 버튼 그룹 | ⬜ |

#### 2.4.7 라이브 프리뷰

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-024 | Overlay Preview | 960x540 미리보기 | 동일 구현 | iframe 임베드 | ⬜ |

#### 2.4.8 Recent Hands

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| GC-025 | 최근 핸드 목록 | Hand#/Winner/Pot/Board | 동일 구현 | DB 최근 10건 쿼리 | ⬜ |

### 2.5 Security 기능 (11개)

#### 2.5.1 Trustless Mode

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| SEC-001 | 운영자 카드 정보 차단 | 30초 딜레이 | 동일 구현 | UID Buffer Queue | ⬜ |
| SEC-002 | 카운트다운 표시 | T=0 → T=30 타이머 | 동일 구현 | Countdown 컴포넌트 | ⬜ |
| SEC-003 | DB 조회 지연 실행 | 딜레이 후 조회 | 동일 구현 | setTimeout + DB | ⬜ |

#### 2.5.2 Realtime Mode

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| SEC-004 | 즉시 카드 정보 표시 | DB 즉시 조회 | 동일 구현 | Direct DB Query | ⬜ |
| SEC-005 | 운영자 실시간 확인 | 지연 없음 | 동일 구현 | 기본 모드 | ⬜ |

#### 2.5.3 암호화 레이어

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| SEC-006 | RFID Card 암호화 | AES-128 DESFire EV3 | 동일 구현 | DESFire 라이브러리 | ⬜ |
| SEC-007 | Serial 암호화 | ChaCha20 + HMAC | 동일 구현 | cryptography 라이브러리 | ⬜ |
| SEC-008 | Database 암호화 | AES-256-GCM SQLCipher | 동일 구현 | SQLCipher 적용 | ⬜ |
| SEC-009 | WebSocket 암호화 | TLS 1.3 WSS | 동일 구현 | wss:// 프로토콜 | ⬜ |

#### 2.5.4 모드 전환

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| SEC-010 | Trustless/Realtime 토글 | GFX Console에서 전환 | 동일 구현 | Config API | ⬜ |
| SEC-011 | Delay 시간 설정 | 초 단위 조정 (기본 30초) | 동일 구현 | NumberInput | ⬜ |

### 2.6 Equity & Statistics 기능 (19개)

#### 2.6.1 승률 비교

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| EQ-001 | 헤즈업 Equity 계산 | Player A vs B | 동일 구현 | Monte Carlo 10,000회 | ⬜ |
| EQ-002 | Hole Cards 표시 | 각 플레이어 핸드 | 동일 구현 | Card 컴포넌트 | ⬜ |
| EQ-003 | Equity % 표시 | 실시간 승률 | 동일 구현 | Percentage 표시 | ⬜ |

#### 2.6.2 보드 상태

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| EQ-004 | Community Cards 표시 | Flop/Turn/River | 동일 구현 | CardGrid | ⬜ |
| EQ-005 | Pending Cards 표시 | [?] 미지의 카드 | 동일 구현 | Placeholder | ⬜ |

#### 2.6.3 아웃츠 분석

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| EQ-006 | Outs 카드 리스트 | 역전 가능한 카드 목록 | 동일 구현 | Card List | ⬜ |
| EQ-007 | Total Outs 카운트 | 총 아웃츠 수 | 동일 구현 | Count 표시 | ⬜ |
| EQ-008 | Turn Hit % | 턴에서 맞을 확률 | 동일 구현 | (Outs/47) * 100 | ⬜ |
| EQ-009 | Turn + River % | 턴+리버 복합 확률 | 동일 구현 | 1-(1-p)^2 | ⬜ |
| EQ-010 | Odds 계산 | 예: 4.2:1 | 동일 구현 | (100-p)/p 계산 | ⬜ |

#### 2.6.4 승리 시나리오

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| EQ-011 | 시나리오별 확률 | Full House/Straight/Backdoor | 동일 구현 | 시나리오 분석 | ⬜ |
| EQ-012 | 확률 % 표시 | 각 시나리오 승률 | 동일 구현 | Percentage 표시 | ⬜ |

#### 2.6.5 플레이어 상세 스탯

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| ST-001 | VPIP% | 자발적 참여율 | 동일 구현 | (참여핸드/총핸드)*100 | ⬜ |
| ST-002 | PFR% | 프리플랍 레이즈 | 동일 구현 | (레이즈핸드/총핸드)*100 | ⬜ |
| ST-003 | AGRfq% | 공격 빈도 | 동일 구현 | (베팅+레이즈)/(베팅+콜) | ⬜ |
| ST-004 | WTSD% | 쇼다운 도달률 | 동일 구현 | (쇼다운/참여핸드)*100 | ⬜ |
| ST-005 | 3Bet% | 3벳 비율 | 동일 구현 | (3벳/기회)*100 | ⬜ |
| ST-006 | Fold to 3Bet% | 3벳에 폴드 비율 | 동일 구현 | (폴드/3벳 당함)*100 | ⬜ |
| ST-007 | Continuation Bet% | 컨티뉴에이션 벳 | 동일 구현 | (CB/기회)*100 | ⬜ |

### 2.7 Hand History 기능 (11개)

#### 2.7.1 필터링

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| HH-001 | Player 필터 | 특정 플레이어 핸드 | 동일 구현 | WHERE player_id | ⬜ |
| HH-002 | Date 필터 | 날짜별 필터링 | 동일 구현 | WHERE date BETWEEN | ⬜ |
| HH-003 | Result 필터 | Win/Lose | 동일 구현 | WHERE result | ⬜ |

#### 2.7.2 핸드 목록

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| HH-004 | 핸드 목록 테이블 | Hand#/Time/Players/Winner/Pot/Board | 동일 구현 | Table 컴포넌트 | ⬜ |
| HH-005 | 선택한 핸드 상세 | 클릭 시 상세 표시 | 동일 구현 | 모달 또는 패널 | ⬜ |
| HH-006 | Pagination | 페이지 네비게이션 | 동일 구현 | LIMIT OFFSET | ⬜ |

#### 2.7.3 핸드 상세

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| HH-007 | Hole Cards 표시 | Winner/Loser 카드 | 동일 구현 | Card 컴포넌트 | ⬜ |
| HH-008 | Board 표시 | 5장 커뮤니티 카드 | 동일 구현 | CardGrid | ⬜ |
| HH-009 | Timeline | Preflop/Flop/Turn/River 흐름 | 동일 구현 | Timeline 컴포넌트 | ⬜ |
| HH-010 | Action 로그 | Player/Action Type/Amount | 동일 구현 | 액션 리스트 | ⬜ |

#### 2.7.4 내보내기

| ID | 기능 | PokerGFX | EBS Stage 1 | 구현 방법 | 상태 |
|----|------|----------|-------------|----------|------|
| HH-011 | Export 버튼 | CSV/JSON 파일 | 동일 구현 | File Download | ⬜ |

---

## 3. UI/UX 복제 상세

### 3.1 Action Tracker UI

**레이아웃 복제 대상:**
- **버튼 위치 및 크기**: PokerGFX와 동일한 그리드 레이아웃
- **색상 스킴**: 다크 테마 유지 (커스터마이징 가능)
- **키보드 단축키**: F (Fold), C (Check), B (Bet), A (All-In)
- **플레이어 그리드**: 10칸 레이아웃, 좌석 번호 표시

**중요 포인트:**
- Action-on 플레이어는 밝은 테두리 강조
- Folded 플레이어는 회색 처리
- DLR/SB/BB 버튼은 아이콘으로 표시

### 3.2 Viewer Overlay 레이아웃

**복제 대상:**
- **카드 표시 위치**: 좌측 하단 Player HUD 위로 겹침
- **HUD 레이아웃**: 수직 스택 (이름 → 스택 → 액션 → Equity)
- **애니메이션 타이밍**: 카드 등장 200ms fade-in
- **상단 바**: Event Logo (좌) | Blinds | Chip Counts | Broadcaster Logo (우)
- **우측 패널**: 보드 카드 (상) | 팟 (중) | 이벤트 정보 (하)

**중요 포인트:**
- OBS Browser Source 최적화 (투명 배경)
- Folded 플레이어는 자동 회색 처리
- Equity %는 실시간 업데이트

### 3.3 GFX Console 레이아웃

**복제 대상:**
- **리더보드 테이블**: 플레이어 목록 + 스탯 컬럼
- **Chip Bar 그래프**: 각 플레이어 상대적 스택 크기
- **System Status**: RFID/WebSocket/DB/OBS 상태 아이콘
- **Quick Actions**: New Table, Add Player, Reset, Test Card 버튼
- **Overlay Preview**: 960x540 iframe 미리보기

---

## 4. 데이터 모델

### 4.1 핸드 데이터 구조

```typescript
interface Hand {
  id: number;
  timestamp: string;
  gameType: 'NLHE' | 'PLO' | 'PLO5' | 'SHORT_DECK';
  blinds: {
    sb: number;
    bb: number;
    ante?: number;
    straddle?: number;
  };
  players: Player[];
  board: Card[];
  pot: number;
  street: 'PREFLOP' | 'FLOP' | 'TURN' | 'RIVER';
  actions: Action[];
  winner?: number; // seat number
  winnerHand?: string; // hand rank
  tagged: boolean; // AT-022
}
```

### 4.2 플레이어 데이터 구조

```typescript
interface Player {
  id: number;
  seat: number;
  name: string;
  position: 'DLR' | 'SB' | 'BB' | 'UTG' | 'UTG1' | 'MP' | 'CO' | 'BTN';
  holeCards: Card[];
  stack: number;
  status: 'active' | 'folded' | 'allin' | 'eliminated';
  stats: PlayerStats;
}

interface PlayerStats {
  vpip: number; // %
  pfr: number; // %
  agrfq: number; // %
  wtsd: number; // %
  threebet: number; // %
  foldTo3Bet: number; // %
  cbet: number; // %
  handsPlayed: number;
  totalWon: number;
}
```

### 4.3 액션 데이터 구조

```typescript
interface Action {
  id: number;
  handId: number;
  seat: number;
  street: 'PREFLOP' | 'FLOP' | 'TURN' | 'RIVER';
  actionType: 'FOLD' | 'CHECK' | 'CALL' | 'BET' | 'RAISE' | 'ALLIN';
  amount?: number;
  timestamp: string;
}
```

### 4.4 Equity 데이터 구조

```typescript
interface Equity {
  playerA: {
    seat: number;
    holeCards: Card[];
    equity: number; // %
    outs: Card[];
    scenarios: Scenario[];
  };
  playerB: {
    seat: number;
    holeCards: Card[];
    equity: number; // %
    outs: Card[];
    scenarios: Scenario[];
  };
  board: Card[];
}

interface Scenario {
  handType: string; // "Full House", "Straight", etc.
  probability: number; // %
}
```

---

## 5. 운영자 워크플로우

### 5.1 핸드 시작 → 종료 전체 흐름

```
1. Pre-Start Setup (PS-001~013)
   ├── 이벤트명 입력 (PS-001)
   ├── 게임 타입 선택 (PS-002)
   ├── 플레이어 이름 입력 (PS-004)
   ├── 칩 스택 입력 (PS-005)
   ├── 블라인드 설정 (PS-008)
   ├── 딜러 버튼 위치 설정 (PS-010)
   └── TRACK THE ACTION 버튼 (PS-012) 또는 AUTO 모드 (PS-013)

2. Hand Start
   ├── 딜러 버튼 자동 이동 (AT-011)
   ├── SB/BB 자동 포스팅 (AT-006)
   └── 홀카드 RFID 스캔 (PS-007) → WebSocket 실시간 표시

3. Preflop Betting Round
   ├── Action-on 플레이어 하이라이트 (AT-010)
   ├── 액션 버튼 클릭 (AT-012)
   │   ├── FOLD → 플레이어 회색 처리 (AT-009)
   │   ├── CHECK → 팟 유지
   │   ├── CALL → 팟 증가
   │   ├── BET/RAISE → 베팅 금액 입력 (AT-015~017)
   │   └── ALL-IN → 전체 스택 팟 이동
   └── 다음 플레이어로 자동 이동

4. Flop (보드 3장)
   ├── 보드 카드 자동 업데이트 (AT-020)
   ├── Equity % 실시간 계산 (VO-008, EQ-001~003)
   └── Betting Round 반복

5. Turn (보드 4장)
   ├── 보드 카드 추가 (AT-020)
   ├── Equity % 재계산
   └── Betting Round 반복

6. River (보드 5장)
   ├── 보드 카드 추가 (AT-020)
   ├── Equity % 재계산
   └── Final Betting Round

7. Showdown
   ├── 위너 자동 판정 (핸드 랭크 계산)
   ├── 팟 분배 (또는 CHOP, AT-024)
   ├── 히스토리 저장 (HH-004~010)
   └── 통계 업데이트 (ST-001~007)

8. Next Hand
   ├── 버튼 자동 이동
   ├── 스택 자동 업데이트
   └── 1번으로 돌아감
```

### 5.2 수동 입력 목록

| 입력 항목 | 방식 | 빈도 | 비고 |
|----------|------|------|------|
| 플레이어 액션 | 버튼 클릭 (AT-012) | 매 액션 | F/C/B/A 키보드 단축키 |
| 베팅 금액 | Quick Bet (AT-017) 또는 직접 입력 (AT-015) | 베팅 시 | MIN/2xBB/½POT/POT/ALL-IN |
| 칩 카운트 | 핸드 시작 시 입력 (PS-005) | 핸드당 1회 | 또는 ADJUST STACK (AT-023) |
| 플레이어 추가/제거 | 좌석 클릭 + 이름 입력 (PS-004) | 필요 시 | - |
| 딜러 버튼 위치 | 화살표 버튼 (PS-010) | 핸드 시작 시 | 자동 이동 가능 |
| 보드 카드 (수동) | 카드 선택 UI (AT-019~020) | RFID 실패 시 | 백업용 |

### 5.3 자동화된 항목

| 항목 | 자동화 방법 |
|------|------------|
| 홀카드 인식 | RFID 자동 스캔 → WebSocket 전송 |
| 팟 계산 | 매 액션 후 자동 합산 |
| Equity % | Monte Carlo 실시간 계산 (< 100ms) |
| 통계 업데이트 | 핸드 종료 시 DB 집계 쿼리 |
| 핸드 번호 | DB auto_increment |
| 버튼 이동 | 핸드 종료 시 자동 순환 |

---

## 6. 기술 구현

### 6.1 RFID 하드웨어

| 구성 | 사양 | 수량 |
|------|------|------|
| 컨트롤러 | ESP32-WROOM-32 | 1개 |
| 리더 | MFRC522 (13.56MHz) | 10개 (각 좌석) |
| 카드 | MIFARE Classic 1K (또는 DESFire EV3) | 52장 + 조커 2장 |
| 통신 | USB Serial (115200 baud) | 1개 (ESP32 → PC) |
| 전원 | 5V 3A | 1개 |

**Wiring (ESP32 → MFRC522)**:
- VCC: 3.3V
- GND: GND
- SDA: GPIO5 (SPI SS)
- SCK: GPIO18 (SPI Clock)
- MOSI: GPIO23
- MISO: GPIO19
- RST: GPIO4

### 6.2 서버 아키텍처

```
FastAPI Server (Python 3.11+)
├── /api/cards
│   ├── GET /api/cards - 전체 카드 목록
│   ├── GET /api/cards/{uid} - UID로 카드 조회
│   ├── POST /api/cards - 카드 등록
│   └── DELETE /api/cards/{uid} - 카드 삭제
├── /api/hands
│   ├── GET /api/hands - 핸드 목록 (필터링 지원)
│   ├── GET /api/hands/{id} - 핸드 상세
│   ├── POST /api/hands - 새 핸드 시작
│   ├── PUT /api/hands/{id} - 핸드 업데이트
│   └── DELETE /api/hands/{id} - 핸드 삭제
├── /api/players
│   ├── GET /api/players - 플레이어 목록
│   ├── GET /api/players/{id} - 플레이어 상세
│   ├── POST /api/players - 플레이어 추가
│   ├── PUT /api/players/{id} - 플레이어 정보 수정
│   └── DELETE /api/players/{id} - 플레이어 삭제
├── /api/actions
│   ├── POST /api/actions - 액션 기록
│   ├── DELETE /api/actions/{id} - 액션 취소 (UNDO)
│   └── GET /api/actions?hand_id={id} - 핸드별 액션 목록
├── /api/equity
│   ├── POST /api/equity/calculate - 승률 계산 (헤즈업)
│   └── POST /api/equity/outs - 아웃츠 분석
├── /api/stats
│   ├── GET /api/stats/player/{id} - 플레이어 상세 스탯
│   └── GET /api/stats/leaderboard - 리더보드
├── /api/config
│   ├── GET /api/config - 현재 설정 조회
│   └── PUT /api/config - 설정 업데이트 (Trustless Mode 등)
└── /ws - WebSocket 엔드포인트
    ├── card_detected - RFID 카드 감지
    ├── action_recorded - 액션 기록
    ├── pot_updated - 팟 업데이트
    ├── equity_updated - 승률 업데이트
    └── system_status - 시스템 상태
```

### 6.3 프론트엔드 구조

```
React App (TypeScript, Vite)
├── src/
│   ├── components/
│   │   ├── ActionTracker/
│   │   │   ├── StatusBar.tsx (AT-001~004)
│   │   │   ├── GameSettings.tsx (AT-005~007)
│   │   │   ├── PlayerGrid.tsx (AT-008~011)
│   │   │   ├── ActionButtons.tsx (AT-012~014)
│   │   │   ├── BetInput.tsx (AT-015~018)
│   │   │   ├── BoardCards.tsx (AT-019~020)
│   │   │   └── BottomControls.tsx (AT-021~026)
│   │   ├── PreStartSetup/
│   │   │   ├── GameSetup.tsx (PS-001~003)
│   │   │   ├── PlayerSetup.tsx (PS-004~007)
│   │   │   ├── BlindsSetup.tsx (PS-008~009)
│   │   │   ├── PositionSetup.tsx (PS-010)
│   │   │   └── StartButton.tsx (PS-012~013)
│   │   ├── ViewerOverlay/
│   │   │   ├── TopBar.tsx (VO-001~004)
│   │   │   ├── PlayerHUD.tsx (VO-005~008)
│   │   │   ├── RightPanel.tsx (VO-009~011)
│   │   │   ├── StatusDisplay.tsx (VO-012~013)
│   │   │   └── FoldedState.tsx (VO-014)
│   │   ├── GFXConsole/
│   │   │   ├── StatsDisplay.tsx (GC-001~008)
│   │   │   ├── Leaderboard.tsx (GC-009~012)
│   │   │   ├── FieldInfo.tsx (GC-013~016)
│   │   │   ├── Controls.tsx (GC-017~020)
│   │   │   ├── Ticker.tsx (GC-021)
│   │   │   ├── SystemStatus.tsx (GC-022~023)
│   │   │   ├── OverlayPreview.tsx (GC-024)
│   │   │   └── RecentHands.tsx (GC-025)
│   │   ├── Security/
│   │   │   ├── TrustlessMode.tsx (SEC-001~003)
│   │   │   ├── RealtimeMode.tsx (SEC-004~005)
│   │   │   └── ModeToggle.tsx (SEC-010~011)
│   │   ├── Equity/
│   │   │   ├── EquityDisplay.tsx (EQ-001~003)
│   │   │   ├── BoardState.tsx (EQ-004~005)
│   │   │   ├── OutsAnalysis.tsx (EQ-006~010)
│   │   │   └── WinScenarios.tsx (EQ-011~012)
│   │   ├── HandHistory/
│   │   │   ├── Filters.tsx (HH-001~003)
│   │   │   ├── HandList.tsx (HH-004~006)
│   │   │   ├── HandDetail.tsx (HH-007~010)
│   │   │   └── ExportButton.tsx (HH-011)
│   │   └── shared/
│   │       ├── Card.tsx
│   │       ├── CardGrid.tsx
│   │       ├── Button.tsx
│   │       └── NumberInput.tsx
│   ├── hooks/
│   │   ├── useWebSocket.ts - WebSocket 연결 관리
│   │   ├── useActionTracker.ts - 액션 입력 상태
│   │   ├── useEquityCalculator.ts - 승률 계산
│   │   └── useHandHistory.ts - 핸드 히스토리 조회
│   ├── services/
│   │   ├── api.ts - REST API 호출
│   │   ├── websocket.ts - WebSocket 클라이언트
│   │   └── equity.ts - 승률 계산 로직
│   ├── types/
│   │   ├── hand.ts
│   │   ├── player.ts
│   │   ├── action.ts
│   │   └── equity.ts
│   └── App.tsx
├── public/
│   ├── logos/ - Event Logo, Broadcaster Logo
│   └── cards/ - 카드 이미지 (52장 + 조커)
└── package.json
```

### 6.4 데이터베이스 스키마 (SQLite + SQLCipher)

```sql
-- cards 테이블 (카드 UID → 카드 정보 매핑)
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    suit TEXT NOT NULL, -- spades, hearts, diamonds, clubs, joker
    rank TEXT NOT NULL, -- A, 2~10, J, Q, K, JOKER
    display TEXT NOT NULL, -- A♠, 2♥, etc.
    value INTEGER NOT NULL -- 1-14 (Ace=1 or 14)
);

-- players 테이블
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    seat INTEGER, -- NULL if not seated
    stack INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active', -- active, eliminated
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- hands 테이블
CREATE TABLE hands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_type TEXT NOT NULL, -- NLHE, PLO, PLO5, SHORT_DECK
    sb INTEGER NOT NULL,
    bb INTEGER NOT NULL,
    ante INTEGER DEFAULT 0,
    straddle INTEGER DEFAULT 0,
    street TEXT NOT NULL DEFAULT 'PREFLOP', -- PREFLOP, FLOP, TURN, RIVER
    pot INTEGER NOT NULL DEFAULT 0,
    board TEXT, -- JSON array of card UIDs
    dealer_seat INTEGER NOT NULL,
    winner_seat INTEGER,
    winner_hand TEXT,
    tagged BOOLEAN NOT NULL DEFAULT FALSE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
);

-- hand_players 테이블 (핸드별 플레이어 참여 정보)
CREATE TABLE hand_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hand_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    seat INTEGER NOT NULL,
    position TEXT NOT NULL, -- DLR, SB, BB, UTG, etc.
    hole_cards TEXT, -- JSON array of card UIDs
    starting_stack INTEGER NOT NULL,
    ending_stack INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active', -- active, folded, allin
    FOREIGN KEY (hand_id) REFERENCES hands(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- actions 테이블
CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hand_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    seat INTEGER NOT NULL,
    street TEXT NOT NULL, -- PREFLOP, FLOP, TURN, RIVER
    action_type TEXT NOT NULL, -- FOLD, CHECK, CALL, BET, RAISE, ALLIN
    amount INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hand_id) REFERENCES hands(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- config 테이블 (시스템 설정)
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- 초기 설정 데이터
INSERT INTO config (key, value) VALUES
    ('trustless_mode', 'false'),
    ('delay_seconds', '30'),
    ('event_name', 'EBS Poker'),
    ('event_logo', ''),
    ('broadcaster_logo', '');

-- 인덱스
CREATE INDEX idx_actions_hand_id ON actions(hand_id);
CREATE INDEX idx_hand_players_hand_id ON hand_players(hand_id);
CREATE INDEX idx_hand_players_player_id ON hand_players(player_id);
```

---

## 7. 주차별 개발 계획

### Week 1-2: Alpha (RFID + 기본 오버레이)

| 주차 | 기능 | Definition of Done | 담당 컴포넌트 |
|------|------|-------------------|--------------|
| 1 | RFID 카드 인식 | 스캔 → 화면 < 200ms | firmware/rfid_reader, server/serial |
| 1 | DB 카드 매핑 | UID → 카드 정보 조회 성공률 100% | server/db, tools/card_mapper |
| 1 | WebSocket 실시간 | 카드 감지 → 프론트엔드 < 50ms | server/websocket, frontend/useWebSocket |
| 2 | 기본 오버레이 UI | OBS Browser Source 연동 | frontend/ViewerOverlay |
| 2 | Player HUD | 카드 2장 + 이름 + 스택 표시 | VO-005~006 |
| 2 | Board Cards | 5장 보드 표시 | VO-009, AT-019~020 |

**Milestone 검증:**
- [ ] RFID 카드 10장 연속 스캔 < 200ms
- [ ] WebSocket 메시지 100개 전송 < 50ms
- [ ] OBS에서 오버레이 표시 확인

### Week 3-4: Beta (Action Tracker 완성)

| 주차 | 기능 | Definition of Done | 담당 컴포넌트 |
|------|------|-------------------|--------------|
| 3 | Action Tracker 그리드 | 10인 좌석 레이아웃 + 상태 표시 | AT-008~011 |
| 3 | 액션 입력 버튼 | FOLD/CHECK/CALL/BET/ALL-IN | AT-012 |
| 3 | 베팅 금액 입력 | Quick Bet + 직접 입력 | AT-015~017 |
| 4 | 팟 자동 계산 | 매 액션 후 팟 업데이트 | server/hand_logic |
| 4 | UNDO 기능 | 마지막 액션 취소 | AT-013 |
| 4 | 키보드 단축키 | F/C/B/A 키 매핑 | AT-014 |

**Milestone 검증:**
- [ ] 10명 플레이어 핸드 진행 (Preflop → River)
- [ ] 팟 계산 정확도 100% (수동 검증)
- [ ] UNDO 버튼 정상 동작

### Week 5-6: RC (플레이어 관리 + 통계)

| 주차 | 기능 | Definition of Done | 담당 컴포넌트 |
|------|------|-------------------|--------------|
| 5 | Pre-Start Setup | 플레이어 이름/칩/포지션 입력 | PS-001~010 |
| 5 | GFX Console 기본 | 시스템 상태 + Quick Actions | GC-022~023 |
| 5 | Overlay Preview | 960x540 미리보기 | GC-024 |
| 6 | 플레이어 스탯 | VPIP/PFR/AGR/WTSD 계산 | ST-001~007, GC-003~006 |
| 6 | 리더보드 | 플레이어 순위 테이블 | GC-009~012 |
| 6 | 승률 계산 (헤즈업) | Monte Carlo < 100ms | EQ-001~003 |

**Milestone 검증:**
- [ ] Pre-Start Setup 완료 → 핸드 시작
- [ ] 플레이어 스탯 계산 정확도 검증 (샘플 100핸드)
- [ ] 승률 계산 < 100ms (헤즈업 10,000회 시뮬레이션)

### Week 7-8: Release (Trustless Mode + 테스트)

| 주차 | 기능 | Definition of Done | 담당 컴포넌트 |
|------|------|-------------------|--------------|
| 7 | Trustless Mode | 30초 딜레이 버퍼링 | SEC-001~003 |
| 7 | 암호화 레이어 | Serial/DB/WebSocket 암호화 | SEC-006~009 |
| 7 | Hand History | 핸드 목록 + 필터링 + 상세 | HH-001~010 |
| 8 | 아웃츠 분석 | 아웃츠 카드 리스트 + 확률 | EQ-006~010 |
| 8 | 통합 테스트 | 4시간 연속 운영 (에러 0건) | - |
| 8 | 운영자 검증 | 2명 이상 "동일 수준" 서명 | - |

**Milestone 검증:**
- [ ] Trustless Mode: 30초 딜레이 후 카드 정보 표시
- [ ] 암호화: SQLCipher DB 암호화 확인
- [ ] 4시간 방송 테스트 (에러 0건, 카드 인식 실패 < 1%)
- [ ] 운영자 2명 "PokerGFX와 동일 수준" 서명

---

## 8. 성공 기준

### 8.1 기능 완성도

- [ ] **54개 기능 100% 완료**: PokerGFX-Feature-Checklist.md 모든 체크박스 ✅
- [ ] **Action Tracker**: AT-001~026 (26개)
- [ ] **Pre-Start Setup**: PS-001~013 (13개)
- [ ] **Viewer Overlay**: VO-001~014 (14개)
- [ ] **GFX Console**: GC-001~025 (25개)
- [ ] **Security**: SEC-001~011 (11개)
- [ ] **Equity & Stats**: EQ-001~012, ST-001~007 (19개)
- [ ] **Hand History**: HH-001~011 (11개)

### 8.2 성능 요구사항

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| **카드 인식 속도** | < 200ms | RFID 스캔 → WebSocket 메시지 수신 |
| **승률 계산 속도** | < 100ms | Monte Carlo 10,000회 시뮬레이션 |
| **UI 응답 속도** | < 50ms | 버튼 클릭 → 화면 업데이트 |
| **WebSocket 지연** | < 50ms | 서버 → 클라이언트 메시지 전송 |
| **시스템 가동률** | 99.9% | 4시간 방송 테스트 (에러 < 1건/1000 액션) |
| **카드 인식 실패율** | < 1% | 1000회 스캔 중 실패 < 10회 |

### 8.3 사용성 검증

- [ ] **운영자 2명+ 서명**: "PokerGFX와 동일 수준" 확인서
- [ ] **4시간 방송 테스트**: 에러 0건, 운영자 피드백 수집
- [ ] **키보드 단축키**: F/C/B/A 키 정상 동작
- [ ] **UNDO 기능**: 마지막 액션 취소 정상 동작
- [ ] **팟 계산 정확도**: 100핸드 수동 검증 100% 일치

### 8.4 보안 검증

- [ ] **Trustless Mode**: 30초 딜레이 정상 동작
- [ ] **암호화**: SQLCipher DB 암호화 확인
- [ ] **WebSocket 암호화**: WSS (TLS 1.3) 연결 확인
- [ ] **Serial 암호화**: ChaCha20 + HMAC 정상 동작

---

## 9. Stage 1 Gate (정량적 전환 조건)

**Gate 시기**: 2026년 12월

Stage 2 착수를 위해 다음 조건을 **모두** 충족해야 합니다:

| 조건 | 기준 | 검증 방법 | 책임자 |
|------|------|----------|--------|
| **기능 구현** | PokerGFX-Feature-Checklist.md 100% 완료 (54/54) | 체크리스트 검토 | 개발팀 |
| **방송 테스트** | 4시간 연속 운영, 에러 0건 | 로그 검증 | QA팀 |
| **운영자 승인** | 2명 이상 "동일 수준" 서명 | 서명 문서 | 운영팀 |
| **성능** | 카드 인식 < 200ms, 승률 계산 < 100ms | 성능 테스트 | QA팀 |
| **보안** | Trustless Mode 정상 동작, 암호화 확인 | 보안 체크리스트 | 보안팀 |

**Gate 통과 시**: Stage 2 PRD 작성 및 착수 가능 (2027년 1월)

**Gate 미통과 시**: 미완료 항목 재작업 후 재검증

---

## 10. Definition of Done

### 10.1 개발 완료 기준

- [ ] **54개 기능 구현 완료**: PokerGFX-Feature-Checklist.md 100%
- [ ] **단위 테스트**: 커버리지 > 80%
- [ ] **통합 테스트**: 주요 워크플로우 자동화 테스트
- [ ] **E2E 테스트**: Playwright로 핵심 시나리오 검증

### 10.2 문서화 완료 기준

- [ ] **API 문서**: OpenAPI/Swagger 자동 생성
- [ ] **DB 스키마**: ERD 다이어그램 + 테이블 설명
- [ ] **운영 매뉴얼**: 운영자용 가이드 작성
- [ ] **트러블슈팅**: 자주 발생하는 이슈 해결 방법

### 10.3 검증 완료 기준

- [ ] **운영자 2명+ 서명**: "기존과 동일" 확인서
- [ ] **4시간 방송 테스트**: 에러 0건
- [ ] **성능 테스트**: 카드 인식 < 200ms, 승률 계산 < 100ms
- [ ] **보안 테스트**: Trustless Mode 정상 동작, 암호화 확인

### 10.4 배포 완료 기준

- [ ] **프로덕션 환경**: 서버 + 프론트엔드 배포
- [ ] **하드웨어 설치**: RFID 리더 10대 + ESP32 설치
- [ ] **카드 매핑**: 52장 + 조커 2장 UID 등록
- [ ] **운영자 교육**: 핸드 진행 워크플로우 숙달

---

## 11. 위험 요소 및 대응 방안

### 11.1 기술 위험

| 위험 요소 | 확률 | 영향 | 대응 방안 |
|----------|------|------|----------|
| **RFID 인식 실패** | 중간 | 높음 | 수동 카드 입력 UI 백업 (AT-019~020) |
| **WebSocket 연결 끊김** | 낮음 | 높음 | 자동 재연결 + 버퍼링 |
| **승률 계산 지연** | 낮음 | 중간 | 비동기 처리 + 캐싱 |
| **DB 암호화 성능** | 낮음 | 낮음 | SQLCipher 최적화 설정 |

### 11.2 일정 위험

| 위험 요소 | 확률 | 영향 | 대응 방안 |
|----------|------|------|----------|
| **Trustless Mode 지연** | 중간 | 중간 | Phase 5로 우선순위 조정 |
| **통계 계산 복잡도** | 낮음 | 낮음 | 샘플 데이터로 먼저 검증 |
| **운영자 교육 시간 부족** | 중간 | 중간 | 조기 Alpha 테스트 |

### 11.3 사용성 위험

| 위험 요소 | 확률 | 영향 | 대응 방안 |
|----------|------|------|----------|
| **운영자 워크플로우 혼란** | 낮음 | 높음 | PokerGFX 1:1 복제 엄수 |
| **키보드 단축키 충돌** | 낮음 | 낮음 | 커스터마이징 옵션 제공 |
| **OBS 연동 이슈** | 중간 | 중간 | OBS 28.0+ 테스트 |

---

## 12. 다음 단계

### 12.1 즉시 시작 (Week 1)

1. **RFID 하드웨어 세팅**: ESP32 + MFRC522 10대 연결
2. **DB 스키마 생성**: SQLite DB + 카드 테이블 초기화
3. **카드 매핑 도구**: UID → 카드 정보 입력 UI
4. **WebSocket 서버**: FastAPI + WebSocket 기본 구조
5. **기본 오버레이 UI**: React + OBS Browser Source 연동

### 12.2 Alpha 출시 목표 (Week 2 말)

- [ ] RFID 카드 인식 정상 동작
- [ ] WebSocket 실시간 통신 확인
- [ ] 기본 오버레이 UI (Player HUD + Board Cards)
- [ ] 내부 테스트 (개발팀)

### 12.3 Beta 출시 목표 (Week 4 말)

- [ ] Action Tracker 완성
- [ ] 팟 계산 자동화
- [ ] Pre-Start Setup 완성
- [ ] 운영자 Alpha 테스트 (2명)

### 12.4 RC 출시 목표 (Week 6 말)

- [ ] GFX Console 완성
- [ ] 플레이어 스탯 계산
- [ ] 승률 계산 (헤즈업)
- [ ] 운영자 Beta 테스트 (2명)

### 12.5 Release 출시 목표 (Week 8 말)

- [ ] Trustless Mode 구현
- [ ] Hand History 완성
- [ ] 4시간 방송 테스트 통과
- [ ] 운영자 2명+ "동일 수준" 서명

---

## 13. UI/UX 목업

Stage 1 개발 시 참조할 B&W 와이어프레임 목업입니다.

### 13.1 핵심 화면

| 목업 | 용도 | 관련 기능 |
|------|------|----------|
| [Action Tracker](../images/mockups/02-action-tracker.png) | 운영자 입력 화면 | AT-008~026 |
| [Action Tracker Pre-Start](../images/mockups/02a-action-tracker-prestart.png) | 게임 설정 화면 | PS-001~013 |
| [Viewer Overlay](../images/mockups/01-viewer-overlay.png) | 시청자 화면 | VO-001~014 |
| [GFX Console (Player Stats)](../images/mockups/06-player-stats.png) | 통계 대시보드 | GC-001~025, ST-001~007 |
| [Production Dashboard](../images/mockups/03-production-dashboard.png) | 프로덕션 통합 | OBS 연동 |

### 13.2 기능별 화면

| 목업 | 용도 | 관련 기능 |
|------|------|----------|
| [Automation Flow](../images/mockups/04-automation-flow.png) | 자동화 워크플로우 | Section 5 |
| [Security Modes](../images/mockups/05-security-modes.png) | Trustless/Realtime 모드 | SEC-001~011 |
| [Equity & Outs](../images/mockups/07-equity-outs.png) | 승률/아웃츠 표시 | EQ-001~012 |
| [Hand History](../images/mockups/08-hand-history.png) | 핸드 히스토리 | HH-001~011 |

### 13.3 확장 기능 (Stage 2-3 참조용)

| 목업 | 용도 | 대상 Stage |
|------|------|-----------|
| [Skin Editor](../images/mockups/09-skin-editor.png) | 스킨 커스터마이징 | Stage 3 |
| [Multi-Table](../images/mockups/10-multi-table.png) | 멀티테이블 관리 | Stage 2-3 |
| [Mobile Tracker](../images/mockups/11-mobile-tracker.png) | 모바일 입력 | Stage 3 |
| [Tournament Mode](../images/mockups/12-tournament.png) | 토너먼트 관리 | Stage 2-3 |

### 13.4 시스템 다이어그램

| 다이어그램 | 용도 |
|-----------|------|
| [Data Flow (Workflow)](../images/diagrams/diagram-08-workflow.png) | 데이터 흐름도 |
| [System Architecture](../images/diagrams/diagram-09-architecture.png) | 시스템 아키텍처 |

> **참고**: HTML 원본은 `docs/mockups/` 디렉토리에 있습니다.
> 스크린샷 재생성: Playwright로 HTML → PNG 변환

---

## 14. 참조 문서

| 문서 | 용도 |
|------|------|
| [PRD-0003-EBS-RFID-System.md](../PRD-0003-EBS-RFID-System.md) | 상위 PRD (전체 로드맵) |
| [PokerGFX-Feature-Checklist.md](PokerGFX-Feature-Checklist.md) | 54개 기능 체크리스트 |
| [ARCHITECTURE-RFID-Software.md](ARCHITECTURE-RFID-Software.md) | 소프트웨어 아키텍처 |
| [DESIGN-RFID-Hardware.md](../1-stage0/DESIGN-RFID-Hardware.md) | 하드웨어 설계 |
| [GUIDE-RFID-Implementation.md](../1-stage0/GUIDE-RFID-Implementation.md) | 구현 가이드 |
| [REPORT-PokerGFX-Server-Analysis.md](REPORT-PokerGFX-Server-Analysis.md) | 경쟁사 분석 |

---

## 15. 문서 정보

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.1.0 |
| **작성일** | 2026-01-28 |
| **작성자** | Claude Code |
| **상태** | Draft |
| **다음 리뷰** | 2026-02-04 (Week 1 종료 시) |

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0.0 | 2026-01-28 | 초안 작성 |
| **1.1.0** | **2026-01-28** | Section 13 (UI/UX 목업) 추가, 목업 참조 정리 |

