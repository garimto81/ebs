---
parent: PRD-0004-EBS-Server-UI-Design.md
screen_id: graphic-editor
element_range: Board / Player
---

# Graphic Editor -- Screen Specification

## Quick Reference

- 단축키: 없음 (별도 창, Skin Editor 경유)
- 요소: Board 모드 + Player 모드 (Player Overlay 8개 요소)
- 스크린샷: `images/mockups/ebs-graphic-editor.png`
- HTML 원본: [ebs-graphic-editor.html](../mockups/ebs-graphic-editor.html)

![Graphic Editor](../images/mockups/ebs-graphic-editor.png)

## Design Decisions

1. Board/Player 듀얼 모드인 이유: 보드 영역(커뮤니티 카드, 팟)과 플레이어 영역(홀카드, 이름, 스택)은 레이아웃 요소가 완전히 다르다. 하나의 에디터에서 모드를 전환하여 편집하면, 동일한 조작 패턴(Position, Animation, Text)을 유지하면서 대상만 바꿀 수 있다.

2. Skin Editor에서만 접근 가능한 이유: Graphic Editor는 가장 세밀한 편집 수준이다. GFX 탭 → Skin Editor → Graphic Editor 순서로 진입 깊이가 깊어지면서, 실수로 픽셀 수준 편집에 접근하는 것을 방지한다. 이 계층 구조는 "변경 빈도가 낮을수록 접근이 깊다"는 원칙을 따른다.

## Workflow

편집 대상 선택 → 위치/크기 조정 → 애니메이션 설정 → 텍스트 스타일 → 실시간 프리뷰 확인.

## Element Catalog

### 핵심 편집 기능

| 기능 | 설명 |
|------|------|
| Element 선택 | 드롭다운으로 편집 대상 선택 |
| Position (LTWH) | Left/Top/Width/Height 픽셀 단위 |
| Anchor | 해상도 변경 시 기준점 |
| Z-order | 레이어 겹침 순서 |
| Angle | 요소 회전 |
| Animation In/Out | 등장/퇴장 + 속도 슬라이더 |
| Transition | Default/Pop/Expand/Slide |
| Text | 폰트, 색상, 강조색, 정렬, 그림자 |
| Background Image | 요소 배경 |
| Live Preview | 하단 실시간 프리뷰 |

### Player Overlay 요소 (8개)

| 코드 | 요소 | 설명 | 우선순위 |
|:----:|------|------|:--------:|
| A | Player Photo | 프로필 이미지 | P1 |
| B | Hole Cards | 홀카드 2~5장 | P0 |
| C | Name | 플레이어 이름 | P0 |
| D | Country Flag | 국적 국기 | P2 |
| E | Equity % | 승률 | P0 |
| F | Action | 최근 액션 | P0 |
| G | Stack | 칩 스택 | P0 |
| H | Position | 포지션 (D/SB/BB) | P0 |

## Navigation

| 목적지 | 방법 | 조건 |
|--------|------|------|
| Skin Editor | 창 닫기 | 편집 완료 후 |
