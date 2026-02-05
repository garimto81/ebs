# Phase 1: PokerGFX 100% 복제

> **BRACELET STUDIO** | EBS Project

**완료 시점**: 2026년 Q4
**목표**: PokerGFX와 동일한 기능, 동일한 워크플로우 구현
**완료 기준**: 운영자가 "GFX와 차이 없음" 서명

---

## 1. Phase 1 개요

### 1.1 목표

> **"PokerGFX를 100% 복제한다. 새로운 기능 추가 금지."**

Phase 1은 기존 PokerGFX 시스템을 완벽하게 복제하는 단계입니다.
운영자가 기존 워크플로우 변경 없이 새 시스템으로 전환할 수 있어야 합니다.

### 1.2 핵심 원칙

| 원칙 | 설명 | 금지 사항 |
|------|------|----------|
| **1:1 복제** | GFX와 동일한 기능만 구현 | 새 기능 추가 금지 |
| **동일 워크플로우** | 운영자 작업 순서 유지 | UI 개선 금지 |
| **54개 기능 완성** | 체크리스트 100% 완료 | 기능 생략 금지 |

### 1.3 성공 기준

| 기준 | 목표 | 검증 방법 |
|------|------|----------|
| 기능 완성도 | 54/54 (100%) | 체크리스트 확인 |
| 카드 인식 속도 | < 200ms | E2E 측정 |
| 인식 실패율 | < 1% | 100회 테스트 |
| 무중단 운영 | 4시간 이상 | 실제 방송 테스트 |
| 운영자 승인 | 2명 이상 서명 | 서명 문서 |

---

## 2. 시스템 아키텍처

### 2.1 전체 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Physical Layer                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   RFID Card ──▶ MFRC522/ST25R3911B ──▶ ESP32 ──▶ USB Serial        │
│   (MIFARE)      (13.56MHz Reader)      (MCU)     (JSON Output)      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Software Layer                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ESP32 ──▶ Python Server ──▶ WebSocket ──▶ React Frontend         │
│   (Serial)   (FastAPI)        (Real-time)   (OBS Overlay)           │
│                  │                                                   │
│                  ▼                                                   │
│              SQLite DB                                               │
│              (cards.db)                                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 레이어별 상세

| Layer | 기술 스택 | 역할 | 산출물 |
|-------|----------|------|--------|
| **Firmware** | Arduino C++ | RFID 태그 읽기, JSON 출력 | `firmware/esp32_rfid.ino` |
| **Server** | Python FastAPI | Serial 수신, DB 조회, WebSocket | `server/` |
| **Frontend** | React + TypeScript | OBS 오버레이, Action Tracker | `frontend/` |
| **Database** | SQLite | 카드/핸드/플레이어 데이터 | `server/db/cards.db` |

### 2.3 데이터 흐름

```
1. 카드 태그 ──▶ RFID 리더 (UID 읽기)
2. RFID 리더 ──▶ ESP32 (SPI 통신)
3. ESP32 ──▶ USB Serial (JSON: {"uid": "04:A2:B3:C4"})
4. Python Server ──▶ DB 조회 (UID → Card Info)
5. Server ──▶ WebSocket ({"card": "A♠", "seat": 1})
6. Frontend ──▶ OBS (화면 업데이트)
```

### 2.4 통신 프로토콜

#### ESP32 → Server (Serial JSON)

```json
{
  "type": "card_read",
  "uid": "04:A2:B3:C4",
  "reader_id": 0,
  "timestamp": 1706400000
}
```

#### Server → Frontend (WebSocket JSON)

```json
{
  "type": "card_detected",
  "uid": "04:A2:B3:C4",
  "card": {
    "suit": "spades",
    "rank": "A",
    "display": "A♠"
  },
  "seat": 1,
  "position": "hole_1"
}
```

---

## 3. 기능 카테고리 (54개)

### 3.1 Action Tracker (26개)

운영자가 플레이어 액션을 입력하는 메인 인터페이스입니다.

#### 상태 표시 (4개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-001 | Network 연결 상태 | 서버 연결 표시 | P0 |
| AT-002 | Table 연결 상태 | RFID 리더 연결 표시 | P0 |
| AT-003 | Stream 상태 | 스트리밍 상태 표시 | P1 |
| AT-004 | Record 상태 | 녹화 상태 표시 | P1 |

#### 게임 설정 (3개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-005 | 게임 타입 | HOLDEM/PLO/SHORT DECK 선택 | P0 |
| AT-006 | Blinds 표시 | SB/BB/Ante 설정 및 표시 | P0 |
| AT-007 | Hand 번호 | 자동 증가하는 핸드 번호 | P1 |

#### 플레이어 그리드 (4개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-008 | 10인 좌석 레이아웃 | 원형 테이블 배치 | P0 |
| AT-009 | 플레이어 상태 | Active/Folded/Empty 표시 | P0 |
| AT-010 | Action-on 하이라이트 | 현재 액션 플레이어 강조 | P0 |
| AT-011 | 포지션 표시 | DLR/SB/BB 버튼 위치 | P0 |

#### 액션 입력 (3개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-012 | 기본 액션 버튼 | FOLD/CHECK/CALL/BET/ALL-IN | P0 |
| AT-013 | UNDO 버튼 | 마지막 액션 취소 | P0 |
| AT-014 | 키보드 단축키 | F/C/B/A 등 단축키 지원 | P1 |

#### 베팅 입력 (4개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-015 | 베팅 금액 입력 | 숫자 직접 입력 | P0 |
| AT-016 | +/- 조정 버튼 | 금액 미세 조정 | P1 |
| AT-017 | Quick Bet | MIN/POT/ALL-IN 버튼 | P1 |
| AT-018 | Min/Max 범위 | 베팅 가능 범위 표시 | P1 |

#### 보드 관리 (2개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-019 | Community Cards | 보드 카드 5장 표시 | P0 |
| AT-020 | 보드 카드 업데이트 | Flop/Turn/River 입력 | P0 |

#### 하단 컨트롤 (6개)
| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| AT-021 | HIDE GFX | 오버레이 숨기기 | P1 |
| AT-022 | TAG HAND | 핸드 북마크 | P2 |
| AT-023 | ADJUST STACK | 칩 수정 | P1 |
| AT-024 | CHOP | 팟 분배 | P2 |
| AT-025 | RUN IT 2x | 더블 런아웃 | P2 |
| AT-026 | MISS DEAL | 딜 취소 | P2 |

### 3.2 Pre-Start Setup (13개)

방송 시작 전 설정 화면입니다.

| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| PS-001 | Event Name | 이벤트명 입력 | P0 |
| PS-002 | Game Type | 게임 타입 선택 | P0 |
| PS-003 | Min Chip | 최소 칩 단위 설정 | P0 |
| PS-004 | 플레이어 이름 | 10인 이름 입력 | P0 |
| PS-005 | 칩 스택 | 시작 칩 입력 | P0 |
| PS-006 | 포지션 할당 | 좌석별 포지션 | P0 |
| PS-007 | RFID 상태 | 카드 감지 상태 표시 | P0 |
| PS-008 | Ante/SB/BB | 블라인드 구조 설정 | P0 |
| PS-009 | Straddle | 스트래들 옵션 | P1 |
| PS-010 | Dealer 위치 | 딜러 버튼 위치 | P0 |
| PS-011 | Board Count | SINGLE/DOUBLE 런아웃 | P1 |
| PS-012 | TRACK THE ACTION | 트래킹 시작 버튼 | P0 |
| PS-013 | AUTO 모드 | 자동 트래킹 모드 | P2 |

### 3.3 Viewer Overlay (14개)

시청자에게 보여지는 방송 오버레이입니다.

| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| VO-001 | Event Logo | 이벤트 로고 표시 | P1 |
| VO-002 | Blinds 정보 | 현재 블라인드 표시 | P0 |
| VO-003 | Chip Counts | 칩 카운트 레이블 | P0 |
| VO-004 | Broadcaster Logo | 방송사 로고 | P1 |
| VO-005 | Hole Cards | 플레이어 홀카드 표시 | P0 |
| VO-006 | Player Name + Stack | 이름, 스택 표시 | P0 |
| VO-007 | 마지막 액션 | 최근 액션 표시 | P0 |
| VO-008 | Equity % | 승률 퍼센트 표시 | P1 |
| VO-009 | Board Cards | 커뮤니티 카드 | P0 |
| VO-010 | Pot Display | 팟 사이즈 표시 | P0 |
| VO-011 | Event Info | 이벤트 정보 배너 | P1 |
| VO-012 | Street 표시 | PREFLOP/FLOP/TURN/RIVER | P0 |
| VO-013 | To Act 표시 | 액션 대기자 표시 | P0 |
| VO-014 | Folded Style | 폴드 플레이어 회색 처리 | P0 |

### 3.4 GFX Console (25개)

통계, 리더보드, 시스템 상태를 관리하는 콘솔입니다.

#### 통계 표시 (8개)
- GC-001~008: VPIP, PFR, AGR, WTSD, WIN%, 3Bet%, CBet%, AFq

#### 리더보드 (4개)
- GC-009~012: 순위 테이블, 그래프, 정렬 옵션, 필터

#### 필드 정보 (4개)
- GC-013~016: Total Players, Remaining, Average Stack, Total Chips

#### 컨트롤 (4개)
- GC-017~020: LIVE Stats 토글, Export CSV, Import, Reset

#### 기타 (5개)
- GC-021~025: 티커, 시스템 상태, Preview, Theme, Layout

### 3.5 Security (11개)

보안 모드 관리입니다.

| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| SEC-001 | Trustless Mode | 30초 딜레이 버퍼링 | P0 |
| SEC-002 | 카운트다운 | 딜레이 타이머 표시 | P0 |
| SEC-003 | DB 조회 지연 | 카드 정보 지연 표시 | P0 |
| SEC-004 | Realtime Mode | 즉시 카드 표시 | P0 |
| SEC-005 | 모드 표시 | 현재 모드 인디케이터 | P0 |
| SEC-006 | RFID 암호화 | 태그-리더 통신 암호화 | P1 |
| SEC-007 | Serial 암호화 | ESP32-서버 통신 암호화 | P1 |
| SEC-008 | DB 암호화 | SQLite 암호화 | P2 |
| SEC-009 | WebSocket 암호화 | WSS 사용 | P1 |
| SEC-010 | 모드 토글 | Trustless ↔ Realtime | P0 |
| SEC-011 | Delay 설정 | 딜레이 시간 설정 (10-60초) | P1 |

### 3.6 Equity & Stats (19개)

승률 계산 및 통계 기능입니다.

#### Equity (12개)
- EQ-001~012: 2-10인 승률 계산, 아웃츠 분석, 타이 확률, 런아웃 시뮬레이션

#### Stats (7개)
- ST-001~007: VPIP, PFR, AGR, WTSD, 3Bet, CBet, 세션 통계

### 3.7 Hand History (11개)

핸드 히스토리 저장 및 조회 기능입니다.

| ID | 기능 | 설명 | 우선순위 |
|----|------|------|:--------:|
| HH-001 | 핸드 자동 저장 | 모든 핸드 DB 저장 | P0 |
| HH-002 | 핸드 목록 | 핸드 리스트 조회 | P0 |
| HH-003 | 날짜 필터 | 날짜별 필터링 | P1 |
| HH-004 | 플레이어 필터 | 플레이어별 필터링 | P1 |
| HH-005 | 팟 크기 필터 | 팟 크기별 필터링 | P2 |
| HH-006 | 검색 | 키워드 검색 | P2 |
| HH-007 | 핸드 상세 | 개별 핸드 상세 보기 | P0 |
| HH-008 | 리플레이 | 핸드 리플레이 | P1 |
| HH-009 | Export JSON | JSON 형식 내보내기 | P1 |
| HH-010 | Export CSV | CSV 형식 내보내기 | P1 |
| HH-011 | 태그 관리 | 핸드 태그/북마크 | P2 |

---

## 4. 하드웨어 설계

### 4.1 RFID 모듈 선택

| 용도 | 모듈 | 가격 | 특징 |
|------|------|------|------|
| **학습/프로토타입** | MFRC522 | $2-5 | 저렴, 검증됨 |
| **프로덕션** | ST25R3911B | $10-15 | 고성능, ISO15693 지원 |

### 4.2 ESP32 배선 (MFRC522)

| ESP32 | MFRC522 | 기능 | 색상 권장 |
|-------|---------|------|----------|
| **3.3V** | VCC | 전원 (⚠️ 5V 금지!) | 빨강 |
| **GND** | GND | 접지 | 검정 |
| GPIO5 | SDA | SPI Slave Select | 노랑 |
| GPIO18 | SCK | SPI Clock | 초록 |
| GPIO23 | MOSI | SPI Master Out | 파랑 |
| GPIO19 | MISO | SPI Master In | 주황 |
| GPIO4 | RST | Reset | 흰색 |

> ⚠️ **경고**: MFRC522에 5V 연결 시 모듈 손상!

### 4.3 멀티 리더 구성

실제 방송에서는 10명 좌석별로 리더가 필요합니다.

```
Seat 1 Reader (GPIO5)  ──┐
Seat 2 Reader (GPIO15) ──┼──▶ ESP32 ──▶ USB Serial
Seat 3 Reader (GPIO16) ──┤
...                      │
Seat 10 Reader (GPIO27)──┘
```

---

## 5. 데이터베이스 설계

### 5.1 카드 테이블 (cards)

```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    uid TEXT UNIQUE,           -- RFID UID
    suit TEXT NOT NULL,        -- spades, hearts, diamonds, clubs
    rank TEXT NOT NULL,        -- A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2
    display TEXT NOT NULL,     -- A♠, K♥, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 플레이어 테이블 (players)

```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    seat INTEGER NOT NULL,     -- 1-10
    stack INTEGER NOT NULL,
    status TEXT DEFAULT 'active',  -- active, folded, eliminated
    session_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### 5.3 핸드 테이블 (hands)

```sql
CREATE TABLE hands (
    id INTEGER PRIMARY KEY,
    hand_number INTEGER NOT NULL,
    session_id INTEGER,
    board TEXT,                -- JSON: ["A♠", "K♥", "Q♦", "J♣", "10♠"]
    pot INTEGER,
    winner_seat INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

### 5.4 액션 테이블 (actions)

```sql
CREATE TABLE actions (
    id INTEGER PRIMARY KEY,
    hand_id INTEGER,
    seat INTEGER NOT NULL,
    action_type TEXT NOT NULL,  -- fold, check, call, bet, raise, all-in
    amount INTEGER,
    street TEXT NOT NULL,       -- preflop, flop, turn, river
    sequence INTEGER NOT NULL,  -- 액션 순서
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hand_id) REFERENCES hands(id)
);
```

---

## 6. 개발 일정

### 6.1 마일스톤

| 주차 | 마일스톤 | 산출물 | 검증 기준 |
|:----:|----------|--------|----------|
| 1-2 | **Alpha** | RFID + 기본 오버레이 | 카드 1장 인식 → 화면 표시 |
| 3-4 | **Beta** | Action Tracker 완성 | 10인 액션 입력 가능 |
| 5-6 | **RC** | 플레이어 관리 + 통계 | 세션 저장/불러오기 |
| 7-8 | **Release** | Trustless Mode + 테스트 | 4시간 무중단 |

### 6.2 주차별 상세

#### Week 1-2: Alpha
- [ ] ESP32 + MFRC522 배선 및 펌웨어
- [ ] Python Serial 리더 구현
- [ ] SQLite 카드 DB 초기화
- [ ] 기본 React 오버레이 (카드 1장 표시)
- [ ] WebSocket 연결

#### Week 3-4: Beta
- [ ] Action Tracker UI 전체 구현
- [ ] 10인 좌석 그리드
- [ ] 모든 액션 버튼 (FOLD/CHECK/CALL/BET/RAISE/ALL-IN)
- [ ] 베팅 입력 UI
- [ ] 키보드 단축키

#### Week 5-6: RC
- [ ] Pre-Start Setup 화면
- [ ] 플레이어 정보 관리
- [ ] 핸드 히스토리 저장
- [ ] 기본 통계 (VPIP, PFR)
- [ ] GFX Console 기본 기능

#### Week 7-8: Release
- [ ] Trustless Mode 구현 (30초 딜레이)
- [ ] Equity 계산기 연동
- [ ] 4시간 무중단 테스트
- [ ] 운영자 피드백 반영
- [ ] 최종 검수 및 서명

---

## 7. 테스트 계획

### 7.1 단위 테스트

| 컴포넌트 | 테스트 항목 | 기대 결과 |
|----------|------------|----------|
| RFID Reader | UID 읽기 | 정확한 UID 반환 |
| Card DB | UID → Card 조회 | 올바른 카드 정보 |
| WebSocket | 메시지 전송 | < 100ms 지연 |
| Action Tracker | 액션 입력 | 상태 정확히 반영 |

### 7.2 통합 테스트

| 시나리오 | 단계 | 검증 |
|----------|------|------|
| **E2E 카드 인식** | 카드 태그 → 화면 표시 | < 200ms |
| **10핸드 세션** | 10핸드 연속 진행 | 모든 데이터 저장 |
| **Trustless 모드** | 카드 태그 → 30초 후 표시 | 정확한 딜레이 |

### 7.3 방송 테스트

| 테스트 | 조건 | 통과 기준 |
|--------|------|----------|
| **4시간 무중단** | 실제 방송 환경 | 에러 0건 |
| **인식률** | 100회 카드 태그 | 99% 이상 |
| **운영자 검증** | 기존 GFX 비교 | "차이 없음" 서명 |

---

## 8. 위험 관리

| 위험 | 영향도 | 발생 확률 | 대응 방안 |
|------|:------:|:--------:|----------|
| RFID 인식 불안정 | 높음 | 중간 | 리더 위치 조정, 차폐 |
| ESP32 연결 끊김 | 높음 | 낮음 | 자동 재연결 로직 |
| DB 손상 | 높음 | 낮음 | 자동 백업 (1시간) |
| WebSocket 끊김 | 중간 | 중간 | 재연결 + 상태 복원 |

---

## 9. Phase 1 완료 조건 (Gate)

Phase 1 진입을 위해 다음 조건을 **모두** 충족해야 합니다:

| 조건 | 기준 | 검증 방법 | 담당 |
|------|------|----------|------|
| **기능 완성** | 54/54 (100%) | 체크리스트 | 개발팀 |
| **카드 인식** | < 200ms | 타이머 측정 | QA |
| **인식률** | > 99% | 100회 테스트 | QA |
| **무중단** | 4시간 이상 | 방송 테스트 | 운영팀 |
| **운영자 승인** | 2명 서명 | 서명 문서 | 운영팀 |

---

## 10. 부록

### 10.1 관련 문서

- [PokerGFX Feature Checklist](PokerGFX-Feature-Checklist.md)
- [Phase Progression Guide](../5-operations/PHASE-PROGRESSION.md)

### 10.2 외부 참조

- [MFRC522 Datasheet](https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf)
- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Version**: 3.0.0 | **Updated**: 2026-02-03
