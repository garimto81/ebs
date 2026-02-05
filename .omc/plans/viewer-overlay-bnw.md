# Work Plan: Viewer Overlay B&W Wireframe Redesign

**Plan ID**: `viewer-overlay-bnw`
**Created**: 2026-01-27
**Status**: READY

---

## Context

### Original Request
Viewer Overlay 목업을 `--mockup --bnw` 표준에 맞게 흑백 와이어프레임으로 재설계

### Current State Analysis
- **File**: `C:\claude\ebs\docs\mockups\01-viewer-overlay.html`
- **Layout**: PokerGFX 스타일 (좌측 하단 HUD, 우측 하단 3-Grid, 상단 바) - **유지**
- **Problems Identified**:
  1. 녹색 테이블 배경 (`#1a3d1a`, `#0d2a0d`, `#1e5f1e`, `#145214`)
  2. 테이블 펠트 갈색 테두리 (`#5c3d2e`)
  3. 빨간색 액센트 (`#c00`) - Blinds 테두리, Active 플레이어, POT 배경
  4. 빨간색 카드 수트 (`.suit.red { color: #c00 }`)
  5. 파란색 카드 뒷면 패턴 (`#1a237e`, `#283593`, `#0d1b5e`)

---

## Work Objectives

### Core Objective
모든 컬러 요소를 흑백/회색조로 변환하여 와이어프레임 표준 준수

### Deliverables
1. 수정된 HTML 파일 (`01-viewer-overlay.html`)
2. 스크린샷 (`docs/images/mockups/01-viewer-overlay.png`)

### Definition of Done
- [ ] 녹색 테이블 배경 제거 (투명/연회색 대체)
- [ ] 모든 `#c00` (빨강) → `#333` 또는 `#666` (회색)
- [ ] 빨간 수트 → 회색 (`#666`)
- [ ] 카드 뒷면 → 회색 패턴
- [ ] 레이아웃 변경 없음 (PokerGFX 스타일 유지)
- [ ] 스크린샷 캡처 완료

---

## Must Have / Must NOT Have

### Must Have (Guardrails)
| Requirement | Reason |
|-------------|--------|
| 흑백/회색조 팔레트만 사용 | B&W 와이어프레임 표준 |
| 기존 레이아웃 100% 유지 | PokerGFX 스타일 승인됨 |
| 카드 가독성 유지 | 수트 구분 가능해야 함 |
| 960x540 해상도 유지 | 오버레이 표준 크기 |

### Must NOT Have
| Forbidden | Reason |
|-----------|--------|
| 녹색 (#1a3d1a, #1e5f1e 등) | 테이블 펠트 시각화 불필요 |
| 빨강 (#c00, #ff0000) | B&W 표준 위반 |
| 파랑 (#1a237e 등) | B&W 표준 위반 |
| 갈색 (#5c3d2e) | B&W 표준 위반 |
| 레이아웃 위치 변경 | 승인된 구조 유지 |

---

## Color Mapping Table

| Element | Current Color | New Color | CSS Location |
|---------|--------------|-----------|--------------|
| Container BG | `linear-gradient(#1a3d1a...)` | `#e0e0e0` (연회색) | `.container` L15 |
| Table Felt | `linear-gradient(#1e5f1e...)` | 제거 | `.table-felt` 전체 제거 |
| Table Border | `#5c3d2e` | 제거 | `.table-felt` 전체 제거 |
| Blinds Border | `#c00` | `#333` | `.blinds-info` L79 |
| Active Player | `#c00` | `#333` | `.chip-item.active` L112 |
| POT Background | `#c00` | `#333` | `.pot-display` L278 |
| Red Suit | `#c00` | `#666` | `.suit.red` L183, L271 |
| Card Back | `#1a237e...` | `#888/#aaa` | `.hud-card.back` L185 |
| Card Back Border | `#0d1b5e` | `#444` | `.hud-card.back` L186 |

---

## Task Flow

```
[T1: CSS Color Replace]
        |
        v
[T2: Remove Table Felt]
        |
        v
[T3: Verify Layout]
        |
        v
[T4: Screenshot Capture]
```

---

## Detailed TODOs

### T1: CSS Color Replacement
**Complexity**: LOW | **Est. Time**: 5 min

**Changes**:
```css
/* Line 15: Container Background */
- background: linear-gradient(135deg, #1a3d1a 0%, #0d2a0d 50%, #1a3d1a 100%);
+ background: #e0e0e0;

/* Line 79: Blinds Info Border */
- border-left: 3px solid #c00;
+ border-left: 3px solid #333;

/* Line 112: Active Chip Item */
- border-bottom-color: #c00;
+ border-bottom-color: #333;

/* Line 183: Red Suit (HUD Card) */
- .hud-card .suit.red { color: #c00; }
+ .hud-card .suit.red { color: #666; }

/* Line 185-186: Card Back Pattern */
- background: repeating-linear-gradient(45deg, #1a237e, #1a237e 3px, #283593 3px, #283593 6px);  /* L185 */
- border-color: #0d1b5e;  /* L186 */
+ background: repeating-linear-gradient(45deg, #888, #888 3px, #aaa 3px, #aaa 6px);
+ border-color: #444;

/* Line 271: Red Suit (Board Card) */
- .board-card .suit.red { color: #c00; }
+ .board-card .suit.red { color: #666; }

/* Line 278: POT Display */
- background: #c00;
+ background: #333;
```

**Acceptance Criteria**:
- [ ] 모든 `#c00` 인스턴스 → `#333` 또는 `#666`
- [ ] 모든 녹색/파란색 제거됨

---

### T2: Remove Table Felt Element
**Complexity**: LOW | **Est. Time**: 2 min

**Changes**:
1. CSS에서 `.table-felt` 스타일 블록 제거 (Lines 21-34)
2. HTML에서 `<div class="table-felt"></div>` 제거 (Line 354)

**Acceptance Criteria**:
- [ ] `.table-felt` CSS 규칙 없음
- [ ] HTML에 `table-felt` div 없음

---

### T3: Layout Verification
**Complexity**: LOW | **Est. Time**: 2 min

**Verification Checklist**:
- [ ] 좌측 하단 HUD 스택 위치 동일
- [ ] 우측 하단 3-Grid 위치 동일
- [ ] 상단 바 레이아웃 동일
- [ ] 960x540 컨테이너 크기 유지

---

### T4: Screenshot Capture
**Complexity**: LOW | **Est. Time**: 3 min

**Command**:
```bash
npx playwright screenshot docs/mockups/01-viewer-overlay.html docs/images/mockups/01-viewer-overlay.png --viewport-size=1000,600
```

**Note**: 명령어는 `C:\claude\ebs` 디렉토리에서 실행. viewport는 여백 포함 1000x600 사용.

**Acceptance Criteria**:
- [ ] PNG 파일 생성됨
- [ ] 이미지 크기 960x540
- [ ] 흑백 색상만 표시됨

---

## Commit Strategy

### Single Commit
```
style(mockup): convert viewer-overlay to B&W wireframe

- Remove green table felt background
- Replace #c00 red accents with #333 gray
- Convert card back pattern to grayscale
- Change red suit color to #666 gray
- Maintain PokerGFX layout unchanged

Closes: mockup-bnw-standard
```

---

## Success Criteria

| Criteria | Verification Method |
|----------|---------------------|
| No color except grayscale | Visual inspection of screenshot |
| Layout unchanged | Compare element positions |
| Cards readable | Verify rank/suit visibility |
| Screenshot exists | File check: `docs/images/mockups/01-viewer-overlay.png` |

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| 수트 구분 어려움 | LOW | 하트/다이아에 hollow 스타일 적용 가능 |
| 레이아웃 깨짐 | VERY LOW | 색상만 변경, 구조 건드리지 않음 |

---

## Files Modified

| File | Action |
|------|--------|
| `docs/mockups/01-viewer-overlay.html` | EDIT (CSS + HTML) |
| `docs/images/mockups/01-viewer-overlay.png` | CREATE (screenshot) |

---

**PLAN_READY: .omc/plans/viewer-overlay-bnw.md**
