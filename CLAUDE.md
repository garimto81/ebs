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

## Build & Run Commands

### 현재 사용 가능한 도구

```powershell
# PDF 도구 의존성 설치
pip install -r C:\claude\ebs\tools\requirements.txt

# PDF 페이지 분할
python C:\claude\ebs\tools\split_pdf.py <input.pdf> 20

# PDF 이미지 추출
python C:\claude\ebs\tools\extract_images.py <input.pdf> --output-dir <output/>

# PDF 토큰 기반 청킹
python C:\claude\ebs\tools\pdf_chunker.py <input.pdf>
```

### Morning Automation (데일리 브리핑)

```powershell
# 의존성: slack-sdk, google-api-python-client, python-dateutil, rich
pip install -r C:\claude\ebs\tools\morning-automation\requirements.txt

# 실행
python C:\claude\ebs\tools\morning-automation\main.py
```

구조: `collectors/` (Slack, Gmail, Lists 수집) -> `reporters/` (Markdown 리포트, Slack 게시)

### Database

```powershell
# SQLite 카드 DB 초기화 (54장: 52장 + 조커 2장, UID 미매핑 상태)
sqlite3 C:\claude\ebs\server\db\cards.db < C:\claude\ebs\server\db\init.sql
```

### Phase 1 이후 (미구현)

```powershell
# Server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
npm run dev  # localhost:5173

# Tests
pytest tests/ -v    # server
npm test            # frontend
```

## Serial/WebSocket Protocol

```jsonc
// ESP32 -> Server
{"type": "card_read", "uid": "04:A2:B3:C4", "reader_id": 0, "timestamp": 123456}

// Server -> Client
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

### Slack/Gmail 자동화 제약

| 규칙 | 내용 |
|------|------|
| `--notify` 사용 금지 | `chat:write:bot` scope 없음 |
| `--post`만 사용 | 채널 메시지 갱신만 가능 |
| DM 발송 불가 | Slack API 제한 |
