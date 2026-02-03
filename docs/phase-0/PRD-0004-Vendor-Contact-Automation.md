# PRD-0004: EBS 업체 컨택 자동화 시스템

**Version**: 1.0.0
**Created**: 2026-02-03
**Status**: Draft

---

## 1. 개요

### 1.1 배경

EBS 프로젝트 Phase-Pre 단계에서 RFID 업체 선정을 위해 다수의 업체에 연락해야 합니다. 현재 Slack List에 16개 업체가 등록되어 있으며, 이 중 10개 업체의 연락처가 확보되었습니다.

### 1.2 목표

- 업체 컨택 프로세스 자동화
- 이메일 템플릿 기반 일괄 발송
- Follow-up 자동 추적 및 알림
- Slack List ↔ Gmail 상태 동기화

### 1.3 범위

| 포함 | 제외 |
|------|------|
| 이메일 템플릿 시스템 | 전화/화상 미팅 일정 |
| Gmail 자동 전송 | CRM 시스템 구축 |
| Follow-up 추적 | 계약서 관리 |
| Slack List 상태 연동 | 결제 프로세스 |

---

## 2. 상태 머신 (State Machine)

### 2.1 업체 상태 전이도

```
                                    ┌──────────────┐
                                    │   NEW        │
                                    │ (신규 등록)   │
                                    └──────┬───────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────┐
│                        CONTACT PHASE                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐    RFI 전송     ┌──────────────┐            │
│  │  IDENTIFIED  │───────────────▶│ RFI_SENT     │            │
│  │ (연락처 확보) │                │ (정보요청 발송)│            │
│  └──────────────┘                └──────┬───────┘            │
│                                         │                     │
│         ┌───────────────────────────────┼───────────────┐     │
│         │                               │               │     │
│         ▼                               ▼               ▼     │
│  ┌──────────────┐              ┌──────────────┐  ┌──────────┐│
│  │ NO_RESPONSE  │              │  RESPONDED   │  │ BOUNCED  ││
│  │ (무응답)      │◀─ 7일 경과 ─│  (응답 수신)  │  │ (반송)   ││
│  └──────┬───────┘              └──────┬───────┘  └──────────┘│
│         │                             │                       │
│         │ Follow-up                   │ 관심 표명              │
│         ▼                             ▼                       │
│  ┌──────────────┐              ┌──────────────┐              │
│  │ FOLLOWUP_1   │              │ INTERESTED   │              │
│  │ (1차 후속)    │              │ (관심 업체)   │              │
│  └──────┬───────┘              └──────┬───────┘              │
│         │                             │                       │
│         │ 7일 경과                     │ RFP 전송              │
│         ▼                             ▼                       │
│  ┌──────────────┐              ┌──────────────┐              │
│  │ FOLLOWUP_2   │              │  RFP_SENT    │              │
│  │ (2차 후속)    │              │ (견적요청 발송)│              │
│  └──────┬───────┘              └──────┬───────┘              │
│         │                             │                       │
│         │ 7일 경과                     │ 견적 수신              │
│         ▼                             ▼                       │
│  ┌──────────────┐              ┌──────────────┐              │
│  │   CLOSED     │              │QUOTE_RECEIVED│              │
│  │ (컨택 종료)   │              │ (견적 수신)   │              │
│  └──────────────┘              └──────┬───────┘              │
│                                       │                       │
└───────────────────────────────────────┼───────────────────────┘
                                        │
                                        ▼
                               ┌──────────────┐
                               │  EVALUATING  │
                               │ (검토 중)     │
                               └──────┬───────┘
                                      │
                      ┌───────────────┼───────────────┐
                      ▼               ▼               ▼
               ┌──────────┐   ┌──────────┐   ┌──────────┐
               │ SELECTED │   │ REJECTED │   │ ON_HOLD  │
               │ (선정)    │   │ (탈락)    │   │ (보류)   │
               └──────────┘   └──────────┘   └──────────┘
```

### 2.2 상태 정의

| 상태 | 설명 | 다음 액션 |
|------|------|----------|
| `NEW` | 리스트에 등록됨 | 연락처 확보 |
| `IDENTIFIED` | 연락처 확보 완료 | RFI 전송 |
| `RFI_SENT` | 정보요청 이메일 발송 | 응답 대기 |
| `RESPONDED` | 이메일 응답 수신 | 내용 검토 |
| `NO_RESPONSE` | 7일간 응답 없음 | Follow-up 발송 |
| `FOLLOWUP_1` | 1차 후속 이메일 발송 | 응답 대기 |
| `FOLLOWUP_2` | 2차 후속 이메일 발송 | 응답 대기 |
| `INTERESTED` | 관심 표명 | RFP 전송 |
| `RFP_SENT` | 견적요청 이메일 발송 | 견적 대기 |
| `QUOTE_RECEIVED` | 견적서 수신 | 검토 진행 |
| `EVALUATING` | 내부 검토 중 | 의사결정 |
| `SELECTED` | 최종 선정 | 계약 진행 |
| `REJECTED` | 탈락 | 감사 메일 |
| `ON_HOLD` | 보류 | 추후 재검토 |
| `BOUNCED` | 이메일 반송 | 대체 연락처 확보 |
| `CLOSED` | 컨택 종료 | - |

---

## 3. 이메일 템플릿 시스템

### 3.1 템플릿 구조

```
templates/
├── rfi/
│   ├── rfi_initial.md          # 초기 정보 요청
│   └── rfi_initial.html        # HTML 버전
├── rfp/
│   ├── rfp_request.md          # 견적 요청
│   └── rfp_request.html
├── followup/
│   ├── followup_1.md           # 1차 후속
│   ├── followup_2.md           # 2차 후속 (최종)
│   └── followup_response.md    # 응답 감사
├── closing/
│   ├── thank_you.md            # 감사 메일
│   ├── rejection.md            # 탈락 통보
│   └── hold.md                 # 보류 안내
└── _base.html                  # HTML 기본 레이아웃
```

### 3.2 템플릿 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `{{vendor_name}}` | 업체명 | FEIG Electronic |
| `{{contact_name}}` | 담당자명 | (확보 시) |
| `{{category}}` | 업체 카테고리 | RFID Hardware |
| `{{our_company}}` | 당사명 | GG Production |
| `{{sender_name}}` | 발신자명 | Aiden Kim |
| `{{sender_title}}` | 발신자 직함 | Technical Director |
| `{{sent_date}}` | 발송일 | 2026-02-03 |
| `{{deadline}}` | 응답 기한 | 2026-02-17 |
| `{{project_name}}` | 프로젝트명 | BRACELET STUDIO |

### 3.3 RFI 템플릿 (초기 정보 요청)

```markdown
Subject: [Inquiry] RFID Solution for Professional Poker Broadcasting - {{our_company}}

Dear {{vendor_name}} Team,

I am {{sender_name}}, {{sender_title}} at {{our_company}}, a broadcast production company specializing in professional poker events including WSOP (World Series of Poker).

We are currently evaluating RFID solutions for our live poker broadcasting system and are interested in learning more about your products.

**Our Requirements:**
- HF (13.56MHz) RFID reader compatible with ISO 15693 or ISO 14443
- Fast read speed (< 100ms per card)
- Multi-tag reading capability (2+ cards simultaneously)
- USB or Serial interface for PC integration
- Compact form factor for table integration

**Information Requested:**
1. Product catalog for applicable RFID readers
2. Technical specifications
3. Pricing information (unit price and volume discounts)
4. Lead time and minimum order quantity
5. Sample availability

We would appreciate a response by {{deadline}}.

Best regards,

{{sender_name}}
{{sender_title}}
{{our_company}}
Email: aiden.kim@ggproduction.net
```

### 3.4 Follow-up 템플릿

**1차 Follow-up (7일 후):**

```markdown
Subject: Re: [Inquiry] RFID Solution for Professional Poker Broadcasting - {{our_company}}

Dear {{vendor_name}} Team,

I am following up on my previous email sent on {{sent_date}} regarding RFID solutions for our poker broadcasting project.

We are actively evaluating vendors and would appreciate any information you can provide about your products.

If this inquiry should be directed to a different department or contact, please let me know.

Best regards,
{{sender_name}}
```

**2차 Follow-up (14일 후, 최종):**

```markdown
Subject: Final Follow-up: RFID Solution Inquiry - {{our_company}}

Dear {{vendor_name}} Team,

This is my final follow-up regarding our RFID solution inquiry.

If we do not hear back by {{deadline}}, we will assume you are unable to assist with our project at this time.

We remain interested in your products for future projects and welcome any response.

Best regards,
{{sender_name}}
```

---

## 4. Follow-up 자동화 로직

### 4.1 타임라인

```
Day 0: RFI 전송
        │
Day 1-7: 응답 대기
        │
        ├─ 응답 수신 → RESPONDED 상태로 전환
        │
Day 7: 무응답 시 → FOLLOWUP_1 자동 전송
        │
Day 8-14: 응답 대기
        │
        ├─ 응답 수신 → RESPONDED 상태로 전환
        │
Day 14: 무응답 시 → FOLLOWUP_2 자동 전송
        │
Day 15-21: 응답 대기
        │
        ├─ 응답 수신 → RESPONDED 상태로 전환
        │
Day 21: 무응답 시 → CLOSED 상태로 전환
```

### 4.2 응답 감지 로직

```python
# Gmail 검색 쿼리
def check_response(vendor_email: str, sent_date: datetime) -> bool:
    query = f"from:{vendor_email} after:{sent_date.strftime('%Y/%m/%d')}"
    emails = gmail_client.list_emails(query=query, max_results=5)
    return len(emails) > 0
```

### 4.3 Morning Automation 연동

기존 `morning-automation` 시스템에 Follow-up 체크 추가:

```python
# collectors/followup_checker.py

class FollowupChecker:
    def check_pending_followups(self) -> list[dict]:
        """
        매일 아침 실행하여 Follow-up 필요한 업체 확인
        """
        vendors = self.get_vendors_with_status(['RFI_SENT', 'FOLLOWUP_1'])

        followups_needed = []
        for vendor in vendors:
            days_since_contact = (datetime.now() - vendor.last_contact_date).days

            if vendor.status == 'RFI_SENT' and days_since_contact >= 7:
                followups_needed.append({
                    'vendor': vendor,
                    'action': 'FOLLOWUP_1',
                    'template': 'followup/followup_1.md'
                })
            elif vendor.status == 'FOLLOWUP_1' and days_since_contact >= 7:
                followups_needed.append({
                    'vendor': vendor,
                    'action': 'FOLLOWUP_2',
                    'template': 'followup/followup_2.md'
                })

        return followups_needed
```

---

## 5. Slack List 연동

### 5.1 컬럼 매핑

현재 Slack List 컬럼을 상태 추적에 활용:

| 컬럼 | 용도 | 값 예시 |
|------|------|---------|
| 업체명 | 업체 식별 | FEIG Electronic |
| 카테고리 | 분류 | RFID Hardware |
| 설명 | 업체 정보 | ISO 15693/14443 산업용 |
| 연락처 | 이메일 | info@feig.de |
| **상태** | **컨택 상태** | RFI_SENT, FOLLOWUP_1 등 |

### 5.2 상태 업데이트 API

```python
def update_vendor_status(vendor_id: str, new_status: str) -> bool:
    """
    Slack List 업체 상태 업데이트
    """
    return lists_collector.update_item_text(
        item_id=vendor_id,
        name=vendor.name,
        url=vendor.url,
        info=f"{vendor.description} | {new_status}"
    )
```

---

## 6. Gmail 라벨 구조

### 6.1 라벨 계층

```
EBS/
├── Vendor/
│   ├── RFI-Sent/        # 정보요청 발송
│   ├── RFP-Sent/        # 견적요청 발송
│   ├── Responded/       # 응답 수신
│   ├── Follow-up/       # 후속 연락
│   └── Closed/          # 컨택 종료
├── Status/
│   ├── ⏳-Awaiting-Reply/   # 응답 대기
│   └── ✅-Replied/          # 응답 완료
└── Priority/
    ├── ⭐-High/         # 우선순위 높음
    └── 📌-Watch/        # 주시 대상
```

### 6.2 라벨 자동 적용

```python
def apply_vendor_labels(email_id: str, vendor: Vendor, action: str):
    """
    이메일 전송/수신 시 라벨 자동 적용
    """
    labels_to_add = []

    if action == 'RFI_SENT':
        labels_to_add = ['EBS/Vendor/RFI-Sent', 'EBS/Status/⏳-Awaiting-Reply']
    elif action == 'RESPONSE_RECEIVED':
        labels_to_add = ['EBS/Vendor/Responded', 'EBS/Status/✅-Replied']

    gmail_client.modify_labels(email_id, add_labels=labels_to_add)
```

---

## 7. 구현 계획

### 7.1 Phase 1: 템플릿 시스템 (Day 1-2)

- [ ] 템플릿 디렉토리 구조 생성
- [ ] RFI, Follow-up 템플릿 작성
- [ ] Jinja2 렌더링 엔진 구현
- [ ] 미리보기 기능

### 7.2 Phase 2: 이메일 발송 (Day 3-4)

- [ ] `contact_manager.py` 구현
- [ ] Gmail 전송 연동
- [ ] Slack List 상태 업데이트 연동
- [ ] Gmail 라벨 자동 적용

### 7.3 Phase 3: Follow-up 자동화 (Day 5-6)

- [ ] `followup_checker.py` 구현
- [ ] Morning Automation 연동
- [ ] 응답 감지 로직
- [ ] 상태 자동 전이

### 7.4 Phase 4: 대시보드 (Day 7)

- [ ] 컨택 현황 리포트
- [ ] Slack 알림 연동
- [ ] 일일 브리핑 포함

---

## 8. 성공 지표

| 지표 | 목표 |
|------|------|
| 초기 응답률 | 50% 이상 |
| Follow-up 후 응답률 | 30% 추가 |
| 견적 수신률 | 응답 업체 중 80% |
| 컨택 완료까지 평균 기간 | 14일 이내 |

---

## 9. 리스크 및 대응

| 리스크 | 영향 | 대응 방안 |
|--------|------|----------|
| 스팸 필터 | 이메일 미도달 | 개별 발송, SPF/DKIM 확인 |
| 언어 장벽 | 소통 어려움 | 영문 템플릿 기본 |
| 무응답 다수 | 후보 부족 | 추가 업체 발굴 |
| 견적 지연 | 일정 차질 | 조기 컨택 시작 |

---

## 10. 부록

### 10.1 현재 컨택 가능 업체 (10개)

| 업체 | 이메일 | 카테고리 | 우선순위 |
|------|--------|----------|:--------:|
| FEIG Electronic | info@feig.de | RFID Hardware | ⭐ |
| GAO RFID | sales@gaorfid.com | RFID Hardware | ⭐ |
| Identiv | sales@identiv.com | RFID Hardware | ⭐ |
| PONGEE Industries | pongee@pongee.com.tw | RFID Hardware | - |
| Waveshare | service@waveshare.com | DIY | - |
| SparkFun | customerservice@sparkfun.com | DIY | - |
| Adafruit | support@adafruit.com | DIY | - |
| Abbiati Casino | info@abbiati.com | Casino | - |
| Faded Spade | info@fadedspade.com | RFID Card | ⭐ |
| Angel Playing Cards | overseas@angel-group.co.jp | RFID Card | ⭐ |

### 10.2 연락처 미확보 업체 (6개)

| 업체 | 사유 | 대응 |
|------|------|------|
| PokerGFX | 현재 사용 중 (원본) | 컨택 불필요 |
| RF Poker | 웹사이트 연락처 없음 | 폼 통해 문의 |
| Matsui Gaming | 도메인 미응답 | 대체 연락처 탐색 |
| Sun-Fly | 웹사이트 직접 연락처 없음 | 폼 통해 문의 |
| S.I.T. Korea | 403 차단 | 대체 경로 탐색 |
| ST Microelectronics | 일반 지원만 제공 | 디스트리뷰터 통해 |
