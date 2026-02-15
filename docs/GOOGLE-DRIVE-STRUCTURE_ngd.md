# EBS Google Drive 문서 구조

> **BRACELET STUDIO** | EBS (Event Broadcasting System)

## 개요

로컬 `docs/` 폴더와 동일한 구조로 Google Drive에 문서를 구성합니다.
로컬 `docs/` 폴더가 곧 Drive 구조이므로 별도의 미러 폴더 없이 직접 동기화합니다.

**_ngd suffix**: 파일명에 `_ngd` (no google drive) 접미사가 있는 파일은 Google Drive에 업로드하지 않습니다.

---

## 폴더 ID (확정)

> **정렬:** 폴더명 앞에 숫자 접두사를 추가하여 Google Drive에서 순서대로 표시됩니다.

| 폴더 | Google Drive ID | URL |
|------|-----------------|-----|
| **EBS/** (root) | `1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF` | [열기](https://drive.google.com/drive/folders/1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF) |
| **01_Phase00/** (로컬: 01_PokerGFX_Analysis) | `1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS` | [열기](https://drive.google.com/drive/folders/1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS) |
| **02_Phase01/** | `18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s` | [열기](https://drive.google.com/drive/folders/18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s) |
| **03_Phase02_ngd/** | `1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-` | [열기](https://drive.google.com/drive/folders/1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-) |
| **04_Phase03_ngd/** | `1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k` | [열기](https://drive.google.com/drive/folders/1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k) |
| **05_Operations_ngd/** | `1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-` | [열기](https://drive.google.com/drive/folders/1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-) |

---

## 폴더 구조

![EBS 문서 구조 다이어그램](90_Images_ngd/mockups/ebs-docs-structure-phase0-1.png)

```
EBS/                                         1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF
├── EBS 문서 (README)
├── PRD-0003: EBS Event Broadcasting System
│
├── 01_Phase00/                              1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS
│   │   (로컬: docs/01_PokerGFX_Analysis/)
│   └── Phase 0: 업체 선정 체크리스트
│
├── 02_Phase01/                              18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s
│   ├── Phase 1: PokerGFX 100% 복제
│   ├── PokerGFX 기능 체크리스트
│   ├── 01_Mockups_ngd/ (비공유)
│   ├── 02_Annotated_ngd/ (비공유)
│   └── 03_Reference_ngd/ (비공유)
│
├── 03_Phase02_ngd/                              1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-
│   └── (향후 DB 연동 문서)
│
├── 04_Phase03_ngd/                              1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k
│   └── (향후 자동화 문서)
│
└── 05_Operations_ngd/                           1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-
    ├── EBS 업무 대시보드
    ├── 업체 관리
    ├── Phase 진행 가이드
    ├── 01_DailyBriefings_ngd/ (비공유)
    └── 02_EmailDrafts_ngd/ (비공유)
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
| `docs/01_PokerGFX_Analysis/VENDOR-SELECTION-CHECKLIST.md` | [Phase 0: 업체 선정 체크리스트](https://docs.google.com/document/d/1n50iyuiU0TNBjUWDKFW1-88ALwZ1ClYXBuw2dW_qKOY/edit) | EBS/01_Phase00/ |

### Phase 1

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/02_Phase01/PRD-0003-Phase1-PokerGFX-Clone.md` | [Phase 1: PokerGFX 100% 복제](https://docs.google.com/document/d/1WmUxqvu18oVuVGWQSjLix54c-ye7mT17ZGRMM22rAio/edit) | EBS/02_Phase01/ |
| `docs/02_Phase01/PokerGFX-Feature-Checklist.md` | [PokerGFX 기능 체크리스트](https://docs.google.com/document/d/1qXdPbUNBEmHNQzPvYlGJA2jgujAEs2qtdANUyVjrR2I/edit) | EBS/02_Phase01/ |

### Operations

| 로컬 파일 | Google Docs | 폴더 |
|----------|-------------|------|
| `docs/05_Operations_ngd/EBS-WORK-DASHBOARD.md` | [EBS 업무 대시보드](https://docs.google.com/document/d/1eHvgCWm5BxXut5iDyOQFzaIawmFAkFAJ1v2FRbIsbN4/edit) | EBS/05_Operations_ngd/ |
| `docs/05_Operations_ngd/VENDOR-MANAGEMENT.md` | [업체 관리](https://docs.google.com/document/d/125VWBAHqkgm6Fx6oTLVa-M2hz48gTGAjAtmU_ci3-aw/edit) | EBS/05_Operations_ngd/ |
| `docs/05_Operations_ngd/PHASE-PROGRESSION.md` | [Phase 진행 가이드](https://docs.google.com/document/d/1d5kOEWgapVOkoo9LQol8MLSH0cPDVMu9HhUy98ZZhP0/edit) | EBS/05_Operations_ngd/ |

---

## Drive 공유 대상

### 공유 대상 (Google Docs로 변환)

| 파일 | Drive 폴더 |
|------|-----------|
| `docs/README.md` | EBS/ |
| `docs/PRD-0003-EBS-RFID-System.md` | EBS/ |
| `docs/01_PokerGFX_Analysis/*.md` (_ngd 하위폴더 제외) | EBS/01_Phase00/ |
| `docs/02_Phase01/*.md` (_ngd 제외, 하위 폴더 제외) | EBS/02_Phase01/ |

### 비공유 (_ngd 폴더/파일)

| 파일 | 제외 사유 |
|------|----------|
| `docs/03_Phase02_ngd/` | Phase 2 전체 (_ngd) |
| `docs/04_Phase03_ngd/` | Phase 3 전체 (_ngd) |
| `docs/05_Operations_ngd/` | Operations 전체 (_ngd) |
| `docs/02_Phase01/01_Mockups_ngd/` | HTML 목업 (_ngd) |
| `docs/02_Phase01/02_Annotated_ngd/` | 주석 이미지 (_ngd) |
| `docs/02_Phase01/03_Reference_ngd/` | PDF, 이미지 바이너리 (_ngd) |
| `docs/90_Images_ngd/`, `docs/91_Mockups_ngd/` | 빌드 산출물 (_ngd) |
| `docs/GOOGLE-DRIVE-STRUCTURE_ngd.md` | 메타 문서 (_ngd) |
| `docs/MAPPING_ngd.json` | 매핑 설정 (_ngd) |

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
| **PDF = 원본 유지** | 03_Reference_ngd 폴더는 파일 업로드 |
| **MAPPING_ngd.json** | `docs/MAPPING_ngd.json`에서 파일별 doc_id 관리 |
| **_ngd 접미사** | `_ngd` 접미사가 있는 파일/폴더는 Google Drive 비공유 |

### 동기화 흐름

```
docs/ (git 마스터)  →  Google Drive (공유)
   원본 편집                팀 리뷰/협업
   버전 관리                코멘트
   MAPPING_ngd.json 참조    doc_id로 연결
   _ngd 파일은 제외         비공유 자료
```

### 새 문서 추가 시

1. **로컬에서 Markdown 작성** -> `docs/NN_PhaseNN/문서명.md`
2. **Google Docs 변환** -> `python -m lib.google_docs convert "경로"`
3. **MAPPING_ngd.json 업데이트** -> doc_id 기록
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

- [x] `01_Phase00/` 폴더 생성 (로컬: 01_PokerGFX_Analysis)
- [x] `VENDOR-SELECTION-CHECKLIST` 문서 생성 및 이동
- [x] `PRD-0004-Vendor-Contact-Automation` 문서 생성 및 이동

### Phase 1 문서

- [x] `02_Phase01/` 폴더 생성
- [x] `PRD-0003-Phase1-PokerGFX-Clone` 문서 생성 및 이동
- [x] `PokerGFX-Feature-Checklist` 문서 생성 및 이동
- [ ] `03_Reference_ngd/` PDF 파일 업로드 (수동)

### Phase 2/3 문서

- [x] `03_Phase02_ngd/` 폴더 생성
- [x] `04_Phase03_ngd/` 폴더 생성
- [ ] PRD 문서 변환 (Phase 착수 시)

### Operations 문서

- [x] `05_Operations_ngd/` 폴더 생성
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
| `EBS/02_Phase01/03_Reference_ngd/` | 읽기 전용 (참조용) |

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| **2026-02-10** | **7.0.0** | **로컬 01_Phase00→01_PokerGFX_Analysis 리네임, PokerGFX 파일 01_PokerGFX_Analysis로 이동, PRD-0004 05_Operations_ngd로 이동, local_to_drive_folder 매핑 도입** |
| 2026-02-10 | 6.0.0 | 새 디렉토리 명명 규칙 적용: 1-phase-0/ → 01_Phase00/, _ngd 접미사 도입 (비공유 파일/폴더 표시) |
| 2026-02-05 | 5.0.0 | gdrive/ 미러 폴더 제거, docs/ 직접 동기화로 전환, 로컬 경로를 숫자 접두사로 통일, Drive 공유 대상 정의 추가 |
| 2026-02-05 | 4.0.0 | gdrive/ 미러 폴더 도입 |
| 2026-02-04 | 3.2.0 | 업체 선정 체크리스트 업데이트 |
| 2026-02-04 | 3.1.0 | 폴더명에 숫자 접두사 추가하여 순서 정렬 |
| 2026-02-04 | 3.0.0 | Phase 2/3 폴더 생성, Operations 문서 3개 추가, 동기화 전략 개선 |
| 2026-02-04 | 2.0.0 | Google Drive 폴더 재구조화 완료, 폴더 ID 추가, 전략 문서화 |
| 2026-02-04 | 1.1.0 | Phase 0/1 문서 Google Docs 변환 완료 |
| 2026-02-04 | 1.0.0 | 초기 구조 설계 |

---

**Version**: 7.0.0 | **Updated**: 2026-02-10 | **BRACELET STUDIO**
