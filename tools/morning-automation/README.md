# EBS Morning Automation

매일 아침 EBS 프로젝트 상태를 자동으로 수집하고 브리핑 리포트를 생성합니다.

## 기능

| 기능 | 설명 |
|------|------|
| **Slack 수집** | #ggpnotice 채널 메시지 수집 및 분석 |
| **Gmail 수집** | EBS 라벨 이메일 수집 및 Follow-up 감지 |
| **Lists 수집** | Slack Lists 업체 관리 현황 |
| **리포트 생성** | Markdown 아침 브리핑 |
| **Slack 알림** | DM으로 요약 전송 |
| **채널 포스팅** | 브리핑/업체 요약 게시 |

## 사용법

### 기본 실행 (증분 수집)

```powershell
cd C:\claude\ebs\tools\morning-automation
python main.py
```

### 전체 수집 (최초 1회)

```powershell
python main.py --full
```

### Slack DM 알림 포함

```powershell
python main.py --notify
```

### 채널 메시지 업데이트

```powershell
python main.py --post
```

**중요**: 새 메시지를 추가하지 않고 기존 업체 관리 메시지를 **수정(update)**합니다.
- `chat.update` API 사용
- 기존 메시지 timestamp: `data/vendor_message_ts.txt`에 저장
- 메시지가 삭제된 경우에만 새로 생성

### 전체 옵션 조합

```powershell
python main.py --full --notify --post
```

## 출력

### Markdown 리포트

`C:\claude\ebs\docs\05_Operations_ngd\01_DailyBriefings_ngd\YYYY-MM-DD.md`

### JSON 데이터

```
data/
├── slack_messages.json    # Slack 메시지
├── slack_last_ts.txt      # 마지막 수집 타임스탬프
├── gmail_emails.json      # Gmail 이메일
├── gmail_last_date.txt    # 마지막 수집 날짜
├── slack_lists.json       # Slack Lists 업체
└── vendor_message_ts.txt  # 채널 업체 메시지 timestamp (update용)
```

## 자동화 설정

### Windows Task Scheduler

관리자 PowerShell에서 실행:

```powershell
.\setup_scheduler.ps1
```

수동 실행:
```powershell
schtasks /run /tn "EBS Morning Automation"
```

상태 확인:
```powershell
schtasks /query /tn "EBS Morning Automation"
```

## 의존성

```powershell
pip install -r requirements.txt
```

- `slack-sdk`: Slack API
- `google-api-python-client`: Gmail API
- `google-auth-oauthlib`: OAuth 인증

## 설정

`config/settings.py`:

| 설정 | 값 |
|------|-----|
| `SLACK_CHANNEL_ID` | C09N8J3UJN9 (#ggpnotice) |
| `SLACK_LIST_ID` | F0ABWAE20K1 (EBS 업체 관리) |
| `GMAIL_EBS_LABEL_ID` | Label_4886549615727008050 |
| `FOLLOWUP_THRESHOLD_HOURS` | 72 (무응답 알림 기준) |
| `GFX_LICENSE_EXPIRY` | 2026-03-17 |

## 관련 문서

- [PRD-Morning-Automation.md](../../docs/0-pre/PRD-Morning-Automation.md)
- [SLACK-LISTS-KANBAN.md](../../docs/05_Operations_ngd/SLACK-LISTS-KANBAN.md)
