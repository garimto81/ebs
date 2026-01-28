# EBS Documentation

EBS (Event Broadcasting System) 프로젝트 문서 색인입니다.

---

## 문서 구조

```
docs/
├── README.md                          # 문서 네비게이션 (현재 파일)
├── PRD-0003-EBS-RFID-System.md        # Master PRD (비전/전략)
│
├── stage-0/                           # 2026 H1: RFID 연결 검증
│   ├── PRD-0003-Stage0-RFID-Connection.md
│   ├── DESIGN-RFID-Hardware.md
│   └── GUIDE-RFID-Implementation.md
│
├── stage-1/                           # 2026 H2: PokerGFX 복제
│   ├── PRD-0003-Stage1-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md
│   ├── ARCHITECTURE-RFID-Software.md
│   └── REPORT-PokerGFX-Server-Analysis.md
│
├── stage-2/                           # 2027: WSOP+ 연동
│   └── PRD-0003-Stage2-WSOP-Integration.md
│
├── stage-3/                           # 2028: EBS 자동화
│   └── PRD-0003-Stage3-EBS-Automation.md
│
├── research/                          # 리서치/의사결정 근거
│   └── RESEARCH-RFID-Poker-Suppliers.md
│
├── mockups/                           # HTML 와이어프레임
├── images/                            # 스크린샷/다이어그램
│
└── archived/                          # 레거시 문서
    ├── PRD-0001-RFID-Poker-Card-Reader-MVP.md
    ├── PRD-0002-Overlay-POC-Feature-Roadmap.md
    └── MEETING-Outsourcing-Questions.md
```

---

## Quick Start

### "지금 무엇을 봐야 하나요?"

| 질문 | 문서 |
|------|------|
| **EBS가 뭔가요?** | [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) |
| **Stage 0에서 뭘 해야 하나요?** | [stage-0/](stage-0/) 폴더 전체 |
| **하드웨어 어떻게 연결하나요?** | [stage-0/DESIGN-RFID-Hardware.md](stage-0/DESIGN-RFID-Hardware.md) |
| **소프트웨어 구조는?** | [stage-1/ARCHITECTURE-RFID-Software.md](stage-1/ARCHITECTURE-RFID-Software.md) |
| **PokerGFX 기능 목록은?** | [stage-1/PokerGFX-Feature-Checklist.md](stage-1/PokerGFX-Feature-Checklist.md) |

---

## 문서 역할 분류

### Master PRD (비전/전략)

| 문서 | 역할 | 독자 |
|------|------|------|
| [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | 왜 만드는가, 무엇을 만드는가 | 경영진, PM |

### Stage PRD (구현 계획)

| Stage | 기간 | 문서 |
|-------|------|------|
| **Stage 0** | 2026 H1 | [PRD-0003-Stage0-RFID-Connection.md](stage-0/PRD-0003-Stage0-RFID-Connection.md) |
| **Stage 1** | 2026 H2 | [PRD-0003-Stage1-PokerGFX-Clone.md](stage-1/PRD-0003-Stage1-PokerGFX-Clone.md) |
| **Stage 2** | 2027 | [PRD-0003-Stage2-WSOP-Integration.md](stage-2/PRD-0003-Stage2-WSOP-Integration.md) |
| **Stage 3** | 2028 | [PRD-0003-Stage3-EBS-Automation.md](stage-3/PRD-0003-Stage3-EBS-Automation.md) |

### 기술 문서 (상세 설계)

| 문서 | 역할 | 주 사용 시점 |
|------|------|-------------|
| [DESIGN-RFID-Hardware.md](stage-0/DESIGN-RFID-Hardware.md) | ESP32+MFRC522 배선도 | Stage 0 |
| [GUIDE-RFID-Implementation.md](stage-0/GUIDE-RFID-Implementation.md) | 구현 체크리스트 | Stage 0 |
| [ARCHITECTURE-RFID-Software.md](stage-1/ARCHITECTURE-RFID-Software.md) | 3-Layer 소프트웨어 구조 | Stage 1+ |
| [PokerGFX-Feature-Checklist.md](stage-1/PokerGFX-Feature-Checklist.md) | 54개 기능 추적 | Stage 1 |

### 리서치 (의사결정 근거)

| 문서 | 용도 |
|------|------|
| [REPORT-PokerGFX-Server-Analysis.md](stage-1/REPORT-PokerGFX-Server-Analysis.md) | 경쟁사 분석 |
| [RESEARCH-RFID-Poker-Suppliers.md](research/RESEARCH-RFID-Poker-Suppliers.md) | 부품 구매 정보 |
| `PokerGFX_Security.pdf` | 경쟁사 보안 분석 |

---

## Stage별 필요 문서

### Stage 0: RFID 연결 검증 (2026 H1)

```
stage-0/
├── PRD-0003-Stage0-RFID-Connection.md  # 무엇을 검증할 것인가
├── DESIGN-RFID-Hardware.md             # 하드웨어 어떻게 연결하나
└── GUIDE-RFID-Implementation.md        # 주차별 체크리스트
```

**참조**: Stage 1의 `ARCHITECTURE-RFID-Software.md` (소프트웨어 구조 이해 시)

### Stage 1: PokerGFX 복제 (2026 H2)

```
stage-1/
├── PRD-0003-Stage1-PokerGFX-Clone.md   # 무엇을 복제할 것인가
├── PokerGFX-Feature-Checklist.md       # 54개 기능 체크리스트
├── ARCHITECTURE-RFID-Software.md       # 소프트웨어 구조
└── REPORT-PokerGFX-Server-Analysis.md  # 경쟁사 분석
```

### Stage 2-3

Stage 2, 3는 Stage 1 완료 후 상세 기술 문서가 추가될 예정입니다.

---

## Archived 문서

`archived/` 폴더의 문서는 더 이상 사용되지 않습니다:

| 문서 | 대체된 문서 |
|------|-------------|
| PRD-0001 | Stage 0 PRD |
| PRD-0002 | Stage 1-3 PRD |
| MEETING-* | 일회성 기록, 보관용 |

---

## 문서 업데이트 정책

- **Master PRD**: 비전/전략 변경 시에만 수정
- **Stage PRD**: 해당 Stage 진행 중 상세화
- **기술 문서**: 구현 중 수시 업데이트
- **Archived**: 수정 금지 (참조용)

---

*Last Updated: 2026-01-28*
