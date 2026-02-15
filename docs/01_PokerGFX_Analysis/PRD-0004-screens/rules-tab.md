---
parent: PRD-0004-EBS-Server-UI-Design.md
screen_id: rules
element_range: R-01 ~ R-06
---

# Rules Tab -- Screen Specification

## Quick Reference

- 단축키: Ctrl+4
- 요소: 6개 (P0: 0, P1: 6, P2: 0)
- 스크린샷: `images/mockups/ebs-rules.png`
- HTML 원본: [ebs-server-ui.html](../mockups/ebs-server-ui.html)

![Rules 탭](../images/mockups/ebs-rules.png)

## Design Decisions

1. GFX 2에서 분리한 이유: PokerGFX에서 게임 규칙(Bomb Pot, Straddle, Rabbit Hunting)이 GFX 2의 리더보드/플레이어 표시 설정과 혼재되어 있었다. 규칙은 Game Engine의 행동을 결정하고, GFX Display는 시각적 출력을 결정한다. 이 둘은 변경 빈도와 영향 범위가 다르므로 독립 탭으로 분리하여 기능 혼재를 해소했다.

2. 모든 요소가 P1인 이유: 게임 규칙은 대부분의 방송에서 기본값으로 운영된다. Bomb Pot이나 Straddle 같은 특수 규칙은 특정 게임 형식에서만 활성화되므로 P0(필수)이 아닌 P1(중요)로 분류했다.

## Workflow

게임 규칙 설정은 독립적이며 순서가 없다. 필요한 규칙만 확인/변경한다.

## Element Catalog

| # | 요소 | 설명 | PGX# | 우선순위 |
|:-:|------|------|:----:|:--------:|
| R-01 | Move Button Bomb Pot | 봄팟 후 버튼 이동 | GFX2 #8 | P1 |
| R-02 | Limit Raises | 유효 스택 기반 레이즈 제한 | GFX2 #9 | P1 |
| R-03 | Allow Rabbit Hunting | 래빗 헌팅 허용 | GFX2 #14 | P1 |
| R-04 | Straddle Sleeper | 스트래들 위치 규칙 | GFX2 #10 | P1 |
| R-05 | Sleeper Final Action | 슬리퍼 최종 액션 | GFX2 #11 | P1 |
| R-06 | Ignore Split Pots | Equity/Outs에서 Split pot 무시 | GFX2 #21 | P1 |

## Navigation

| 목적지 | 방법 | 조건 |
|--------|------|------|
| GFX 탭 | Ctrl+3 | 규칙과 연동되는 표시 설정 확인 |
| Main Window | 탭 영역 외 클릭 | 설정 완료 후 |
