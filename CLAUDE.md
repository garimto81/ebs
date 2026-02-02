# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Status

> **Current Phase: 🟡 Stage-Pre** (진행 중)
>
> | 단계 | 상태 | 설명 |
> |------|:----:|------|
> | **Stage-Pre** | 🟡 | 기획/관리 체계 수립 ← **현재** |
> | Stage 0 | ⏳ | RFID 연결 검증 (Stage-Pre 완료 후) |
> | Stage 1-3 | ⏳ | 개발 단계 |
>
> 현재는 문서 작업, 업체 리서치, 관리 시스템 구축이 주요 작업입니다.

## Project Overview

EBS (Event Broadcasting System)는 RFID 기반 포커 카드 인식 시스템입니다.

**Goal**: WSOP STUDIO DB 자산 내재화 + 방송 워크플로우 자동화

## Architecture

```
Hardware: RFID Card → MFRC522/ST25R3911B → ESP32 → USB Serial
Software: ESP32 → Python Server (FastAPI) → WebSocket → React Frontend
Database: SQLite (cards.db)
```

**3-Layer Structure**:
- **Firmware (Arduino/C++)**: ESP32에서 RFID 태그 읽기, JSON Serial 출력
- **Server (Python/FastAPI)**: Serial 수신, DB 조회, WebSocket 브로드캐스트
- **Frontend (React/TypeScript)**: 실시간 카드 UI, OBS 오버레이

**RFID 모듈**:
| 용도 | 모듈 | 비고 |
|------|------|------|
| 학습용 | MFRC522 | Stage 0 Phase 0-1~0-2 |
| **프로덕션** | **ST25R3911B** | Stage 0 Phase 0-3~0-4, Stage 1+ |

## Current Tools (Available Now)

`tools/` 디렉토리에 문서 처리 유틸리티가 있습니다:

```powershell
# 의존성 설치
pip install -r tools/requirements.txt

# PDF 페이지 분할 (20페이지씩)
python tools/split_pdf.py <input.pdf> 20

# 특정 페이지 범위 추출
python tools/split_pdf.py <input.pdf> --extract <start> <end>

# PDF 이미지 추출
python tools/extract_images.py <input.pdf> --output-dir <output/>

# PDF 토큰 기반 청킹
python tools/pdf_chunker.py <input.pdf>
```

**의존성**: `pymupdf>=1.24.0`, `tiktoken>=0.5.0`

## Database

카드 DB 초기화 스크립트: `server/db/init.sql`
- 54장 카드 (52장 + 조커 2장) 초기 데이터 포함
- UID 매핑 전 상태로 생성

```powershell
# SQLite DB 초기화
sqlite3 server/db/cards.db < server/db/init.sql
```

## Build & Run Commands (Planned)

> ⚠️ Stage 0 완료 후 실제 구현 시 사용 예정

```powershell
# Server (Python)
cd C:\claude\ebs\server
python -m venv venv && .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (React)
cd C:\claude\ebs\frontend
npm install && npm run dev  # localhost:5173

# Tests
cd C:\claude\ebs\server && pytest tests/ -v
cd C:\claude\ebs\frontend && npm test
```

## Hardware Wiring (ESP32 → MFRC522)

| ESP32 | MFRC522 | Function |
|-------|---------|----------|
| 3.3V  | VCC     | Power (3.3V 필수!) |
| GND   | GND     | Ground   |
| GPIO5 | SDA     | SPI SS   |
| GPIO18| SCK     | SPI Clock|
| GPIO23| MOSI    | SPI MOSI |
| GPIO19| MISO    | SPI MISO |
| GPIO4 | RST     | Reset    |

## Serial/WebSocket Protocol

```jsonc
// ESP32 → Server
{"type": "card_read", "uid": "04:A2:B3:C4", "reader_id": 0, "timestamp": 123456}

// Server → Client
{"type": "card_detected", "uid": "...", "card": {"suit": "spades", "rank": "A", "display": "A♠"}}
{"type": "reader_status", "connected": true, "port": "COM3"}
```

## Documentation

문서 네비게이션: `docs/README.md`

### 디렉토리 구조 (숫자 순서 = 진행 순서)

```
docs/
├── 0-pre/      # Stage-Pre: 기획/준비 ◀ 현재
├── 1-stage0/   # Stage 0: RFID 검증
├── 2-stage1/   # Stage 1: GFX 복제
├── 3-stage2/   # Stage 2: DB 연동
├── 4-stage3/   # Stage 3: 자동화
└── operations/ # 업무 관리 문서
```

### 주요 문서

| 문서 유형 | 경로 | 용도 |
|----------|------|------|
| Master PRD | `docs/PRD-0003-EBS-RFID-System.md` | 비전/전략 |
| 업무 대시보드 | `docs/operations/EBS-WORK-DASHBOARD.md` | 현재 작업 현황 |
| Stage 진행 가이드 | `docs/operations/STAGE-PROGRESSION.md` | Stage 순서/조건 |
| Stage-Pre 문서 | `docs/0-pre/` | 기획 문서 |
| Stage 0 문서 | `docs/1-stage0/` | RFID 검증 |
| 하드웨어 설계 | `docs/1-stage0/DESIGN-RFID-Hardware.md` | 배선도/MCU 비교 |
| 초보자 가이드 | `docs/1-stage0/BEGINNER-Hardware-Quickstart.md` | 하드웨어 입문 |

## Stage 0 Gate 조건

Stage 1 진입을 위해 다음 조건 충족 필요:

- [ ] RFID 읽기: 5장 카드 100% 인식
- [ ] E2E 지연: 카드→화면 < 1초
- [ ] 연속 운영: 4시간 무중단
- [ ] **ST25R3911B 검증**: SPEC 문서 10항목 PASS
- [ ] 팀 합의: "Stage 1 진행 가능"

**Latency Target**: < 200ms E2E

---

## Google Docs 동기화

| 문서 | Google Docs ID |
|------|---------------|
| BEGINNER-Hardware-Quickstart | `1Q61fgxFZeU1L0epB44ybSJ1dKxXslvmLorqAqmLcotc` |
