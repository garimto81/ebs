# Phase 0: 업체 선정 체크리스트 (v2.0)

> **BRACELET STUDIO** | EBS Project | Phase 0

**목표**: 포커 방송용 RFID 전문 업체 선정 및 프로덕션 품질 솔루션 확보 (2026 Q2)

---

## Executive Summary

### 전략 전환 배경

| 항목 | v1.0 (기존) | v2.0 (신규) |
|------|-------------|-------------|
| **업체 유형** | PCB/SMT 제조업체 | 포커 RFID 전문 업체 |
| **제품 형태** | 칩 구매 + 자체 PCB | 완성 솔루션 또는 OEM |
| **예산** | ~$400 | $5,000~$15,000 |
| **목표** | 저가 프로토타입 | 프로덕션 품질 시스템 |

### 왜 전환하는가?

1. **PokerGFX 100% 복제 목표**: 소프트웨어만 복제하려면 검증된 하드웨어 필요
2. **카지노 산업 요구사항**: 신뢰성, 보안, 인증 충족 필수
3. **Time-to-Market**: 자체 개발보다 도입이 빠름 (6개월 vs 2년+)

---

## 1. 업체 후보 리스트

### 1.1 Tier 1: 방송용 솔루션 (검증됨)

| 순위 | 업체 | 웹사이트 | 주요 고객 | 제품 |
|:----:|------|----------|----------|------|
| **1** | **PokerGFX** | pokergfx.io | WSOP, PokerGO | RFID 리더+안테나+카드+SW |
| 2 | RF Poker | rfpoker.com | 다수 카지노 | 카드+칩+테이블 통합 |
| 3 | Tableswin | tables-win.com | 캐시 게임 | 자동 POT/RAKE 계산 |

### 1.2 Tier 2: 테이블 통합업체

| 업체 | 웹사이트 | 역할 | 비고 |
|------|----------|------|------|
| BBO Poker Tables | bbopokertables.com | PokerGFX 공식 통합 | 테이블+RFID 원스톱 |
| Off Tilt Poker Tables | offtiltpokertables.com | 커스텀 RFID 테이블 | 2010년~ |
| Rye Park Gaming | ryeparkgaming.com | WSOP 테이블 공급 | 하이엔드 |

### 1.3 Tier 3: 카드/칩 전문

| 업체 | 제품 | 고객 | 비고 |
|------|------|------|------|
| Faded Spade | RFID 카드 | WPT, Lodge Live | Best-in-class |
| Angel Group | Angel Eye, 카드 | MGM China, Sands | 아시아 시장 |

---

## 2. 업체 선정 기준

### 2.1 필수 조건 (Must Have)

| # | 조건 | 확인 방법 | 상태 |
|:-:|------|----------|:----:|
| 1 | 포커 방송 납품 실적 보유 | 고객사 리스트, 영상 증빙 | ⏳ |
| 2 | RFID 시스템 통합 제공 (카드+안테나+리더) | 제품 스펙 확인 | ⏳ |
| 3 | 소프트웨어 API/프로토콜 문서화 | 기술 문서 요청 | ⏳ |
| 4 | 해외 배송 및 기술 지원 | 이메일 소통 테스트 | ⏳ |
| 5 | OEM/White-label 가능 또는 하드웨어만 구매 가능 | 영업 문의 | ⏳ |

### 2.2 평가 기준

| 항목 | 가중치 | 평가 방법 |
|------|:------:|----------|
| **방송 실적** | 30% | WSOP/WPT급 = 100%, 지역 = 70%, 없음 = 30% |
| **시스템 완성도** | 25% | 통합 솔루션 = 100%, 부분 = 70%, 칩만 = 30% |
| **기술 호환성** | 20% | 문서화 + 샘플코드 = 100%, 문서만 = 70% |
| **기술 지원** | 15% | 24h응답 = 100%, 72h = 70%, 1주+ = 30% |
| **가격** | 10% | 상대 비교 |

---

## 3. 전략 옵션

### Option A: PokerGFX 직접 도입 (권장)

**개요**: 공식 하드웨어 구매 + 소프트웨어는 자체 개발

| 항목 | 내용 |
|------|------|
| **구매 대상** | RFID Reader Module V2, Player Antenna x10, RFID Cards x2덱 |
| **예상 비용** | $3,000~$5,000 (하드웨어만, SW 라이선스 제외) |
| **장점** | 검증된 하드웨어, 즉시 테스트 가능, WSOP 동일 품질 |
| **단점** | 소프트웨어 별도 개발 필요, 해외 배송 |
| **적합 시점** | Phase 0~1 (즉시) |

**구매 항목 상세**:

| 품목 | 수량 | 예상 단가 | 소계 |
|------|:----:|----------:|-----:|
| RFID Reader Module V2 | 1 | $800 | $800 |
| Player Antenna (1.5m cable) | 10 | $150 | $1,500 |
| Muck Antenna | 2 | $150 | $300 |
| RFID Cards (54장 덱) | 2 | $200 | $400 |
| USB Cable + Extender | 1 | $100 | $100 |
| **소계** | | | **$3,100** |
| 배송비 (한국) | 1 | $200 | $200 |
| **합계** | | | **~$3,300** |

### Option B: RF Poker OEM 협력

**개요**: RF Poker 하드웨어 + 자체 소프트웨어

| 항목 | 내용 |
|------|------|
| **장점** | 하드웨어 독립, 칩 트래킹 포함, 자동화 강점 |
| **단점** | OEM 협상 필요, 커스터마이징 범위 불명확 |
| **적합 시점** | Phase 2 (하드웨어 다각화 시) |

### Option C: 자체 개발 (장기)

**개요**: ST25R3911B 기반 자체 시스템 개발

| 항목 | 내용 |
|------|------|
| **장점** | 완전한 소유권, 커스터마이징 자유 |
| **단점** | 2년+ 개발 기간, 높은 리스크, 하드웨어 전문가 필요 |
| **적합 시점** | Phase 3 이후 (옵션으로만 검토) |

---

## 4. 진행 체크리스트

### 4.1 리서치 단계 (Week 1-2)

- [x] 카지노 RFID 시장 분석
- [x] 주요 업체 후보 리스트업
- [x] 업체 선정 기준 정의
- [ ] PokerGFX 공식 스토어 제품 목록 확인
- [ ] RF Poker 제품/가격 문의
- [ ] BBO Poker Tables RFID 패키지 견적

### 4.2 컨택 단계 (Week 3-4)

- [ ] PokerGFX 하드웨어 Only 구매 가능 여부 문의
- [ ] RF Poker OEM 협력 가능성 문의
- [ ] 배송비/납기 확인
- [ ] 기술 문서 (프로토콜, API) 요청

### 4.3 평가 단계 (Week 5-6)

- [ ] 업체별 점수 산정 (평가 기준표)
- [ ] 예산 대비 ROI 분석
- [ ] 최종 업체 선정

### 4.4 발주 단계 (Week 7-8)

- [ ] 발주서 작성
- [ ] 결제 완료
- [ ] 배송 추적
- [ ] 하드웨어 수령 및 검수

---

## 5. 컨택 템플릿

### 5.1 PokerGFX 문의 (영어)

```
Subject: Inquiry - RFID Hardware Purchase (South Korea)

Hi PokerGFX Team,

We are BRACELET STUDIO, a poker broadcast production company based in South Korea.

We are developing our own broadcast software and would like to purchase your
RFID hardware components (without the PokerGFX software license initially):

- RFID Reader Module V2 x1
- Player Antenna x10 (with 1.5m cables)
- Muck Antenna x2
- RFID Cards (2 decks)
- USB-to-Ethernet Extender x1

Questions:
1. Is it possible to purchase hardware only, without software license?
2. What is the total cost including shipping to South Korea?
3. Do you provide technical documentation for the RFID protocol/communication?
4. What is the estimated delivery time?

Best regards,
[Name]
BRACELET STUDIO
```

### 5.2 RF Poker OEM 문의 (영어)

```
Subject: OEM Partnership Inquiry - RFID Poker System

Hi RF Poker Team,

We are BRACELET STUDIO, developing a poker broadcast system for the Korean market.

We are interested in your RFID hardware for potential OEM partnership:
- RFID card readers and antennas
- RFID embedded playing cards

We plan to develop our own broadcast software and would like to integrate
your hardware.

Questions:
1. Do you offer OEM/White-label options for RFID hardware?
2. What is the MOQ for RFID cards and readers?
3. Can you provide technical specifications and communication protocols?
4. What certifications do your products have?

Looking forward to your response.

Best regards,
[Name]
BRACELET STUDIO
```

---

## 6. 예상 비용 비교

| 항목 | Option A (PokerGFX) | Option B (RF Poker) | Option C (자체개발) |
|------|--------------------:|--------------------:|-------------------:|
| 하드웨어 | $3,300 | TBD | $500~1,000 |
| 소프트웨어 | 자체 개발 | 자체 개발 | 자체 개발 |
| 개발 기간 | 6개월 | 8개월 | 24개월+ |
| 리스크 | 낮음 | 중간 | 높음 |
| **총 예상** | **$3,300** | **$4,000~6,000** | **$10,000+** |

---

## 7. 완료 조건

| # | 조건 | 달성 기준 |
|:-:|------|----------|
| 1 | 업체 선정 | 1개 이상 업체 확정, 평가표 완료 |
| 2 | 하드웨어 발주 | 결제 및 주문 확인서 수령 |
| 3 | 기술 문서 확보 | RFID 프로토콜 문서 또는 샘플 코드 |
| 4 | 납기 확정 | 예상 도착일 확인 (8주 이내) |
| 5 | Phase 1 준비 | 소프트웨어 개발 환경 구축 완료 |

---

## 8. 참고 자료

### 8.1 주요 업체 링크

| 업체 | URL |
|------|-----|
| PokerGFX | https://www.pokergfx.io/ |
| PokerGFX Store | https://www.pokergfx.io/store |
| RF Poker | https://rfpoker.com/ |
| Tableswin | https://tables-win.com/ |
| BBO Poker Tables | https://www.bbopokertables.com/ |
| Faded Spade | https://www.fadedspade.com/ |

### 8.2 관련 문서

| 문서 | 용도 |
|------|------|
| `docs/PRD-0003-EBS-RFID-System.md` | Master PRD |
| `docs/phase-1/PokerGFX-Feature-Checklist.md` | 복제 대상 기능 |
| `docs/operations/VENDOR-MANAGEMENT.md` | 업체 관리 가이드 |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2026-02-03 | 초안 (PCB 업체 중심) | EBS Team |
| **2.0.0** | **2026-02-04** | **전략 전환: 포커 RFID 전문 업체 중심으로 재작성** | BRACELET STUDIO |

---

**Version**: 2.0.0 | **Updated**: 2026-02-04
