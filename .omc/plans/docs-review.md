# 문서 구조 및 내용 전면 재점검 계획

**Plan ID**: docs-review
**Created**: 2026-02-04
**Status**: Draft

---

## 1. 현황 분석 결과

### 1.1 발견된 문제점

| # | 문제 유형 | 위치 | 상세 |
|:-:|----------|------|------|
| 1 | **README.md 구조 불일치** | `docs/README.md` | phase-0에 PRD-0004 문서 누락, CONCEPT-EBS-Vision.md 참조는 있으나 파일 미존재 |
| 2 | **끊어진 링크** | `docs/PRD-0003-EBS-RFID-System.md:66,106,328` | `CONCEPT-EBS-Vision.md` 참조하지만 해당 파일 없음 |
| 3 | **Phase 번호 불일치** | `docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md` | 제목은 "Phase 0"이라고 하면서 파일은 phase-1 폴더에 있음 |
| 4 | **Phase 번호 불일치** | `docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md` | 제목은 "Phase 1"이라고 되어 있음 |
| 5 | **Phase 번호 불일치** | `docs/phase-3/PRD-0003-Phase3-EBS-Automation.md` | 제목은 "Phase 2"라고 되어 있음 |
| 6 | **중복 변경 이력** | `docs/PRD-0003-EBS-RFID-System.md` | 변경 이력이 최하단에 있지만 버전 정보 없음 (푸터 누락) |
| 7 | **Stage→Phase 용어 불일치** | `docs/operations/EBS-WORK-DASHBOARD.md:31,57` | "Stage 0"이라는 구용어 사용 |
| 8 | **부록 링크 오류** | `docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md:488-490` | BEGINNER-Hardware-Quickstart.md 파일 미존재, Phase 진행 가이드 링크 오류 |
| 9 | **부록 링크 오류** | `docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md:535-537` | 잘못된 파일명 참조 (Phase0→Phase1, Phase2→Phase3) |
| 10 | **부록 링크 오류** | `docs/phase-3/PRD-0003-Phase3-EBS-Automation.md:676-678` | 잘못된 파일명 참조 |
| 11 | **YAML frontmatter 중복** | `docs/PRD-0003-EBS-RFID-System.md:9-10` | `phase` 키가 2번 정의됨 |
| 12 | **변경 이력 미배치** | `docs/phase-0/PRD-0004-Vendor-Contact-Automation.md` | 변경 이력 섹션 없음 |
| 13 | **기능 개수 불일치** | 체크리스트 vs PRD | 체크리스트는 119개, PRD는 54개라고 표기 |

### 1.2 문서별 상태

| 문서 | 변경이력 위치 | 푸터 | Phase 번호 | 링크 상태 |
|------|:------------:|:----:|:----------:|:---------:|
| README.md | 해당없음 | ✅ | ✅ | ⚠️ 일부 누락 |
| PRD-0003-EBS-RFID-System.md | ✅ 최하단 | ❌ 없음 | ✅ | ❌ 끊어진 링크 |
| VENDOR-SELECTION-CHECKLIST.md | 해당없음 | ✅ | ✅ | ✅ |
| PRD-0004-Vendor-Contact-Automation.md | ❌ 없음 | ✅ 상단 | - | ✅ |
| PRD-0003-Phase1-PokerGFX-Clone.md | 해당없음 | ✅ | ❌ Phase 0 | ❌ 끊어진 링크 |
| PokerGFX-Feature-Checklist.md | 해당없음 | ✅ | - | ✅ |
| PRD-0003-Phase2-WSOP-Integration.md | 해당없음 | ✅ | ❌ Phase 1 | ❌ 끊어진 링크 |
| PRD-0003-Phase3-EBS-Automation.md | 해당없음 | ✅ | ❌ Phase 2 | ❌ 끊어진 링크 |
| EBS-WORK-DASHBOARD.md | 해당없음 | 해당없음 | ⚠️ Stage 혼용 | ✅ |
| VENDOR-MANAGEMENT.md | ✅ 최하단 | ✅ | ✅ | ✅ |
| PHASE-PROGRESSION.md | ✅ 최하단 | ✅ | ✅ | ⚠️ CONCEPT 링크 |

---

## 2. 수정 계획

### 2.1 우선순위 P0 (Critical)

| # | 파일 | 수정 내용 |
|:-:|------|----------|
| 1 | `docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md` | 제목 "Phase 0" → "Phase 1" 수정 |
| 2 | `docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md` | 제목 "Phase 1" → "Phase 2" 수정 |
| 3 | `docs/phase-3/PRD-0003-Phase3-EBS-Automation.md` | 제목 "Phase 2" → "Phase 3" 수정 |
| 4 | `docs/PRD-0003-EBS-RFID-System.md` | YAML frontmatter 중복 `phase` 키 제거 |

### 2.2 우선순위 P1 (High)

| # | 파일 | 수정 내용 |
|:-:|------|----------|
| 5 | `docs/PRD-0003-EBS-RFID-System.md` | 끊어진 CONCEPT-EBS-Vision.md 링크 제거 또는 수정 |
| 6 | `docs/README.md` | phase-0에 PRD-0004 문서 추가 |
| 7 | `docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md` | 부록 링크 수정 (BEGINNER-Hardware-Quickstart.md 제거) |
| 8 | `docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md` | 부록 링크 수정 |
| 9 | `docs/phase-3/PRD-0003-Phase3-EBS-Automation.md` | 부록 링크 수정 |
| 10 | `docs/operations/EBS-WORK-DASHBOARD.md` | "Stage 0" → "Phase 0" 용어 통일 |

### 2.3 우선순위 P2 (Medium)

| # | 파일 | 수정 내용 |
|:-:|------|----------|
| 11 | `docs/PRD-0003-EBS-RFID-System.md` | 푸터 추가 (Version/Updated) |
| 12 | `docs/phase-0/PRD-0004-Vendor-Contact-Automation.md` | 버전 정보를 상단에서 하단으로 이동, 변경 이력 섹션 추가 |
| 13 | `docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md` | 기능 개수 표기 통일 (54개 → 119개 또는 설명 추가) |
| 14 | `docs/operations/PHASE-PROGRESSION.md` | CONCEPT-EBS-Vision.md 링크 수정 |

---

## 3. 수정 상세

### 3.1 Phase 번호 수정 (P0)

**docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md**
```diff
- # Phase 0: PokerGFX 100% 복제
+ # Phase 1: PokerGFX 100% 복제

- ## 1. Phase 0 개요
+ ## 1. Phase 1 개요

- Phase 0은 기존 PokerGFX 시스템을 완벽하게 복제하는 단계입니다.
+ Phase 1은 기존 PokerGFX 시스템을 완벽하게 복제하는 단계입니다.

- ## 9. Phase 0 완료 조건 (Gate)
+ ## 9. Phase 1 완료 조건 (Gate)
```

**docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md**
```diff
- # Phase 1: WSOPLIVE DB 연동
+ # Phase 2: WSOPLIVE DB 연동

- ## 1. Phase 1 개요
+ ## 1. Phase 2 개요
```

**docs/phase-3/PRD-0003-Phase3-EBS-Automation.md**
```diff
- # Phase 2: 자동화 프로토콜
+ # Phase 3: 자동화 프로토콜

- ## 1. Phase 2 개요
+ ## 1. Phase 3 개요

- ## 11. Phase 2 완료 조건 (프로젝트 완료)
+ ## 11. Phase 3 완료 조건 (프로젝트 완료)
```

### 3.2 끊어진 링크 수정 (P1)

**docs/PRD-0003-EBS-RFID-System.md**
- Line 66: `[CONCEPT-EBS-Vision.md](phase-0/CONCEPT-EBS-Vision.md)` 삭제
- Line 106-107: CONCEPT-EBS-Vision.md 링크 삭제
- Line 328: CONCEPT-EBS-Vision.md 링크 삭제

**docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md**
- Line 489: `[BEGINNER Hardware Quickstart](BEGINNER-Hardware-Quickstart.md)` 삭제

**docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md**
```diff
- - [Phase 0 PRD](../phase-0/PRD-0003-Phase0-PokerGFX-Clone.md)
- - [Phase 2 PRD](../phase-2/PRD-0003-Phase2-EBS-Automation.md)
+ - [Phase 1 PRD](../phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)
+ - [Phase 3 PRD](../phase-3/PRD-0003-Phase3-EBS-Automation.md)
```

**docs/phase-3/PRD-0003-Phase3-EBS-Automation.md**
```diff
- - [Phase 0 PRD](../phase-0/PRD-0003-Phase0-PokerGFX-Clone.md)
- - [Phase 1 PRD](../phase-1/PRD-0003-Phase1-WSOP-Integration.md)
+ - [Phase 1 PRD](../phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)
+ - [Phase 2 PRD](../phase-2/PRD-0003-Phase2-WSOP-Integration.md)
```

### 3.3 README.md 업데이트 (P1)

```diff
### Phase 0: 업체 선정

| 문서 | 설명 |
|------|------|
| [VENDOR-SELECTION-CHECKLIST.md](phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 기준, 후보, 체크리스트 |
+ | [PRD-0004-Vendor-Contact-Automation.md](phase-0/PRD-0004-Vendor-Contact-Automation.md) | 업체 컨택 자동화 시스템 |
```

### 3.4 용어 통일 (P1)

**docs/operations/EBS-WORK-DASHBOARD.md**
```diff
- **1순위 업체**: JLCPCB (Stage 0 프로토타입)
+ **1순위 업체**: JLCPCB (Phase 0 프로토타입)

- ## 예상 비용 (Stage 0)
+ ## 예상 비용 (Phase 0)
```

### 3.5 YAML frontmatter 수정 (P0)

**docs/PRD-0003-EBS-RFID-System.md**
```diff
  phase: "master"
- phase: "planning"
```

---

## 4. 검증 체크리스트

수정 후 확인 사항:

- [ ] 모든 Phase 번호가 폴더명과 일치
- [ ] 끊어진 링크 0개
- [ ] 변경 이력이 모든 PRD 문서 최하단에 위치
- [ ] Stage 용어 0개 (Phase로 통일)
- [ ] README.md가 실제 파일 구조와 일치
- [ ] YAML frontmatter 중복 키 없음

---

## 5. 예상 작업량

| 우선순위 | 파일 수 | 예상 수정 |
|:--------:|:------:|----------|
| P0 | 4 | 제목/용어 치환 |
| P1 | 6 | 링크 수정/추가 |
| P2 | 4 | 구조 정리 |
| **합계** | **14** | |

---

## 6. 실행 순서

1. P0 수정 (Critical) - Phase 번호 불일치 해결
2. P1 수정 (High) - 끊어진 링크 수정
3. P2 수정 (Medium) - 구조 정리
4. 최종 검증 - 모든 체크리스트 확인

---

**Plan Status**: PLAN_READY
**Plan Path**: .omc/plans/docs-review.md
