# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Status

> **Current Phase: Phase 0** (업체 선정, 준비)
>
> | 단계 | 상태 | 설명 |
> |------|:----:|------|
> | **Phase 0** | 진행 중 | 업체 선정, 준비 |
> | Phase 1 | 대기 | PokerGFX 복제 |
> | Phase 2 | 대기 | WSOPLIVE DB 연동 |
> | Phase 3 | 대기 | 자동화 프로토콜 |

## Project Overview

EBS (Event Broadcasting System)는 포커 방송 프로덕션 전체 워크플로우의 인프라스트럭처.

**핵심 목표**:
- **자산 내재화**: 자체 RFID 시스템 구축 (완제품 도입이 아닌 자체 개발)
- **운영 효율화**: 30명 -> 15~20명 (자막 연출 자동화)

**PokerGFX는 구매/도입 대상이 아니라 소프트웨어 벤치마크/복제 대상이다.**

## Repository Relationship (CRITICAL)

두 개의 별도 Git 레포가 존재하며, 역할이 명확히 구분된다.

| 레포 | 원격 | 역할 | 작업 범위 |
|------|------|------|----------|
| **`C:/claude/ebs/`** | `garimto81/ebs` | **기획 레포** — 독립적 PRD, 운영 도구, 업체 관리 | Phase 0 운영 + 독립 기획 문서 |
| **`C:/claude/ebs_reverse/`** | `garimto81/ebs_reverse` | **역설계 레포** — PokerGFX 분석, 복제 프로젝트 진행 | 바이너리 분석 + 프로토콜 스펙 + 구현 |

### 핵심 규칙

1. **`ebs`에서 `ebs_reverse` 파일을 직접 수정하지 않는다**
2. **`ebs`는 `ebs_reverse`의 분석 결과를 "참조"하여 독립 기획 문서를 작성한다**
3. **mockup/PRD 작업 시 대상 레포를 반드시 확인한다**

### 문서 흐름

```
ebs_reverse (역설계)          ebs (기획)
─────────────────────        ─────────────────────
바이너리 분석
프로토콜 스펙                  ← 참조하여
UI 분석/mockup                독립 PRD 작성
구현 코드                     운영 도구 (morning-automation)
                              업체 관리 (VENDOR-MANAGEMENT)
```

### 레포별 주요 경로

| 내용 | `ebs` | `ebs_reverse` |
|------|-------|---------------|
| PokerGFX 분석 | `docs/01_PokerGFX_Analysis/` (참조 문서) | `docs/01-plan/` (원본 분석) |
| Mockup HTML | 사용하지 않음 | `docs/01-plan/mockups/` |
| PRD | `docs/PRD-0003-EBS-RFID-System.md` (독립 기획) | `docs/01-plan/pokergfx-development-prd.md` (복제 PRD) |
| 운영 도구 | `tools/morning-automation/` | 없음 |
| 업체 관리 | `docs/05_Operations_ngd/VENDOR-MANAGEMENT.md` | 없음 |

## Architecture

```
RFID Card -> RFID Reader -> MCU -> USB Serial -> Server -> WebSocket -> Flutter (Rive)
```

| Layer | 기술 | 역할 |
|-------|------|------|
| Firmware | 미정 | RFID 태그 읽기, JSON Serial 출력 |
| Server | 미정 | Serial 수신, DB 조회, WebSocket 브로드캐스트 |
| Frontend | Flutter, Rive | 실시간 카드 UI, 방송 오버레이 |

**RFID 모듈**: 테스트용 MFRC522, 프로덕션 ST25R3911B (Phase 0 업체 선정 중)

**현재 구현 상태**: Server/Frontend/Firmware 코드는 아직 없음. DB 스키마와 운영 도구만 존재.

## Build & Run Commands

### Morning Automation (데일리 브리핑)

Phase 0의 핵심 운영 도구. Slack, Gmail, Slack Lists에서 업체 관련 데이터를 수집하여 일일 브리핑을 생성한다.

```powershell
# 의존성 설치
pip install -r C:\claude\ebs\tools\morning-automation\requirements.txt

# 기본 실행 (incremental, 전일 데이터)
python C:\claude\ebs\tools\morning-automation\main.py

# 전체 수집 (초기 실행 또는 전체 재수집)
python C:\claude\ebs\tools\morning-automation\main.py --full

# Slack 채널에 업체 현황 갱신
python C:\claude\ebs\tools\morning-automation\main.py --post

# 표준 워크플로우 (수집 + 채널 갱신)
python C:\claude\ebs\tools\morning-automation\main.py --post

# 전체 재수집 + 채널 갱신 (스키마 변경 시)
python C:\claude\ebs\tools\morning-automation\main.py --full --post

# 특정 날짜 리포트
python C:\claude\ebs\tools\morning-automation\main.py --date 2026-02-01

# 리포트 파일 생성 건너뛰기
python C:\claude\ebs\tools\morning-automation\main.py --no-report
```

**Slack API 제약**:
- `--notify` 사용 금지 (`chat:write:bot` scope 없음)
- `--post`만 사용 가능 (기존 채널 메시지 `chat.update`로 갱신)
- DM 발송 불가

### PDF 도구

```powershell
pip install -r C:\claude\ebs\tools\requirements.txt

python C:\claude\ebs\tools\split_pdf.py <input.pdf> 20              # 페이지 분할
python C:\claude\ebs\tools\extract_images.py <input.pdf> --output-dir <output/>  # 이미지 추출
python C:\claude\ebs\tools\pdf_chunker.py <input.pdf>               # 토큰 기반 청킹
```

### PokerGFX UI 분석 도구

```powershell
pip install Pillow

# 주석 오버레이 이미지 생성 (images/pokerGFX/ → docs/01_PokerGFX_Analysis/02_Annotated_ngd/)
python C:\claude\ebs\tools\generate_annotations.py
python C:\claude\ebs\tools\generate_annotations.py --calibrate       # 자동 캘리브레이션
python C:\claude\ebs\tools\generate_annotations.py --debug --target 02  # 디버그 모드 (단일 이미지)
```

### Google Drive 정리

```powershell
python C:\claude\ebs\tools\gdrive_organizer.py status              # 현재 상태 조회
python C:\claude\ebs\tools\gdrive_organizer.py create-folder NAME  # 폴더 생성
python C:\claude\ebs\tools\gdrive_organizer.py --dry-run ...       # 미리보기
```

### Database

```powershell
# SQLite 카드 DB 초기화 (54장: 52장 + 조커 2장, UID 미매핑 상태)
sqlite3 C:\claude\ebs\server\db\cards.db < C:\claude\ebs\server\db\init.sql
```

## Code Architecture

### Morning Automation (`tools/morning-automation/`)

유일한 실행 가능 코드베이스 (~2,400 LOC, Python).

```
main.py                 # CLI 진입점 (argparse: --full, --post, --notify, --date, --no-report)
config/settings.py      # Slack channel/list ID, Gmail label ID, 업체 키워드, 이메일 도메인 매핑
collectors/
  slack_collector.py    # #ggpnotice 채널 메시지 수집, 업체 언급 감지
  gmail_collector.py    # EBS 라벨 이메일 수집 (4경로: EBS 라벨 + 키워드 검색 + 도메인 검색 + Thread 추적)
  lists_collector.py    # Slack Lists 5컬럼 업체 데이터 동기화, sync_from_analysis로 상태 자동 갱신
reporters/
  markdown_reporter.py  # docs/05_Operations_ngd/01_DailyBriefings_ngd/ 에 Markdown 생성
  slack_poster.py       # Slack 채널 메시지 갱신 (chat.update, RFI 현황/회신 포함)
  slack_notifier.py     # DM 알림 (현재 scope 부족으로 비활성)
data/                   # JSON 중간 파일 (slack_messages.json, gmail_emails.json, slack_lists.json)
```

**데이터 파이프라인**:
```
Collectors (Slack/Gmail/Lists API)
    ↓ JSON 중간 파일 저장 (data/)
Sync (lists_collector.sync_from_analysis)
    ↓ 배송 실패 감지, 상태 자동 갱신
Reporters (Markdown 파일 + Slack 채널 메시지)
```

**Gmail Collector 4경로 수집 전략**:
1. `label:EBS` 라벨 검색
2. `in:sent` 키워드 검색 (RFID, poker, 카드 인식 등)
3. 업체 도메인 검색 (`VENDOR_EMAIL_DOMAINS` 기반)
4. Thread 기반 회신 감지 (발송 메일의 thread에서 새 메시지 탐색)

**Slack Poster 동작 방식**: 새 메시지 post가 아닌 기존 메시지 `chat.update`. `vendor_message_ts.txt`에 저장된 timestamp로 갱신 대상 식별. 메시지 미발견 시 새 메시지 생성으로 fallback.

### 외부 공유 라이브러리

Morning Automation은 EBS 외부의 공유 라이브러리에 의존한다:

| 라이브러리 | 경로 | 용도 |
|-----------|------|------|
| SlackClient | `C:\claude\lib\slack\client.py` | Slack API 래퍼 (Browser OAuth) |
| GmailClient | `C:\claude\lib\gmail\client.py` | Gmail API 래퍼 (Browser OAuth) |

`sys.path.insert(0, "C:/claude")`로 import path를 설정하여 `from lib.slack.client import SlackClient` 형태로 사용.

### 업체 키워드/도메인 설정 (`config/settings.py`)

업체 자동 감지를 위한 두 가지 매핑:
- `VENDOR_KEYWORDS`: 이메일 subject/sender에서 업체 감지 (예: `"sunfly": ["sun-fly", "sunfly", "선플라이"]`)
- `VENDOR_EMAIL_DOMAINS`: 수신자 도메인으로 발송 업체 감지 (예: `"sunfly": ["sun-fly.com"]`)

새 업체 추가 시 두 매핑 모두 업데이트 필요.

### Database Schema (`server/db/init.sql`)

`cards` 테이블: 54장 카드 (suit, rank, display, value). `uid` 컬럼은 초기 NULL이며, RFID 매핑 시 업데이트.

## Project Rules

### 외부 커뮤니케이션 규칙

외부 업체 이메일 작성 시 반드시 준수. 상세: `docs/05_Operations_ngd/COMMUNICATION-RULES_ngd.md`

| 규칙 | 내용 |
|------|------|
| 회사명 비공개 | "BRACELET STUDIO"를 외부 이메일에 절대 노출하지 않음 |
| 기술 스펙 비공개 | 주파수, 프로토콜, IC 칩명 언급 안 함 |
| 서명 | 이름만, 회사명 없음 |

### 업체 카테고리 체계

| 카테고리 | 정의 | 이메일 |
|---------|------|--------|
| **A** (통합 파트너) | RFID 카드 + 리더 통합 공급 가능 | 동일 RFI 발송 |
| **B** (부품 공급) | 카드 또는 리더 한쪽만 가능 | 개별 문의 |
| **C** (벤치마크) | 소프트웨어/참조 업체 | 이메일 불필요 |

- `VENDOR-MANAGEMENT.md`가 업체 정보의 1차 소스 (Source of Truth)
- 통일 RFI 템플릿: `docs/05_Operations_ngd/02_EmailDrafts_ngd/UNIFIED-RFI-TEMPLATE.md`
- Slack List는 VENDOR-MANAGEMENT.md에서 동기화

### 용어 규칙

| 금지 | 사용 | 이유 |
|------|------|------|
| chips (카지노 맥락) | 베팅 토큰 | 반도체 칩과 혼동 방지 |
| chips (반도체 맥락) | IC, 반도체 | 위와 구분 |

### 문서 작성 규칙

변경 이력은 반드시 문서 최하단에 배치:

```markdown
# 문서 제목
## 핵심 내용
## 상세 내용
---
## 변경 이력        <- 항상 마지막 섹션
---
**Version**: X.X.X | **Updated**: YYYY-MM-DD
```

## Directory Naming Convention

| 규칙 | 설명 | 예시 |
|------|------|------|
| **`_ngd` suffix** | Google Drive 비공유 파일/폴더 | `03_Phase02_ngd/`, `COMMUNICATION-RULES_ngd.md` |
| **숫자 prefix** | `NN_PascalCase` 형식 (docs/ 내부) | `01_PokerGFX_Analysis/`, `05_Operations_ngd/` |
| **Drive 동기화 대상** | `01_PokerGFX_Analysis`, `02_Phase01` + root docs만 | `MAPPING_ngd.json` 참조 |

> Drive 폴더명과 로컬 폴더명이 다를 수 있음: `01_PokerGFX_Analysis` (로컬) = `01_Phase00` (Drive)

## Key Documents

| 문서 | 경로 | 용도 |
|------|------|------|
| Master PRD | `docs/PRD-0003-EBS-RFID-System.md` | 비전/전략/로드맵 |
| 업체 관리 | `docs/05_Operations_ngd/VENDOR-MANAGEMENT.md` | 업체 정보 1차 소스 |
| 커뮤니케이션 규칙 | `docs/05_Operations_ngd/COMMUNICATION-RULES_ngd.md` | 외부 이메일 규칙 |
| 업체 선정 체크리스트 | `docs/05_Operations_ngd/VENDOR-SELECTION-CHECKLIST.md` | Phase 0 선정 기준 |
| 기능 체크리스트 | `docs/01_PokerGFX_Analysis/PokerGFX-Feature-Checklist.md` | 149개 복제 대상 |
| PokerGFX 분석 | `docs/01_PokerGFX_Analysis/PokerGFX-UI-Analysis.md` | UI 분석 |
| PokerGFX 참조 자료 | `docs/01_PokerGFX_Analysis/03_Reference_ngd/` | 매뉴얼/보안 PDF |
| 이메일 드래프트 | `docs/05_Operations_ngd/02_EmailDrafts_ngd/` | 업체 컨택 이메일 |
| 데일리 브리핑 | `docs/05_Operations_ngd/01_DailyBriefings_ngd/` | 일일 현황 보고 |
| 문서 네비게이션 | `docs/README.md` | 전체 문서 색인 |

## Google Docs 동기화

| 레포 | 로컬 파일 | Google Docs ID | URL |
|------|-----------|---------------|-----|
| **ebs_reverse** | `C:/claude/ebs_reverse/docs/01-plan/pokergfx-development-prd.md` | `1xz3T1tp0jGxp6Dmwicvqf1DD01SW6RYmmGrNzUZ92Y4` | [PRD: PokerGFX Clone](https://docs.google.com/document/d/1xz3T1tp0jGxp6Dmwicvqf1DD01SW6RYmmGrNzUZ92Y4/edit) |

> **주의**: 위 Google Docs는 `ebs_reverse` 레포의 파일과 동기화된다. `ebs` 레포의 문서가 아님.

## System Files

| 위치 | 설명 |
|------|------|
| `.omc/bkit/` | bkit PDCA 상태, 스냅샷 (삭제 금지) |
| `.omc/plans/` | 작업 계획 문서 |
| `.claude/` | Claude 커맨드, 스킬, 에이전트 설정 |
