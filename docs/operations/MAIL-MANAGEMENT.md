# EBS 메일 관리 시스템 (Mail Management System)

**작성일**: 2026-02-02
**대상**: Stage 0 하드웨어 외주 업체 커뮤니케이션
**버전**: 1.0.0

---

## 1. 개요

EBS 프로젝트의 하드웨어 외주 업체(RFID 카드/모듈 제조사)와의 메일 커뮤니케이션을 체계적으로 관리하기 위한 시스템입니다.

### 1.1 목적

| 목적 | 설명 |
|------|------|
| **업체 응답 추적** | 견적 요청, 기술 문의, 계약 협의 상태 추적 |
| **메일 히스토리 보존** | 중요 결정 사항 및 합의 내용 기록 |
| **커뮤니케이션 효율화** | 템플릿 활용으로 반복 작업 감소 |
| **팀 협업 강화** | 메일 상태를 팀 전체가 공유 |

### 1.2 관리 대상 업체

RESEARCH-RFID-Poker-Suppliers.md에서 식별된 업체:

| 업체명 | 유형 | 우선순위 | 비고 |
|--------|------|----------|------|
| **RFIDup.com** | OEM 제조 | HIGH | MOQ 낮음, MVP 최적 |
| **TP-RFID** | OEM 제조 | HIGH | 칩 옵션 다양 |
| **D.O RFID TAG** | OEM 제조 | MEDIUM | 15년 경력, 안정성 |
| **NFC Tag Factory** | OEM 제조 | MEDIUM | 종이/PVC 옵션 |
| **JLCPCB** | PCB 제조 | HIGH | 리더 모듈 PCB 제작 |
| **PCBWay** | PCB 제조 | HIGH | 리더 모듈 PCB 제작 |
| **KOREAECM** | 국내 제조 | LOW | 국내 대안 (고비용) |

---

## 2. Gmail 라벨 시스템

### 2.1 라벨 구조 (계층적 설계)

```
EBS-Project/
├── Vendors/
│   ├── RFID-Cards/
│   │   ├── RFIDup
│   │   ├── TP-RFID
│   │   ├── DO-RFID
│   │   └── NFC-Tag-Factory
│   └── PCB-Manufacturing/
│       ├── JLCPCB
│       ├── PCBWay
│       └── KOREAECM
├── Stage/
│   ├── Stage-0-RFID-Connection
│   ├── Stage-1-PokerGFX-Clone
│   └── Stage-2-WSOP-Integration
├── Status/
│   ├── 📧-Sent
│   ├── ⏳-Awaiting-Reply
│   ├── ✅-Replied
│   └── 🚫-Rejected
└── Type/
    ├── 💰-Quote-Request
    ├── 🔧-Technical-Inquiry
    ├── 📝-Contract-Discussion
    └── 📦-Order-Confirmation
```

### 2.2 Gmail 라벨 생성 방법

**Gmail 설정 → 라벨 → 새 라벨 만들기**

1. 최상위 라벨 `EBS-Project` 생성
2. 하위 라벨은 "중첩 대상: EBS-Project" 체크
3. 색상 코드 적용:
   - 📧 Sent: 회색
   - ⏳ Awaiting-Reply: 노란색
   - ✅ Replied: 초록색
   - 🚫 Rejected: 빨간색

### 2.3 자동 필터 설정 (권장)

**Gmail 설정 → 필터 및 차단된 주소 → 새 필터 만들기**

| 필터 규칙 | 액션 | 라벨 |
|----------|------|------|
| `from:(*@rfidup.com)` | 라벨 적용 + 별표 | `EBS-Project/Vendors/RFID-Cards/RFIDup` + `Status/✅-Replied` |
| `from:(*@tp-rfid.com)` | 라벨 적용 + 별표 | `EBS-Project/Vendors/RFID-Cards/TP-RFID` + `Status/✅-Replied` |
| `from:(*@jlcpcb.com)` | 라벨 적용 + 별표 | `EBS-Project/Vendors/PCB-Manufacturing/JLCPCB` + `Status/✅-Replied` |

**자동화 효과**: 업체 답변 시 자동으로 라벨 부여 + 알림

---

## 3. 메일 추적 템플릿

### 3.1 스프레드시트 설계 (Google Sheets 권장)

**파일명**: `EBS-Mail-Tracker.xlsx` (또는 Google Sheets)
**위치**: `docs/operations/EBS-Mail-Tracker.xlsx`

**컬럼 구조**:

| 컬럼 | 설명 | 타입 | 예시 |
|------|------|------|------|
| **Mail ID** | 고유 식별자 | 텍스트 | `EBS-MAIL-001` |
| **Date Sent** | 발송일 | 날짜 | `2026-02-02` |
| **Vendor** | 업체명 | 드롭다운 | `RFIDup` |
| **Type** | 메일 유형 | 드롭다운 | `Quote Request` |
| **Subject** | 메일 제목 | 텍스트 | `RFID Card Quote Request for EBS Project` |
| **Status** | 현재 상태 | 드롭다운 | `⏳ Awaiting Reply` |
| **Date Replied** | 답변일 | 날짜 | `2026-02-05` |
| **Response Summary** | 답변 요약 | 텍스트 | `Quote: $150/deck, MOQ 10 decks` |
| **Next Action** | 다음 단계 | 텍스트 | `Request sample, Clarify delivery time` |
| **Priority** | 우선순위 | 드롭다운 | `HIGH` / `MEDIUM` / `LOW` |
| **Gmail Link** | 메일 링크 | URL | `https://mail.google.com/mail/u/0/#inbox/...` |

### 3.2 상태 코드 정의

| 상태 | 아이콘 | 의미 | 다음 액션 |
|------|--------|------|----------|
| **Sent** | 📧 | 발송 완료, 답변 대기 전 | 48시간 후 `Awaiting Reply`로 전환 |
| **Awaiting Reply** | ⏳ | 답변 대기 중 | 72시간 초과 시 Follow-up 발송 |
| **Replied** | ✅ | 답변 수신 | Response Summary 작성 + Next Action 결정 |
| **Rejected** | 🚫 | 거절/진행 불가 | Reason 기록, 대체 업체 검토 |
| **On Hold** | ⏸️ | 보류 (내부 사유) | 재개 조건 명시 |
| **Completed** | 🎯 | 계약 완료/주문 확정 | 이동: Contract Tracker로 |

### 3.3 메일 유형 분류

| Type | 아이콘 | 설명 | 평균 응답 시간 |
|------|--------|------|----------------|
| **Quote Request** | 💰 | 견적 요청 | 3-7 영업일 |
| **Technical Inquiry** | 🔧 | 기술 사양 문의 | 1-3 영업일 |
| **Sample Request** | 🧪 | 샘플 제품 요청 | 7-14일 (배송 포함) |
| **Contract Discussion** | 📝 | 계약 조건 협의 | 3-5 영업일 |
| **Order Confirmation** | 📦 | 주문 확정 | 1-2 영업일 |
| **Follow-up** | 🔄 | 재문의 (무응답 후) | 1-2 영업일 |

---

## 4. 메일 템플릿

### 4.1 견적 요청 (Quote Request)

**Subject**: `[EBS Project] RFID Card Quote Request - MVP Stage`

```
Dear [Vendor Name] Sales Team,

I am writing on behalf of the EBS (Event Broadcasting System) project team. We are developing an RFID-based poker card recognition system for live broadcast production.

We are currently at the MVP stage (Stage 0) and would like to request a quote for the following:

**RFID Card Specifications:**
- Frequency: 13.56 MHz (HF)
- Chip: NXP Mifare Ultralight EV1 or NTAG213
- Size: 88×63mm (standard poker size)
- Material: PVC
- Quantity: 10 decks (540 cards total)
- Customization: Single-side custom printing (optional)

**Questions:**
1. Unit price per deck (for 10 decks)
2. Minimum Order Quantity (MOQ)
3. Lead time from order confirmation to delivery
4. Shipping cost to South Korea (Seoul)
5. Sample availability and cost
6. Payment terms

**Project Background:**
EBS is a live poker broadcasting system that uses RFID technology to automatically recognize and display hole cards to viewers. This quote is for the initial prototype phase (Stage 0), with potential for larger orders in Stage 1 (Q3 2026).

Could you please provide a detailed quote by [Date: 1 week from now]?

Best regards,
[Your Name]
EBS Project Team
[Email]
[Phone]
```

### 4.2 기술 문의 (Technical Inquiry)

**Subject**: `[EBS Project] Technical Inquiry - RFID Card Compatibility`

```
Dear [Vendor Name] Technical Team,

I am reaching out regarding RFID card compatibility for our EBS project. We are using the MFRC522 reader module with an ESP32 microcontroller.

**Our Hardware Setup:**
- Reader: MFRC522 (13.56 MHz, ISO 14443A)
- MCU: ESP32 DevKitC
- Library: MFRC522 Arduino Library

**Questions:**
1. Are your RFID cards compatible with MFRC522 readers?
2. What is the recommended read distance for poker card thickness (0.35-0.37mm)?
3. Do you provide UID (Unique Identifier) mapping data?
4. Is the UID format compatible with ISO 14443A?
5. Can the RFID chip survive repeated bending (poker shuffle)?

**Additional Request:**
If available, could you share:
- Technical datasheet (chip model, antenna design)
- Sample code or integration guide for MFRC522

Thank you for your assistance.

Best regards,
[Your Name]
EBS Project Team
```

### 4.3 샘플 요청 (Sample Request)

**Subject**: `[EBS Project] Sample Request - RFID Poker Cards`

```
Dear [Vendor Name],

Following our previous discussion, we would like to request a sample of your RFID poker cards for testing.

**Sample Requirements:**
- Quantity: 1 deck (52 cards + 2 jokers)
- Chip: Mifare Ultralight or NTAG213
- Frequency: 13.56 MHz
- Design: Standard poker card design (face values + suits)

**Testing Plan:**
We will conduct the following tests:
1. MFRC522 reader compatibility
2. Read distance measurement
3. Read speed under real-world conditions (poker table scenario)
4. Durability test (shuffle, bending)

**Shipping Information:**
- Address: [Your Address]
- Contact: [Phone]
- Preferred Delivery: DHL or FedEx

**Timeline:**
We aim to complete testing by [Date] and make a purchase decision for the full order (10+ decks) shortly after.

Could you provide:
1. Sample cost (including shipping)
2. Estimated delivery time
3. Payment method for sample order

Thank you.

Best regards,
[Your Name]
EBS Project Team
```

### 4.4 Follow-up (무응답 후 재문의)

**Subject**: `Re: [EBS Project] RFID Card Quote Request - Follow-up`

```
Dear [Vendor Name],

I am following up on my previous email sent on [Date] regarding an RFID card quote request for the EBS project.

We are on a tight timeline for Stage 0 development (target: June 2026) and would greatly appreciate your response.

If you need any additional information to provide a quote, please let me know.

Alternatively, if you are unable to fulfill this order, I would appreciate confirmation so we can explore other options.

Thank you for your time.

Best regards,
[Your Name]
EBS Project Team
```

### 4.5 계약 협의 (Contract Discussion)

**Subject**: `[EBS Project] Contract Terms Discussion - Order Confirmation`

```
Dear [Vendor Name],

Thank you for your quote dated [Date]. We are ready to proceed with the order and would like to discuss the following contract terms:

**Proposed Order:**
- Product: RFID Poker Cards (Mifare Ultralight)
- Quantity: 10 decks (540 cards)
- Unit Price: [Price from quote]
- Total Amount: [Total]

**Contract Discussion Points:**
1. **Payment Terms:** 50% deposit + 50% before shipment?
2. **Warranty:** Defective card replacement policy?
3. **Delivery:** Expected delivery date after payment?
4. **Quality Assurance:** Pre-shipment testing/inspection available?
5. **Future Orders:** Discount for Stage 1 bulk order (50+ decks)?

**Documentation Request:**
- Proforma Invoice
- Draft Contract (if applicable)
- Company Registration Certificate (for accounting)

Could we schedule a call to finalize these details?

Available times:
- [Date/Time Option 1]
- [Date/Time Option 2]

Thank you.

Best regards,
[Your Name]
EBS Project Team
```

---

## 5. 자동화 가능 항목

### 5.1 Gmail API 활용 (선택 사항)

**자동화 후보**:

| 자동화 항목 | 도구 | 난이도 |
|------------|------|--------|
| 메일 수신 시 자동 라벨 부여 | Gmail 필터 | ⭐ (쉬움) |
| 메일 수신 시 Google Sheets 자동 기록 | Apps Script | ⭐⭐ (중간) |
| 72시간 무응답 시 자동 Follow-up | Apps Script + Time Trigger | ⭐⭐⭐ (어려움) |
| Slack/Discord 알림 연동 | Zapier / Make.com | ⭐⭐ (중간) |

### 5.2 Google Apps Script 예시 (메일 → Sheets 자동 기록)

**파일**: `docs/operations/scripts/mail-to-sheets.gs`

```javascript
function mailToSheets() {
  const label = GmailApp.getUserLabelByName('EBS-Project/Status/✅-Replied');
  const threads = label.getThreads();
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Mail Tracker');

  threads.forEach(thread => {
    const messages = thread.getMessages();
    const lastMessage = messages[messages.length - 1];

    sheet.appendRow([
      `EBS-MAIL-${Date.now()}`,               // Mail ID
      lastMessage.getDate(),                   // Date Replied
      lastMessage.getFrom(),                   // Vendor (Email)
      lastMessage.getSubject(),                // Subject
      '✅ Replied',                            // Status
      lastMessage.getPlainBody().slice(0, 200) // Response Summary (첫 200자)
    ]);
  });
}
```

**실행 방법**:
1. Google Sheets에서 `확장 프로그램 → Apps Script` 열기
2. 위 코드 붙여넣기
3. `트리거 → 시간 기반 트리거 추가` (일 1회 실행)

### 5.3 Zapier/Make.com 자동화 (No-Code)

**시나리오 1: 메일 수신 → Slack 알림**

```
Trigger: Gmail - New Email (Label: EBS-Project/Status/✅-Replied)
Action 1: Parse Email (Subject, From, Body Preview)
Action 2: Slack - Send Channel Message (#ebs-project)
```

**시나리오 2: 72시간 무응답 → Follow-up 알림**

```
Trigger: Schedule (Daily at 9 AM)
Action 1: Google Sheets - Find Row (Status = ⏳ Awaiting Reply)
Action 2: Filter (Date Sent + 72 hours < Today)
Action 3: Gmail - Send Draft (Follow-up Template)
Action 4: Slack - Send DM to Project Manager
```

---

## 6. 문서화 위치 및 형식

### 6.1 디렉토리 구조

```
docs/operations/
├── MAIL-MANAGEMENT.md               # 본 문서 (메일 관리 시스템 설명)
├── EBS-Mail-Tracker.xlsx            # 메일 추적 스프레드시트
├── templates/                       # 메일 템플릿 모음
│   ├── quote-request.txt
│   ├── technical-inquiry.txt
│   ├── sample-request.txt
│   ├── follow-up.txt
│   └── contract-discussion.txt
├── scripts/                         # 자동화 스크립트
│   └── mail-to-sheets.gs            # Gmail → Sheets 자동화
└── attachments/                     # 첨부 파일 보관 (PDF, 견적서 등)
    ├── quotes/
    ├── contracts/
    └── technical-docs/
```

### 6.2 문서 버전 관리

**Git 커밋 규칙**:
```
docs(ebs): Update mail tracker - [Vendor Name] quote received
docs(ebs): Add contract discussion template
docs(ebs): Mail automation script v1.0
```

### 6.3 팀 공유 방법

| 도구 | 용도 | 접근 권한 |
|------|------|----------|
| **GitHub** | 문서 버전 관리 (MAIL-MANAGEMENT.md, templates) | 팀 전체 (읽기/쓰기) |
| **Google Sheets** | 실시간 메일 추적 (EBS-Mail-Tracker) | 팀 전체 (편집 권한) |
| **Google Drive** | 첨부 파일 보관 (quotes/, contracts/) | 팀 전체 + PM 승인 |
| **Slack/Discord** | 실시간 알림 (#ebs-project 채널) | 팀 전체 |

---

## 7. 운영 프로세스

### 7.1 메일 발송 프로세스

```
1. 템플릿 선택
   ↓
2. 업체 정보 기입 (Vendor Name, Email)
   ↓
3. 메일 발송 (Gmail / Outlook)
   ↓
4. Mail Tracker에 기록 (Mail ID, Date Sent, Status: 📧 Sent)
   ↓
5. Gmail 라벨 부여 (EBS-Project/Vendors/..., Status/📧-Sent)
   ↓
6. 48시간 후 상태 변경 (Status: ⏳ Awaiting Reply)
```

### 7.2 메일 수신 프로세스

```
1. Gmail 자동 필터 적용 (라벨: Status/✅-Replied)
   ↓
2. Mail Tracker 업데이트 (Date Replied, Response Summary)
   ↓
3. 답변 검토 (Quote 분석, Technical Compatibility 확인)
   ↓
4. Next Action 결정
   ├── 샘플 요청 → Sample Request 템플릿 사용
   ├── 추가 문의 → Technical Inquiry 템플릿 사용
   ├── 계약 협의 → Contract Discussion 템플릿 사용
   └── 거절/보류 → Status: 🚫 Rejected or ⏸️ On Hold
```

### 7.3 Follow-up 프로세스

```
조건: Date Sent + 72시간 초과 AND Status = ⏳ Awaiting Reply

1. Mail Tracker에서 무응답 건 필터링
   ↓
2. Follow-up 템플릿 사용
   ↓
3. 메일 재발송 (Subject: Re: [Original Subject])
   ↓
4. Mail Tracker에 Follow-up 기록 (Type: 🔄 Follow-up)
   ↓
5. 추가 48시간 대기
   ↓
6. 여전히 무응답 시 → 대체 업체 검토 또는 PM 에스컬레이션
```

---

## 8. 체크리스트

### 8.1 초기 설정 체크리스트

- [ ] Gmail 라벨 생성 (Section 2.1 참조)
- [ ] Gmail 필터 설정 (Section 2.3 참조)
- [ ] Google Sheets 생성 (`EBS-Mail-Tracker`)
- [ ] 템플릿 파일 생성 (`docs/operations/templates/`)
- [ ] 팀원에게 Google Sheets 편집 권한 부여
- [ ] Slack 채널 생성 (`#ebs-project`) (선택 사항)

### 8.2 메일 발송 전 체크리스트

- [ ] 템플릿 선택 완료
- [ ] 업체 정보 정확성 확인 (Email, Contact Person)
- [ ] 첨부 파일 확인 (Spec Sheet, Drawings 등)
- [ ] Mail Tracker에 사전 기록 (Mail ID 부여)
- [ ] 발송 후 Gmail 라벨 수동 확인

### 8.3 메일 수신 후 체크리스트

- [ ] Mail Tracker 업데이트 (Date Replied, Response Summary)
- [ ] 견적서 PDF 저장 (`docs/operations/attachments/quotes/`)
- [ ] Next Action 결정 및 기록
- [ ] 우선순위 재평가 (HIGH/MEDIUM/LOW)
- [ ] 팀 공유 (Slack 메시지 또는 주간 회의)

---

## 9. KPI 및 성과 측정

### 9.1 추적 지표

| KPI | 목표 | 측정 방법 |
|-----|------|----------|
| **평균 응답 시간** | < 5 영업일 | `Date Replied - Date Sent` |
| **Follow-up 필요 비율** | < 30% | `(Follow-up 발송 건수 / 전체 발송 건수) × 100` |
| **견적 수신률** | > 70% | `(견적 수신 건수 / 견적 요청 건수) × 100` |
| **계약 전환율** | > 50% | `(계약 체결 건수 / 견적 수신 건수) × 100` |

### 9.2 주간 리뷰 템플릿

**Meeting**: EBS Weekly Sync (매주 금요일 오전)

**Agenda**:
1. 금주 발송 메일 요약 (Mail Tracker 리뷰)
2. 무응답 건 Follow-up 계획
3. 견적 비교 및 업체 선정 논의
4. Next Week Action Items

---

## 10. 트러블슈팅

### 10.1 자주 발생하는 문제

| 문제 | 원인 | 해결 방법 |
|------|------|----------|
| **메일 무응답** | 잘못된 이메일 주소 / 스팸 차단 | 업체 웹사이트 확인, 전화 문의 |
| **견적 정보 불충분** | 불명확한 요청 사항 | 상세 Spec Sheet 첨부, 질문 구체화 |
| **배송 지연** | 국제 물류 이슈 | 추적 번호 확인, DHL/FedEx 문의 |
| **기술 호환성 문제** | 칩 모델 불일치 | Technical Inquiry 재발송, Datasheet 요청 |

### 10.2 에스컬레이션 기준

| 상황 | 액션 | 담당자 |
|------|------|--------|
| 2회 Follow-up 후 무응답 | PM에게 에스컬레이션 | Project Manager |
| 견적 예산 초과 (30%+) | CFO 승인 필요 | Finance Team |
| 기술 사양 불일치 | 아키텍트 검토 | Technical Architect |
| 계약 조건 분쟁 | 법무 검토 | Legal Team |

---

## 11. 부록

### 11.1 참조 문서

| 문서 | 경로 | 용도 |
|------|------|------|
| 공급업체 리서치 | `docs/research/RESEARCH-RFID-Poker-Suppliers.md` | 업체 배경 정보 |
| Stage 0 PRD | `docs/1-stage0/PRD-0003-Stage0-RFID-Connection.md` | 하드웨어 요구사항 |
| 하드웨어 설계 | `docs/1-stage0/DESIGN-RFID-Hardware.md` | 기술 사양 참조 |

### 11.2 업체 연락처 빠른 참조

| 업체 | Email | 웹사이트 | 우선순위 |
|------|-------|----------|----------|
| **RFIDup** | director@rfidup.com | https://www.rfidup.com/ | HIGH |
| **TP-RFID** | sales@tp-rfid.com | https://www.tp-rfid.com/ | HIGH |
| **D.O RFID TAG** | (웹사이트 문의 폼) | https://www.dorfidtag.com/ | MEDIUM |
| **NFC Tag Factory** | (웹사이트 문의 폼) | https://www.nfctagfactory.com/ | MEDIUM |
| **JLCPCB** | support@jlcpcb.com | https://jlcpcb.com/ | HIGH |
| **PCBWay** | info@pcbway.com | https://www.pcbway.com/ | HIGH |

### 11.3 용어 정의

| 용어 | 설명 |
|------|------|
| **MOQ** | Minimum Order Quantity (최소 주문 수량) |
| **Lead Time** | 주문 확정 후 배송까지 소요 시간 |
| **Proforma Invoice** | 정식 계약 전 견적서 겸 송장 |
| **NDA** | Non-Disclosure Agreement (비밀 유지 계약) |

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **작성일** | 2026-02-02 |
| **버전** | 1.0.0 |
| **작성자** | EBS Operations Team |
| **검토자** | Project Manager |
| **다음 검토일** | 2026-03-01 (또는 Stage 0 완료 시) |

---

**문서 끝**
