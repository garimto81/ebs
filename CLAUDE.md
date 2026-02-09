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

## Architecture

```
RFID Card -> ST25R3911B -> ESP32 -> USB Serial -> FastAPI -> WebSocket -> React
```

| Layer | 기술 | 역할 |
|-------|------|------|
| Firmware | Arduino/C++, ESP32 | RFID 태그 읽기, JSON Serial 출력 |
| Server | Python, FastAPI | Serial 수신, DB 조회, WebSocket 브로드캐스트 |
| Frontend | React, TypeScript | 실시간 카드 UI, OBS 오버레이 |

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

# 특정 날짜 리포트
python C:\claude\ebs\tools\morning-automation\main.py --date 2026-02-01

# 리포트 파일 생성 건너뛰기
python C:\claude\ebs\tools\morning-automation\main.py --no-report
```

**제약**: `--notify` 사용 금지 (`chat:write:bot` scope 없음). `--post`만 사용 가능 (채널 메시지 갱신). DM 발송 불가.

### PDF 도구

```powershell
pip install -r C:\claude\ebs\tools\requirements.txt

python C:\claude\ebs\tools\split_pdf.py <input.pdf> 20              # 페이지 분할
python C:\claude\ebs\tools\extract_images.py <input.pdf> --output-dir <output/>  # 이미지 추출
python C:\claude\ebs\tools\pdf_chunker.py <input.pdf>               # 토큰 기반 청킹
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
main.py                 # CLI 진입점 (argparse)
config/settings.py      # Slack channel/list ID, Gmail label ID, 분석 설정
collectors/
  slack_collector.py    # #ggpnotice 채널 메시지 수집, 업체 언급 감지
  gmail_collector.py    # EBS 라벨 이메일 수집, 대기/회신 상태 분류
  lists_collector.py    # Slack Lists 5컬럼 업체 관리 데이터 동기화
reporters/
  markdown_reporter.py  # docs/5-operations/daily-briefings/ 에 Markdown 생성
  slack_poster.py       # Slack 채널 메시지 갱신 (기존 메시지 update)
  slack_notifier.py     # DM 알림 (현재 scope 부족으로 비활성)
```

**데이터 흐름**: Collectors가 Slack/Gmail API로 원시 데이터 수집 -> Reporters가 Markdown 파일 생성 및 Slack 채널 갱신

**외부 의존성**: `C:\claude\lib\slack\client.py`, `C:\claude\lib\gmail\client.py` (공유 라이브러리)

### Database Schema (`server/db/init.sql`)

`cards` 테이블: 54장 카드 (suit, rank, display, value). `uid` 컬럼은 초기 NULL이며, RFID 매핑 시 업데이트.

## Serial/WebSocket Protocol

```jsonc
// ESP32 -> Server (계획)
{"type": "card_read", "uid": "04:A2:B3:C4", "reader_id": 0, "timestamp": 123456}

// Server -> Client (계획)
{"type": "card_detected", "uid": "...", "card": {"suit": "spades", "rank": "A", "display": "A♠"}}
{"type": "reader_status", "connected": true, "port": "COM3"}
```

## Hardware Wiring (ESP32 -> MFRC522)

| ESP32 | MFRC522 | Function |
|-------|---------|----------|
| 3.3V  | VCC     | Power (3.3V 필수) |
| GND   | GND     | Ground |
| GPIO5 | SDA     | SPI SS |
| GPIO18| SCK     | SPI Clock |
| GPIO23| MOSI    | SPI MOSI |
| GPIO19| MISO    | SPI MISO |
| GPIO4 | RST     | Reset |

## Project Rules

### 외부 커뮤니케이션 규칙

외부 업체 이메일 작성 시 반드시 준수. 상세: `docs/5-operations/COMMUNICATION-RULES.md`

| 규칙 | 내용 |
|------|------|
| 회사명 비공개 | "BRACELET STUDIO"를 외부 이메일에 절대 노출하지 않음 |
| 기술 스펙 비공개 | 주파수, 프로토콜, IC 칩명 언급 안 함 |
| 서명 | 이름만, 회사명 없음 |

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

## Key Documents

| 문서 | 경로 | 용도 |
|------|------|------|
| Master PRD | `docs/PRD-0003-EBS-RFID-System.md` | 비전/전략/로드맵 |
| 업체 관리 | `docs/5-operations/VENDOR-MANAGEMENT.md` | 업체 정보 1차 소스 |
| 커뮤니케이션 규칙 | `docs/5-operations/COMMUNICATION-RULES.md` | 외부 이메일 규칙 |
| 업체 선정 체크리스트 | `docs/1-phase-0/VENDOR-SELECTION-CHECKLIST.md` | Phase 0 기준 |
| 기능 체크리스트 | `docs/2-phase-1/PokerGFX-Feature-Checklist.md` | 119개 복제 대상 |
| PokerGFX 참조 자료 | `docs/2-phase-1/reference/` | 매뉴얼/보안 PDF |
| 이메일 드래프트 | `docs/5-operations/email-drafts/` | 업체 컨택 이메일 |
| 데일리 브리핑 | `docs/5-operations/daily-briefings/` | 일일 현황 보고 |
| 문서 네비게이션 | `docs/README.md` | 전체 문서 색인 |

## System Files

| 위치 | 설명 |
|------|------|
| `.omc/bkit/` | bkit PDCA 상태, 스냅샷 (삭제 금지) |
| `.omc/plans/` | 작업 계획 문서 |
| `.claude/` | Claude 커맨드, 스킬, 에이전트 설정 |
