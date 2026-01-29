# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Status

> **Current Phase: Planning / Pre-implementation (Stage 0)**
>
> 실제 코드는 아직 구현되지 않았습니다. 아래 Build & Run 명령어는 **계획된 설계**입니다.
> 현재는 문서 작업과 리서치가 주요 작업입니다.

## Project Overview

EBS (Event Broadcasting System)는 RFID 기반 포커 카드 인식 시스템입니다. ESP32 + MFRC522 하드웨어와 Python/React 소프트웨어로 구성되며, 실시간 카드 인식 및 방송 오버레이 기능을 제공합니다.

**Goal**: WSOP STUDIO DB 자산 내재화 + 방송 워크플로우 자동화

## Architecture

```
Hardware: RFID Card → MFRC522 → ESP32 → USB Serial
Software: ESP32 → Python Server (FastAPI) → WebSocket → React Frontend
Database: SQLite (cards.db)
```

**3-Layer Structure**:
- **Firmware (Arduino/C++)**: ESP32에서 RFID 태그 읽기, JSON Serial 출력
- **Server (Python/FastAPI)**: Serial 수신, DB 조회, WebSocket 브로드캐스트
- **Frontend (React/TypeScript)**: 실시간 카드 UI, OBS 오버레이

## Build & Run Commands (Planned)

> ⚠️ Stage 0 완료 후 실제 구현 시 사용 예정

### Firmware (Arduino IDE)
```bash
# ESP32 펌웨어 업로드
# Arduino IDE에서 firmware/rfid_reader/rfid_reader.ino 열고 Upload
```

### Server (Python)
```bash
cd server
python -m venv venv
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev                # Development (localhost:5173)
npm run build              # Production build
```

### Tests (Planned)
```bash
cd server && pytest tests/ -v
cd frontend && npm test
```

## Current Tools (Available Now)

`tools/` 디렉토리에 문서 처리 유틸리티가 있습니다:

```bash
# PDF 페이지 분할
python tools/split_pdf.py <input.pdf> --pages 20

# PDF 이미지 추출
python tools/extract_images.py <input.pdf> --output-dir <output/>

# 의존성 설치
pip install -r tools/requirements.txt
```

## Key Technical Details

### Hardware Wiring (ESP32 → MFRC522)
| ESP32 | MFRC522 | Function |
|-------|---------|----------|
| 3.3V  | VCC     | Power    |
| GND   | GND     | Ground   |
| GPIO5 | SDA     | SPI SS   |
| GPIO18| SCK     | SPI Clock|
| GPIO23| MOSI    | SPI MOSI |
| GPIO19| MISO    | SPI MISO |
| GPIO4 | RST     | Reset    |

### Serial Protocol (ESP32 → Server)
```json
{"type": "card_read", "uid": "04:A2:B3:C4", "reader_id": 0, "timestamp": 123456}
```

### WebSocket Events (Server → Client)
```json
{"type": "card_detected", "uid": "...", "card": {"suit": "spades", "rank": "A", "display": "A♠"}}
{"type": "reader_status", "connected": true, "port": "COM3"}
```

## Documentation

전체 문서 네비게이션은 `docs/README.md` 참조

### Stage별 PRD
| Stage | Document | 기간 | 핵심 목표 |
|-------|----------|------|----------|
| **0** | `docs/stage-0/PRD-0003-Stage0-RFID-Connection.md` | 2026 H1 | RFID 연결 검증 |
| 1 | `docs/stage-1/PRD-0003-Stage1-PokerGFX-Clone.md` | 2026 H2 | PokerGFX 복제 |
| 2 | `docs/stage-2/PRD-0003-Stage2-WSOP-Integration.md` | 2027 | WSOP+ 연동 |
| 3 | `docs/stage-3/PRD-0003-Stage3-EBS-Automation.md` | 2028 | 80% 자동화 |

### 핵심 기술 문서
| Document | 용도 |
|----------|------|
| `docs/PRD-0003-EBS-RFID-System.md` | Master PRD (비전/전략) |
| `docs/stage-1/ARCHITECTURE-RFID-Software.md` | 소프트웨어 아키텍처 |
| `docs/stage-0/DESIGN-RFID-Hardware.md` | 하드웨어 설계 (배선도) |
| `docs/stage-0/GUIDE-RFID-Implementation.md` | 구현 가이드 |

## Data Flow

```
RFID Card → MFRC522 (13.56MHz) → ESP32 (SPI) → USB Serial JSON
    → Python Server (DB lookup) → WebSocket → React UI → OBS Overlay
```

**Latency Target**: < 200ms E2E
