---
name: daily
description: EBS 데일리 브리핑 - Slack/Gmail 분석 및 종합 보고
version: 2.1.0
triggers:
  keywords:
    - "/daily"
    - "/briefing"
    - "daily briefing"
    - "morning briefing"
    - "아침 브리핑"
model_preference: sonnet
auto_trigger: true
---

# /daily - EBS 데일리 브리핑

> **핵심**: 하루 1회 실행으로 Slack/Gmail/업체 현황을 종합 분석하고 브리핑 제공

## 사용법

```bash
/daily                    # 전체 워크플로우 (수집 + 리포트 + 채널업데이트 + DM)
/daily --collect-only     # 데이터 수집만
/daily --no-post          # 채널 메시지 업데이트 생략
/daily --no-notify        # DM 브리핑 생략
/daily --full             # 전체 재수집 (incremental 대신)
```

## 실행 워크플로우 (CRITICAL)

**이 스킬이 활성화되면 반드시 아래 절차를 실행하세요!**

### Step 1: 옵션 파싱

| 입력 | 플래그 조합 |
|------|------------|
| `/daily` | `--post` |
| `/daily --collect-only` | (플래그 없음) |
| `/daily --no-post` | (플래그 없음) |
| `/daily --full` | `--full --post` |

**⚠️ CRITICAL**: `--notify` 플래그 사용 금지 (`chat:write:bot` scope 없음)

### Step 2: Python 실행

```bash
cd C:\claude\ebs\tools\morning-automation && python main.py <플래그>
```

**예시**:
```bash
# 기본 실행 (채널 메시지 갱신만, DM 없음)
cd C:\claude\ebs\tools\morning-automation && python main.py --post

# 수집만
cd C:\claude\ebs\tools\morning-automation && python main.py

# 전체 재수집
cd C:\claude\ebs\tools\morning-automation && python main.py --full --post
```

**채널 갱신 실패 시**: 오류 출력 후 Slack List만 업데이트
```bash
/auto --update slacklist sync
```

### Step 3: 출력 분석

Python 실행 결과에서 다음 정보 추출:

| 항목 | 위치 |
|------|------|
| 리포트 경로 | `Report: C:\claude\ebs\docs\...` |
| Slack 메시지 수 | `Total messages: N` |
| Gmail 이메일 수 | `Total emails: N` |
| 업체 수 | `Total items: N` |
| 미완료 작업 | `Pending tasks: N` |
| Follow-up 필요 | `Follow-up needed: N` |

### Step 4: 결과 표시

**정상 완료 시**:
```
## EBS 데일리 브리핑 완료

| 항목 | 값 |
|------|-----|
| 리포트 | `docs/5-operations/daily-briefings/2026-02-04.md` |
| Slack 메시지 | N개 수집 |
| Gmail 이메일 | N개 수집 |
| 등록 업체 | N개 |
| 미완료 작업 | N건 |
| Follow-up 필요 | N건 |

**알림 전송**: Slack DM 완료
**채널 업데이트**: #ggpnotice 메시지 갱신
```

**에러 발생 시**:
- Gmail 인증 실패: `python -m lib.gmail login` 안내
- Slack 인증 실패: `slack_credentials.json` 확인 안내

## 브리핑 내용

### 긴급 알림 (자동 감지)

| 조건 | 알림 |
|------|------|
| GFX 라이선스 D-60 이하 | `GFX 라이선스 D-{N}` |
| 72시간+ 무응답 메일 | `Follow-up 필요 N건` |
| 미완료 멘션 (reaction 없음) | `미완료 작업 N건` |

### 업체 현황

Slack List에서 수집한 업체를 카테고리별로 정리:
- RFID 리더/모듈 업체
- 카지노 통합 솔루션
- DIY/개발 업체
- 완제품 벤치마크

### 오늘 할 일 제안

Gmail/Slack 분석 결과를 바탕으로 자동 생성:
1. Follow-up 메일 발송
2. Slack 요청 처리
3. 업체 컨택 진행

## 관련 파일

| 파일 | 용도 |
|------|------|
| `tools/morning-automation/main.py` | 메인 오케스트레이터 |
| `tools/morning-automation/config/settings.py` | 설정 (채널ID, 임계값) |
| `docs/5-operations/daily-briefings/` | 일일 리포트 저장 |

---

## Phase 2: Gmail 첨부파일 분석 (Claude 직접 수행)

**이 Phase는 Claude가 직접 실행합니다. Python 자동화 이후 추가 분석입니다.**

### Step 2.1: Gmail 데이터 읽기

```
Read: C:\claude\ebs\tools\morning-automation\data\gmail_emails.json
```

Claude가 확인할 필드:
- `emails`: 이메일 목록
- 각 이메일의 `attachments` 배열

### Step 2.2: 첨부파일 다운로드 및 분석

**PDF 첨부파일이 있는 경우:**

```
# 1. 첨부파일 목록 확인
attachments = email["attachments"]

# 2. PDF 파일 경로 (다운로드 후)
# 임시 경로: C:\Users\AidenKim\AppData\Local\Temp\claude\...\scratchpad\
# 형식: {message_id}_{attachment_name}.pdf

# 3. Read 도구로 PDF 읽기 (20페이지 초과 시 pages 파라미터 사용)
Read: {pdf_path}
# 또는
Read: {pdf_path}, pages="1-20"
```

### Step 2.3: 첨부파일 요약 생성

| 항목 | 내용 |
|------|------|
| 파일명 | 원본 첨부파일명 |
| 타입 | 견적서/데이터시트/계약서 등 |
| 핵심 내용 | 3줄 이내 요약 |
| 필요 액션 | 검토/회신/보관 등 |

### Step 2.4: 회신 일정 확인

`reply_tracker.json` 파일 확인:
```
Read: C:\claude\ebs\tools\morning-automation\data\reply_tracker.json
```

**Overdue 알림 기준:**
- 기본: 72시간 (3일)
- 업체 이메일 + 미회신 = Follow-up 필요

**출력 형식:**
```markdown
## 📧 Follow-up 필요 메일

| 발신자 | 제목 | 경과 | 액션 |
|--------|------|------|------|
| vendor@feig.de | RE: Quote Request | D+5 | 회신 필요 |
```

---

## Phase 3: Slack 메시지 분석 (Claude 직접 수행)

**이 Phase는 Claude가 직접 실행합니다. Python 자동화가 아닙니다.**

### Step 3.1: Slack 데이터 읽기

```
Read: C:\claude\ebs\tools\morning-automation\data\slack_messages.json
```

Claude가 확인할 필드:
- `mentions_to_me`: 내게 온 멘션 목록
- `action_items`: 액션 아이템 목록
- `vendor_mentions`: 업체별 언급

### Step 3.2: 미완료 멘션 분석

`mentions_to_me` 배열에서 `completed: false`인 항목 확인:
- 메시지 내용 파악
- 긴급도 판단 (HIGH/MEDIUM/LOW)
- 필요한 액션 도출

**긴급도 기준:**

| 긴급도 | 기준 |
|:------:|------|
| 🔴 HIGH | "오늘까지", "urgent", "ASAP", 명시적 기한 |
| 🟡 MEDIUM | "확인 부탁", "검토 필요", 질문 형태 |
| 🟢 LOW | "참고로", "FYI", 정보 공유 |

**판단 로직:**
```
1. HIGH 키워드 있음? → 🔴 HIGH
2. 날짜/기한 언급 있음? → 🔴 HIGH
3. 질문/요청 형태? → 🟡 MEDIUM
4. 나머지 → 🟢 LOW
```

### Step 3.3: 업체별 메시지 요약

`vendor_mentions`에서 각 업체별 최근 활동 요약:
- 최근 메시지 내용
- 필요한 후속 조치

### Step 3.4: 분석 결과 출력

**User ID는 Slack deep link로 출력** (이름 대신):
```
[요청자](slack://user?team=T05SZ8VE39U&id={user_id})
```

**출력 형식:**
```markdown
## Slack 분석

### 🔴 긴급 (N건)
| 메시지 | 요청자 | 날짜 | 필요 액션 |
|--------|--------|------|----------|
| "내용" | [요청자](slack://...) | 02-04 | 액션 |

### 🟡 확인 필요 (N건)
| 메시지 | 요청자 | 날짜 | 필요 액션 |
|--------|--------|------|----------|

### 🟢 참고 (N건)
- 업체명: 메시지 요약

### 업체별 요약
| 업체 | 최근 내용 | 상태 |
|------|----------|------|
```

---

## /auto 통합

`/auto --daily` 또는 `/auto --briefing`으로도 호출 가능합니다.

---

## 설계 문서

상세 설계는 아래 문서 참조:

| 문서 | 경로 | 내용 |
|------|------|------|
| Master Design | `.omc/plans/daily-intelligence-system.md` | 시스템 비전/목표 |
| Gmail 분석 | `.omc/plans/gmail-attachment-analysis.md` | 첨부파일 분석 상세 |
| Slack 분석 | `.omc/plans/slack-message-analysis.md` | 메시지 분석 상세 |
