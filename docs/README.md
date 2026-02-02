# EBS 문서 네비게이션

**Last Updated**: 2026-02-02
**Current Stage**: 🟡 **Stage-Pre** (진행 중)

---

## 🚨 현재 단계 (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         EBS 프로젝트 진행 단계                                │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│   │Stage-Pre│───▶│ Stage 0 │───▶│ Stage 1 │───▶│ Stage 2 │───▶│ Stage 3 │   │
│   │  기획   │    │  검증   │    │  복제   │    │  연동   │    │ 자동화  │   │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│       🟡             ⏳             ⏳             ⏳             ⏳          │
│      현재           대기           대기           대기           대기         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

⚠️ Stage-Pre가 Stage 0보다 먼저입니다!
⚠️ Stage-Pre 완료 전까지 Stage 0 작업을 시작하지 마세요!
```

---

## 빠른 시작

### 지금 무엇을 해야 하나요?

**현재 Stage-Pre 진행 중입니다.**

| 해야 할 일 | 문서 | 상태 |
|-----------|------|:----:|
| Slack Lists 칸반보드 생성 | [SLACK-LISTS-KANBAN.md](operations/SLACK-LISTS-KANBAN.md) | 📋 |
| 1순위 업체 견적 요청 | [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | 📋 |
| Stage 0 부품 발주 | [procurement/](procurement/) | 📋 |

**상세 현황**: [operations/EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md)

---

## 문서 구조 (Stage 순서)

> ⚠️ **반드시 숫자 순서대로 진행하세요!**

```
docs/
│
├── 📌 README.md ..................... 이 문서 (네비게이션)
├── 📌 PRD-0003-EBS-RFID-System.md ... Master PRD (전체 로드맵)
│
│
│   ══════════════════════════════════════════════════════════════
│   🟡 Stage-Pre: 기획 및 준비 (현재 진행 중)
│   ══════════════════════════════════════════════════════════════
│
├── 0-pre/  ◀◀◀ 현재 단계
│   ├── CONCEPT-EBS-Vision.md ........ EBS 비전 정의
│   ├── STRATEGY-*.md ................ 기술 전략
│   └── RFP-*.md ..................... 개발 제안서
│
├── operations/ ◀◀◀ 현재 작업 문서
│   ├── EBS-WORK-DASHBOARD.md ........ 📊 업무 대시보드
│   ├── STAGE-PROGRESSION.md ......... 📋 Stage 진행 가이드
│   ├── SLACK-LISTS-KANBAN.md ........ Slack 칸반보드 설정
│   ├── VENDOR-MANAGEMENT.md ......... 업체 관리
│   ├── MAIL-MANAGEMENT.md ........... 메일 관리
│   └── SLACK-MANAGEMENT.md .......... Slack 관리
│
│
│   ══════════════════════════════════════════════════════════════
│   ⏳ Stage 0: RFID 연결 검증 (대기)
│   ══════════════════════════════════════════════════════════════
│
├── 1-stage0/
│   ├── PRD-0003-Stage0-*.md ......... Stage 0 기획서
│   ├── DESIGN-RFID-Hardware.md ...... 하드웨어 설계
│   ├── GUIDE-*.md ................... 구현 가이드
│   └── BEGINNER-*.md ................ 초보자 가이드
│
│
│   ══════════════════════════════════════════════════════════════
│   ⏳ Stage 1: PokerGFX 복제 (대기)
│   ══════════════════════════════════════════════════════════════
│
├── 2-stage1/
│   ├── PRD-0003-Stage1-*.md ......... Stage 1 기획서
│   └── ARCHITECTURE-*.md ............ 소프트웨어 아키텍처
│
│
│   ══════════════════════════════════════════════════════════════
│   ⏳ Stage 2-3: 연동 및 자동화 (대기)
│   ══════════════════════════════════════════════════════════════
│
├── 3-stage2/
│   └── PRD-0003-Stage2-*.md ......... Stage 2 기획서
│
├── 4-stage3/
│   └── PRD-0003-Stage3-*.md ......... Stage 3 기획서
│
│
│   ══════════════════════════════════════════════════════════════
│   📁 공통 문서
│   ══════════════════════════════════════════════════════════════
│
├── procurement/ ..................... 구매/조달 문서
├── specs/ ........................... 기술 스펙
├── research/ ........................ 리서치 자료
├── design/ .......................... 설계 문서
├── decisions/ ....................... 의사결정 기록
└── archived/ ........................ 폐기 문서
```

---

## Stage별 상세

### 🟡 Stage-Pre: 기획 및 준비 (현재)

**목표**: 프로젝트 방향성 확립 + 관리 체계 구축

| 구분 | 문서 | 상태 |
|------|------|:----:|
| **비전** | [CONCEPT-EBS-Vision.md](0-pre/CONCEPT-EBS-Vision.md) | ✅ |
| **전략** | [STRATEGY-Lean-Production.md](0-pre/STRATEGY-Lean-Production.md) | ✅ |
| **제안서** | [RFP-EBS-Hardware-Development.md](0-pre/RFP-EBS-Hardware-Development.md) | ✅ |
| **업체 관리** | [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | ✅ |
| **칸반보드** | [SLACK-LISTS-KANBAN.md](operations/SLACK-LISTS-KANBAN.md) | 📋 |

**완료 조건**: [operations/STAGE-PROGRESSION.md](operations/STAGE-PROGRESSION.md)

---

### ⏳ Stage 0: RFID 연결 검증

**목표**: ESP32 + RFID 모듈로 카드 읽기 성공

| 구분 | 문서 | 비고 |
|------|------|------|
| **기획서** | [PRD-0003-Stage0-RFID-Connection.md](1-stage0/PRD-0003-Stage0-RFID-Connection.md) | |
| **하드웨어** | [DESIGN-RFID-Hardware.md](1-stage0/DESIGN-RFID-Hardware.md) | 배선도 포함 |
| **가이드** | [GUIDE-RFID-Implementation.md](1-stage0/GUIDE-RFID-Implementation.md) | |
| **초보자** | [BEGINNER-Hardware-Quickstart.md](1-stage0/BEGINNER-Hardware-Quickstart.md) | |

**시작 조건**: Stage-Pre 완료 + 부품 도착

---

### ⏳ Stage 1: PokerGFX 복제

**목표**: PokerGFX와 100% 동일한 기능

| 구분 | 문서 | 비고 |
|------|------|------|
| **기획서** | [PRD-0003-Stage1-PokerGFX-Clone.md](2-stage1/PRD-0003-Stage1-PokerGFX-Clone.md) | |
| **아키텍처** | [ARCHITECTURE-RFID-Software.md](2-stage1/ARCHITECTURE-RFID-Software.md) | 3-Layer |

**시작 조건**: Stage 0 Gate 통과

---

### ⏳ Stage 2-3: 연동 및 자동화

| Stage | 목표 | 기획서 |
|:-----:|------|--------|
| 2 | WSOP+ DB 연동 | [PRD-0003-Stage2-WSOP-Integration.md](3-stage2/PRD-0003-Stage2-WSOP-Integration.md) |
| 3 | 80% 자동화 | [PRD-0003-Stage3-EBS-Automation.md](4-stage3/PRD-0003-Stage3-EBS-Automation.md) |

---

## 역할별 시작점

| 역할 | 시작 문서 | 다음 문서 |
|------|----------|----------|
| **PM** | [EBS-WORK-DASHBOARD.md](operations/EBS-WORK-DASHBOARD.md) | [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md) |
| **하드웨어** | [BEGINNER-Hardware-Quickstart.md](1-stage0/BEGINNER-Hardware-Quickstart.md) | [DESIGN-RFID-Hardware.md](1-stage0/DESIGN-RFID-Hardware.md) |
| **소프트웨어** | [ARCHITECTURE-RFID-Software.md](2-stage1/ARCHITECTURE-RFID-Software.md) | - |
| **구매** | [VENDOR-MANAGEMENT.md](operations/VENDOR-MANAGEMENT.md) | [procurement/](procurement/) |

---

## 상태 아이콘

| 아이콘 | 의미 |
|:------:|------|
| 🟡 | 현재 진행 중 |
| ⏳ | 대기 (이전 단계 완료 필요) |
| ✅ | 완료 |
| 📋 | 작업 필요 |
| 🔴 | 긴급/차단됨 |

---

## 문서 변경 시 체크리스트

Stage 전환 시 반드시 업데이트:

- [ ] `CLAUDE.md` - Current Phase 변경
- [ ] `docs/README.md` (이 문서) - 현재 단계 표시
- [ ] `operations/EBS-WORK-DASHBOARD.md` - Current Stage
- [ ] `operations/STAGE-PROGRESSION.md` - 상태 이모지

---

**문서 버전**: 2.0.0
**마지막 업데이트**: 2026-02-02
