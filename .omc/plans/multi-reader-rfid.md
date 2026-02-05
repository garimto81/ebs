# Work Plan: Multi-Reader RFID Architecture

**Version**: 1.0.0
**Created**: 2026-01-29
**Status**: Ready for Execution
**Spec Reference**: `.omc/autopilot/spec.md`

---

## 1. Context

### 1.1 Objective

포커 테이블에 다중 RFID 리더(최대 10개)를 매립하여 각 플레이어 위치에서 독립적으로 카드를 인식하는 시스템 설계 문서 작성.

### 1.2 Scope

**In Scope (Documentation Only):**
- DESIGN-RFID-Hardware.md에 Section 10 "Multi-Reader Architecture" 추가
- 펌웨어 pseudo-code 및 배선도 포함
- Configuration schema 정의

**Out of Scope:**
- 실제 펌웨어 코드 구현 (Stage 1 범위)
- 서버/프론트엔드 코드 구현 (Stage 1 범위)
- 하드웨어 프로토타입 제작

### 1.3 Critic Feedback Integration

| Critical Issue | Resolution |
|----------------|------------|
| SPI Bus Recovery 미정의 | Section 10.7에 Bus Recovery Protocol 추가 |
| Per-Reader Health Check 부재 | Section 10.6에 Health Check Sequence 추가 |
| Power Threshold 불일치 | 5+ readers = external power로 통일 |

---

## 2. Deliverables

| # | Deliverable | Location |
|---|-------------|----------|
| 1 | Multi-Reader Architecture Section | DESIGN-RFID-Hardware.md Section 10 |
| 2 | GPIO Pin Assignment Table | Section 10.2 |
| 3 | SPI Bus Topology Diagram | Section 10.1 |
| 4 | Time-Division Polling Diagram | Section 10.4 |
| 5 | Failure Handling Strategy | Section 10.6, 10.7 |
| 6 | Configuration Schema | Section 10.8 |
| 7 | Success Criteria Checklist | Section 10.9 |

---

## 3. Task Breakdown

### Task 1: Add Section 10 Header and Overview

**Target**: DESIGN-RFID-Hardware.md 문서 끝에 Section 10 추가

**Content:**
```markdown
## 10. Multi-Reader Architecture (Stage 1+)

### 10.1 System Overview
- Single ESP32, SPI bus sharing, 최대 10 readers
- ASCII art: SPI bus topology diagram
```

**Acceptance Criteria:**
- [ ] Section 10 header 추가됨
- [ ] Overview 텍스트 및 다이어그램 포함

---

### Task 2: GPIO Pin Assignment Table

**Target**: Section 10.2

**Content:**
- 10개 리더 SS 핀 할당 테이블
- Shared SPI 핀 (SCK, MOSI, MISO, RST) 명시
- GPIO 선택 근거 설명

**Acceptance Criteria:**
- [ ] 10개 SS 핀 할당 테이블
- [ ] Avoided GPIOs 설명 (boot strapping 등)

---

### Task 3: Power Distribution Design

**Target**: Section 10.3

**Content:**
- USB Only (≤4 readers) vs External Power (5+ readers)
- Power budget calculation
- Decoupling capacitor 배치 가이드
- **5+ readers = external 3.3V 권장**으로 통일

**Acceptance Criteria:**
- [ ] Power budget 계산 테이블
- [ ] 외부 전원 회로도 (AMS1117-3.3V)

---

### Task 4: Time-Division Polling Strategy

**Target**: Section 10.4

**Content:**
- Sequential polling diagram (ASCII art)
- Polling parameters: 20ms/reader, 200ms full cycle
- Card presence state machine

**Acceptance Criteria:**
- [ ] Time-division polling 다이어그램
- [ ] State machine 다이어그램

---

### Task 5: Physical Spacing Guidelines

**Target**: Section 10.5

**Content:**
- 최소 리더 간격: 15cm 권장
- 포커 테이블 레이아웃 예시
- 케이블 관리 가이드
- 메탈 테이블 대응 (페라이트 시트)

**Acceptance Criteria:**
- [ ] 물리적 배치 다이어그램
- [ ] 케이블 길이 제한 명시

---

### Task 6: Failure Handling & Health Check

**Target**: Section 10.6

**Content:**
- Per-reader health check sequence (Critic feedback)
- Failure modes table
- Graceful degradation strategy
- Error recovery sequence

**Acceptance Criteria:**
- [ ] Health check pseudo-code
- [ ] Failure mode/recovery 테이블

---

### Task 7: SPI Bus Recovery Protocol

**Target**: Section 10.7

**Content:**
- SPI bus lockup detection (Critic feedback)
- Bus recovery sequence
- Watchdog timer integration

**Acceptance Criteria:**
- [ ] Bus recovery 절차 문서화
- [ ] Watchdog timeout 값 명시

---

### Task 8: Configuration Schema

**Target**: Section 10.8

**Content:**
- JSON configuration schema
- Reader-to-seat mapping
- Runtime configuration API endpoints

**Acceptance Criteria:**
- [ ] JSON schema 예시
- [ ] API endpoint 목록

---

### Task 9: Success Criteria & Testing

**Target**: Section 10.9

**Content:**
- Performance targets
- Testing checklist
- Implementation phases

**Acceptance Criteria:**
- [ ] Measurable success criteria 목록
- [ ] Phase별 scope 정의

---

### Task 10: Document Version Update

**Target**: Document header

**Content:**
- Version: 2.3.0 → 2.4.0
- 수정일: 2026-01-29

**Acceptance Criteria:**
- [ ] Version 업데이트
- [ ] Changelog 추가

---

## 4. Task Dependencies

```
Task 1 (Header)
    │
    ├── Task 2 (GPIO)
    ├── Task 3 (Power)
    ├── Task 4 (Polling)
    ├── Task 5 (Spacing)
    │
    ├── Task 6 (Failure) ──┐
    │                      ├── Task 7 (Recovery) depends on 6
    │                      │
    ├── Task 8 (Config)    │
    └── Task 9 (Testing)   │
                           │
Task 10 (Version) ─────────┘ (final)
```

**Parallel Execution Groups:**
- Group A: Tasks 2, 3, 4, 5, 8, 9 (independent)
- Group B: Task 6 → Task 7 (sequential)
- Final: Task 10 (after all)

---

## 5. Execution Strategy

### 5.1 Ultrawork Parallelization

```
[Phase 1: Independent Tasks - Parallel]
Tasks 2, 3, 4, 5, 8, 9 simultaneously

[Phase 2: Sequential Tasks]
Task 6 → Task 7

[Phase 3: Finalization]
Task 1 (header wraps everything)
Task 10 (version update)
```

### 5.2 Delegation Plan

| Task | Agent | Model |
|------|-------|-------|
| Tasks 2-9 | executor | sonnet |
| Task 1, 10 | executor-low | haiku |
| Final Review | architect | opus |

---

## 6. Definition of Done

- [ ] DESIGN-RFID-Hardware.md에 Section 10 추가됨
- [ ] 모든 서브섹션(10.1-10.9) 완성
- [ ] ASCII 다이어그램 포함 (SPI topology, polling, state machine)
- [ ] Critic 피드백 3가지 모두 반영
- [ ] 문서 버전 2.4.0으로 업데이트
- [ ] Architect 검증 통과

---

**PLANNING_COMPLETE**
