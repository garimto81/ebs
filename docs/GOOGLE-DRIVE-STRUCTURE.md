# EBS Google Drive 문서 구조

> **BRACELET STUDIO** | EBS (Event Broadcasting System)

## 개요

로컬 `docs/` 폴더와 동일한 구조로 Google Drive에 문서를 구성합니다.
로컬 `docs/` 폴더가 곧 Drive 구조이므로 별도의 미러 폴더 없이 직접 동기화합니다.

---

## 폴더 ID (확정)

> **정렬:** 폴더명 앞에 숫자 접두사를 추가하여 Google Drive에서 순서대로 표시됩니다.

| 폴더 | Google Drive ID | URL |
|------|-----------------|-----|
| **EBS/** (root) | `1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF` | [열기](https://drive.google.com/drive/folders/1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF) |
| **1-phase-0/** | `1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS` | [열기](https://drive.google.com/drive/folders/1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS) |
| **2-phase-1/** | `18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s` | [열기](https://drive.google.com/drive/folders/18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s) |
| **3-phase-2/** | `1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-` | [열기](https://drive.google.com/drive/folders/1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-) |
| **4-phase-3/** | `1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k` | [열기](https://drive.google.com/drive/folders/1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k) |
| **5-operations/** | `1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-` | [열기](https://drive.google.com/drive/folders/1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-) |

---

## 폴더 구조

![EBS 문서 구조 다이어그램](images/mockups/ebs-docs-structure-phase0-1.png)

```
EBS/                                         1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF
├── EBS 문서 (README)
├── PRD-0003: EBS Event Broadcasting System
│
├── 1-phase-0/                               1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS
│   ├── Phase 0: 업체 선정 체크리스트
│   └── PRD-0004: EBS 업체 컨택 자동화 시스템
│
├── 2-phase-1/                               18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s
│   ├── Phase 1: PokerGFX 100% 복제
│   └── PokerGFX 기능 체크리스트
│
├── 3-phase-2/                               1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-
│   └── (향후 DB 연동 문서)
│
├── 4-phase-3/                               1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k
│   └── (향후 자동화 문서)
│
└── 5-operations/                            1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-
    ├── EBS 업무 대시보드
    ├── 업체 관리
    └── Phase 진행 가이드
```

---

## 문서 매핑

### EBS Root

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/README.md` | [EBS 문서](https://docs.google.com/document/d/1SQ_cx83kGliBpFAxO9vDeltnc6EetwILFbuRGY8C384/edit) | EBS/ |
| `docs/PRD-0003-EBS-RFID-System.md` | [PRD-0003: EBS Event Broadcasting System](https://docs.google.com/document/d/17qt7bq4tvesEMub7Cfc-8QIIGUhkE6csqvmdOwskzIg/edit) | EBS/ |

### Phase 0

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/1-phase-0/VENDOR-SELECTION-CHECKLIST.md` | [Phase 0: 업체 선정 체크리스트](https://docs.google.com/document/d/1n50iyuiU0TNBjUWDKFW1-88ALwZ1ClYXBuw2dW_qKOY/edit) | EBS/1-phase-0/ |
| `docs/1-phase-0/PRD-0004-Vendor-Contact-Automation.md` | [PRD-0004: EBS 업체 컨택 자동화 시스템](https://docs.google.com/document/d/1K6huVaSnwxoxMI9UPx0MBT-cz_CEa4dIou0USwK0LWQ/edit) | EBS/1-phase-0/ |

### Phase 1

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/2-phase-1/PRD-0003-Phase1-PokerGFX-Clone.md` | [Phase 1: PokerGFX 100% 복제](https://docs.google.com/document/d/1WmUxqvu18oVuVGWQSjLix54c-ye7mT17ZGRMM22rAio/edit) | EBS/2-phase-1/ |
| `docs/2-phase-1/PokerGFX-Feature-Checklist.md` | [PokerGFX 기능 체크리스트](https://docs.google.com/document/d/1qXdPbUNBEmHNQzPvYlGJA2jgujAEs2qtdANUyVjrR2I/edit) | EBS/2-phase-1/ |

### Operations

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/5-operations/EBS-WORK-DASHBOARD.md` | [EBS 업무 대시보드](https://docs.google.com/document/d/1eHvgCWm5BxXut5iDyOQFzaIawmFAkFAJ1v2FRbIsbN4/edit) | EBS/5-operations/ |
| `docs/5-operations/VENDOR-MANAGEMENT.md` | [업체 관리](https://docs.google.com/document/d/125VWBAHqkgm6Fx6oTLVa-M2hz48gTGAjAtmU_ci3-aw/edit) | EBS/5-operations/ |
| `docs/5-operations/PHASE-PROGRESSION.md` | [Phase 진행 가이드](https://docs.google.com/document/d/1d5kOEWgapVOkoo9LQol8MLSH0cPDVMu9HhUy98ZZhP0/edit) | EBS/5-operations/ |

---

## Drive 공유 대상

### 공유 대상 (Google Docs로 변환)

| 파일 | Drive 폴더 |
|------|-----------|
| `docs/README.md` | EBS/ |
| `docs/PRD-0003-EBS-RFID-System.md` | EBS/ |
| `docs/1-phase-0/*.md` | EBS/1-phase-0/ |
| `docs/2-phase-1/*.md` (reference/ 제외) | EBS/2-phase-1/ |
| `docs/3-phase-2/*.md` | EBS/3-phase-2/ |
| `docs/4-phase-3/*.md` | EBS/4-phase-3/ |
| `docs/5-operations/EBS-WORK-DASHBOARD.md` | EBS/5-operations/ |
| `docs/5-operations/VENDOR-MANAGEMENT.md` | EBS/5-operations/ |
| `docs/5-operations/PHASE-PROGRESSION.md` | EBS/5-operations/ |

### 비공유 (로컬/보안)

| 파일 | 제외 사유 |
|------|----------|
| `docs/5-operations/COMMUNICATION-RULES.md` | 보안 규칙 |
| `docs/5-operations/daily-briefings/` | 일일 운영 데이터 |
| `docs/5-operations/email-drafts/` | 컨택 이메일 |
| `docs/2-phase-1/reference/` | PDF, 이미지 바이너리 |
| `docs/mockups/`, `docs/images/` | 빌드 산출물 |
| `docs/GOOGLE-DRIVE-STRUCTURE.md` | 메타 문서 |
| `docs/MAPPING.json` | 매핑 설정 |

---

## 문서 관리 전략

### 동기화 전략: Dual Master with Sync Point

```
┌─────────────────────────────────────────────────────────────────┐
│  WRITING PHASE         REVIEW PHASE            FINAL           │
│  (로컬 Markdown)       (Google Docs)           (동기화)         │
│                                                                 │
│  ┌──────────┐  변환   ┌──────────┐  확정   ┌──────────┐        │
│  │  Local   │ ─────▶ │  Google  │ ─────▶ │  Both    │        │
│  │ Markdown │        │   Docs   │        │  Synced  │        │
│  └──────────┘        └──────────┘        └──────────┘        │
│       │                   │                                    │
│       │ git commit        │ 팀 리뷰/코멘트                      │
│       ▼                   ▼                                    │
│  Version Control     Collaboration                             │
└─────────────────────────────────────────────────────────────────┘
```

| Phase | Master | 용도 |
|-------|--------|------|
| 초안 작성 | 로컬 Markdown | 버전 관리, 코드 리뷰 |
| 팀 리뷰 | Google Docs | 코멘트, 협업 |
| 확정 후 | 양쪽 동기화 | 최종본 유지 |

### 동기화 규칙

| 규칙 | 설명 |
|------|------|
| **Dual Master** | 로컬(버전관리) + Google Docs(협업) |
| **변환 도구** | `python -m lib.google_docs convert` |
| **동기화** | `/prd-sync`로 Google Docs -> 로컬 |
| **PDF = 원본 유지** | reference 폴더는 파일 업로드 |
| **MAPPING.json** | `docs/MAPPING.json`에서 파일별 doc_id 관리 |

### 동기화 흐름

```
docs/ (git 마스터)  →  Google Drive (공유)
   원본 편집             팀 리뷰/협업
   버전 관리             코멘트
   MAPPING.json 참조     doc_id로 연결
```

### 새 문서 추가 시

1. **로컬에서 Markdown 작성** -> `docs/N-phase-N/문서명.md`
2. **Google Docs 변환** -> `python -m lib.google_docs convert "경로"`
3. **MAPPING.json 업데이트** -> doc_id 기록
4. **이 문서 업데이트** -> 문서 매핑 테이블에 추가

---

## 자동화 도구

### gdrive_organizer.py

```powershell
# 현재 상태 확인
python tools/gdrive_organizer.py status

# 문서 목록 및 URL
python tools/gdrive_organizer.py list-docs

# 폴더 생성
python tools/gdrive_organizer.py create-folder phase-2 --parent root

# 파일 이동
python tools/gdrive_organizer.py move <FILE_ID> phase-1

# 미리보기 (실행 안함)
python tools/gdrive_organizer.py --dry-run move <FILE_ID> phase-1
```

---

## 생성 체크리스트

### Phase 0 문서

- [x] `1-phase-0/` 폴더 생성
- [x] `VENDOR-SELECTION-CHECKLIST` 문서 생성 및 이동
- [x] `PRD-0004-Vendor-Contact-Automation` 문서 생성 및 이동

### Phase 1 문서

- [x] `2-phase-1/` 폴더 생성
- [x] `PRD-0003-Phase1-PokerGFX-Clone` 문서 생성 및 이동
- [x] `PokerGFX-Feature-Checklist` 문서 생성 및 이동
- [ ] `reference/` PDF 파일 업로드 (수동)

### Phase 2/3 문서

- [x] `3-phase-2/` 폴더 생성
- [x] `4-phase-3/` 폴더 생성
- [ ] PRD 문서 변환 (Phase 착수 시)

### Operations 문서

- [x] `5-operations/` 폴더 생성
- [x] `EBS-WORK-DASHBOARD` 문서 생성 및 이동
- [x] `VENDOR-MANAGEMENT` 문서 생성 및 이동
- [x] `PHASE-PROGRESSION` 문서 생성 및 이동

### 공통 문서

- [x] EBS root 폴더 확인
- [x] `README` 문서 생성 및 이동
- [x] `PRD-0003-EBS-RFID-System` 문서 생성 및 이동

---

## 접근 권한

| 폴더 | 권한 |
|------|------|
| `EBS/` | 팀 전체 편집 |
| `EBS/2-phase-1/reference/` | 읽기 전용 (참조용) |

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| **2026-02-05** | **5.0.0** | **gdrive/ 미러 폴더 제거, docs/ 직접 동기화로 전환, 로컬 경로를 숫자 접두사로 통일, Drive 공유 대상 정의 추가** |
| 2026-02-05 | 4.0.0 | gdrive/ 미러 폴더 도입 |
| 2026-02-04 | 3.2.0 | 업체 선정 체크리스트 업데이트 |
| 2026-02-04 | 3.1.0 | 폴더명에 숫자 접두사 추가하여 순서 정렬 |
| 2026-02-04 | 3.0.0 | Phase 2/3 폴더 생성, Operations 문서 3개 추가, 동기화 전략 개선 |
| 2026-02-04 | 2.0.0 | Google Drive 폴더 재구조화 완료, 폴더 ID 추가, 전략 문서화 |
| 2026-02-04 | 1.1.0 | Phase 0/1 문서 Google Docs 변환 완료 |
| 2026-02-04 | 1.0.0 | 초기 구조 설계 |

---

**Version**: 5.0.0 | **Updated**: 2026-02-05 | **BRACELET STUDIO**
