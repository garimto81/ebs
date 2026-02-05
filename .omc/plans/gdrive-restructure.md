# Work Plan: Google Drive EBS 폴더 재구조화

> **Plan ID**: gdrive-restructure
> **Created**: 2026-02-04
> **Status**: READY

---

## 1. Context

### 1.1 Original Request

Google Drive EBS 폴더 재구조화 및 문서 관리 전략 수립
- 현재: 6개 Google Docs가 flat 구조로 존재
- 목표: 로컬 `docs/` 폴더와 동일한 계층 구조로 정리

### 1.2 Current State

**변환 완료된 Google Docs (6개, flat 구조)**:

| 문서 | Google Docs ID |
|------|----------------|
| EBS 문서 (README) | `1SQ_cx83kGliBpFAxO9vDeltnc6EetwILFbuRGY8C384` |
| PRD-0003: EBS Event Broadcasting System | `17qt7bq4tvesEMub7Cfc-8QIIGUhkE6csqvmdOwskzIg` |
| Phase 0: 업체 선정 체크리스트 | `1WMkUC61Ls9_ftwlZVtmy7pxRewBWQVsw3DJaGgEbtJQ` |
| PRD-0004: EBS 업체 컨택 자동화 시스템 | `1K6huVaSnwxoxMI9UPx0MBT-cz_CEa4dIou0USwK0LWQ` |
| Phase 1: PokerGFX 100% 복제 | `1WmUxqvu18oVuVGWQSjLix54c-ye7mT17ZGRMM22rAio` |
| PokerGFX 기능 체크리스트 | `1qXdPbUNBEmHNQzPvYlGJA2jgujAEs2qtdANUyVjrR2I` |

### 1.3 Known Parameters (확정됨)

| 파라미터 | 값 | 설명 |
|----------|-----|------|
| EBS Root Folder ID | `1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF` | EBS 전용 폴더 |
| DEFAULT_FOLDER_ID | `1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW` | Google AI Studio 폴더 (문서 현재 위치) |

**현재 문서 위치**: 6개 EBS 문서가 `DEFAULT_FOLDER` (Google AI Studio)에 flat 구조로 존재. EBS 폴더가 아님.

**필요 작업**:
1. 문서를 EBS 폴더로 이동
2. EBS 폴더 내에 phase-0, phase-1 하위 폴더 생성
3. 문서를 적절한 하위 폴더로 정리

### 1.4 Research Findings

**사용 가능한 도구**:
- `C:\claude\lib\google_docs\drive_organizer.py` - Drive 파일 정리 모듈
  - `DriveOrganizer.create_folder()` - 폴더 생성 (중복 체크 포함)
  - `DriveOrganizer.move_file()` - 파일 이동 (ID 보존)
  - `DriveOrganizer.create_folder_structure()` - 계층 구조 생성
- `C:\claude\lib\google_docs\auth.py` - OAuth 인증
- OAuth 인증: `C:\claude\json\desktop_credentials.json`

---

## 2. Work Objectives

### 2.1 Core Objective

Google Drive의 EBS 문서를 로컬 `docs/` 구조와 동일하게 재구조화하여 문서 관리 일관성 확보

### 2.2 Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| D1 | **Google Drive 폴더 구조** | `EBS/phase-0/`, `EBS/phase-1/`, `EBS/operations/` 폴더 생성 |
| D2 | **문서 이동 완료** | 6개 문서를 적절한 폴더로 이동 (ID 보존) |
| D3 | **문서 매핑 테이블 업데이트** | `docs/GOOGLE-DRIVE-STRUCTURE.md`에 폴더 ID 추가 |
| D4 | **자동화 스크립트** | 향후 문서 추가 시 사용할 Python 스크립트 |

### 2.3 Definition of Done

- [ ] Google Drive에 phase-0, phase-1, operations 폴더 존재
- [ ] 모든 문서가 올바른 폴더에 위치
- [ ] 문서 URL이 변경 없이 접근 가능 (ID 보존 확인)
- [ ] `GOOGLE-DRIVE-STRUCTURE.md`에 폴더 ID 문서화
- [ ] 재사용 가능한 스크립트 작성 완료

---

## 3. Guardrails

### 3.1 Must Have

| # | Requirement |
|---|-------------|
| M1 | 문서 이동 시 ID/URL 보존 (Drive API `addParents`/`removeParents` 사용) |
| M2 | 모든 작업 전 dry-run으로 사전 검증 |
| M3 | 작업 로그 저장 (롤백 가능) |
| M4 | Google API Rate Limit 준수 (요청 간 0.5초 대기) |

### 3.2 Must NOT Have

| # | Constraint |
|---|------------|
| N1 | 문서 삭제 후 재생성 (ID 변경 발생) |
| N2 | API 키 방식 인증 (OAuth만 사용) |
| N3 | 수동 작업 (모든 작업 스크립트화) |

---

## 4. Task Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 1: 준비 (Tasks 1-2)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┴────────────────────┐
         │                                          │
    ┌────┴────┐                              ┌─────┴─────┐
    │ Task 1  │                              │  Task 2   │
    │ 현재    │                              │ 폴더 구조 │
    │ 상태    │                              │ 설계      │
    │ 분석    │                              │           │
    └────┬────┘                              └─────┬─────┘
         │                                          │
         └────────────────────┬────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 2: 구현 (Tasks 3-5)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    ┌────────┐          ┌────────┐          ┌────────┐
    │ Task 3 │          │ Task 4 │          │ Task 5 │
    │ 폴더   │ ──────▶  │ 문서   │ ──────▶  │ 검증   │
    │ 생성   │          │ 이동   │          │        │
    └────────┘          └────────┘          └────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Phase 3: 문서화 (Tasks 6-7)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                          ▼
    ┌────────┐                              ┌────────┐
    │ Task 6 │                              │ Task 7 │
    │ 문서   │                              │ 스크립트│
    │ 업데이트│                              │ 작성   │
    └────────┘                              └────────┘
```

---

## 5. Detailed TODOs

### Task 1: 현재 상태 분석

**목적**: Google Drive의 현재 EBS 폴더 상태 파악

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 1.1 | Drive API로 EBS 폴더 내 모든 파일/폴더 조회 | JSON 형식 파일 목록 출력 |
| 1.2 | 각 문서의 현재 parent folder ID 기록 | 6개 문서 모두 parent 확인 |
| 1.3 | 기존 폴더 존재 여부 확인 | phase-0, phase-1, operations 폴더 유무 |

**Files**:
- Input: `C:\claude\lib\google_docs\drive_organizer.py`
- Output: `.omc/logs/gdrive-current-state.json`

---

### Task 2: 폴더 구조 설계

**목적**: 생성할 폴더 구조와 문서 매핑 정의

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 2.1 | 로컬 `docs/` 구조와 매칭되는 폴더 구조 정의 | 폴더 트리 문서화 |
| 2.2 | 문서-폴더 매핑 테이블 작성 | 6개 문서의 대상 폴더 지정 |

**Target Structure**:
```
EBS/                                    (root - 기존)
├── README                              (root에 유지)
├── PRD-0003-EBS-RFID-System           (root에 유지)
├── phase-0/                            (신규 생성)
│   ├── VENDOR-SELECTION-CHECKLIST
│   └── PRD-0004-Vendor-Contact-Automation
├── phase-1/                            (신규 생성)
│   ├── PRD-0003-Phase1-PokerGFX-Clone
│   └── PokerGFX-Feature-Checklist
└── operations/                         (향후 사용)
```

**Document-Folder Mapping**:
| 문서 | 문서 ID | 현재 위치 | 대상 위치 | 이동 필요 |
|------|---------|----------|----------|----------|
| EBS 문서 (README) | `1SQ_cx83kGliBpFAxO9vDeltnc6EetwILFbuRGY8C384` | DEFAULT_FOLDER | EBS/ | Yes |
| PRD-0003 (Master PRD) | `17qt7bq4tvesEMub7Cfc-8QIIGUhkE6csqvmdOwskzIg` | DEFAULT_FOLDER | EBS/ | Yes |
| VENDOR-SELECTION-CHECKLIST | `1WMkUC61Ls9_ftwlZVtmy7pxRewBWQVsw3DJaGgEbtJQ` | DEFAULT_FOLDER | EBS/phase-0/ | Yes |
| PRD-0004 (Vendor Contact) | `1K6huVaSnwxoxMI9UPx0MBT-cz_CEa4dIou0USwK0LWQ` | DEFAULT_FOLDER | EBS/phase-0/ | Yes |
| Phase 1 PRD | `1WmUxqvu18oVuVGWQSjLix54c-ye7mT17ZGRMM22rAio` | DEFAULT_FOLDER | EBS/phase-1/ | Yes |
| PokerGFX Feature Checklist | `1qXdPbUNBEmHNQzPvYlGJA2jgujAEs2qtdANUyVjrR2I` | DEFAULT_FOLDER | EBS/phase-1/ | Yes |

**참고**: 현재 6개 문서 모두 DEFAULT_FOLDER(`1JwdlUe_v4Ug-yQ0veXTldFl6C24GH8hW`)에 있으므로 전체 이동 필요

---

### Task 3: 폴더 생성

**목적**: Google Drive에 폴더 계층 구조 생성

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 3.1 | EBS root 폴더 ID 확인 | ID 저장 |
| 3.2 | `phase-0` 폴더 생성 | 폴더 ID 반환 |
| 3.3 | `phase-1` 폴더 생성 | 폴더 ID 반환 |
| 3.4 | `operations` 폴더 생성 (향후용) | 폴더 ID 반환 |
| 3.5 | 생성된 폴더 ID 기록 | `.omc/logs/gdrive-folders.json` |

**Code Reference**:
```python
from lib.google_docs.auth import get_credentials
from googleapiclient.discovery import build

EBS_ROOT_ID = "1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF"  # 확정된 EBS 폴더 ID

creds = get_credentials()
drive = build('drive', 'v3', credentials=creds)

# 폴더 생성 함수
def create_folder(name, parent_id):
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = drive.files().create(body=metadata, fields='id').execute()
    return folder.get('id')

phase0_id = create_folder("phase-0", EBS_ROOT_ID)
phase1_id = create_folder("phase-1", EBS_ROOT_ID)
operations_id = create_folder("operations", EBS_ROOT_ID)
```

---

### Task 4: 문서 이동

**목적**: 6개 문서를 EBS 폴더 계층으로 이동

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 4.1 | Dry-run 실행 (이동 대상 확인) | 이동 계획 출력, 실제 이동 없음 |
| 4.2 | EBS 문서 (README) → EBS/ | 이동 성공, ID 유지 |
| 4.3 | PRD-0003 (Master PRD) → EBS/ | 이동 성공, ID 유지 |
| 4.4 | VENDOR-SELECTION-CHECKLIST → EBS/phase-0/ | 이동 성공, ID 유지 |
| 4.5 | PRD-0004 → EBS/phase-0/ | 이동 성공, ID 유지 |
| 4.6 | Phase 1 PRD → EBS/phase-1/ | 이동 성공, ID 유지 |
| 4.7 | Feature Checklist → EBS/phase-1/ | 이동 성공, ID 유지 |
| 4.8 | 각 이동 후 0.5초 대기 (Rate Limit) | API 에러 없음 |

**Code Reference**:
```python
# Drive API move (ID 보존)
def move_file(file_id: str, new_parent_id: str):
    file = drive.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents", []))

    drive.files().update(
        fileId=file_id,
        addParents=new_parent_id,
        removeParents=previous_parents,
        fields="id, parents"
    ).execute()
```

---

### Task 5: 검증

**목적**: 이동 완료 후 상태 검증

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 5.1 | 모든 문서 URL 접근 테스트 | 6개 URL 모두 정상 접근 |
| 5.2 | 폴더 구조 확인 | Drive API로 구조 조회, 예상과 일치 |
| 5.3 | 문서 parent 확인 | 4개 문서의 새 parent가 올바른 폴더 |

---

### Task 6: 문서 업데이트

**목적**: `docs/GOOGLE-DRIVE-STRUCTURE.md` 업데이트

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 6.1 | 폴더 ID 테이블 추가 | phase-0, phase-1, operations 폴더 ID 기록 |
| 6.2 | 문서 매핑 테이블 업데이트 | 새 URL/경로 반영 |
| 6.3 | 버전 업데이트 | 1.2.0으로 변경, 변경 이력 추가 |

**Files**:
- `C:\claude\ebs\docs\GOOGLE-DRIVE-STRUCTURE.md`

---

### Task 7: 자동화 스크립트 작성

**목적**: 향후 문서 추가 시 사용할 스크립트

| Step | Action | Acceptance Criteria |
|------|--------|---------------------|
| 7.1 | `tools/gdrive_organizer.py` 작성 | CLI 인터페이스 |
| 7.2 | 기능: 폴더 생성, 문서 이동, 상태 조회 | 3가지 subcommand |
| 7.3 | dry-run 옵션 | `--dry-run` 플래그 지원 |

**Files**:
- Output: `C:\claude\ebs\tools\gdrive_organizer.py`

---

## 6. Commit Strategy

| Commit # | Scope | Message |
|----------|-------|---------|
| 1 | Task 3 완료 | `feat(ebs): Google Drive 폴더 구조 생성 (phase-0, phase-1, operations)` |
| 2 | Task 4-5 완료 | `feat(ebs): Google Docs 문서 폴더별 이동 완료` |
| 3 | Task 6 완료 | `docs(ebs): GOOGLE-DRIVE-STRUCTURE.md 폴더 ID 추가` |
| 4 | Task 7 완료 | `feat(ebs): gdrive_organizer.py 자동화 스크립트 추가` |

---

## 7. Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| 문서 이동 시 권한 문제 | HIGH | 작업 전 권한 확인, 소유자 계정으로 실행 |
| API Rate Limit 초과 | MEDIUM | 요청 간 0.5초 대기, exponential backoff |
| 이동 중 네트워크 오류 | MEDIUM | 각 이동 후 상태 저장, 재시도 로직 |
| 잘못된 폴더로 이동 | HIGH | Dry-run 필수, 이동 전 확인 프롬프트 |

---

## 8. Success Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| S1 | 6개 문서가 올바른 폴더에 위치 | Drive API 조회로 parent 확인 |
| S2 | 모든 문서 URL 정상 작동 | Python requests.get() 또는 브라우저 접근 테스트 |
| S3 | 문서 ID 변경 없음 | 이동 전후 ID 비교 |
| S4 | `GOOGLE-DRIVE-STRUCTURE.md` 완전함 | 모든 폴더 ID, 문서 URL 포함 |
| S5 | 자동화 스크립트 작동 | `python tools/gdrive_organizer.py status` 성공 |

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-02-04 | 1.1.0 | Critic 피드백 반영: EBS Root ID 확정, 문서 위치 명확화, 6개 문서 전체 이동으로 수정 |
| 2026-02-04 | 1.0.0 | 초기 계획 작성 |

---

**Version**: 1.1.0 | **Updated**: 2026-02-04
