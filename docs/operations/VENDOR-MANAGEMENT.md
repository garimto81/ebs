# 업체 관리

이 문서는 **BRACELET STUDIO** EBS 프로젝트의 외주 업체 선정, 관리, 커뮤니케이션을 위한 운영 문서입니다.

---

## 1. 업체 관리 개요

### 1.1 업체 필요 영역

| 영역 | 필요 시기 | 업체 유형 | 우선순위 |
|------|----------|----------|:--------:|
| PCB 제조 | Phase 0 | PCB 제조업체 | 1순위 |
| PCB 조립 (SMT) | Phase 0 | EMS 업체 | 1순위 |
| RFID 안테나 설계 | Phase 0 | RF 전문업체 | 2순위 |
| 하우징 제작 | Phase 1 | 사출/CNC 업체 | 3순위 |

### 1.2 업체 상태 정의

```
업체 라이프사이클:

후보 ──▶ 조사중 ──▶ 견적요청 ──▶ 협상중 ──▶ 계약완료
  │         │          │          │          │
  │         │          │          │          └── 발주 가능
  │         │          │          └── 가격/조건 협의
  │         │          └── RFQ 발송 완료
  │         └── 정보 수집 중
  └── 리스트에 추가됨
```

---

## 2. 업체 현황 대시보드

### 2.1 전체 업체 현황

#### PCB/EMS 업체

| 업체명 | 국가 | 용도 | Phase | 상태 | 우선순위 |
|--------|------|------|:-----:|:----:|:--------:|
| **JLCPCB** | 중국 | PCB+SMT | 0 | 견적요청 | 1순위 |
| **PCBWay** | 중국 | PCB+SMT | 0 | 후보 | 대안 |
| **KOREAECM** | 한국 | EMS | 1-2 | 후보 | 2순위 |

#### RFID 솔루션 업체

| 업체명 | 국가 | 용도 | Phase | 상태 | 우선순위 | 연락처 |
|--------|------|------|:-----:|:----:|:--------:|--------|
| **PokerGFX** | 미국 | RFID 완제품 | - | 벤치마크 | ⭐ | pokergfx.io |
| **RF Poker** | 미국(Atlanta) | RFID 테이블 | - | 벤치마크 | - | rfpoker.com (문의폼) |
| **Faded Spade** | 미국 | RFID 카드 | 0-1 | 조사중 | - | sales@fadedspade.com |
| **엠포플러스** | 한국 | RFID 컨설팅 | 0-1 | 조사중 | - | emfoplus.com |
| **서울테크** | 한국 | RF 안테나 | 0 | 후보 | - | - |

#### RFID 하드웨어/부품 업체

| 업체명 | 국가 | 용도 | Phase | 상태 | 우선순위 | 연락처 |
|--------|------|------|:-----:|:----:|:--------:|--------|
| **ST Microelectronics** | 스위스 | ST25R3911B 제조사 | 0-1 | 핵심 | ⭐ | st.com/contact-us |
| **Waveshare** | 중국 | ST25R3911B 평가보드 | 0 | 조사중 | 1순위 | service.waveshare.com |
| **FEIG Electronic** | 독일 | HF 리더 | 1-2 | 조사중 | - | info@feig.de |
| **GAO RFID** | 미국/캐나다 | 산업용 리더 | 1-2 | 후보 | - | sales@gaorfid.com |
| **Identiv** | 미국 | OEM 모듈 | 1 | 후보 | - | sales@identiv.com |
| **PONGEE Industries** | 대만 | HF 리더 모듈 | 1 | 후보 | - | pongee@pongee.com.tw |

#### DIY/개발용 부품 업체

| 업체명 | 국가 | 용도 | Phase | 상태 | 우선순위 | 연락처 |
|--------|------|------|:-----:|:----:|:--------:|--------|
| **SparkFun** | 미국 | RFID 모듈 | 0 | 학습용 | - | sales@sparkfun.com |
| **Adafruit** | 미국 | PN532 모듈 | 0 | 학습용 | - | support@adafruit.com |

#### 카지노 장비 업체

| 업체명 | 국가 | 용도 | Phase | 상태 | 우선순위 | 연락처 |
|--------|------|------|:-----:|:----:|:--------:|--------|
| **Abbiati Casino** | 이탈리아 | RFID 칩/카드 | - | 참조 | - | info@abbiati.com |
| **Matsui Gaming** | 일본 | 카지노 RFID | - | 참조 | - | matsui-gaming.co.jp |
| **Sun-Fly** | 중국 | RFID 칩 | - | 회신대기 | - | 웹폼 문의 |
| **S.I.T. Korea** | 한국 | 카지노 장비 | - | 참조 | - | casinovendors.com 통해 |
| **Angel Playing Cards** | 일본 | AI+RFID | - | 조사중 | - | angelplayingcards.com |

### 2.2 Phase별 업체 매핑

```
Phase 0 (프로토타입)
├── PCB 제조: JLCPCB (1순위), PCBWay (대안)
├── SMT 조립: JLCPCB (1순위), PCBWay (대안)
└── RFID 컨설팅: 엠포플러스 (조사중)

Phase 1 (소량 10-20개)
├── PCB+SMT: KOREAECM (1순위), JLCPCB (대안)
└── 하우징: 미정

Phase 2 (양산 50+개)
├── PCB+SMT: KOREAECM (1순위)
├── 하우징: 미정
└── 조립: 미정
```

---

## 3. 업체 상세 정보

### 3.1 JLCPCB

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://jlcpcb.com |
| **본사** | 중국 선전 |
| **설립** | 2006년 |
| **주요 서비스** | PCB 제조, SMT 조립, 3D 프린팅 |
| **특징** | 초저가 프로토타입, 24-48h Quick Turn |

**장점:**

- 업계 최저가 PCB 제조 (5장 $2부터)
- 빠른 제조 (24-48시간 옵션)
- 온라인 견적 시스템 (즉시 확인)
- 풍부한 부품 재고 (LCSC 연동)
- ST25R3911B 취급 확인됨

**단점:**

- 중국 발송 (배송 7-14일)
- 영어 커뮤니케이션
- 복잡한 문의는 느린 응답

**예상 비용 (프로토타입 5세트):**

| 항목 | 단가 | 수량 | 소계 |
|------|-----:|:----:|-----:|
| PCB 제작 (2L, 100x100mm) | $2 | 10장 | $20 |
| SMT Assembly | $2/장 | 5장 | $10 |
| ST25R3911B | $15 | 5 | $75 |
| ESP32-WROOM-32 | $3 | 5 | $15 |
| 기타 수동 부품 | - | - | $20 |
| 배송비 (DHL) | - | - | $25 |
| **합계** | | | **$165** |

**다음 액션:**

- [ ] JLCPCB 계정 생성
- [ ] BOM 리스트 정리
- [ ] Gerber 파일 업로드 테스트
- [ ] 온라인 견적 확인
- [ ] ST25R3911B 재고 확인

---

### 3.2 PCBWay

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://pcbway.com |
| **본사** | 중국 선전 |
| **주요 서비스** | PCB, PCBA, CNC, 3D 프린팅 |
| **특징** | 다양한 옵션, 복잡한 보드 강점 |

**장점:**

- 다양한 PCB 옵션 (Flex, HDI, 알루미늄 등)
- 복잡한 보드에 강함
- 한국어 지원 (제한적)

**단점:**

- JLCPCB 대비 10-20% 비쌈
- 배송 다소 느림 (10-20일)

**예상 비용:**

| 항목 | 비용 |
|------|-----:|
| PCB + SMT (5세트) | $100 |
| 부품 | $90 |
| 배송 | $30 |
| **합계** | **$220** |

**상태:** JLCPCB 대안으로 유지

---

### 3.3 KOREAECM

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.korecm.com |
| **위치** | 한국 (경기도) |
| **주요 서비스** | PCB, SMT, 완제품 조립 |
| **특징** | 소량 프로토타입, 한국어 지원 |

**장점:**

- 한국어 소통 가능
- 빠른 대응 (당일 답변)
- 국내 배송 (2-3일)
- 소량 주문 가능 (10개부터)

**단점:**

- 중국 대비 2-3배 비용
- 급행 비용 추가

**예상 비용 (10세트):**

| 항목 | 비용 |
|------|-----:|
| PCB + SMT | $400 |
| 부품 | $200 |
| 배송 | 무료 |
| **합계** | **$600** |

**적합 용도:**

- Phase 1 이후 소량 생산
- 급한 수정/재발주
- 국내 A/S 필요 시

**다음 액션:**

- [ ] Phase 1 착수 시 RFQ 발송

---

### 3.4 엠포플러스

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.emfoplus.com |
| **위치** | 한국 (서울) |
| **주요 서비스** | RFID 솔루션 컨설팅, 커스텀 개발 |
| **특징** | HF/UHF RFID 전문, 안테나 설계 |

**조사 필요 항목:**

- [ ] HF 13.56MHz 안테나 커스텀 설계 가능 여부
- [ ] ST25R3911B 경험 유무
- [ ] 최소 주문 수량
- [ ] 대략적인 비용 범위

**상태:** 추가 조사 필요

---

### 3.5 PokerGFX ⭐ 현재 사용 중 (원본 제품)

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.pokergfx.io |
| **본사** | 미국 |
| **주요 서비스** | RFID 포커 테이블 그래픽 시스템 |
| **특징** | 완제품 RFID 솔루션, 포커 방송 전문 |

**참고:** 현재 BRACELET STUDIO에서 사용 중인 원본 제품. 경쟁사가 아닌 벤치마크 및 복제 대상.

**역할:**

- Phase 0 벤치마크 대상 (기능/UI 100% 복제 목표)
- 1단계 완료 기준: PokerGFX와 동일한 기능 구현

---

### 3.6 Faded Spade

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.fadedspade.com |
| **이메일 (영업/도매)** | sales@fadedspade.com |
| **이메일 (서비스)** | service@fadedspade.com |
| **문의** | https://www.fadedspade.com/contact |
| **Twitter** | @FadedSpadeBrand |
| **Instagram** | @fadedspade |
| **주요 서비스** | RFID 포커 카드 |
| **특징** | WPT 공식 카드, Genesis Gaming 협력 |
| **도매 조건** | 1000세트 이상 시 도매가 적용 |

**회사 소개:**

100% 플라스틱 카드, 커스텀 포커 인덱스, 새로운 페이스 카드 디자인. 포커 플레이어를 위해 제작.

**다음 액션:**

- [ ] RFID 카드 스펙 확인
- [ ] 샘플 구매 문의 (sales@fadedspade.com)

---

### 3.7 Angel Playing Cards

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.angelplayingcards.com |
| **본사** | 일본 교토 |
| **주소** | 8-1-5 Seikadai, Seikacho Soraku-gun, Kyoto 619-0238, Japan |
| **전화** | +81 75 354 8525 |
| **문의폼** | [온라인 문의폼](https://ws.formzu.net/dist/S31266024/) |
| **이메일 도메인** | @angelplayingcards.com |
| **설립** | 1949년 (창업), 1956년 (법인화) |
| **주요 서비스** | AI+RFID 스마트 테이블 시스템, 카지노 카드, Hanafuda |
| **글로벌 거점** | 일본, 싱가포르, 마카오, 호주, 필리핀, 미국, 프랑스 |
| **특징** | 아시아, 오세아니아, 유럽, 북미 지사 보유 |

**적합 용도:**

- 고급 AI+RFID 시스템 참조
- 대규모 카지노 솔루션 벤치마크
- RFID 읽기 시스템 및 AI/광학 인식 시스템 참조

---

### 3.8 Abbiati Casino Equipment

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.abbiati.com |
| **본사** | 이탈리아 토리노 |
| **이메일** | info@abbiati.com |
| **전화** | +39 011 956 78 65 |
| **팩스** | +39 011 956 78 71 |
| **주소** | 9 Strada della Risera, 10090 Rosta TO, Italy |
| **설립** | 1976년 (40년+ 업력) |
| **주요 서비스** | 카지노 칩, 테이블, 룰렛 휠, 레이아웃 |

**적합 용도:**

- RFID 칩/카드 스펙 참조
- 카지노 장비 표준 참조

---

### 3.9 FEIG Electronic

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.feig.de/en |
| **본사** | 독일 헤센 |
| **전화** | +49-6471-3109-0 |
| **운영시간** | 월-목 8am-4pm, 금 8am-1pm |
| **설립** | 50년+ 역사 |
| **직원** | 500명+ |
| **주요 서비스** | HF/LF/UHF RFID 리더, 접근 제어 |
| **특징** | 한국 대리점(MINU) 있음 |

**적합 용도:**

- Phase 1-2 고성능 HF 리더 후보
- 독일 품질 RFID 솔루션

---

### 3.10 GAO RFID

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://gaorfid.com |
| **본사** | 캐나다 토론토 / 미국 뉴욕 |
| **이메일 (영업)** | sales@gaorfid.com |
| **이메일 (기술)** | support@gaorfid.com |
| **전화 (무료)** | 1-877-585-9555 |
| **전화 (일반)** | 1-289-660-5590 |
| **캐나다 주소** | 1885 Clements Rd, Suites 215-218, Pickering, Ontario, L1W 3V4 |
| **미국 주소** | 244 Fifth Avenue, Suite A31, Manhattan, NY 10001 |
| **특징** | 안티콜리전 50태그/초, Global Top 10 BLE & RFID Supplier |

**적합 용도:**

- 멀티 태그 동시 읽기 필요 시
- 산업용 리더 참조

---

### 3.11 Identiv

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.identiv.com |
| **본사** | 미국 캘리포니아 |
| **이메일 (영업)** | sales@identiv.com |
| **이메일 (IR)** | IR@identiv.com |
| **전화** | +1 866-358-1029 (무료) |
| **주소** | 1900-B Carnegie Avenue, Santa Ana, CA 92705 |
| **주요 서비스** | uTrust OEM 모듈, RFID/BLE IoT 솔루션 |
| **특징** | SDK 지원, 다양한 산업 적용 |

**적합 용도:**

- OEM 모듈 필요 시
- Phase 1 커스텀 리더 개발

---

### 3.12 PONGEE Industries

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.pongee.com |
| **본사** | 대만 뉴타이베이시 |
| **이메일** | pongee@pongee.com.tw |
| **전화** | +886-2-8228-0198 |
| **팩스** | +886-2-8228-0191 |
| **주소** | 5F., No.738, Chung-Cheng Rd., Chung-Ho District, New Taipei City 235603, Taiwan |
| **주요 서비스** | HF 리더 모듈, OEM/ODM |
| **특징** | RFID 접근 제어, 전자 잠금장치 |

**적합 용도:**

- Phase 1 OEM 모듈 후보
- 대만 제조 옵션

---

### 3.13 Waveshare

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.waveshare.com |
| **제품 페이지** | https://www.waveshare.com/wiki/ST25R3911B_NFC_Board |
| **기술지원** | https://service.waveshare.com |
| **운영시간** | 9AM-6PM GMT+8 (월-금) |
| **예상 가격** | $50-80 |

**ST25R3911B NFC Board 스펙:**

| 항목 | 내용 |
|------|------|
| NFC 칩 | ST25R3911B |
| 주파수 | 13.56MHz |
| 최대 출력 | 1.4W |
| 인터페이스 | SPI |
| 프로토콜 | ISO18092, ISO14443A/B, ISO15693, FeliCa |
| 컨트롤러 | AT32F413RBT7 |
| 디스플레이 | 1.3" OLED |

**적합 용도:**

- Phase 0 프로토타입 개발
- ST25R3911B 학습/평가

---

### 3.14 SparkFun

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.sparkfun.com |
| **이메일 (영업)** | sales@sparkfun.com |
| **기술지원** | https://forum.sparkfun.com |
| **전화** | (303) 284-0979 |
| **본사** | 미국 콜로라도 Niwot |
| **주요 서비스** | DIY 전자부품, RFID 모듈 |
| **특징** | 풍부한 튜토리얼, 오픈소스 |
| **유통** | DigiKey, Arrow 공식 디스트리뷰터 |

**적합 용도:**

- Phase 0 학습용
- DIY 프로토타입
- 대량 구매 시 sales@sparkfun.com 문의

---

### 3.15 Adafruit

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.adafruit.com |
| **이메일** | support@adafruit.com |
| **문의** | https://www.adafruit.com/contact_us |
| **기술지원** | https://forums.adafruit.com |
| **전화** | +1 646-248-7822 |
| **본사** | 미국 뉴욕 |
| **주요 서비스** | PN532 모듈, DIY 전자부품 |
| **특징** | 풍부한 문서, 학습 자료, 100% 여성 소유 기업 |
| **유통** | Arrow 공식 디스트리뷰터 |

**참고:** 소매점 없음, 방문 불가. 포럼을 통한 기술 지원.

**적합 용도:**

- Phase 0 학습용
- PN532 기반 프로토타입

---

### 3.16 Sun-Fly Casino Chips

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.sunflycasinochips.com |
| **본사** | 중국 |
| **설립** | 2004년 |
| **주요 서비스** | RFID 카지노 칩, PJM 3.0 |
| **생산량** | 연간 600만+ 칩 |
| **특징** | 세계 최대 세라믹 칩 제조사 |

**적합 용도:**

- RFID 칩 기술 참조
- 카지노 RFID 표준 참조

---

### 3.17 Matsui Gaming Machine

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://www.matsui-gaming.co.jp/en/ |
| **본사** | 일본 도쿄 |
| **미국 법인** | https://www.matsui-americainc.com/en |
| **유럽 법인** | https://matsuieurope.com/ |
| **유럽 이메일** | sales@matsuieurope.co.uk |
| **유럽 전화** | +44 (0)161 736 9011 |
| **글로벌 거점** | Manchester, Moscow, Las Vegas, Macau, Seoul |
| **제조 공장** | 일본, 한국 |
| **주요 서비스** | 카지노 칩, 플레이 카드, 레이아웃, 테이블, 룰렛 휠 |
| **특징** | 일본 유일 카지노 장비 제조사, 130개국 공급 |

**적합 용도:**

- 카지노 장비 표준 참조
- 아시아 시장 진출 시 파트너십 후보
- Bicycle 카드 일본 유통사

**컨택 방법:**

- 유럽: sales@matsuieurope.co.uk
- 한국: Seoul 지사 통해 연락

---

### 3.18 RF Poker

**기본 정보:**

| 항목 | 내용 |
|------|------|
| **웹사이트** | https://rfpoker.com |
| **이메일** | contact@rf.team |
| **문의폼** | https://rfpoker.com/contact |
| **본사** | 미국 애틀랜타 |
| **설립** | 2021년 (Seed Stage) |
| **창업자** | Maanit Madan |
| **투자사** | Chocho Ventures |
| **모회사** | RF Labs (https://www.rf.team/) |
| **주요 서비스** | RFID 포커 테이블 시스템 |
| **기술** | 온보드 컴퓨터, 360° 카메라, 스마트 조명, RFID 칩/카드/버튼 |

**적합 용도:**

- RFID 포커 시스템 벤치마크
- 차세대 포커 기술 트렌드 참조

**컨택 방법:**

- 일반 문의: contact@rf.team
- 투자사: sb@chochoventures.com

---

## 4. 선정 기준

### 4.1 평가 항목

| 항목 | 가중치 | 설명 |
|------|:------:|------|
| 비용 | 30% | 총 비용 (제조+부품+배송) |
| 품질 | 25% | 불량률, 마감 품질 |
| 납기 | 20% | 제조+배송 소요 시간 |
| 커뮤니케이션 | 15% | 응답 속도, 언어 |
| 기술 지원 | 10% | DFM 피드백, 문제 해결 |

### 4.2 Phase별 선정 기준

**Phase 0 (프로토타입):**

```
우선순위:
1. 비용 (40%) - 저예산으로 빠른 검증
2. 납기 (30%) - GFX 만료 전 완료 필수
3. 품질 (20%) - 기본 동작 보장
4. 기타 (10%)

→ 결론: JLCPCB 1순위
```

**Phase 1 (소량 생산):**

```
우선순위:
1. 품질 (35%) - 실제 운영용
2. 커뮤니케이션 (25%) - 수정 대응
3. 납기 (20%) - 빠른 반복
4. 비용 (20%)

→ 결론: KOREAECM 1순위
```

---

## 5. 커뮤니케이션 가이드

### 5.1 RFQ 템플릿 (영문)

```
Subject: [EBS RFID Project] Request for Quotation

Dear [Company Name] Team,

We are developing an RFID-based card detection system for poker broadcasting.
We would like to request a quotation for the following:

■ Project Overview
- Application: RFID poker card recognition
- Frequency: 13.56MHz (HF)
- RFID IC: ST25R3911B
- MCU: ESP32-WROOM-32

■ PCB Specifications
- Layers: 2L
- Dimensions: 100mm x 80mm (TBD)
- Quantity: [수량] pcs
- Surface Finish: HASL/ENIG

■ Assembly Requirements
- SMT Assembly: Yes
- Through-hole: Minimal (headers only)
- Components: Customer-provided or sourced by you

■ Questions
1. Do you have experience with ST25R3911B?
2. Can you provide antenna design support?
3. What is the expected lead time?
4. What is the estimated total cost?

Please provide a quotation at your earliest convenience.

Best regards,
[이름]
BRACELET STUDIO
[연락처]
```

### 5.2 RFQ 템플릿 (국문)

```
제목: [EBS RFID 프로젝트] 견적 요청

안녕하세요,

포커 방송용 RFID 카드 인식 시스템을 개발 중입니다.
아래 사양으로 견적 요청드립니다.

■ 프로젝트 개요
- 용도: RFID 포커 카드 인식
- 주파수: 13.56MHz (HF)
- RFID IC: ST25R3911B
- MCU: ESP32-WROOM-32

■ PCB 사양
- 레이어: 2층
- 크기: 100mm x 80mm (예상)
- 수량: [수량]개
- 표면처리: HASL 또는 ENIG

■ 조립 요구사항
- SMT 조립: 필요
- 스루홀: 최소 (커넥터만)
- 부품: 지급 또는 업체 소싱

■ 문의사항
1. ST25R3911B 작업 경험이 있으신가요?
2. 안테나 설계 지원이 가능한가요?
3. 예상 리드타임은 어떻게 되나요?
4. 예상 총 비용은 얼마인가요?

빠른 회신 부탁드립니다.

감사합니다.
[이름]
BRACELET STUDIO
[연락처]
```

### 5.3 필수 문의 항목

| 항목 | 질문 | 이유 |
|------|------|------|
| ST25R3911B 경험 | "Have you worked with ST25R3911B before?" | RF 부품 납땜 경험 확인 |
| 안테나 설계 | "Can you design/tune the antenna?" | 안테나 성능이 핵심 |
| 리드타임 | "What is the lead time for [수량] pcs?" | 일정 계획 |
| 부품 소싱 | "Can you source components or should we provide?" | 비용/시간 최적화 |
| MOQ | "What is your minimum order quantity?" | 소량 주문 가능 여부 |
| 샘플 비용 | "Is there additional cost for prototypes?" | 추가 비용 확인 |

---

## 6. 발주 프로세스

### 6.1 발주 전 체크리스트

**설계 파일:**

- [ ] Gerber 파일 (PCB 레이아웃)
- [ ] BOM (Bill of Materials)
- [ ] Pick & Place 파일 (SMT용)
- [ ] 회로도 PDF (참조용)
- [ ] 어셈블리 도면

**요구사항 문서:**

- [ ] 기능 요구사항
- [ ] 테스트 기준
- [ ] 납품 조건

### 6.2 발주 흐름

```
설계 완료
    │
    ▼
┌─────────────────────────────────────────┐
│ 1. 파일 준비                             │
│    - Gerber, BOM, P&P 파일 정리          │
│    - DRC (Design Rule Check) 통과 확인   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 2. 온라인 업로드 (JLCPCB 기준)           │
│    - https://jlcpcb.com 접속             │
│    - "Quote Now" → Gerber 업로드         │
│    - PCB 옵션 선택 → SMT 추가            │
│    - BOM & P&P 업로드                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 3. 견적 확인 & 결제                      │
│    - 자동 DFM 검토 결과 확인             │
│    - 부품 재고/대체품 확인               │
│    - 배송 옵션 선택                      │
│    - 결제 (PayPal/신용카드)              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ 4. 생산 추적                             │
│    - 주문 상태 확인 (웹사이트)           │
│    - 문제 발생 시 이메일 대응            │
└─────────────────────────────────────────┘
    │
    ▼
수령 & 검수
```

### 6.3 검수 체크리스트

| 항목 | 검사 방법 | 합격 기준 |
|------|----------|----------|
| 외관 | 육안 검사 | 손상, 이물질 없음 |
| 납땜 | 현미경/확대경 | 브릿지, 미납 없음 |
| 전원 | 멀티미터 | 쇼트 없음, 정상 전압 |
| 기본 동작 | 테스트 코드 | LED 점등, Serial 출력 |
| RFID 인식 | 카드 태깅 | 5장 중 5장 인식 |

---

## 7. 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-04 | 5.0.0 | 미확보 연락처 업체 조사 완료: SparkFun, Adafruit, Faded Spade, Matsui, RF Poker, Angel 등 |
| 2026-02-03 | 4.0.0 | Slack List 기반 업체 16개 통합, 연락처 정보 추가 |
| 2026-02-03 | 3.1.0 | 회사명 BRACELET STUDIO 통일 |
| 2026-02-03 | 3.0.0 | 상세 정보 복원, 커뮤니케이션 가이드 추가 |
| 2026-02-02 | 2.0.0 | 초기 작성 |

---

**Version**: 5.0.0 | **Updated**: 2026-02-04 | **BRACELET STUDIO**
