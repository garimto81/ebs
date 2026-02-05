# Work Plan: RFID Hardware Vendor Selection Criteria

**Plan ID**: rfid-hardware-selection-criteria
**Created**: 2026-02-04
**Status**: Ready for Execution

---

## 1. Context

### 1.1 Original Request

RFID 하드웨어 업체 선정 기준 수립 및 Phase 0 발주 계획 작성

### 1.2 Background

EBS(Event Broadcasting System)는 BRACELET STUDIO의 포커 방송 인프라 프로젝트입니다. Phase 0의 핵심 목표는 RFID 업체 선정 및 POC 검증입니다.

**핵심 요구사항:**
- **최우선**: 포커 카드 인식 장비 (HF 13.56MHz, ISO 14443A/B)
- **확장성**: 칩 인식은 Phase 2 이후 추가 개발 가능한 아키텍처
- **필수**: 실물 테스트 가능한 형태 (평가 보드/샘플 구매 가능)

### 1.3 Research Findings

**평가 대상 업체 (6개):**

| 업체 | 제품 유형 | 국가 | 강점 |
|------|----------|------|------|
| ST Microelectronics | ST25R3911B 제조사 | 스위스 | 원천 기술, 공식 문서 |
| Waveshare | ST25R3911B 평가보드 | 중국 | 즉시 구매 가능, 저렴 |
| FEIG Electronic | HF 리더 | 독일 | 산업용 품질, 한국 대리점 |
| GAO RFID | 산업용 리더 | 미국/캐나다 | 멀티 태그 동시 읽기 |
| Identiv | OEM 모듈 | 미국 | SDK 지원 |
| PONGEE Industries | HF 리더 모듈 | 대만 | OEM/ODM |

**기존 문서 분석:**
- VENDOR-MANAGEMENT.md: 16개 업체 상세 정보 보유
- Waveshare ST25R3911B 보드: $50-80 예상, 즉시 구매 가능
- JLCPCB: PCB+SMT 원스톱, ST25R3911B 재고 확인됨

---

## 2. Work Objectives

### 2.1 Core Objective

RFID 하드웨어 업체 선정을 위한 **평가 체계 수립** 및 **Phase 0 발주 계획 확정**

### 2.2 Deliverables

| # | 산출물 | 형식 | 위치 |
|:-:|--------|------|------|
| 1 | 업체별 평가표 | Markdown 테이블 | VENDOR-SELECTION-CHECKLIST.md |
| 2 | 최종 추천 업체 (우선순위/근거) | 섹션 추가 | VENDOR-SELECTION-CHECKLIST.md |
| 3 | Phase 0 발주 계획 (구성/비용) | 섹션 추가 | VENDOR-SELECTION-CHECKLIST.md |

### 2.3 Definition of Done

- [ ] 업체별 평가표가 5개 핵심 기준으로 작성됨
- [ ] 최종 추천 업체 3순위까지 선정 및 근거 명시
- [ ] Phase 0 발주 하드웨어 구성 및 예상 비용 명시
- [ ] 기존 VENDOR-SELECTION-CHECKLIST.md에 통합됨

---

## 3. Guardrails

### 3.1 Must Have

| # | 항목 | 이유 |
|:-:|------|------|
| 1 | HF 13.56MHz, ISO 14443A/B 지원 | 포커 카드 RFID 표준 |
| 2 | ST25R3911B 기반 | 프로젝트 핵심 IC |
| 3 | 평가 보드/샘플 구매 가능 | POC 검증 필수 |
| 4 | 소량 주문 가능 (5개 이하) | Phase 0 프로토타입 |
| 5 | 해외 배송 가능 (한국) | 실물 테스트 필수 |

### 3.2 Must NOT Have

| # | 항목 | 이유 |
|:-:|------|------|
| 1 | UHF (860-960MHz) 전용 | 포커 카드에 부적합 |
| 2 | MOQ 100개 이상 | Phase 0 예산 초과 |
| 3 | 커스텀 제작만 가능 | 즉시 테스트 불가 |

---

## 4. Task Breakdown

### Phase 1: 평가 기준 정의 [1h]

| Task | Description | Acceptance Criteria |
|------|-------------|---------------------|
| 1.1 | 평가 기준 5개 항목 정의 | 카드 인식 성능, 확장성, 테스트 가능성, 가격, 기술 지원 |
| 1.2 | 가중치 배분 | 합계 100%, 우선순위 반영 |
| 1.3 | 점수 체계 정의 | 1-5점 스케일, 기준 명확화 |

### Phase 2: 업체별 평가 [2h]

| Task | Description | Acceptance Criteria |
|------|-------------|---------------------|
| 2.1 | ST Microelectronics 평가 | 5개 기준 점수 산정 |
| 2.2 | Waveshare 평가 | 5개 기준 점수 산정 |
| 2.3 | FEIG Electronic 평가 | 5개 기준 점수 산정 |
| 2.4 | GAO RFID 평가 | 5개 기준 점수 산정 |
| 2.5 | Identiv 평가 | 5개 기준 점수 산정 |
| 2.6 | PONGEE Industries 평가 | 5개 기준 점수 산정 |

### Phase 3: 최종 추천 도출 [1h]

| Task | Description | Acceptance Criteria |
|------|-------------|---------------------|
| 3.1 | 총점 계산 및 순위화 | 가중치 적용 점수 |
| 3.2 | 1-3순위 업체 선정 | 근거 및 리스크 명시 |
| 3.3 | 추천 전략 작성 | Phase 0 최적 접근법 |

### Phase 4: 발주 계획 수립 [1h]

| Task | Description | Acceptance Criteria |
|------|-------------|---------------------|
| 4.1 | 하드웨어 구성 정의 | 필수 품목 리스트 |
| 4.2 | 예상 비용 산정 | 항목별 단가, 총액 |
| 4.3 | 발주 일정 계획 | 타임라인 명시 |

### Phase 5: 문서 통합 [0.5h]

| Task | Description | Acceptance Criteria |
|------|-------------|---------------------|
| 5.1 | VENDOR-SELECTION-CHECKLIST.md 업데이트 | 평가표, 추천, 발주 계획 통합 |
| 5.2 | 상호 참조 확인 | 링크 정합성 검증 |

---

## 5. Detailed Work Specifications

### 5.1 평가 기준 상세

| 기준 | 가중치 | 평가 방법 | 점수 기준 |
|------|:------:|----------|----------|
| **카드 인식 성능** | 30% | ISO 14443A/B 지원, 읽기 거리, 속도 | 5=완벽, 3=적합, 1=부적합 |
| **테스트 가능성** | 25% | 평가 보드 유무, 즉시 구매, 문서화 | 5=즉시 가능, 3=가능, 1=불가 |
| **가격** | 20% | 단가, 배송비, 총 비용 | 5=<$100, 3=$100-300, 1=>$300 |
| **확장성** | 15% | 칩 인식 추가 가능, API/SDK | 5=우수, 3=보통, 1=제한적 |
| **기술 지원** | 10% | 문서, 샘플 코드, 응답 속도 | 5=우수, 3=보통, 1=미흡 |

### 5.2 발주 하드웨어 구성 (안)

**Option A: Waveshare 평가 보드 중심**

| 항목 | 수량 | 예상 단가 | 소계 |
|------|:----:|----------:|-----:|
| Waveshare ST25R3911B NFC Board | 2 | $60 | $120 |
| ESP32-DevKitC | 2 | $10 | $20 |
| RFID 테스트 카드 (ISO 14443A) | 10 | $1 | $10 |
| 점퍼 와이어/브레드보드 | 1세트 | $15 | $15 |
| 배송비 | - | - | $30 |
| **합계** | | | **~$195** |

**Option B: JLCPCB 커스텀 PCB**

| 항목 | 수량 | 예상 단가 | 소계 |
|------|:----:|----------:|-----:|
| 커스텀 PCB + SMT | 5 | $50 | $250 |
| ST25R3911B (JLCPCB 소싱) | 5 | $15 | $75 |
| ESP32-WROOM-32 | 5 | $3 | $15 |
| 기타 수동 부품 | - | - | $20 |
| 배송비 (DHL) | - | - | $25 |
| **합계** | | | **~$385** |

### 5.3 추천 전략 (예상)

**Phase 0 최적 접근:**

1. **1차 (즉시)**: Waveshare 평가 보드 구매 → POC 검증
2. **2차 (POC 성공 후)**: JLCPCB 커스텀 PCB 발주 → Phase 1 준비

**근거:**
- Waveshare: 즉시 구매 가능, 저렴, 학습/검증에 적합
- JLCPCB: 프로덕션 수준 품질, 커스텀 설계 가능

---

## 6. Commit Strategy

| Commit | Scope | Message |
|:------:|-------|---------|
| 1 | 평가 기준/업체 평가표 | `docs(ebs): add RFID vendor evaluation criteria and scorecard` |
| 2 | 최종 추천/발주 계획 | `docs(ebs): add vendor recommendation and Phase 0 procurement plan` |

---

## 7. Success Criteria

| # | Criteria | Verification |
|:-:|----------|--------------|
| 1 | 6개 업체 평가 완료 | 평가표에 모든 점수 기재 |
| 2 | 최종 추천 업체 선정 | 1-3순위 명확, 근거 제시 |
| 3 | Phase 0 발주 계획 확정 | 하드웨어 구성, 예상 비용, 일정 명시 |
| 4 | 기존 문서와 정합성 | VENDOR-MANAGEMENT.md, PRD와 일관성 |

---

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| VENDOR-MANAGEMENT.md | Input | Ready |
| PRD-0003-EBS-RFID-System.md | Input | Ready |
| VENDOR-SELECTION-CHECKLIST.md | Output | To be updated |

---

## 9. Notes

- **Waveshare 우선 권장**: 즉시 구매 가능, POC 검증에 최적
- **JLCPCB 병렬 준비**: 커스텀 PCB 설계 병행하여 Phase 1 가속화
- **확장성 고려**: 칩 인식은 Phase 2 이후이나, 아키텍처 수준에서 대비

---

**Version**: 1.0.0 | **Created by**: Prometheus
