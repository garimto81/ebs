# EBS Vible Update - Autopilot Specification

**Generated**: 2026-02-02
**Phase**: Stage-Pre (Planning)

---

## Executive Summary

**User Request:**
- Vible 업데이트 - EBS 관련
- RFID 수급할 업체를 정해 외주 줍니다
- 1차: PokerGFX 기능 따라하기
- 2차: AI를 활용한 자동화

**Interpretation:**
- "Vible" = Vendor Information documents (VENDOR-MANAGEMENT.md 등)
- 업체 선정 = Stage 0 RFID 외주 벤더 선정
- 1차/2차 = Stage 1 (PokerGFX 복제) / Stage 3 (AI 자동화)

---

## Requirements Analysis (from Analyst)

### Functional Requirements
1. RFID 벤더 선정 및 문서화
2. Stage 0 외주 업체 결정 (JLCPCB vs PCBWay vs KOREAECM)
3. 벤더 관리 문서 업데이트
4. 견적 요청(RFQ) 준비

### Non-Functional Requirements
- 예산: Stage 0 $200-500 범위
- 리드타임: 프로토타입 2주 이내
- 품질: ST25R3911B 100% 인식률

### Key Decisions Made
| 역할 | 벤더 | 비용 | 리드타임 | 근거 |
|------|------|------|----------|------|
| **Primary (Stage 0)** | JLCPCB | $100-150 | 10-14일 | 최저가, ST25R3911B 재고, 빠른 턴어라운드 |
| **Backup** | PCBWay | $150-200 | 15-22일 | 안테나 설계 지원 우수 |
| **Consulting** | Empoph Plus | $500-1000 | N/A | 13.56MHz 안테나 전문 |

---

## Deliverables

### P0 - Must Create/Update

| File | Action | Purpose |
|------|--------|---------|
| `docs/operations/VENDOR-MANAGEMENT.md` | Update | JLCPCB 상태를 "견적요청"으로 변경 |
| `docs/decisions/DECISION-RFID-Vendor-Stage0.md` | Create | 벤더 선정 의사결정 문서 |
| `docs/operations/vendors/JLCPCB.md` | Create | 상세 벤더 카드 |

### P1 - Should Create

| File | Action | Purpose |
|------|--------|---------|
| `docs/operations/vendors/KOREAECM.md` | Create | Stage 1 벤더 카드 |
| `docs/contracts/RFQ-JLCPCB-Stage0.md` | Create | 견적요청 템플릿 |

### P2 - Nice to Have

| File | Action | Purpose |
|------|--------|---------|
| `docs/operations/EBS-WORK-DASHBOARD.md` | Update | 작업 현황 반영 |

---

## Vendor Scoring Matrix

**Stage 0 가중치 기준:**

| 기준 | 가중치 | 설명 |
|------|:------:|------|
| 기술력 | 30% | RFID 안테나 설계, ST25R3911B 지원 |
| 가격 | 25% | 프로토타입 + 소량 생산 비용 |
| 리드타임 | 20% | 프로토타입 납기 |
| 커뮤니케이션 | 15% | 언어, 시차, 응답 속도 |
| 확장성 | 10% | 소량→대량 전환 가능성 |

**점수 결과:**

| 벤더 | 기술(30%) | 가격(25%) | 리드(20%) | 소통(15%) | 확장(10%) | **총점** |
|------|:---------:|:---------:|:---------:|:---------:|:---------:|:--------:|
| **JLCPCB** | 3.0 | 5.0 | 5.0 | 3.0 | 4.0 | **4.00** |
| **KOREAECM** | 4.0 | 3.0 | 4.0 | 5.0 | 5.0 | **4.00** |
| **PCBWay** | 4.0 | 4.0 | 4.0 | 3.0 | 4.0 | **3.85** |

---

## Acceptance Criteria

### 완료 체크리스트

**문서 완료:**
- [ ] `VENDOR-MANAGEMENT.md` JLCPCB 상태 업데이트
- [ ] `DECISION-RFID-Vendor-Stage0.md` 생성
- [ ] `vendors/JLCPCB.md` 벤더 카드 생성

**기술 준비:**
- [ ] ST25R3911B JLCPCB 재고 확인
- [ ] PCB 사이즈 제약 이해 (10x10cm = 최저가)

---

## Blocking Dependencies

| 블로커 | 해결 방법 | 담당 | ETA |
|--------|----------|------|-----|
| **예산 승인** | Stage 0 예산 정의 ($200-500) | PM | 벤더 접촉 전 |
| **PCB 설계** | KiCad 회로도 작성 | HW 엔지니어 | JLCPCB 주문 전 |
| **BOM 목록** | 부품 목록 생성 | HW 엔지니어 | PCB 설계와 함께 |

---

## Phase Reference

| Phase | Stage | 내용 |
|-------|-------|------|
| **현재** | Stage-Pre | 벤더 선정 + 문서화 |
| Phase 1 | Stage 1 | PokerGFX 복제 (54개 기능) |
| Phase 2 | Stage 3 | AI 자동화, WSOP 통합 |

---

**EXPANSION_COMPLETE**
