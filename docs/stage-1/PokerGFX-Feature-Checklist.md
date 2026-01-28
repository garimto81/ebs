# PokerGFX 기능 체크리스트

**버전**: 1.0.0
**생성일**: 2026-01-28
**소스**: EBS 기존 mockup 파일 기반 분석

---

## 요약

| 카테고리 | 기능 수 | 완료 |
|----------|---------|------|
| Action Tracker | 14 | 0/14 |
| Pre-Start Setup | 10 | 0/10 |
| Viewer Overlay | 8 | 0/8 |
| GFX Console | 9 | 0/9 |
| Security | 6 | 0/6 |
| Statistics & History | 7 | 0/7 |
| **Total** | **54** | **0/54** |

---

## 1. Action Tracker 기능

### 1.1 상태 표시 (Status Bar)
- [ ] **AT-001**: Network 연결 상태 - 실시간 네트워크 연결 모니터링
- [ ] **AT-002**: Table 연결 상태 - 테이블 연결 상태 표시
- [ ] **AT-003**: Stream 상태 - 스트리밍 활성화 표시
- [ ] **AT-004**: Record 상태 - 녹화 활성화 표시

### 1.2 게임 설정
- [ ] **AT-005**: 게임 타입 선택 - HOLDEM / PLO / SHORT DECK 토글
- [ ] **AT-006**: Blinds 정보 표시 - SB/BB/Ante 표시
- [ ] **AT-007**: Hand 번호 추적 - 핸드 카운터 표시

### 1.3 플레이어 그리드
- [ ] **AT-008**: 10인 좌석 레이아웃 - 시각적 좌석 배치
- [ ] **AT-009**: 플레이어 상태 표시 - Active / Dealt / Folded / Empty
- [ ] **AT-010**: Action-on 하이라이트 - 현재 차례 플레이어 강조
- [ ] **AT-011**: 포지션 표시 - DLR / SB / BB 버튼

### 1.4 액션 입력
- [ ] **AT-012**: 기본 액션 버튼 - FOLD / CHECK / CALL / BET / ALL-IN
- [ ] **AT-013**: UNDO 버튼 - 마지막 액션 취소
- [ ] **AT-014**: 키보드 단축키 - F(Fold) / C(Check) / B(Bet) / A(All-In)

### 1.5 베팅 입력
- [ ] **AT-015**: 베팅 금액 직접 입력 - 숫자 키패드 입력
- [ ] **AT-016**: +/- 조정 버튼 - 금액 증감
- [ ] **AT-017**: Quick Bet 버튼 - MIN / 2xBB / 3xBB / ½POT / POT / ALL-IN
- [ ] **AT-018**: Min/Max 범위 표시 - 유효 베팅 범위 안내

### 1.6 보드 관리
- [ ] **AT-019**: Community Cards 표시 - 5장 보드 카드 표시
- [ ] **AT-020**: 보드 카드 업데이트 - Flop / Turn / River 진행

### 1.7 하단 컨트롤
- [ ] **AT-021**: HIDE GFX - 오버레이 숨김/표시
- [ ] **AT-022**: TAG HAND - 핸드 북마크
- [ ] **AT-023**: ADJUST STACK - 칩 스택 수동 조정
- [ ] **AT-024**: CHOP - 팟 나누기
- [ ] **AT-025**: RUN IT 2x - 보드 2번 런
- [ ] **AT-026**: MISS DEAL - 미스딜 처리

---

## 2. Pre-Start Setup 기능

### 2.1 게임 설정
- [ ] **PS-001**: Event Name 입력 - 이벤트명 설정
- [ ] **PS-002**: Game Type 선택 - NLHE / PLO / PLO5
- [ ] **PS-003**: Min Chip 설정 - 최소 칩 단위

### 2.2 플레이어 설정
- [ ] **PS-004**: 플레이어 이름 입력 - 각 좌석별 이름
- [ ] **PS-005**: 칩 스택 입력 - 시작 칩 스택 설정
- [ ] **PS-006**: 포지션 할당 - DLR / SB / BB 버튼 배치
- [ ] **PS-007**: 카드 감지 상태 - RFID 카드 2장 감지 표시

### 2.3 블라인드/앤티 설정
- [ ] **PS-008**: Ante / SB / BB / 3rd Blind 입력
- [ ] **PS-009**: Straddle 추가 - 스트래들 활성화 및 금액

### 2.4 딜러 포지션
- [ ] **PS-010**: Dealer / SB / BB 위치 조정 - 화살표로 좌석 변경

### 2.5 보드 설정
- [ ] **PS-011**: Board Count 선택 - SINGLE / DOUBLE / TRIPLE

### 2.6 시작
- [ ] **PS-012**: TRACK THE ACTION 버튼 - 핸드 시작
- [ ] **PS-013**: AUTO 모드 - RFID 자동 감지로 핸드 시작

---

## 3. Viewer Overlay 기능

### 3.1 상단 바 (Top Bar)
- [ ] **VO-001**: Event Logo 표시
- [ ] **VO-002**: Blinds 정보 - SB/BB/Ante 표시
- [ ] **VO-003**: Chip Counts - 5-6명 플레이어 칩 스택 (가로 스크롤)
- [ ] **VO-004**: Broadcaster Logo 표시

### 3.2 Player HUD (좌측 하단 수직 스택)
- [ ] **VO-005**: Hole Cards 표시 - HUD 위로 겹치는 카드 2장
- [ ] **VO-006**: Player Name + Stack - 이름 및 칩 스택
- [ ] **VO-007**: 마지막 액션 표시 - CHECK / BET / RAISE 등
- [ ] **VO-008**: Equity % 표시 - 실시간 승률

### 3.3 우측 패널 (컴팩트 3-Grid)
- [ ] **VO-009**: Board Cards - 5장 커뮤니티 카드
- [ ] **VO-010**: Pot Display - 현재 팟 금액
- [ ] **VO-011**: Event Info - 이벤트명 및 게임 타입

### 3.4 상태 표시 (좌측 상단)
- [ ] **VO-012**: Street 표시 - PREFLOP / FLOP / TURN / RIVER
- [ ] **VO-013**: To Act 표시 - 현재 차례 플레이어

### 3.5 Folded State
- [ ] **VO-014**: Folded Player 스타일 - 회색 처리 + Equity 숨김

---

## 4. GFX Console (Production Dashboard) 기능

### 4.1 통계 표시 모드
- [ ] **GC-001**: Seat 순서 - 좌석 순서대로 표시
- [ ] **GC-002**: Stack 순위 - 칩 스택 순위
- [ ] **GC-003**: VPIP% - 자발적 참여율
- [ ] **GC-004**: PFR% - 프리플랍 레이즈
- [ ] **GC-005**: AGRfq% - 공격 빈도
- [ ] **GC-006**: WTSD% - 쇼다운 도달률
- [ ] **GC-007**: WIN - 순수익
- [ ] **GC-008**: Payouts - 상금

### 4.2 리더보드
- [ ] **GC-009**: 플레이어 순위 테이블 - Stack/VPIP/PFR/AGR/WTSD 표시
- [ ] **GC-010**: Chip Bar 그래프 - 상대적 스택 크기
- [ ] **GC-011**: Stat Bar 그래프 - 각 스탯 시각화
- [ ] **GC-012**: 정렬 기능 - STACK / NAME / SEAT 정렬

### 4.3 필드 정보
- [ ] **GC-013**: Total Field - 전체 참가자 수
- [ ] **GC-014**: Remaining - 남은 참가자 수
- [ ] **GC-015**: Avg Stack - 평균 스택
- [ ] **GC-016**: Total Chips - 전체 칩

### 4.4 컨트롤
- [ ] **GC-017**: LIVE Stats 토글 - 실시간 통계 업데이트
- [ ] **GC-018**: Show Eliminated 토글 - 탈락자 표시/숨김
- [ ] **GC-019**: PIP Display - Picture-in-Picture 모드
- [ ] **GC-020**: Export CSV - 통계 CSV 내보내기

### 4.5 티커
- [ ] **GC-021**: Ticker Message 입력 - 우→좌 스크롤 메시지

### 4.6 시스템 상태
- [ ] **GC-022**: System Status Panel - RFID / WebSocket / DB / OBS 상태
- [ ] **GC-023**: Quick Actions - New Table / Add Player / Reset / Test Card

### 4.7 라이브 프리뷰
- [ ] **GC-024**: Overlay Preview - 960x540 오버레이 미리보기

### 4.8 Recent Hands
- [ ] **GC-025**: 최근 핸드 목록 - Hand# / Winner / Pot / Board

---

## 5. Security 기능

### 5.1 Trustless Mode
- [ ] **SEC-001**: 운영자 카드 정보 차단 - 30초 딜레이 중 UID만 버퍼링
- [ ] **SEC-002**: 카운트다운 표시 - T=0 → T=30 타이머
- [ ] **SEC-003**: DB 조회 지연 실행 - 딜레이 후 카드 정보 조회

### 5.2 Realtime Mode
- [ ] **SEC-004**: 즉시 카드 정보 표시 - DB 즉시 조회
- [ ] **SEC-005**: 운영자 실시간 확인 - 지연 없음

### 5.3 암호화 레이어
- [ ] **SEC-006**: RFID Card 암호화 - AES-128 DESFire EV3
- [ ] **SEC-007**: Serial 암호화 - ChaCha20 + HMAC
- [ ] **SEC-008**: Database 암호화 - AES-256-GCM SQLCipher
- [ ] **SEC-009**: WebSocket 암호화 - TLS 1.3 WSS

### 5.4 모드 전환
- [ ] **SEC-010**: Trustless/Realtime 토글 - GFX Console에서 전환
- [ ] **SEC-011**: Delay 시간 설정 - 초 단위 조정 (기본 30초)

---

## 6. Player Statistics 기능

### 6.1 플레이어 상세 스탯
- [ ] **ST-001**: VPIP% - 자발적 참여율
- [ ] **ST-002**: PFR% - 프리플랍 레이즈
- [ ] **ST-003**: AGRfq% - 공격 빈도
- [ ] **ST-004**: WTSD% - 쇼다운 도달률
- [ ] **ST-005**: 3Bet% - 3벳 비율
- [ ] **ST-006**: Fold to 3Bet% - 3벳에 폴드 비율
- [ ] **ST-007**: Continuation Bet% - 컨티뉴에이션 벳

---

## 7. Equity & Outs 기능

### 7.1 승률 비교
- [ ] **EQ-001**: 헤즈업 Equity 계산 - Player A vs Player B
- [ ] **EQ-002**: Hole Cards 표시 - 각 플레이어 핸드
- [ ] **EQ-003**: Equity % 표시 - 실시간 승률

### 7.2 보드 상태
- [ ] **EQ-004**: Community Cards 표시 - Flop / Turn / River
- [ ] **EQ-005**: Pending Cards 표시 - 아직 나오지 않은 카드 [?]

### 7.3 아웃츠 분석
- [ ] **EQ-006**: Outs 카드 리스트 - 역전 가능한 카드 목록
- [ ] **EQ-007**: Total Outs 카운트 - 총 아웃츠 수
- [ ] **EQ-008**: Turn Hit % - 턴에서 맞을 확률
- [ ] **EQ-009**: Turn + River % - 턴+리버 복합 확률
- [ ] **EQ-010**: Odds 계산 - 예: 4.2:1

### 7.4 승리 시나리오
- [ ] **EQ-011**: 시나리오별 확률 - Full House / Straight / Backdoor 등
- [ ] **EQ-012**: 확률 % 표시 - 각 시나리오 승률

---

## 8. Hand History 기능

### 8.1 필터링
- [ ] **HH-001**: Player 필터 - 특정 플레이어 핸드만 보기
- [ ] **HH-002**: Date 필터 - 날짜별 필터링
- [ ] **HH-003**: Result 필터 - Win / Lose 필터

### 8.2 핸드 목록
- [ ] **HH-004**: 핸드 목록 테이블 - Hand# / Time / Players / Winner / Pot / Board
- [ ] **HH-005**: 선택한 핸드 상세 - 클릭 시 상세 표시
- [ ] **HH-006**: Pagination - 페이지 네비게이션

### 8.3 핸드 상세
- [ ] **HH-007**: Hole Cards 표시 - Winner / Loser 카드
- [ ] **HH-008**: Board 표시 - 5장 커뮤니티 카드
- [ ] **HH-009**: Timeline - Preflop / Flop / Turn / River 액션 흐름
- [ ] **HH-010**: Action 로그 - Player / Action Type / Amount

### 8.4 내보내기
- [ ] **HH-011**: Export 버튼 - CSV / JSON 파일 내보내기

---

## 9. Stage 1 구현 우선순위

| 우선순위 | 기능 ID | 카테고리 | 설명 | 난이도 |
|:--------:|---------|----------|------|:------:|
| **1** | AT-012 | Action Tracker | 기본 액션 버튼 (FOLD/CHECK/CALL/BET/ALL-IN) | 낮음 |
| **2** | AT-015~017 | Action Tracker | 베팅 입력 (직접 입력 + Quick Bet) | 중간 |
| **3** | AT-008~011 | Action Tracker | 플레이어 그리드 (10인 좌석 + 상태 표시) | 중간 |
| **4** | PS-001~007 | Pre-Start | 플레이어/게임 설정 (이름/칩/포지션) | 낮음 |
| **5** | PS-008~009 | Pre-Start | 블라인드/앤티 설정 | 낮음 |
| **6** | AT-019~020 | Action Tracker | 보드 카드 관리 | 낮음 |
| **7** | VO-005~008 | Viewer Overlay | Player HUD (카드+이름+스택+액션) | 중간 |
| **8** | VO-009~011 | Viewer Overlay | 우측 패널 (보드+팟+이벤트) | 낮음 |
| **9** | VO-001~004 | Viewer Overlay | 상단 바 (로고+블라인드+칩카운트) | 중간 |
| **10** | SEC-004~005 | Security | Realtime Mode (즉시 표시) | 낮음 |
| **11** | AT-001~004 | Action Tracker | 상태 표시 (Network/Table/Stream) | 낮음 |
| **12** | GC-022~023 | GFX Console | 시스템 상태 + Quick Actions | 중간 |
| **13** | GC-024~025 | GFX Console | 라이브 프리뷰 + Recent Hands | 중간 |
| **14** | SEC-001~003 | Security | Trustless Mode (30초 딜레이) | 높음 |
| **15** | EQ-001~005 | Equity | 헤즈업 승률 계산 + 보드 표시 | 높음 |
| **16** | EQ-006~010 | Equity | 아웃츠 분석 | 높음 |
| **17** | GC-001~008 | GFX Console | 통계 표시 모드 (VPIP/PFR 등) | 중간 |
| **18** | GC-009~012 | GFX Console | 리더보드 테이블 + 그래프 | 중간 |
| **19** | HH-001~006 | Hand History | 핸드 목록 + 필터링 | 중간 |
| **20** | HH-007~010 | Hand History | 핸드 상세 + Timeline | 높음 |

---

## 10. 카테고리별 구현 단계

### Phase 1: MVP (Minimum Viable Product)
**목표**: 기본 게임 진행 가능
**기능**: AT-012, AT-015~017, AT-008~011, PS-001~009, AT-019~020

### Phase 2: Viewer Overlay
**목표**: 방송용 오버레이
**기능**: VO-001~014, AT-001~004

### Phase 3: Production Tools
**목표**: 프로덕션 대시보드
**기능**: GC-022~025, SEC-004~005

### Phase 4: Advanced Features
**목표**: 통계 및 분석
**기능**: GC-001~021, EQ-001~012, HH-001~011

### Phase 5: Security
**목표**: Trustless Mode
**기능**: SEC-001~011

---

## 11. 기술 스택 매핑

| 카테고리 | Frontend | Backend | 기타 |
|----------|----------|---------|------|
| Action Tracker | React (Input/Grid) | FastAPI (Action API) | WebSocket |
| Pre-Start | React (Form) | FastAPI (Game Setup) | - |
| Viewer Overlay | React (OBS Browser) | FastAPI (WebSocket) | OBS |
| GFX Console | React (Dashboard) | FastAPI (Stats API) | - |
| Security | React (Mode Toggle) | Python (Delay Buffer) | SQLCipher |
| Equity | React (Equity Display) | Python (Monte Carlo) | poker-eval |
| Hand History | React (Table/Filter) | FastAPI (DB Query) | SQLite |

---

## 12. 다음 단계

1. **우선순위 1-6 기능 구현** (Phase 1 MVP)
2. **PokerGFX PRD 작성** (이 체크리스트 기반)
3. **UI/UX 상세 설계** (Figma 또는 HTML 프로토타입)
4. **API 스펙 정의** (OpenAPI/Swagger)
5. **DB 스키마 설계** (SQLite ERD)

---

**END OF CHECKLIST**
