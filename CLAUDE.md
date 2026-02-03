# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Status

> **Current Phase: 🟡 Phase-Pre** (진행 중)
>
> | 단계 | 상태 | 설명 |
> |------|:----:|------|
> | **Phase-Pre** | 🟡 | 업체 선정, 준비 ← **현재** |
> | 1단계 | ⏳ | PokerGFX 동일 제품 개발 |
> | 2단계 | ⏳ | 운영 효율화 (1단계 완료 후) |
>
> **마일스톤**: RFID POC (Q2) → PokerGFX 복제 (Q4) → WSOPLIVE 연동 (27Q4) → 자동화 (28Q4)

## Project Overview

> **BRACELET STUDIO** | EBS (Event Broadcasting System)

EBS는 **포커 방송 프로덕션 전체 워크플로우의 인프라스트럭처**입니다.

**핵심 목표**:
- **자산 내재화/독립화**: 자체 시스템 소유
- **운영 효율화**: 30명 → 15~20명 (자막 연출 자동화)

## Architecture

```
Hardware: RFID Card → MFRC522/ST25R3911B → ESP32 → USB Serial
Software: ESP32 → Python Server (FastAPI) → WebSocket → React Frontend
```

**3-Layer Structure**:
- **Firmware (Arduino/C++)**: ESP32에서 RFID 태그 읽기, JSON Serial 출력
- **Server (Python/FastAPI)**: Serial 수신, DB 조회, WebSocket 브로드캐스트
- **Frontend (React/TypeScript)**: 실시간 카드 UI, OBS 오버레이

**RFID 모듈**:
| 용도 | 모듈 | 비고 |
|------|------|------|
| 학습용 | MFRC522 | Phase 0 (초기 프로토타입) |
| **프로덕션** | **ST25R3911B** | 업체 선정 후 도입 |

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

> ⚠️ 1단계 진행 시 실제 구현 예정

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

### 디렉토리 구조

```
docs/
├── README.md                           # 네비게이션
├── PRD-0003-EBS-RFID-System.md        # Master PRD
│
├── phase-pre/                          # Phase-Pre: 기획/준비
│   └── CONCEPT-EBS-Vision.md          # EBS 비전
│
├── phase-0/                            # 1단계: PokerGFX 동일 제품
│   ├── PRD-0003-Phase0-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md  # 119개 기능
│   └── BEGINNER-Hardware-Quickstart.md
│
├── phase-1/                            # (미래) DB 연동
│   └── PRD-0003-Phase1-WSOP-Integration.md
│
├── phase-2/                            # (미래) 자동화
│   └── PRD-0003-Phase2-EBS-Automation.md
│
└── operations/                         # 운영 문서
    ├── EBS-WORK-DASHBOARD.md
    ├── VENDOR-MANAGEMENT.md
    └── PHASE-PROGRESSION.md
```

### 주요 문서

| 문서 유형 | 경로 | 용도 |
|----------|------|------|
| Master PRD | `docs/PRD-0003-EBS-RFID-System.md` | 비전/전략 |
| EBS 비전 | `docs/phase-pre/CONCEPT-EBS-Vision.md` | 프로덕션 인프라 역할 |
| 업무 대시보드 | `docs/operations/EBS-WORK-DASHBOARD.md` | 현재 작업 현황 |
| Phase 진행 가이드 | `docs/operations/PHASE-PROGRESSION.md` | Phase 순서/조건 |
| 초보자 가이드 | `docs/phase-0/BEGINNER-Hardware-Quickstart.md` | 하드웨어 입문 |

## 1단계 완료 조건

PokerGFX 동일 제품 완성 기준:

- [ ] **PokerGFX 100% 복제**: UI/UX 완전 동일
- [ ] **카드 표시 정확도**: 52장 카드 100% 정확
- [ ] **실시간 성능**: 카드→화면 < 1초 (목표 < 200ms)
- [ ] **OBS 오버레이**: 투명도/크로마키 정상 작동
- [ ] **안정성**: 4시간 연속 운영 무중단

---

## Google Docs 동기화

| 문서 | Google Docs ID |
|------|---------------|
| BEGINNER-Hardware-Quickstart | `1Q61fgxFZeU1L0epB44ybSJ1dKxXslvmLorqAqmLcotc` |
