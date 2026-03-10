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
├── 00-prd/                             # PRD 문서
│   ├── EBS-UI-Design-v3.prd.md        # EBS UI Design SSOT (v8.1.0)
│   ├── ebs-console.prd.md             # EBS Console PRD
│   └── action-tracker.prd.md          # Action Tracker PRD
│
├── 01_PokerGFX_Analysis/              # PokerGFX 분석 (Phase 0 기획)
│   ├── PRD-0003-Phase1-PokerGFX-Clone.md
│   ├── PokerGFX-Feature-Checklist.md  # 149개 기능 체크리스트
│   ├── PokerGFX-UI-Analysis.md        # PokerGFX UI 스크린샷 분석
│   ├── PokerGFX-Server-Binary-Analysis.md  # 바이너리 분석
│   ├── PRD-0004-technical-specs.md       # 기술 명세서
│   ├── 01_Mockups_ngd/                # HTML 목업 + PNG
│   ├── 02_Annotated_ngd/              # 주석 이미지
│   ├── 03_Reference_ngd/              # PokerGFX 참조 자료
│   │   ├── PokerGFX_Security.pdf
│   │   ├── user-manual_split/         # 매뉴얼 PDF (6개 파일)
│   │   └── user-manual_images/        # 매뉴얼 이미지
│   ├── 04_Protocol_Spec/             # 프로토콜 스펙
│   ├── 05_Behavioral_Spec/           # 상태 머신
│   ├── 06_Cross_Reference/           # 레지스트리 + 감사
│   ├── 07_Decompiled_Archive/        # 디컴파일 (gitignored)
│   └── 08_PDCA_Archive/              # PDCA plan/design/report
│
├── 03_Phase02_ngd/                     # Phase 2: WSOPLIVE DB 연동
│   └── PRD-0003-Phase2-WSOP-Integration.md
│
├── 04_Phase03_ngd/                     # Phase 3: 자동화
│   └── PRD-0003-Phase3-EBS-Automation.md
│
├── 05_Operations_ngd/                  # 운영 문서
│   ├── VENDOR-MANAGEMENT.md           # 업체 관리 (Source of Truth)
│   ├── PHASE-PROGRESSION.md           # Phase 진행 가이드
│   ├── COMMUNICATION-RULES_ngd.md     # 외부 커뮤니케이션 규칙
│   ├── VENDOR-SELECTION-CHECKLIST.md  # 업체 선정 체크리스트
│   ├── PRD-0004-Vendor-Contact-Automation.md  # 업체 컨택 자동화
│   ├── VIMEO-OTT-PRICING-SUMMARY_ngd.md  # OTT 견적
│   ├── 01_DailyBriefings_ngd/         # 일일 브리핑 보고서
│   └── 02_EmailDrafts_ngd/            # 업체 이메일 드래프트
│
├── 90_Images_ngd/                      # 이미지 자료
├── 91_Mockups_ngd/                     # 목업
├── GOOGLE-DRIVE-STRUCTURE_ngd.md      # Google Drive 폴더 구조
└── MAPPING_ngd.json                    # 매핑 정보
```

---

## 문서 목록

### 핵심 기획

| 문서 | 설명 |
|------|------|
| [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | Master PRD (비전/전략/로드맵) |

### PokerGFX 분석

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase1-PokerGFX-Clone.md](01_PokerGFX_Analysis/PRD-0003-Phase1-PokerGFX-Clone.md) | PokerGFX 시스템 아키텍처 참조 |
| [PokerGFX-Feature-Checklist.md](01_PokerGFX_Analysis/PokerGFX-Feature-Checklist.md) | 149개 기능 체크리스트 |
| [PokerGFX-UI-Analysis.md](01_PokerGFX_Analysis/PokerGFX-UI-Analysis.md) | PokerGFX UI 스크린샷 분석 (v3.0.0) |
| [EBS-UI-Design-v3.prd.md](00-prd/EBS-UI-Design-v3.prd.md) | EBS UI Design SSOT (v8.1.0) |
| [PRD-0004-technical-specs.md](01_PokerGFX_Analysis/PRD-0004-technical-specs.md) | 기술 명세서 (카드, 게임 엔진, GPU) |
| [PokerGFX-Server-Binary-Analysis.md](01_PokerGFX_Analysis/PokerGFX-Server-Binary-Analysis.md) | 서버 바이너리 분석 |
| [03_Reference_ngd/](01_PokerGFX_Analysis/03_Reference_ngd/) | PokerGFX 매뉴얼, 보안 문서 |

### 운영

| 문서 | 설명 |
|------|------|
| [VENDOR-MANAGEMENT.md](05_Operations_ngd/VENDOR-MANAGEMENT.md) | 업체 관리 (Source of Truth) |
| [PHASE-PROGRESSION.md](05_Operations_ngd/PHASE-PROGRESSION.md) | Phase 진행 조건/가이드 |
| [COMMUNICATION-RULES_ngd.md](05_Operations_ngd/COMMUNICATION-RULES_ngd.md) | 외부 커뮤니케이션 규칙 |
| [VENDOR-SELECTION-CHECKLIST.md](05_Operations_ngd/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 체크리스트 |
| [01_DailyBriefings_ngd/](05_Operations_ngd/01_DailyBriefings_ngd/) | 일일 브리핑 보고서 |
| [02_EmailDrafts_ngd/](05_Operations_ngd/02_EmailDrafts_ngd/) | 업체 이메일 드래프트 |
| [GOOGLE-DRIVE-STRUCTURE_ngd.md](GOOGLE-DRIVE-STRUCTURE_ngd.md) | Google Drive 폴더 구조 |

### 미래 단계 (Phase 1 완료 후)

| 문서 | 설명 |
|------|------|
| [PRD-0003-Phase2-WSOP-Integration.md](03_Phase02_ngd/PRD-0003-Phase2-WSOP-Integration.md) | DB 연동 계획 |
| [PRD-0003-Phase3-EBS-Automation.md](04_Phase03_ngd/PRD-0003-Phase3-EBS-Automation.md) | 자동화 계획 |

---

## 역할별 시작점

| 역할 | 시작 문서 | 목적 |
|------|----------|------|
| **경영/PM** | [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) | 프로젝트 비전/전략 |
| **구매** | [VENDOR-MANAGEMENT.md](05_Operations_ngd/VENDOR-MANAGEMENT.md) | 업체 관리 |
| **개발** | [PokerGFX-Feature-Checklist.md](01_PokerGFX_Analysis/PokerGFX-Feature-Checklist.md) | 복제 대상 기능 |
| **운영** | [PHASE-PROGRESSION.md](05_Operations_ngd/PHASE-PROGRESSION.md) | Phase 진행 현황 |

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
| 사용자 매뉴얼 | `01_PokerGFX_Analysis/03_Reference_ngd/user-manual_split/` | 기능/UI 분석 |
| 매뉴얼 이미지 | `01_PokerGFX_Analysis/03_Reference_ngd/user-manual_images/` | UI 참조 |
| 보안 문서 | `01_PokerGFX_Analysis/03_Reference_ngd/PokerGFX_Security.pdf` | 보안 구조 참조 |

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

**Version**: 10.0.0 | **Updated**: 2026-02-15 | **BRACELET STUDIO**
