# Phase 0: 업체 선정 체크리스트

> **BRACELET STUDIO** | EBS Project | Phase 0

**목표**: RFID 업체 선정 및 프로토타입 발주 완료 (2026 Q2)

---

## 1. 업체 선정 기준

### 1.1 필수 조건

| # | 조건 | 확인 방법 | 상태 |
|:-:|------|----------|:----:|
| 1 | ST25R3911B 취급 가능 | 견적서에 부품 명시 | ⏳ |
| 2 | PCB 제작 + SMT 조립 | 원스톱 서비스 확인 | ⏳ |
| 3 | 소량 주문 가능 (5-10개) | MOQ 확인 | ⏳ |
| 4 | 해외 배송 가능 | 배송비/납기 확인 | ⏳ |
| 5 | 영어 커뮤니케이션 | 이메일/견적 소통 | ⏳ |

### 1.2 평가 기준

| 항목 | 가중치 | 평가 방법 |
|------|:------:|----------|
| **가격** | 30% | 동일 스펙 기준 최저가 |
| **납기** | 25% | 주문 후 배송까지 기간 |
| **품질** | 25% | 샘플 테스트 결과 |
| **소통** | 20% | 응답 속도, 명확성 |

---

## 2. 업체 후보 리스트

| 순위 | 업체 | 국가 | 강점 | 약점 | 상태 |
|:----:|------|------|------|------|:----:|
| 1 | JLCPCB | 중국 | 저가, 빠른 납기 | 소통 제한 | 🔄 견적 요청 |
| 2 | PCBWay | 중국 | 품질, 소통 | 가격 약간 높음 | ⏳ |
| 3 | Seeed Studio | 중국 | 원스톱 | MOQ 높음 | ⏳ |

---

## 3. 진행 체크리스트

### 3.1 리서치 단계 ✅

- [x] PCB 업체 후보 조사
- [x] SMT 조립 서비스 확인
- [x] ST25R3911B 공급처 확인
- [x] 업체 관리 문서 작성

### 3.2 견적 단계 🔄

- [ ] JLCPCB 견적 요청
- [ ] PCBWay 견적 요청 (백업)
- [ ] 견적 비교표 작성
- [ ] 최종 업체 선정

### 3.3 계약/발주 단계 ⏳

- [ ] 발주서 작성
- [ ] 결제 완료
- [ ] 배송 추적
- [ ] 프로토타입 수령

---

## 4. 견적 요청 템플릿

```
Subject: RFQ - RFID Reader PCB (ST25R3911B)

Hi,

We are looking for PCB fabrication + SMT assembly for an RFID reader board.

Specifications:
- Main IC: ST25R3911B (NFC/RFID reader)
- Board size: ~50x50mm (TBD)
- Layers: 4-layer
- Quantity: 5-10 units (prototype)
- SMT: Full assembly including IC
- Connector: USB-C or FPC

Please provide:
1. Unit price (including components)
2. Lead time
3. Shipping cost to South Korea

Best regards,
[Name]
BRACELET STUDIO
```

---

## 5. 예상 비용

| 항목 | 수량 | 단가 | 소계 |
|------|:----:|-----:|-----:|
| PCB + SMT | 5 | $50 | $250 |
| ST25R3911B | 5 | $10 | $50 |
| 기타 부품 | - | - | $50 |
| 배송비 | 1 | $30 | $30 |
| **합계** | | | **~$380** |

---

## 6. 완료 조건

| # | 조건 | 달성 기준 |
|:-:|------|----------|
| 1 | 업체 선정 | 1개 이상 업체 확정 |
| 2 | 발주 완료 | 결제 및 주문 확인 |
| 3 | 납기 확정 | 예상 도착일 확인 |
| 4 | Phase 1 준비 | 소프트웨어 개발 착수 가능 |

---

**Version**: 1.0.0 | **Updated**: 2026-02-03
