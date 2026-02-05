# EBS PoC Implementation Plan

**Version**: 1.0.0
**Created**: 2026-01-30
**Status**: Ready for Execution

---

## Context

### Original Request
6개 PoC 목표를 달성하기 위한 구체적 작업 목록 작성:
1. RFID 모듈 정하기 (P0)
2. 모듈 공급원 확보 (P0)
3. RFID 모듈 통신 성공 (P0)
4. 오버레이 샘플 선정 + 백오피스 기술 기반 (P1)
5. 에디터 구성 - Card-UID 매핑 UI (P2)
6. WSOP+ 데이터 연동 방안 수립 (P2)

### Research Findings
기존 문서 분석 결과:
- **MCU**: ESP32-WROOM-32 확정 (Stage 0 최적)
- **RFID**: MFRC522 확정 (Stage 0), ST25R3911B (Stage 1+ 업그레이드)
- **공급원**: RFIDup.com, TP-RFID (OEM), Faded Spade (프리미엄)
- **기술 스택**: FastAPI + React + WebSocket 확정
- **PRD/가이드**: 이미 상세 문서 존재

### Constraints
- 코드 구현은 executor 에이전트에게 위임
- 이 플랜은 "무엇을 할지" 정의
- 문서 작업과 리서치는 이 단계에서 완료 가능

---

## Work Objectives

### Core Objective
PoC 6개 목표를 병렬 가능한 작업으로 분해하여 Stage 0 완료 기반 마련

### Deliverables
| ID | 산출물 | 형식 | 목표 |
|----|--------|------|------|
| D1 | RFID 모듈 선정 문서 | Markdown | 최종 결정 + 근거 |
| D2 | 공급업체 발주서/연락 목록 | Markdown | 구매 가능 상태 |
| D3 | ESP32-MFRC522 통신 검증 | Code + Log | Serial JSON 출력 |
| D4 | 오버레이 샘플 선정 문서 | Markdown | 3개 후보 + 기술 요구사항 |
| D5 | Card-UID 매핑 UI 프로토타입 | React + HTML Mockup | CRUD 기능 |
| D6 | WSOP+ 연동 방안 문서 | Markdown | API 분석 + 데이터 흐름 |

### Definition of Done
- [ ] P0 목표 3개 완료 (모듈, 공급원, 통신)
- [ ] P1 목표 1개 완료 (오버레이 + 백오피스 기반)
- [ ] P2 목표 2개 완료 (에디터, WSOP+ 방안)
- [ ] 모든 산출물 `docs/` 또는 코드베이스에 저장

---

## Must Have / Must NOT Have

### Must Have
| 항목 | 이유 |
|------|------|
| MFRC522 최종 확정 문서 | 현재 "권장"만 있음, 공식 결정 필요 |
| 구매처 우선순위 목록 | 배송 기간, 가격, 신뢰도 포함 |
| 최소 1회 RFID 통신 성공 로그 | 기술 검증 증거 |
| 오버레이 3개 후보 비교표 | 의사결정 근거 |
| Card-UID 매핑 DB 스키마 | 백오피스 기반 |

### Must NOT Have
| 항목 | 이유 |
|------|------|
| 프로덕션 수준 UI | Stage 0 범위 초과 |
| 다중 리더 구현 | Stage 1 범위 |
| WSOP+ 실제 연동 코드 | 방안 수립만, 구현은 Stage 2 |
| 보안 기능 | Stage 0 범위 초과 |

---

## Task Flow and Dependencies

```
                          [START]
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    [TASK-001]          [TASK-002]          [TASK-003]
    RFID 모듈           공급원 조사          WSOP+ API
    최종 결정           및 발주 준비          리서치
         │                   │                   │
         └─────────┬─────────┘                   │
                   │                             │
                   ▼                             │
              [TASK-004]                         │
              하드웨어 구매                       │
              (외부 의존성)                       │
                   │                             │
         ┌────────┴────────┐                    │
         ▼                 ▼                    │
    [TASK-005]        [TASK-006]               │
    환경 설정          오버레이                  │
    (Arduino IDE)      샘플 조사                │
         │                 │                    │
         ▼                 │                    │
    [TASK-007]             │                    │
    RFID 통신 검증         │                    │
         │                 │                    │
         └────────┬────────┘                    │
                  │                             │
                  ▼                             ▼
             [TASK-008]                    [TASK-009]
             백오피스                       WSOP+ 연동
             DB 스키마                      방안 문서
                  │                             │
                  ▼                             │
             [TASK-010]                         │
             Card-UID                           │
             매핑 UI                            │
                  │                             │
                  └─────────────┬───────────────┘
                                │
                                ▼
                            [DONE]
```

---

## Detailed TODOs

### TASK-001: RFID 모듈 최종 결정 (P0)
**Priority**: P0 | **Effort**: 2h | **Parallel**: Yes

**Description**: 기존 DESIGN-RFID-Hardware.md 분석 결과를 바탕으로 최종 결정 문서 작성

**Acceptance Criteria**:
- [ ] `docs/decisions/DECISION-RFID-Module.md` 생성
- [ ] MFRC522 선택 공식화 + 근거 3개 이상
- [ ] ST25R3911B 업그레이드 경로 명시
- [ ] 대안 비교표 포함

**Dependencies**: None
**Assignee**: writer agent

---

### TASK-002: 공급원 조사 및 발주 준비 (P0)
**Priority**: P0 | **Effort**: 4h | **Parallel**: Yes

**Description**: 기존 RESEARCH-RFID-Poker-Suppliers.md 기반으로 발주 가능한 상태까지 정리

**Acceptance Criteria**:
- [ ] `docs/procurement/PROCUREMENT-RFID-Parts.md` 생성
- [ ] 구매처 우선순위 목록 (Top 3)
  - AliExpress (저가, 2-4주 배송)
  - Amazon (중가, 1주 배송)
  - 국내 (고가, 2-3일 배송)
- [ ] BOM (Bill of Materials) 작성
- [ ] 총 예산 추정 ($15-50)
- [ ] 담당자 연락처 정리 (OEM 문의용)

**Dependencies**: TASK-001 (모듈 확정 후)
**Assignee**: researcher agent

---

### TASK-003: WSOP+ API 리서치 (P2)
**Priority**: P2 | **Effort**: 8h | **Parallel**: Yes

**Description**: WSOP+ 데이터 연동 가능성 조사 (공식 API, 비공식 방법, 수동 입력)

**Acceptance Criteria**:
- [ ] `docs/research/RESEARCH-WSOP-Integration.md` 생성
- [ ] WSOP+ 공식 API 존재 여부 확인
- [ ] 방송 업계 일반적 연동 방식 조사
- [ ] 데이터 포인트 목록 (플레이어명, 칩 카운트, 핸드 히스토리 등)
- [ ] 3가지 연동 시나리오 제안

**Dependencies**: None
**Assignee**: researcher agent

---

### TASK-004: 하드웨어 구매 (외부)
**Priority**: P0 | **Effort**: External | **Parallel**: No

**Description**: 실제 부품 구매 및 배송 대기

**Acceptance Criteria**:
- [ ] 주문 완료
- [ ] 배송 추적 번호 확보
- [ ] 예상 도착일 기록

**Dependencies**: TASK-001, TASK-002
**Assignee**: User (수동)

**BOM (기존 문서 기반)**:
| 부품 | 수량 | 예상 단가 |
|------|------|----------|
| ESP32-WROOM-32 DevKit | 1 | $5-10 |
| MFRC522 모듈 | 1 | $1-5 |
| MIFARE Classic 1K 카드 | 5 | $2.50 |
| 점퍼 와이어 (F-F) | 10 | $1 |
| USB-C 케이블 | 1 | $2 |
| **총계** | - | **$15-25** |

---

### TASK-005: 개발 환경 설정 (P0)
**Priority**: P0 | **Effort**: 2h | **Parallel**: After TASK-004

**Description**: Arduino IDE + ESP32 보드 매니저 + 라이브러리 설치

**Acceptance Criteria**:
- [ ] Arduino IDE 2.0+ 설치 확인
- [ ] ESP32 보드 매니저 추가 (espressif URL)
- [ ] MFRC522 라이브러리 설치 (miguelbalboa/rfid)
- [ ] ArduinoJson 라이브러리 설치
- [ ] USB 드라이버 설치 (CP2102 또는 CH340)
- [ ] Blink 예제 업로드 성공 증거 (스크린샷 또는 로그)

**Dependencies**: TASK-004 (하드웨어 도착)
**Assignee**: executor agent

---

### TASK-006: 오버레이 샘플 조사 (P1)
**Priority**: P1 | **Effort**: 6h | **Parallel**: Yes

**Description**: PokerGFX 스타일 오버레이 3개 후보 선정 및 기술 요구사항 분석

**Acceptance Criteria**:
- [ ] `docs/research/RESEARCH-Overlay-Samples.md` 생성
- [ ] 후보 3개 선정 (스크린샷 포함)
  - PokerGFX 스타일
  - WPT 스타일
  - 자체 커스텀 스타일
- [ ] 각 스타일별 기술 요구사항
  - 해상도, 프레임레이트, 투명도
  - 폰트, 색상 팔레트
  - 애니메이션 요구사항
- [ ] HTML 목업 1개 이상 (`docs/mockups/overlay-sample.html`)

**Dependencies**: None
**Assignee**: designer agent + researcher agent

---

### TASK-007: RFID 통신 검증 (P0)
**Priority**: P0 | **Effort**: 8h | **Parallel**: After TASK-005

**Description**: ESP32 + MFRC522 배선 및 첫 통신 성공

**Acceptance Criteria**:
- [ ] 배선 완료 (7핀 연결)
- [ ] `firmware/rfid_reader/rfid_reader.ino` 업로드
- [ ] Serial Monitor에서 JSON 출력 확인
  ```json
  {"type":"init","status":"ready","reader_id":0}
  {"type":"card_read","uid":"04:A2:B3:C4","reader_id":0,"timestamp":1234}
  ```
- [ ] 5장 MIFARE 카드 인식 테스트 (100% 성공)
- [ ] 통신 성공 로그 저장 (`docs/logs/rfid-first-success.log`)

**Dependencies**: TASK-004, TASK-005
**Assignee**: executor agent (펌웨어) + User (하드웨어 조립)

---

### TASK-008: 백오피스 DB 스키마 설계 (P1)
**Priority**: P1 | **Effort**: 4h | **Parallel**: After TASK-007

**Description**: Card-UID 매핑을 위한 SQLite 스키마 설계

**Acceptance Criteria**:
- [ ] `docs/design/DESIGN-Database-Schema.md` 생성
- [ ] SQLite 스키마 정의
  ```sql
  CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    uid TEXT UNIQUE NOT NULL,
    suit TEXT NOT NULL,  -- spades, hearts, diamonds, clubs
    rank TEXT NOT NULL,  -- A, 2-10, J, Q, K
    display TEXT NOT NULL,  -- "A♠", "K♥", etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- [ ] 52장 카드 + 조커 2장 (54장) 구조
- [ ] 초기 데이터 SQL 스크립트 (`server/db/init.sql`)

**Dependencies**: TASK-007 (UID 포맷 확인 후)
**Assignee**: architect agent

---

### TASK-009: WSOP+ 연동 방안 문서 (P2)
**Priority**: P2 | **Effort**: 4h | **Parallel**: After TASK-003

**Description**: TASK-003 리서치 결과를 바탕으로 구체적 연동 방안 제안

**Acceptance Criteria**:
- [ ] `docs/plans/PLAN-WSOP-Integration.md` 생성
- [ ] 3가지 연동 시나리오 상세화
  1. 공식 API 연동 (가능 시)
  2. 웹 스크래핑 (비공식)
  3. 수동 입력 + CSV Import
- [ ] 데이터 흐름도 (Mermaid 또는 ASCII)
- [ ] Stage 2 구현 로드맵 제안
- [ ] 법적/약관 검토 필요 사항 명시

**Dependencies**: TASK-003
**Assignee**: architect agent

---

### TASK-010: Card-UID 매핑 UI 프로토타입 (P2)
**Priority**: P2 | **Effort**: 12h | **Parallel**: After TASK-008

**Description**: 관리자가 카드 UID와 포커 카드를 매핑하는 웹 UI

**Acceptance Criteria**:
- [ ] HTML 목업 생성 (`docs/mockups/card-editor.html`)
- [ ] React 컴포넌트 구현 (`frontend/src/components/CardEditor/`)
  - 카드 목록 표시 (52+2장)
  - UID 수동 입력 또는 스캔 연동
  - 매핑 저장/수정/삭제
- [ ] FastAPI 엔드포인트 (`server/app/routes/cards.py`)
  - GET /api/cards - 전체 목록
  - POST /api/cards - 매핑 추가
  - PUT /api/cards/{id} - 매핑 수정
  - DELETE /api/cards/{id} - 매핑 삭제
- [ ] 스크린샷 저장 (`docs/images/card-editor-ui.png`)

**Dependencies**: TASK-008
**Assignee**: executor agent (프론트+백엔드)

---

## Parallelization Plan

### Phase 1: 즉시 시작 (병렬)
| Task | Assignee | Est. Hours |
|------|----------|------------|
| TASK-001 | writer | 2h |
| TASK-002 | researcher | 4h |
| TASK-003 | researcher | 8h |
| TASK-006 | designer + researcher | 6h |

**총 병렬 작업 시간**: ~20h (4개 작업)
**실제 소요 시간 (병렬)**: ~8h

### Phase 2: 하드웨어 도착 후
| Task | Assignee | Est. Hours |
|------|----------|------------|
| TASK-005 | executor | 2h |
| TASK-007 | executor + User | 8h |

### Phase 3: 통신 성공 후
| Task | Assignee | Est. Hours |
|------|----------|------------|
| TASK-008 | architect | 4h |
| TASK-009 | architect | 4h |
| TASK-010 | executor | 12h |

---

## Risk and Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| MFRC522 품질 불량 (AliExpress) | 중 | 중 | 여분 1개 추가 구매, Amazon 백업 |
| ESP32 USB 드라이버 문제 | 중 | 중 | CH340 + CP2102 둘 다 준비 |
| RFID 카드 인식 불안정 | 중 | 고 | 바이패스 커패시터 추가, 배선 재점검 |
| WSOP+ API 미존재 | 고 | 중 | 수동 입력 + CSV 대안 준비 |
| 배송 지연 | 저 | 중 | 국내 쇼핑몰 빠른 배송 옵션 |

---

## Commit Strategy

| Milestone | Commit Message |
|-----------|----------------|
| TASK-001 완료 | `docs(ebs): RFID 모듈 최종 결정 문서 추가` |
| TASK-002 완료 | `docs(ebs): 부품 조달 계획서 추가` |
| TASK-003 완료 | `docs(ebs): WSOP+ API 리서치 결과 추가` |
| TASK-006 완료 | `docs(ebs): 오버레이 샘플 조사 + 목업 추가` |
| TASK-007 완료 | `feat(ebs): RFID 펌웨어 초기 구현` |
| TASK-008 완료 | `docs(ebs): DB 스키마 설계 문서 추가` |
| TASK-009 완료 | `docs(ebs): WSOP+ 연동 방안 문서 추가` |
| TASK-010 완료 | `feat(ebs): Card-UID 매핑 UI 프로토타입` |

---

## Success Criteria

### P0 목표 (필수)
- [ ] RFID 모듈 최종 결정 문서 존재
- [ ] 구매 가능 상태 (BOM + 구매처 확정)
- [ ] RFID 통신 성공 로그 1회 이상

### P1 목표 (중요)
- [ ] 오버레이 샘플 3개 비교표
- [ ] DB 스키마 문서 + SQL 스크립트

### P2 목표 (선택)
- [ ] Card-UID 매핑 UI 동작
- [ ] WSOP+ 연동 방안 3가지 시나리오

---

## Document Info

| Item | Value |
|------|-------|
| **Plan Version** | 1.0.0 |
| **Created** | 2026-01-30 |
| **Author** | Prometheus (Planner Agent) |
| **Status** | Ready for Execution |

---

**Plan End**
