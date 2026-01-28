# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EBS (RFID Poker Card Reader)는 RFID 기반 포커 카드 인식 시스템입니다. ESP32 + MFRC522 하드웨어와 Python/React 소프트웨어로 구성되며, 실시간 카드 인식 및 웹 UI 표시 기능을 제공합니다.

## Architecture

```
Hardware: RFID Card → MFRC522 → ESP32 → USB Serial
Software: ESP32 → Python Server (FastAPI) → WebSocket → React Frontend
Database: SQLite (cards.db)
```

**3-Layer Structure**:
- **Firmware (Arduino/C++)**: ESP32에서 RFID 태그 읽기, JSON Serial 출력
- **Server (Python/FastAPI)**: Serial 수신, DB 조회, WebSocket 브로드캐스트
- **Frontend (React/TypeScript)**: 실시간 카드 UI, 연결 상태 표시

## Project Structure (Planned)

```
ebs/
├── firmware/           # ESP32 Arduino 코드
│   └── rfid_reader/
├── server/             # Python FastAPI 서버
│   └── app/
│       ├── api/        # REST/WebSocket 엔드포인트
│       ├── services/   # Serial, Card, WebSocket 서비스
│       ├── models/     # Pydantic 모델
│       └── db/         # SQLite 연결
├── frontend/           # React TypeScript 앱
│   └── src/
│       ├── components/ # Card, CardSlot, History
│       ├── hooks/      # useWebSocket
│       └── types/      # TypeScript 타입
├── data/               # SQLite DB 파일
├── tools/              # 카드 매핑 도구
└── docs/               # 설계 문서
```

## Build & Run Commands

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

### Tests
```bash
# Server 테스트
cd server
pytest tests/ -v

# Frontend 테스트
cd frontend
npm test
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

### Database Schema
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    uid TEXT UNIQUE NOT NULL,
    suit TEXT NOT NULL,  -- spades, hearts, diamonds, clubs, joker
    rank TEXT NOT NULL,
    display TEXT NOT NULL,
    value INTEGER NOT NULL
);
```

## Development Status

**Current Phase**: Planning / Pre-implementation

아직 실제 코드는 구현되지 않았습니다. 구조와 명령어는 계획된 설계입니다.

## Documentation

전체 문서 네비게이션은 `docs/README.md` 참조

### Master PRD
| Document | Purpose |
|----------|---------|
| `docs/PRD-0003-EBS-RFID-System.md` | **Master PRD (v5.3)** - 비전/전략/로드맵 |

### Stage별 PRD
| Stage | Document | 기간 |
|-------|----------|------|
| 0 | `docs/stage-0/PRD-0003-Stage0-RFID-Connection.md` | 2026 H1 |
| 1 | `docs/stage-1/PRD-0003-Stage1-PokerGFX-Clone.md` | 2026 H2 |
| 2 | `docs/stage-2/PRD-0003-Stage2-WSOP-Integration.md` | 2027 |
| 3 | `docs/stage-3/PRD-0003-Stage3-EBS-Automation.md` | 2028 |

### 기술 문서
| Document | Purpose |
|----------|---------|
| `docs/stage-1/ARCHITECTURE-RFID-Software.md` | 소프트웨어 아키텍처 (3-Layer, API 설계) |
| `docs/stage-0/DESIGN-RFID-Hardware.md` | 하드웨어 설계 (ESP32 배선, 부품 목록) |
| `docs/stage-0/GUIDE-RFID-Implementation.md` | 구현 가이드 (Week별 체크리스트) |
| `docs/stage-1/PokerGFX-Feature-Checklist.md` | Stage 1 기능 추적 (54개 항목) |

## Google Docs Reference

| 문서 | Google Docs ID | 버전 | 동기화 날짜 |
|------|----------------|------|-------------|
| **PRD-0003-EBS-RFID-System** | `1_uP4A_LXPWFRh9_T_JKeizx1wscawU0LzI0QAlqJnXc` | v5.3.0 | 2026-01-28 |

> **동기화 필요**: 로컬 v5.3.0 → Google Docs 업데이트 필요
> Section 4-6 경량화 (상세 스펙 → Stage PRD 위임)

**Google Docs URL**: https://docs.google.com/document/d/1_uP4A_LXPWFRh9_T_JKeizx1wscawU0LzI0QAlqJnXc/edit

## UI Mockups

`docs/mockups/` 디렉토리에 B&W 와이어프레임 HTML 목업이 있으며, `docs/images/mockups/`에 스크린샷이 저장됩니다.

주요 목업: Viewer Overlay, Action Tracker, Production Dashboard, Automation Flow, Security Modes 등

## Data Flow Summary

```
1. RFID Card → MFRC522 (13.56MHz RF)
2. MFRC522 → ESP32 (SPI)
3. ESP32 → Server (USB Serial JSON)
4. Server: UID → DB lookup → Card info
5. Server → Frontend (WebSocket broadcast)
6. Frontend → OBS (Browser Source overlay)
```

**Latency Target**: < 200ms E2E
