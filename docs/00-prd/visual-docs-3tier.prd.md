---
doc_type: "prd"
doc_id: "PRD-VD-001"
version: "1.0.0"
status: "draft"
owner: "BRACELET STUDIO"
last_updated: "2026-02-19"
phase: "phase-0.5"
priority: "high"
---

# PRD-VD-001: 3-Tier 시각적 문서화 시스템

## 1. 배경 및 목적

### 1.1 왜 필요한가

PokerGFX UI 역설계 분석은 현재 두 계층의 시각 자료를 제공한다.

- **Tier 1**: 원본 스크린샷 (`images/pokerGFX/`) — 맥락 파악용
- **Tier 2**: 번호 박스 오버레이 (`02_Annotated_ngd/`) — 요소 위치 식별용

그러나 **Tier 3이 없다.** 개별 UI 요소의 세부 설명을 읽을 때, 독자는 오버레이 전체 이미지에서 해당 박스를 눈으로 찾아야 한다. 화면당 20~30개 박스가 밀집되어 있어 참조 비용이 높다.

**3-tier 구조**로 크롭 이미지를 각 설명 항목에 인라인 삽입하면, 독자는 "맥락 → 위치 → 세부"를 단계적으로 이해할 수 있다.

### 1.2 목표

`generate_annotations.py`에 `--crop` 모드를 추가하고, `PokerGFX-UI-Analysis.md`를 3-tier 구조로 재편한다.

---

## 2. 요구사항

| ID | 요구사항 | 우선순위 |
|----|----------|---------|
| R1 | `generate_annotations.py`에 `--crop` 옵션 추가 | P0 |
| R2 | 각 박스 좌표 기준으로 패딩 포함 크롭 이미지 생성 | P0 |
| R3 | 크롭 이미지 출력 디렉토리 구조 정의 및 생성 | P0 |
| R4 | `PokerGFX-UI-Analysis.md`에 Tier 3 크롭 이미지 + 세부 설명 반영 | P1 |
| R5 | 크롭 이미지 파일명 규칙 정의 (`{screen-id}-crop-{box-number}.png`) | P0 |

### R1 상세: `--crop` 옵션

```
python generate_annotations.py --crop               # 전체 화면 크롭 생성
python generate_annotations.py --crop --target 02   # 단일 화면만 크롭
```

- 기존 `--calibrate`, `--debug`, `--ocr` 옵션과 독립적으로 동작
- `--crop` 단독 실행 시 기존 오버레이 이미지의 박스 좌표를 읽어 크롭만 수행

### R2 상세: 크롭 사양

| 항목 | 값 |
|------|-----|
| 패딩 | 상하좌우 8px |
| 포맷 | PNG |
| 해상도 | 원본 해상도 유지 (리사이즈 없음) |
| 박스 번호 표시 | 좌상단 레이블 오버레이 포함 (선택, `--label` 옵션) |

### R3 상세: 출력 디렉토리 구조

```
docs/01_PokerGFX_Analysis/03_Cropped_ngd/
├── 02-sources-tab/
│   ├── 02-crop-01.png
│   ├── 02-crop-02.png
│   └── ...
├── 03-outputs-tab/
│   ├── 03-crop-01.png
│   └── ...
└── {screen-id}-{screen-name}/
    └── {screen-id}-crop-{NN}.png
```

### R4 상세: `PokerGFX-UI-Analysis.md` 3-tier 구조

각 UI 요소 설명 섹션에 다음 순서로 배치:

```markdown
#### [N] 요소명

![Tier 1 - 원본](../../images/pokerGFX/{screen}.png)
![Tier 2 - 오버레이](../02_Annotated_ngd/{screen}-annotated.png)

| | |
|--|--|
| ![크롭](../03_Cropped_ngd/{screen-id}/{screen-id}-crop-{N:02d}.png) | **설명**: ... |
```

---

## 3. 기능 범위

**포함:**
- `generate_annotations.py` `--crop` 모드 구현
- `03_Cropped_ngd/` 디렉토리 자동 생성
- `PokerGFX-UI-Analysis.md` Tier 3 섹션 추가 (11개 화면)

**제외:**
- 기존 Tier 1/Tier 2 생성 로직 변경
- OCR 분석 재실행
- HTML mockup 변경

---

## 4. 비기능 요구사항

| 항목 | 기준 |
|------|------|
| 크롭 생성 속도 | 화면당 < 2초 |
| 파일 크기 | 크롭 1장 < 200KB |
| 멱등성 | 재실행 시 동일 결과 (덮어쓰기) |

---

## 5. 제약사항

- 좌표 소스: 기존 JSON sidecar (`{screen}-ocr.json`) 또는 하드코딩 박스 좌표 사용
- `pytesseract`, `Pillow` 의존성 — 기존 환경과 동일
- 크롭 대상: `02_Annotated_ngd/`에 이미 생성된 11개 화면만 적용 (21장 원본 중 주석 완성 화면)

---

## 6. 우선순위 및 실행 순서

```
Step 1: R1+R2+R3 — generate_annotations.py --crop 구현 및 검증
Step 2: R5       — 파일명 규칙 확정 후 일괄 생성
Step 3: R4       — UI-Analysis.md 3-tier 구조 재편 (11개 화면)
```

---

## 변경 이력

---
**Version**: 1.0.0 | **Updated**: 2026-02-19
