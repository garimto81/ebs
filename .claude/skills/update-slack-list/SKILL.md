---
name: update-slack-list
description: >
  Slack Lists 업체 관리 시스템 업데이트. 업체 추가/수정/삭제, 상태 변경, 채널 동기화.
  "slack list", "slacklist", "업체 리스트", "vendor list" 요청 시 사용.
version: 1.0.0
triggers:
  keywords:
    - "update slack list"
    - "update slacklist"
    - "slack list"
    - "slacklist"
    - "slack-list"
    - "업체 리스트"
    - "vendor list"
    - "업체 목록"
  patterns:
    - "--update\\s+(slack\\s*list|slacklist)"
    - "slack\\s*list.*(update|sync|add|remove)"
    - "업체.*(추가|수정|삭제|동기화)"
  file_patterns:
    - "**/slack_lists.json"
    - "**/lists_collector.py"
model_preference: sonnet
auto_trigger: true
---

# Update Slack List

EBS 프로젝트의 Slack Lists 업체 관리 시스템을 업데이트합니다.

## 호출 방법

다음 모든 형식이 동일하게 작동합니다:

```bash
/auto --update slacklist
/auto --update slack list
/auto --update slack-list
/update-slack-list
```

## 기능

| 명령 | 설명 |
|------|------|
| `sync` | Slack에서 최신 데이터 동기화 |
| `add <name> <url> <info>` | 새 업체 추가 |
| `update <id> <field> <value>` | 업체 정보 수정 |
| `status <id> <status>` | 상태 변경 (후보→견적요청→계약 등) |
| `post` | 채널에 요약 메시지 업데이트 |
| `report` | 현재 상태 리포트 출력 |

## 강제 실행 규칙 (MANDATORY)

**이 스킬이 활성화되면 반드시 다음을 실행합니다.**

### Step 1: 현재 상태 확인

```powershell
cd C:\claude\ebs\tools\morning-automation
python -c "from collectors import ListsCollector; c = ListsCollector(); print(c.get_summary())"
```

### Step 2: 요청별 실행

| 사용자 요청 | 실행할 명령 |
|-------------|-------------|
| "동기화", "sync", "최신화" | `python main.py --full --no-report` |
| "채널 업데이트", "post" | `python main.py --post` |
| "리포트", "상태 확인" | `python main.py` (incremental) |
| "업체 추가" | `ListsCollector().add_vendor(...)` |
| "상태 변경" | `ListsCollector().update_item_status(...)` |

### Step 3: 결과 확인 및 보고

```powershell
# 동기화 후 결과
python -c "
from collectors import ListsCollector
c = ListsCollector()
s = c.get_summary()
print(f'총 {s[\"total\"]}개 업체')
print(f'  RFID Readers: {s[\"rfid_readers\"]}')
print(f'  Casino Solutions: {s[\"casino_solutions\"]}')
print(f'  DIY/Development: {s[\"diy_development\"]}')
print(f'  Benchmarks: {s[\"benchmarks\"]}')
"
```

## 업체 카테고리

| 카테고리 | 설명 | 업체 예시 |
|----------|------|----------|
| `rfid_readers` | RFID 리더 모듈 | FEIG, GAO, Identiv, PONGEE |
| `casino_solutions` | 카지노 솔루션 | Matsui, Abbiati, Sun-Fly, S.I.T. Korea |
| `diy_development` | DIY 개발용 | ST Micro, Waveshare, Adafruit, SparkFun |
| `benchmarks` | 벤치마크 (경쟁사) | PokerGFX, RF Poker, Faded Spade, Angel |

## 상태 값

| 상태 | 설명 |
|------|------|
| `후보` | 초기 상태 |
| `견적요청` | RFQ 전송됨 |
| `견적수신` | 견적서 받음 |
| `협상중` | 가격/조건 협상 |
| `계약` | 계약 완료 |
| `보류` | 일시 보류 |
| `제외` | 후보에서 제외 |

## 파일 위치

| 파일 | 용도 |
|------|------|
| `C:\claude\ebs\tools\morning-automation\main.py` | 메인 스크립트 |
| `C:\claude\ebs\tools\morning-automation\collectors\lists_collector.py` | Lists API 클라이언트 |
| `C:\claude\ebs\tools\morning-automation\data\slack_lists.json` | 캐시된 데이터 |
| `C:\claude\json\slack_credentials.json` | 인증 정보 (user_token 필요) |

## 인증 요구사항

Slack Lists API는 **User Token** (`xoxp-...`)이 필요합니다.

`C:\claude\json\slack_credentials.json`에 다음이 있어야 합니다:

```json
{
  "user_token": "xoxp-..."
}
```

## 예시

### 전체 동기화
```
/auto --update slacklist sync
```

### 업체 추가
```
/auto --update slacklist add "NewVendor" "https://example.com" "RFID 모듈 제조사"
```

### 상태 변경
```
/auto --update slacklist status Rec0ACEPH1DSP 견적요청
```

### 채널 업데이트
```
/auto --update slacklist post
```

## 자동 트리거

다음 키워드 감지 시 자동 활성화:
- "update slack list"
- "슬랙 리스트 업데이트"
- "업체 목록 동기화"
- "vendor list sync"
