# Work Plan: EBS Daily Briefing Workflow

**Plan ID**: `daily-briefing-workflow`
**Version**: 1.0.0
**Created**: 2026-02-04
**Status**: READY FOR EXECUTION

---

## Context

### Original Request

사용자가 매일 1회 `/daily` 또는 `/briefing` 명령을 실행하면:
1. Slack/Gmail/Lists 데이터 수집 및 분석
2. 미완료 작업/무응답 메일 감지
3. Slack List 메시지 자동 업데이트
4. 종합 브리핑 (DM + 마크다운 리포트)

### Pre-Gathered Codebase Context

**기존 인프라 (완전히 구현됨)**:

| 모듈 | 파일 | 기능 |
|------|------|------|
| `SlackCollector` | `collectors/slack_collector.py` | incremental 수집, 멘션 분석, 업체 감지 |
| `GmailCollector` | `collectors/gmail_collector.py` | incremental 수집, 72시간+ 무응답 감지 |
| `ListsCollector` | `collectors/lists_collector.py` | Slack Lists 업체 데이터 동기화 |
| `SlackNotifier` | `reporters/slack_notifier.py` | DM 브리핑 전송 (GFX D-day 포함) |
| `SlackPoster` | `reporters/slack_poster.py` | 채널 메시지 **chat.update** (NOT post) |
| `MarkdownReporter` | `reporters/markdown_reporter.py` | 일일 리포트 생성 |
| `main.py` | 메인 오케스트레이터 | `--notify`, `--post` 플래그 지원 |

**현재 main.py CLI**:
```bash
python main.py              # incremental 수집
python main.py --full       # 전체 수집
python main.py --notify     # + Slack DM 브리핑
python main.py --post       # + 채널 메시지 업데이트
```

**출력 경로**:
- 리포트: `C:\claude\ebs\docs\operations\daily-briefings\{YYYY-MM-DD}.md`
- 데이터: `C:\claude\ebs\tools\morning-automation\data\`

### Research Findings

1. **기존 코드 100% 재활용 가능**: `main.py --notify --post`가 이미 모든 기능 수행
2. **스킬만 추가하면 됨**: Python 코드 수정 불필요
3. **`/auto --daily` 옵션**: `/auto` 스킬의 옵션으로 통합 가능

---

## Work Objectives

### Core Objective

`/daily` 또는 `/briefing` 스킬을 생성하여 기존 morning-automation을 Claude Code에서 쉽게 호출할 수 있도록 한다.

### Deliverables

| # | Deliverable | 경로 | 설명 |
|---|-------------|------|------|
| 1 | **스킬 파일** | `.claude/skills/daily/SKILL.md` | `/daily` 명령 정의 |
| 2 | **`/auto` 옵션 통합** | `.claude/skills/auto/SKILL.md` 수정 | `--daily` 옵션 추가 |

### Definition of Done

- [ ] `/daily` 단독 실행 시 전체 브리핑 워크플로우 수행
- [ ] `/daily --collect-only` 옵션으로 수집만 가능
- [ ] `/auto --daily` 옵션으로 동일 기능 호출 가능
- [ ] 스킬 문서에 전체 워크플로우 명시

---

## Must Have / Must NOT Have

### Must Have (Guardrails)

| # | Requirement |
|---|-------------|
| 1 | 기존 `morning-automation` Python 코드 **수정 없이** 재활용 |
| 2 | Slack DM 브리핑 전송 |
| 3 | 채널 메시지 **업데이트** (새 메시지 생성 아님) |
| 4 | 마크다운 리포트 파일 생성 |
| 5 | GFX 라이선스 D-day 알림 포함 |

### Must NOT Have (Out of Scope)

| # | Exclusion | Reason |
|---|-----------|--------|
| 1 | 새 Python 코드 작성 | 기존 인프라 완전 |
| 2 | 스케줄러/cron 설정 | 수동 호출만 지원 |
| 3 | 새 Slack Bot 권한 요청 | 기존 Bot/User Token 사용 |

---

## Task Flow and Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    /daily 워크플로우                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: 데이터 수집 (Python main.py)                        │
│  ├─ SlackCollector.collect_incremental()                    │
│  ├─ GmailCollector.collect_incremental()                    │
│  └─ ListsCollector.collect()                                │
│         │                                                   │
│         ▼                                                   │
│  Step 2: 리포트 생성                                         │
│  └─ MarkdownReporter.generate()                             │
│     → docs/operations/daily-briefings/{date}.md             │
│         │                                                   │
│         ▼                                                   │
│  Step 3: 채널 업데이트 (--post)                              │
│  └─ SlackPoster.update_vendor_summary()                     │
│     → chat.update API 호출                                  │
│         │                                                   │
│         ▼                                                   │
│  Step 4: DM 브리핑 (--notify)                               │
│  └─ SlackNotifier.send_briefing()                           │
│     → 긴급 알림 + 요약 통계                                  │
│         │                                                   │
│         ▼                                                   │
│  Step 5: 결과 출력                                           │
│  └─ 리포트 경로 + 요약 통계 표시                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**의존성**:
- Step 2-5는 Step 1 완료 후 순차 실행
- `--collect-only` 옵션 시 Step 1만 실행

---

## Detailed TODOs

### TODO 1: `/daily` 스킬 파일 생성

**File**: `C:\claude\ebs\.claude\skills\daily\SKILL.md`

**Acceptance Criteria**:
- [ ] YAML frontmatter에 triggers, description 정의
- [ ] `auto_trigger: true`로 키워드 자동 감지
- [ ] 전체 실행 워크플로우 문서화
- [ ] 옵션별 분기 처리 정의

**Content Structure**:
```yaml
---
name: daily
description: EBS 데일리 브리핑 - Slack/Gmail 분석 및 종합 보고
version: 1.0.0
triggers:
  keywords:
    - "/daily"
    - "/briefing"
    - "daily briefing"
    - "morning briefing"
model_preference: sonnet
auto_trigger: true
---
```

**Workflow Sections**:
1. 옵션 파싱 (`--collect-only`, `--no-post`, `--no-notify`)
2. Python 실행 명령어 구성
3. 출력 결과 파싱 및 표시
4. 에러 처리

---

### TODO 2: `/auto --daily` 옵션 통합

**File**: `C:\claude\ebs\.claude\skills\auto\SKILL.md` (수정)

**Acceptance Criteria**:
- [ ] Phase 1 옵션 테이블에 `--daily` 추가
- [ ] `Skill(skill="daily")` 호출 지시 추가

**Changes**:
```markdown
| 옵션 | 실행할 스킬 | 설명 |
|------|-------------|------|
| `--daily` | `Skill(skill="daily")` | 데일리 브리핑 실행 |
| `--briefing` | `Skill(skill="daily")` | (동일) |
```

---

## Implementation Details

### `/daily` SKILL.md 전체 내용

```markdown
---
name: daily
description: EBS 데일리 브리핑 - Slack/Gmail 분석 및 종합 보고
version: 1.0.0
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
| `/daily` | `--notify --post` |
| `/daily --collect-only` | (플래그 없음) |
| `/daily --no-post` | `--notify` |
| `/daily --no-notify` | `--post` |
| `/daily --full` | `--full --notify --post` |

### Step 2: Python 실행

```bash
cd C:\claude\ebs\tools\morning-automation && python main.py <플래그>
```

**예시**:
```bash
# 기본 실행
cd C:\claude\ebs\tools\morning-automation && python main.py --notify --post

# 수집만
cd C:\claude\ebs\tools\morning-automation && python main.py

# 전체 재수집
cd C:\claude\ebs\tools\morning-automation && python main.py --full --notify --post
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
| 리포트 | `docs/operations/daily-briefings/2026-02-04.md` |
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
| `docs/operations/daily-briefings/` | 일일 리포트 저장 |

## /auto 통합

`/auto --daily` 또는 `/auto --briefing`으로도 호출 가능합니다.
```

---

## Commit Strategy

**단일 커밋**:
```
feat(ebs): add /daily briefing skill

- Create .claude/skills/daily/SKILL.md
- Integrate with existing morning-automation infrastructure
- Add --daily option to /auto skill
```

---

## Success Criteria

| # | Criterion | Verification Method |
|---|-----------|---------------------|
| 1 | `/daily` 단독 실행 시 전체 워크플로우 수행 | 수동 테스트 |
| 2 | 리포트 파일 생성 확인 | `docs/operations/daily-briefings/` 확인 |
| 3 | Slack DM 수신 확인 | Slack 앱에서 확인 |
| 4 | 채널 메시지 업데이트 확인 | #ggpnotice 메시지 시간 확인 |
| 5 | `/auto --daily` 동작 확인 | 수동 테스트 |

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gmail 인증 만료 | Medium | 에러 메시지에 재인증 안내 포함 |
| Slack API 제한 | Low | incremental 수집으로 최소화 |
| 기존 코드 버그 | Low | 이미 검증된 인프라 활용 |

---

## Estimated Effort

| Task | Effort |
|------|--------|
| SKILL.md 생성 | 10분 |
| /auto 수정 | 5분 |
| 테스트 | 10분 |
| **Total** | **~25분** |

---

## Notes for Executor

1. **Python 코드 수정 불필요**: 기존 `main.py`가 완전히 동작함
2. **스킬 파일만 생성**: `.claude/skills/daily/SKILL.md`
3. **`/auto` 옵션 추가**: 기존 옵션 테이블에 `--daily` 행 추가
4. **테스트 방법**: `/daily` 실행 후 DM 수신 확인

---

**Version**: 1.0.0 | **Updated**: 2026-02-04
