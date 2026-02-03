# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Status

> **Current Phase: 🟡 Phase 0** (진행 중)
>
> | 단계 | 상태 | 설명 |
> |------|:----:|------|
> | **Phase 0** | 🟡 | 업체 선정, 준비 ← **현재** |
> | Phase 1 | ⏳ | PokerGFX 복제 |
> | Phase 2 | ⏳ | WSOPLIVE DB 연동 |
> | Phase 3 | ⏳ | 자동화 프로토콜 |
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
| 테스트용 | MFRC522 | Phase 1 초기 |
| **프로덕션** | **ST25R3911B** | Phase 0 업체 선정 |

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

> ⚠️ Phase 1 진행 시 실제 구현 예정

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
├── PRD-0003-EBS-RFID-System.md        # Master PRD (비전/전략)
│
├── phase-0/                            # Phase 0: 업체 선정
│   └── VENDOR-SELECTION-CHECKLIST.md  # 업체 선정 체크리스트
│
├── phase-1/                            # Phase 1: PokerGFX 복제
│   ├── PRD-0003-Phase1-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md  # 119개 기능
│   └── reference/                      # PokerGFX 참조 자료
│       ├── PokerGFX_Security.pdf
│       ├── user-manual_split/
│       └── user-manual_images/
│
├── phase-2/                            # Phase 2: DB 연동
│   └── PRD-0003-Phase2-WSOP-Integration.md
│
├── phase-3/                            # Phase 3: 자동화
│   └── PRD-0003-Phase3-EBS-Automation.md
│
└── operations/                         # 운영 문서
    ├── EBS-WORK-DASHBOARD.md
    ├── VENDOR-MANAGEMENT.md
    └── PHASE-PROGRESSION.md
```

### 주요 문서

| 문서 유형 | 경로 | 용도 |
|----------|------|------|
| Master PRD | `docs/PRD-0003-EBS-RFID-System.md` | 비전/전략/로드맵 |
| 업체 선정 | `docs/phase-0/VENDOR-SELECTION-CHECKLIST.md` | 업체 선정 기준/체크리스트 |
| 기능 체크리스트 | `docs/phase-1/PokerGFX-Feature-Checklist.md` | 119개 복제 대상 기능 |
| 참조 자료 | `docs/phase-1/reference/` | PokerGFX 매뉴얼/보안 문서 |
| 업무 대시보드 | `docs/operations/EBS-WORK-DASHBOARD.md` | 현재 작업 현황 |

## Phase 1 완료 조건

PokerGFX 100% 복제 완성 기준:

- [ ] **PokerGFX 100% 복제**: UI/UX 완전 동일
- [ ] **카드 표시 정확도**: 52장 카드 100% 정확
- [ ] **실시간 성능**: 카드→화면 < 1초 (목표 < 200ms)
- [ ] **OBS 오버레이**: 투명도/크로마키 정상 작동
- [ ] **안정성**: 4시간 연속 운영 무중단

---

## 시스템 파일 위치

| 파일 유형 | 위치 | 설명 |
|----------|------|------|
| bkit 상태 | `.omc/bkit/` | PDCA 상태, 스냅샷 |
| Claude 설정 | `.claude/` | 커맨드, 스킬, 에이전트 |
| OMC 상태 | `.omc/` | oh-my-claudecode 상태 |

**⚠️ 주의**: `.omc/bkit/` 폴더는 bkit 플러그인의 작업 상태를 저장합니다. 삭제하지 마세요.

---

## 문서 작성 규칙

### 변경 이력 위치 (CRITICAL)

**모든 문서의 변경 이력/핵심 변경사항/버전 히스토리는 반드시 문서 최하단에 배치합니다.**

| 규칙 | 설명 |
|------|------|
| **변경 이력 = 최하단** | 독자는 변경 이력보다 내용에 관심 |
| **Version 푸터 = 변경 이력 직후** | 날짜/버전 정보는 맨 마지막 |
| **금지: 중간 배치** | 변경 이력이 문서 중간에 있으면 최하단으로 이동 |

**올바른 문서 구조:**
```markdown
# 문서 제목
## 1. 핵심 내용
## 2. 상세 내용
...
## N. 참고 자료
---
## 변경 이력        ← 항상 마지막 섹션
| 날짜 | 버전 | 변경 내용 |
---
**Version**: X.X.X | **Updated**: YYYY-MM-DD
```
