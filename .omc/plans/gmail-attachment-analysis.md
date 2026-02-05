# Gmail 첨부파일 분석 및 회신 일정 추적 기능 설계

**Version**: 2.1.0
**Created**: 2026-02-04
**Status**: READY FOR EXECUTION

---

## 설계 철학 변경 (v2.0.0)

### v1.0.0 (폐기)
- Python 백그라운드 자동 처리
- 로컬 텍스트 추출 후 요약

### v2.0.0 (채택)
- **스킬 기반**: Claude가 직접 첨부파일을 열어서 확인 및 추론
- **인터랙티브**: `/daily` 실행 시 Claude가 메일 분석 후 판단
- **지능형**: 단순 텍스트 추출이 아닌 AI 기반 내용 이해

---

## Context

### Original Request

1. Gmail 분석 시 신규 메일의 **첨부파일을 열어서 내용 파악** 후 업데이트
2. 매일 실행 시 **마지막 피드백 메일 회신 일정 확인**하여 알림
3. **스킬로 구현하여 Claude가 직접 확인하고 추론**

### 핵심 설계 결정

| 항목 | 결정 | 이유 |
|------|------|------|
| 첨부파일 분석 | Claude 직접 읽기 | AI 추론 능력 활용 |
| 요약 방식 | Claude 생성 | 단순 텍스트 추출보다 정확 |
| 회신 추적 | JSON 기반 추적 | 단순, 빠름 |
| 실행 방식 | `/daily` 스킬 확장 | 기존 워크플로우 통합 |

---

## Work Objectives

### Core Objective

`/daily` 스킬 실행 시 Claude가:
1. 신규 메일의 첨부파일을 직접 다운로드하여 읽고 분석
2. 업체별 마지막 교신 날짜 추적 및 회신 예정일 계산
3. 브리핑에 분석 결과 포함

### Deliverables

| # | 산출물 | 설명 |
|:-:|--------|------|
| 1 | `GmailClient.get_attachment()` | Gmail API 첨부파일 다운로드 메서드 |
| 2 | `GmailClient.download_attachment()` | 첨부파일 로컬 저장 메서드 |
| 3 | `ReplyTracker` | 업체별 회신 일정 추적 |
| 4 | `/daily` 스킬 확장 | 첨부파일 분석 워크플로우 추가 |

### Definition of Done

- [ ] `get_attachment()` 메서드 구현
- [ ] `download_attachment()` 메서드로 임시 파일 저장
- [ ] GmailCollector에 첨부파일 메타데이터 저장 (email_id 포함)
- [ ] Claude가 PDF 파일을 Read 도구로 직접 읽기 가능
- [ ] ReplyTracker 구현 및 통합점 정의
- [ ] 업체별 마지막 메일 날짜 추적 (JSON 저장)
- [ ] `/daily` 스킬에 첨부파일 분석 워크플로우 문서화
- [ ] 브리핑에 첨부파일 분석 결과 및 회신 일정 포함

---

## Execution Order (CRITICAL)

**의존성 기반 실행 순서:**

```
┌────────────────────────────────────────────────────────────────┐
│  순서 1: GmailCollector 수정                                     │
│  └─ 첨부파일 메타데이터 저장 (email_id + attachment_id)          │
├────────────────────────────────────────────────────────────────┤
│  순서 2: GmailClient 메서드 추가                                 │
│  └─ get_attachment(), download_attachment()                    │
├────────────────────────────────────────────────────────────────┤
│  순서 3: ReplyTracker 클래스 생성                                │
│  └─ 데이터 구조 및 메서드 구현                                   │
├────────────────────────────────────────────────────────────────┤
│  순서 4: /daily 스킬 확장                                        │
│  └─ 첨부파일 분석 + 회신 추적 워크플로우 추가                     │
└────────────────────────────────────────────────────────────────┘
```

| 순서 | Task | 의존성 | 파일 |
|:----:|------|--------|------|
| 1 | GmailCollector 수정 | 없음 | `collectors/gmail_collector.py` |
| 2 | GmailClient 메서드 | 없음 | `lib/gmail/client.py` |
| 3 | ReplyTracker | 없음 | `trackers/reply_tracker.py` |
| 4 | `/daily` 스킬 확장 | 1, 2, 3 완료 필요 | `.claude/skills/daily/SKILL.md` |

---

## Architecture

### 워크플로우 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                      /daily 스킬 실행                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: 데이터 수집 (기존)                                     │
│  └─ python main.py --notify --post                              │
│                                                                 │
│  Phase 2: Claude 첨부파일 분석 (신규)                            │
│  ├─ Step 2.1: 신규 메일 중 첨부파일 있는 메일 필터                 │
│  │   └─ Read: data/gmail_emails.json                            │
│  │                                                               │
│  ├─ Step 2.2: 각 첨부파일 다운로드                                │
│  │   └─ Bash: python -c "from lib.gmail import ...; download()" │
│  │                                                               │
│  ├─ Step 2.3: Claude가 첨부파일 직접 읽기                        │
│  │   └─ Read: temp/attachments/{filename}.pdf                   │
│  │                                                               │
│  ├─ Step 2.4: Claude 분석 및 요약 생성                           │
│  │   └─ AI 추론: 내용 이해, 핵심 정보 추출, 액션 아이템 도출      │
│  │                                                               │
│  └─ Step 2.5: 임시 파일 삭제                                     │
│      └─ PowerShell: Remove-Item -Recurse -Force temp/attachments│
│                                                                 │
│  Phase 3: 회신 일정 추적 (신규)                                  │
│  ├─ Read: data/reply_schedule.json                              │
│  ├─ 업체별 마지막 연락일 확인                                     │
│  └─ Overdue 업체 알림 생성                                       │
│                                                                 │
│  Phase 4: 브리핑 출력                                            │
│  └─ 첨부파일 분석 결과 + 회신 일정 포함                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed TODOs

### Task 1: GmailClient 첨부파일 다운로드 메서드

**파일**: `C:\claude\lib\gmail\client.py`

**추가 메서드**:
```python
def get_attachment(self, email_id: str, attachment_id: str) -> bytes:
    """Download attachment content as bytes."""
    attachment = self.service.users().messages().attachments().get(
        userId="me",
        messageId=email_id,
        id=attachment_id
    ).execute()

    data = attachment.get("data", "")
    return base64.urlsafe_b64decode(data)

def download_attachment(
    self,
    email_id: str,
    attachment_id: str,
    filename: str,
    output_dir: Path = None
) -> Path:
    """Download attachment to local file."""
    if output_dir is None:
        output_dir = Path("temp/attachments")
    output_dir.mkdir(parents=True, exist_ok=True)

    content = self.get_attachment(email_id, attachment_id)
    output_path = output_dir / filename
    output_path.write_bytes(content)

    return output_path
```

---

### Task 2: ReplyTracker 클래스

**파일**: `C:\claude\ebs\tools\morning-automation\trackers\reply_tracker.py` (신규)

**데이터 구조** (`data/reply_schedule.json`):
```json
{
  "vendors": {
    "feig": {
      "last_contact_date": "2026-02-01",
      "last_email_subject": "Re: RFID Module Inquiry",
      "contact_type": "sent",
      "expected_reply_days": 14,
      "status": "pending",
      "thread_id": "abc123"
    },
    "pokergfx": {
      "last_contact_date": "2026-01-23",
      "last_email_subject": "Re: API Integration",
      "contact_type": "received",
      "expected_reply_days": 7,
      "status": "replied",
      "thread_id": "def456"
    }
  },
  "vendor_reply_days": {
    "feig": 14,
    "st_micro": 10,
    "default": 7
  },
  "updated_at": "2026-02-04T09:00:00"
}
```

**구현**:
```python
class ReplyTracker:
    """Track vendor reply schedules for follow-up notifications."""

    DATA_FILE = Path("data/reply_schedule.json")
    DEFAULT_REPLY_DAYS = 7

    def __init__(self, data_dir: Path = None):
        self.data_file = data_dir / "reply_schedule.json" if data_dir else self.DATA_FILE
        self.data = self._load()

    def update_contact(self, vendor: str, email_date: datetime,
                       subject: str, thread_id: str, contact_type: str = "sent"):
        """Record new contact with vendor."""
        pass

    def check_reply(self, vendor: str, reply_date: datetime):
        """Mark vendor as having replied."""
        pass

    def get_overdue(self) -> list[dict]:
        """Get vendors past expected reply date."""
        pass

    def get_pending(self) -> list[dict]:
        """Get vendors awaiting reply."""
        pass

    def get_summary(self) -> dict:
        """Get summary for briefing."""
        pass
```

---

### Task 3: `/daily` 스킬 확장

**파일**: `C:\claude\ebs\.claude\skills\daily\SKILL.md`

**추가할 워크플로우 섹션**:

```markdown
## Phase 2: 첨부파일 분석 (CRITICAL - Claude 직접 수행)

**이 Phase는 Claude가 직접 실행합니다. Python 자동화가 아닙니다.**

### Step 2.1: 신규 첨부파일 메일 확인

```python
# 실행할 Python 코드
import json
from pathlib import Path

data = json.loads(Path("C:/claude/ebs/tools/morning-automation/data/gmail_emails.json").read_text())
for email in data.get("emails", []):
    if email.get("has_attachments"):
        print(f"Email: {email['subject']}")
        print(f"  From: {email['sender']}")
        print(f"  Attachments: {email.get('attachment_count', 'unknown')}")
```

### Step 2.2: 첨부파일 다운로드

중요한 첨부파일이 있는 메일에 대해:

```python
from lib.gmail import GmailClient
from pathlib import Path

client = GmailClient()
# email_id와 attachment_id는 Step 2.1에서 확인한 값 사용
output_path = client.download_attachment(
    email_id="<email_id>",
    attachment_id="<attachment_id>",
    filename="<filename>",
    output_dir=Path("C:/claude/ebs/tools/morning-automation/temp/attachments")
)
print(f"Downloaded: {output_path}")
```

### Step 2.3: Claude가 첨부파일 직접 읽기

다운로드된 PDF 파일을 Read 도구로 직접 읽습니다:

```
Read: C:\claude\ebs\tools\morning-automation\temp\attachments\<filename>.pdf
```

**대용량 PDF 처리 (10페이지 이상):**
```
Read: C:\claude\ebs\tools\morning-automation\temp\attachments\<filename>.pdf, pages: "1-10"
```

**첨부파일 우선순위 (분석 대상 선별):**
| 우선순위 | 파일 유형 | 설명 |
|:--------:|----------|------|
| HIGH | `*_datasheet.pdf`, `*_quotation.pdf` | 데이터시트, 견적서 |
| MEDIUM | `*.pdf` (일반) | 일반 PDF |
| LOW | `*.png`, `*.jpg` | 이미지 (메타데이터만) |
| SKIP | `*_brochure.pdf`, `newsletter_*` | 마케팅 자료 |

Claude는 PDF 내용을 직접 읽고:
- 문서 유형 파악 (데이터시트, 견적서, 매뉴얼 등)
- 핵심 정보 추출 (가격, 스펙, 납기 등)
- 필요한 액션 아이템 도출

### Step 2.4: 분석 결과 정리

| 메일 | 첨부파일 | 문서 유형 | 핵심 내용 | 액션 아이템 |
|------|----------|----------|----------|------------|
| Re: RFID Inquiry | ST25R3911B_datasheet.pdf | 데이터시트 | 13.56MHz, ISO14443 지원 | 스펙 비교표 업데이트 |

### Step 2.5: 임시 파일 정리

```powershell
Remove-Item -Recurse -Force C:\claude\ebs\tools\morning-automation\temp\attachments\*
```

## Phase 3: 회신 일정 확인

### Step 3.1: 회신 일정 데이터 읽기

```
Read: C:\claude\ebs\tools\morning-automation\data\reply_schedule.json
```

### Step 3.2: Overdue 업체 확인

예상 회신일이 지난 업체를 확인하고 알림 생성:

| 업체 | 마지막 연락 | 경과일 | 예상 회신일 | 상태 |
|------|------------|-------|------------|------|
| FEIG | 2026-01-20 | 15일 | 2026-02-03 | ⚠️ OVERDUE |
| ST Micro | 2026-02-01 | 3일 | 2026-02-11 | ⏳ Pending |

### Step 3.3: 회신 일정 업데이트

신규 메일 분석 결과를 바탕으로 reply_schedule.json 업데이트:
- 업체로부터 회신 받은 경우: status → "replied"
- 내가 메일 보낸 경우: last_contact_date 업데이트

### Step 3.4: ReplyTracker 통합 (CRITICAL)

**업체 메일 분석 후 ReplyTracker 호출 시점:**

```python
# /daily 스킬에서 Claude가 직접 실행할 Python 코드
import sys
sys.path.insert(0, "C:/claude/ebs/tools/morning-automation")

from trackers.reply_tracker import ReplyTracker
from datetime import datetime

tracker = ReplyTracker()

# 업체로부터 메일 받은 경우
tracker.update_contact(
    vendor="feig",
    email_date=datetime.fromisoformat("2026-02-04"),
    subject="Re: RFID Module Inquiry",
    thread_id="abc123",
    contact_type="received"  # 받은 메일
)

# 내가 메일 보낸 경우
tracker.update_contact(
    vendor="st_micro",
    email_date=datetime.fromisoformat("2026-02-04"),
    subject="Follow-up: NFC Reader Quotation",
    thread_id="def456",
    contact_type="sent"  # 보낸 메일
)

# 변경사항 저장
tracker.save()
print("Reply schedule updated")
```

**호출 시점:**
1. Phase 1 (데이터 수집) 완료 후
2. Claude가 `gmail_emails.json` 분석하면서
3. 업체 메일 발견 시 → `tracker.update_contact()` 호출
4. 분석 완료 후 → `tracker.save()` 호출
```

---

## GmailCollector 확장

**파일**: `C:\claude\ebs\tools\morning-automation\collectors\gmail_collector.py`

**수정 사항**:
1. `has_attachments` 필드 저장
2. `attachments` 배열 저장 (id, filename, mime_type, size)

```python
# 기존 email_info에 추가 (CRITICAL: email_id 필수)
email_info = {
    "id": email.id,  # ← 첨부파일 다운로드 시 필요!
    # ... 기존 필드 ...
    "has_attachments": email.has_attachments,
    "attachments": [
        {
            "attachment_id": att.id,  # ← 명시적으로 attachment_id 사용
            "filename": att.filename,
            "mime_type": att.mime_type,
            "size": att.size,
        }
        for att in email.attachments
    ] if email.has_attachments else [],
}
```

**중요**: 첨부파일 다운로드 시 `email_id`와 `attachment_id` 둘 다 필요합니다.

---

## Success Criteria

### Functional

- [ ] `download_attachment()` 메서드로 PDF 다운로드 성공
- [ ] Claude가 Read 도구로 PDF 직접 읽기 성공
- [ ] 회신 일정 JSON 저장/로드 성공
- [ ] `/daily` 실행 시 첨부파일 분석 워크플로우 수행

### User Experience

- [ ] `/daily` 실행 후 첨부파일 요약 브리핑에 포함
- [ ] Overdue 업체 알림 명확히 표시
- [ ] 분석 결과 기반 액션 아이템 제안

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| 대용량 PDF 읽기 실패 | MEDIUM | 10MB 제한, 페이지 단위 읽기 |
| 암호화된 PDF | LOW | 스킵 후 "encrypted" 표시 |
| Gmail API 제한 | LOW | 배치 다운로드 (5개/회) |

---

## Commit Strategy

| # | Commit | 파일 |
|:-:|--------|------|
| 1 | `feat(gmail): add attachment download methods` | `lib/gmail/client.py` |
| 2 | `feat(ebs): add ReplyTracker for vendor follow-up` | `trackers/reply_tracker.py` |
| 3 | `feat(ebs): store attachment metadata in GmailCollector` | `collectors/gmail_collector.py` |
| 4 | `feat(ebs): extend /daily skill with attachment analysis workflow` | `.claude/skills/daily/SKILL.md` |

---

## Change History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-04 | 1.0.0 | Initial plan (Python 자동화 방식) |
| 2026-02-04 | 2.0.0 | **스킬 기반으로 재설계** - Claude 직접 분석 |
| 2026-02-04 | 2.1.0 | **Critic 피드백 반영**: 실행 순서 추가, DoD 수정, Windows 명령어, PDF 크기 처리, ReplyTracker 통합점 명시 |

---

**Version**: 2.1.0 | **Updated**: 2026-02-04
