# EBS 문서

> **BRACELET STUDIO** | EBS (Event Broadcasting System)

## 현재 상태

| 단계 | 상태 | 설명 |
|:----:|:----:|------|
| **Phase 0** | 🟡 | 업체 선정, 준비 |
| **Phase 1** | ⏳ | PokerGFX 복제 |
| **Phase 2** | ⏳ | WSOPLIVE DB 연동 |
| **Phase 3** | ⏳ | 자동화 프로토콜 |

**마일스톤**: RFID POC (Q2) → PokerGFX 복제 (Q4) → WSOPLIVE 연동 (27Q4) → 자동화 (28Q4)

---

## 문서 구조

```
docs/
├── README.md                           ← 현재 문서
├── PRD-0003-EBS-RFID-System.md        # Master PRD (비전/전략)
│
├── phase-0/                            # Phase 0: 업체 선정
│   ├── VENDOR-SELECTION-CHECKLIST.md  # 업체 선정 체크리스트
│   └── PRD-0004-Vendor-Contact-Automation.md  # 업체 컨택 자동화
│
├── phase-1/                            # Phase 1: PokerGFX 복제
│   ├── PRD-0003-Phase1-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md  # 119개 기능 체크리스트
│   └── reference/                      # PokerGFX 참조 자료
│       ├── PokerGFX_Security.pdf
│       ├── user-manual_split/         # 매뉴얼 PDF (6개 파일)
│       └── user-manual_images/        # 매뉴얼 이미지
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
| [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | Master PRD (비전/전략/로드맵) |

### Phase 0: 업체 선정

| 문서 | 설명 |
|------|------|
| [VENDOR-SELECTION-CHECKLIST.md](phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 기준, 후보, 체크리스트 |
| [PRD-0004-Vendor-Contact-Automation.md](phase-0/PRD-0004-Vendor-Contact-Automation.md) | 업체 컨택 자동화 시스템 |

### Phase 1: PokerGFX 복제

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase1-PokerGFX-Clone.md](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) | Phase 1 상세 계획 |
| [PokerGFX-Feature-Checklist.md](phase-1/PokerGFX-Feature-Checklist.md) | 119개 기능 체크리스트 |
| [reference/](phase-1/reference/) | PokerGFX 매뉴얼, 보안 문서 |

### 운영

| 문서 | 설명 |
|------|------|
| [EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md) | 업무 현황 대시보드 |
| [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | 업체 관리 |
| [PHASE-PROGRESSION.md](operations/PHASE-PROGRESSION.md) | Phase 진행 조건/가이드 |
| [GOOGLE-DRIVE-STRUCTURE.md](GOOGLE-DRIVE-STRUCTURE.md) | Google Drive 폴더 구조 |

### 미래 단계 (Phase 1 완료 후)

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase2-WSOP-Integration.md](phase-2/PRD-0003-Phase2-WSOP-Integration.md) | DB 연동 계획 |
| [PRD-0003-Phase3-EBS-Automation.md](phase-3/PRD-0003-Phase3-EBS-Automation.md) | 자동화 계획 |

---

## 역할별 시작점

| 역할 | 시작 문서 | 목적 |
|------|----------|------|
| **경영/PM** | [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | 프로젝트 비전/전략 |
| **구매** | [VENDOR-SELECTION-CHECKLIST.md](phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 기준 |
| **개발** | [PokerGFX-Feature-Checklist.md](phase-1/PokerGFX-Feature-Checklist.md) | 복제 대상 기능 |
| **운영** | [EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md) | 현재 업무 현황 |

---

## Phase 1: PokerGFX 복제 가이드

Phase 1의 목표는 **PokerGFX의 모든 기능을 100% 복제**하는 것입니다.

### 복제 방법론

| 방법 | 설명 | 우선순위 |
|------|------|:--------:|
| **매뉴얼 분석** | user-manual PDF에서 기능/UI 추출 | 1 |
| **실사용 관찰** | 실제 방송에서 사용 패턴 기록 | 2 |
| **UI 캡처** | 스크린샷으로 레이아웃 분석 | 3 |
| **리버스 엔지니어링** | 통신 프로토콜, 데이터 구조 분석 | 4 |

### 참조 자료

| 자료 | 위치 | 용도 |
|------|------|------|
| 사용자 매뉴얼 | `phase-1/reference/user-manual_split/` | 기능/UI 분석 |
| 매뉴얼 이미지 | `phase-1/reference/user-manual_images/` | UI 참조 |
| 보안 문서 | `phase-1/reference/PokerGFX_Security.pdf` | 보안 구조 참조 |

---

## 문서 작성 규칙

### 변경 이력 위치

**모든 문서의 변경 이력/핵심 변경사항은 문서 최하단에 배치합니다.**

```markdown
# 문서 제목
## 1. 핵심 내용
## 2. 상세 내용
...
---
## 변경 이력        ← 항상 마지막 섹션
---
**Version**: X.X.X | **Updated**: YYYY-MM-DD
```

**이유**: 독자는 변경 이력보다 내용에 관심이 있음

---

**Version**: 7.2.0 | **Updated**: 2026-02-04 | **BRACELET STUDIO**
