# Work Plan: RFID 모듈 최초 연결

---

## Context

### Original Request
RFID 모듈(ESP32 + MFRC522)과 포커 카드 최초 연결. 하드웨어 연결부터 카드 UID 읽기까지의 구현 계획.

### Execution Mode
**ultrawork** - 병렬 실행으로 빠른 구현

### Reference Documents
- `docs/DESIGN-RFID-Hardware.md` - 하드웨어 설계 가이드
- `docs/PRD-0003-EBS-RFID-System.md` - 시스템 PRD v4.0

### Current State
- `firmware/` 디렉토리: 미생성
- Arduino 코드: 없음
- Python 서버: 미구현
- 하드웨어 문서: 완비 (핀맵, 배선도 포함)

---

## Work Objectives

### Core Objective
ESP32 + MFRC522 하드웨어를 연결하고, RFID 카드의 UID를 읽어 시리얼 모니터에 출력하는 기본 펌웨어를 구현한다.

### Deliverables
1. **Arduino 펌웨어** - ESP32용 RFID 카드 UID 읽기 코드
2. **Python Serial Reader** - ESP32 시리얼 출력을 PC에서 수신하는 테스트 스크립트
3. **카드 매핑 도구** - UID ↔ 카드 정보 매핑 유틸리티

### Definition of Done
- [ ] ESP32 + MFRC522 하드웨어 연결 완료 (7핀 배선)
- [ ] 카드를 리더에 대면 UID가 시리얼 모니터에 출력됨
- [ ] Python 스크립트로 시리얼 데이터 수신 확인
- [ ] 최소 3장의 카드 UID를 정상적으로 읽음

---

## Guardrails

### MUST Have
| 요구사항 | 이유 |
|----------|------|
| 3.3V 전원 사용 | MFRC522는 5V에서 손상됨 |
| SPI 핀맵 준수 | GPIO5/18/23/19/4 고정 |
| JSON 형식 출력 | 서버 파싱 호환성 |
| 115200 baud rate | 표준 속도 |

### MUST NOT Have
| 금지사항 | 이유 |
|----------|------|
| WiFi 기능 | Phase 0 MVP 범위 초과 |
| 카드 DB 조회 | Phase 0 범위 초과 |
| 다중 리더 | 단일 리더로 시작 |
| 복잡한 에러 처리 | MVP는 기본 기능에 집중 |

---

## Task Flow and Dependencies

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      RFID First Connection Task Flow                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │                    Phase 1: Setup (병렬)                        │    │
│   │                                                                 │    │
│   │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐ │    │
│   │   │  Task 1.1     │    │  Task 1.2     │    │  Task 1.3     │ │    │
│   │   │ 디렉토리 생성 │    │ 라이브러리   │    │ 하드웨어 배선 │ │    │
│   │   │ firmware/     │    │ 설치 가이드  │    │ 가이드 작성   │ │    │
│   │   └───────┬───────┘    └───────┬───────┘    └───────┬───────┘ │    │
│   │           │                    │                    │          │    │
│   └───────────┼────────────────────┼────────────────────┼──────────┘    │
│               │                    │                    │               │
│               ▼                    ▼                    ▼               │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │                    Phase 2: Firmware (순차)                     │    │
│   │                                                                 │    │
│   │   ┌───────────────────────────────────────────────────────┐   │    │
│   │   │  Task 2.1: Arduino 펌웨어 작성                         │   │    │
│   │   │  - rfid_reader.ino 생성                                │   │    │
│   │   │  - SPI 초기화, MFRC522 초기화                          │   │    │
│   │   │  - UID 읽기 루프                                       │   │    │
│   │   │  - JSON 시리얼 출력                                    │   │    │
│   │   └───────────────────────────────────────────────────────┘   │    │
│   │                              │                                  │    │
│   └──────────────────────────────┼──────────────────────────────────┘    │
│                                  │                                       │
│                                  ▼                                       │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │                    Phase 3: Testing (병렬)                      │    │
│   │                                                                 │    │
│   │   ┌───────────────┐    ┌───────────────┐                      │    │
│   │   │  Task 3.1     │    │  Task 3.2     │                      │    │
│   │   │ Python Serial │    │ 카드 매핑    │                      │    │
│   │   │ Reader 작성   │    │ 도구 작성    │                      │    │
│   │   └───────────────┘    └───────────────┘                      │    │
│   │                                                                 │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed TODOs

### Phase 1: Setup (병렬 실행)

#### Task 1.1: 디렉토리 구조 생성
**Executor**: executor-low
**Estimated**: 2분

```
C:\claude\ebs\
├── firmware/
│   └── rfid_reader/
│       ├── rfid_reader.ino
│       └── README.md
└── tools/
    ├── serial_reader.py
    └── card_mapper.py
```

**Acceptance Criteria**:
- [ ] firmware/rfid_reader/ 디렉토리 생성
- [ ] tools/ 디렉토리에 Python 스크립트용 공간 확보

#### Task 1.2: Arduino 라이브러리 설치 가이드
**Executor**: writer
**Estimated**: 5분

**내용**:
```
1. Arduino IDE 설치 (2.x 권장)
2. ESP32 보드 매니저 추가
   - URL: https://dl.espressif.com/dl/package_esp32_index.json
3. ESP32 보드 설치 (esp32 by Espressif Systems)
4. MFRC522 라이브러리 설치
   - Library Manager → "MFRC522" 검색 → miguelbalboa/rfid 설치
```

**Acceptance Criteria**:
- [ ] README.md에 설치 가이드 포함

#### Task 1.3: 하드웨어 배선 Quick Reference
**Executor**: writer
**Estimated**: 3분

**핀맵** (docs/DESIGN-RFID-Hardware.md 참조):
| ESP32 | MFRC522 | Wire Color |
|-------|---------|------------|
| 3V3   | VCC     | Red        |
| GND   | GND     | Black      |
| GPIO5 | SDA     | Yellow     |
| GPIO18| SCK     | Green      |
| GPIO23| MOSI    | Blue       |
| GPIO19| MISO    | Orange     |
| GPIO4 | RST     | White      |

**Acceptance Criteria**:
- [ ] README.md에 배선 테이블 포함

---

### Phase 2: Firmware (순차 실행)

#### Task 2.1: Arduino 펌웨어 작성
**Executor**: executor
**Estimated**: 15분
**File**: `firmware/rfid_reader/rfid_reader.ino`

**구현 요구사항**:
```cpp
// 핵심 기능
1. SPI 버스 초기화 (핀: 5, 18, 23, 19)
2. MFRC522 초기화 (RST: GPIO4, SS: GPIO5)
3. 카드 감지 루프 (폴링 방식)
4. UID 읽기 및 JSON 출력

// 시리얼 출력 형식
{
  "type": "card_read",
  "uid": "04:A2:B3:C4",
  "reader_id": 0,
  "timestamp": 123456
}

// 설정
- Baud Rate: 115200
- 폴링 간격: 100ms
- 중복 읽기 방지: 같은 UID 연속 무시 (2초 타임아웃)
```

**Acceptance Criteria**:
- [ ] 컴파일 에러 없음
- [ ] 카드 스캔 시 JSON 형식으로 UID 출력
- [ ] 중복 읽기 방지 동작

---

### Phase 3: Testing (병렬 실행)

#### Task 3.1: Python Serial Reader
**Executor**: executor
**Estimated**: 10분
**File**: `tools/serial_reader.py`

**구현 요구사항**:
```python
# 기능
1. COM 포트 자동 감지 (ESP32)
2. 115200 baud로 시리얼 연결
3. JSON 파싱 및 출력
4. Ctrl+C로 종료

# 의존성
- pyserial
```

**Acceptance Criteria**:
- [ ] `python serial_reader.py` 실행 시 시리얼 데이터 수신
- [ ] JSON 파싱 성공 시 카드 정보 출력

#### Task 3.2: 카드 매핑 도구
**Executor**: executor
**Estimated**: 10분
**File**: `tools/card_mapper.py`

**구현 요구사항**:
```python
# 기능
1. 시리얼에서 UID 읽기
2. 사용자에게 카드 정보 입력 요청 (예: "A♠")
3. JSON 파일에 UID-카드 매핑 저장

# 출력 형식 (cards.json)
{
  "04:A2:B3:C4": {"suit": "spades", "rank": "A", "display": "A♠"},
  "04:B5:C6:D7": {"suit": "hearts", "rank": "K", "display": "K♥"}
}
```

**Acceptance Criteria**:
- [ ] 카드 스캔 → UID 표시 → 사용자 입력 → 저장 흐름 동작
- [ ] cards.json 파일 생성/업데이트

---

## Commit Strategy

```
Phase 1 완료 후:
  feat(firmware): add project structure and setup guide

Phase 2 완료 후:
  feat(firmware): implement ESP32 RFID card reader

Phase 3 완료 후:
  feat(tools): add serial reader and card mapping utilities
```

---

## Success Criteria

| 기준 | 측정 방법 | 목표 |
|------|----------|------|
| 카드 인식 | 시리얼 모니터 출력 | UID 정상 출력 |
| 인식 속도 | 카드 대기 → 출력 시간 | < 500ms |
| 안정성 | 10회 연속 스캔 | 100% 성공 |
| Python 수신 | serial_reader.py 출력 | JSON 파싱 성공 |

---

## Risk Mitigation

| 리스크 | 확률 | 대응 |
|--------|------|------|
| ESP32 드라이버 미인식 | 중 | CP2102/CH340 드라이버 설치 가이드 제공 |
| SPI 통신 실패 | 중 | 배선 체크리스트, 멀티미터 확인 권장 |
| 카드 인식 불가 | 낮 | 리더 전원 확인, 거리 조정 |
| Python 시리얼 점유 | 낮 | COM 포트 명시적 지정 옵션 |

---

## Execution Order (ultrawork)

```
병렬 1: [Task 1.1] + [Task 1.2] + [Task 1.3]
         ↓
순차:    [Task 2.1]
         ↓
병렬 2: [Task 3.1] + [Task 3.2]
```

**예상 총 시간**: 약 25분 (병렬 실행 시)

---

**PLAN_READY: C:\claude\ebs\.omc\plans\rfid-first-connection.md**
