# EBS 문서

> **BRACELET STUDIO** | EBS (Event Broadcasting System)

## 현재 상태

| 단계 | 상태 | 설명 |
|:----:|:----:|------|
| **Phase 0** | 🟡 | 업체 선정, 준비 |
| **Phase 1** | ⏳ | PokerGFX 동일 제품 개발 |
| **Phase 2** | ⏳ | WSOPLIVE DB 연동 |
| **Phase 3** | ⏳ | 자동화 프로토콜 |

**마일스톤**: RFID POC (Q2) → PokerGFX 복제 (Q4) → WSOPLIVE 연동 (27Q4) → 자동화 (28Q4)

---

## 문서 구조

```
docs/
├── README.md                           ← 현재 문서
├── PRD-0003-EBS-RFID-System.md        # Master PRD
│
├── phase-0/                            # Phase 0: 업체 선정, 준비
│   └── CONCEPT-EBS-Vision.md          # EBS 비전/목표
│
├── phase-1/                            # Phase 1: PokerGFX 동일 제품
│   ├── PRD-0003-Phase1-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md  # 119개 기능
│   ├── BEGINNER-Hardware-Quickstart.md
│   └── DESIGN-RFID-Hardware.md
│
├── phase-2/                            # Phase 2: WSOPLIVE DB 연동
│   └── PRD-0003-Phase2-WSOP-Integration.md
│
├── phase-3/                            # Phase 3: 자동화
│   └── PRD-0003-Phase3-EBS-Automation.md
│
└── operations/                         # 운영 문서
    ├── EBS-WORK-DASHBOARD.md          # 업무 현황
    ├── VENDOR-MANAGEMENT.md           # 업체 관리
    └── PHASE-PROGRESSION.md           # Phase 진행 가이드
```

---

## 문서 목록

### 핵심 기획

| 문서 | 설명 |
|------|------|
| [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | Master PRD |
| [CONCEPT-EBS-Vision.md](phase-0/CONCEPT-EBS-Vision.md) | EBS 비전, 프로덕션 인프라로서의 역할 |

### Phase 1: PokerGFX 동일 제품

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase1-PokerGFX-Clone.md](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) | Phase 1 상세 계획 |
| [PokerGFX-Feature-Checklist.md](phase-1/PokerGFX-Feature-Checklist.md) | 119개 기능 체크리스트 |
| [BEGINNER-Hardware-Quickstart.md](phase-1/BEGINNER-Hardware-Quickstart.md) | RFID 하드웨어 참조 |

### 운영

| 문서 | 설명 |
|------|------|
| [EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md) | 업무 현황 대시보드 |
| [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | 업체 관리 |
| [PHASE-PROGRESSION.md](operations/PHASE-PROGRESSION.md) | Phase 진행 조건/가이드 |

### 미래 단계 (Phase 1 완료 후)

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase2-WSOP-Integration.md](phase-2/PRD-0003-Phase2-WSOP-Integration.md) | DB 연동 계획 |
| [PRD-0003-Phase3-EBS-Automation.md](phase-3/PRD-0003-Phase3-EBS-Automation.md) | 자동화 계획 |

---

## 역할별 시작점

| 역할 | 시작 문서 | 목적 |
|------|----------|------|
| **경영/PM** | [CONCEPT-EBS-Vision.md](phase-0/CONCEPT-EBS-Vision.md) | 프로젝트 목표/가치 이해 |
| **개발** | [BEGINNER-Hardware-Quickstart.md](phase-1/BEGINNER-Hardware-Quickstart.md) | 하드웨어 학습 |
| **구매** | [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | 업체 정보/RFQ |
| **운영** | [EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md) | 현재 업무 현황 |

---

## Google Drive 폴더 구조

로컬 문서와 1:1 매핑되는 Google Drive 구조:

```
EBS (Google Drive)/
├── 00_Overview/                    # 프로젝트 개요
│   └── Master-PRD.gdoc
│
├── 01_Phase-0-Preparation/         # Phase 0: 기획/준비
│   └── EBS-Vision.gdoc
│
├── 02_Phase-1-GFX-Clone/          # Phase 1: PokerGFX 복제
│   ├── PRD-Phase1.gdoc
│   ├── Feature-Checklist.gdoc
│   └── Hardware-Reference.gdoc
│
├── 03_Phase-2-DB-Integration/     # Phase 2: DB 연동
│   └── PRD-Phase2.gdoc
│
├── 04_Phase-3-Automation/         # Phase 3: 자동화
│   └── PRD-Phase3.gdoc
│
└── 90_Operations/                  # 운영
    ├── Work-Dashboard.gdoc
    ├── Vendor-Management.gdoc
    └── Phase-Progression.gdoc
```

| 번호 | 용도 |
|:----:|------|
| 00 | 개요/Master 문서 |
| 01-04 | Phase별 문서 (순서대로) |
| 90 | 운영 문서 (Phase 독립적) |

---

## 참고 자료

| 파일 | 설명 |
|------|------|
| `user-manual_split/` | PokerGFX 매뉴얼 PDF (6개 파일) |
| `user-manual_images/` | 매뉴얼에서 추출한 이미지 |
| `PokerGFX_Security.pdf` | 보안 관련 참고 |

---

**Version**: 6.0.0 | **Updated**: 2026-02-03 | **BRACELET STUDIO**
