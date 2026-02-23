---
doc_type: "design"
doc_id: "DESIGN-AT-001"
version: "1.0.0"
status: "draft"
owner: "BRACELET STUDIO"
last_updated: "2026-02-19"
prd_ref: "PRD-AT-001 v2.0.0"
---

# EBS Action Tracker — UI Design Document

## 1. 디자인 비전

EBS Action Tracker는 방송 스튜디오의 어두운 환경 속에서 수 시간을 연속 운영하는 전문 운영자를 위한 도구다. 디자인 철학은 단 하나의 원칙으로 수렴한다: **운영자가 화면을 "읽지" 않고 "느끼도록"** 만든다. 어두운 네이비 배경 위에 앰버 골드 액센트가 현재 액션을 지시하고, 스트리트 진행 바가 게임 흐름을 직선으로 시각화하며, 키보드 단축키 하나로 핵심 액션이 완료된다. 운영자의 주의력이 화면 탐색이 아닌 실제 게임 관찰에 집중될 때 방송 품질이 완성된다.

### PokerGFX와의 차별점

| 구분 | PokerGFX Action Tracker | EBS Action Tracker |
|------|------------------------|-------------------|
| **팟 정보** | 팟 사이즈 미표시 | 팟 사이즈 + 현재 콜 금액 항상 표시 |
| **스트리트 상태** | 버튼 레이블만으로 유추 | Pre-Flop → Flop → Turn → River 진행 바 |
| **카드 선택 UX** | 52장 4×13 밀집 그리드 | 슈트별 탭 + 카드 크기 확대 (56px+) |
| **RFID 등록** | 단순 카드 표시 | 프로그레스 바 (N/52) + 완료 애니메이션 |
| **온보딩** | 없음 | 단축키 가이드 오버레이 (F1 토글) |

---

## 2. 디자인 시스템

### 2.1 색상 팔레트

모든 색상 값은 CSS/Flutter 구현 시 CSS 변수 또는 Dart const로 선언한다.

#### 배경 레이어

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-bg-base` | `#1A1A2E` | 앱 최상위 배경 (다크 네이비) |
| `color-bg-surface` | `#252540` | 패널/섹션 배경 |
| `color-bg-cell` | `#2E2E4A` | 카드 셀/입력 필드 배경 |
| `color-bg-modal` | `#0D0D1A` | 모달/오버레이 배경 (90% 불투명) |
| `color-bg-hover` | `#38385A` | 버튼 hover 상태 |
| `color-bg-pressed` | `#44446A` | 버튼 pressed 상태 |

#### 텍스트

| 토큰 | Hex | 용도 | WCAG 대비율 (bg-base 기준) |
|------|-----|------|---------------------------|
| `color-text-primary` | `#E0E0E0` | 기본 텍스트 | 12.1:1 (AAA) |
| `color-text-secondary` | `#9E9E9E` | 보조 텍스트, 레이블 | 5.9:1 (AA) |
| `color-text-disabled` | `#5A5A7A` | 비활성 요소 텍스트 | - |
| `color-text-inverse` | `#1A1A2E` | 밝은 배경 위 텍스트 | - |

#### 액센트 — 상태별

| 토큰 | Hex | 용도 | 의미 |
|------|-----|------|------|
| `color-accent-amber` | `#F4A228` | Action-on 좌석, 현재 차례 강조 | 주목 필요 |
| `color-accent-green` | `#4CAF50` | Connected, Active, CHECK 버튼 | 정상/긍정 |
| `color-accent-red` | `#E53935` | FOLD 버튼, Disconnected, 오류 | 위험/종료 |
| `color-accent-orange` | `#FF6D00` | ALL-IN 버튼, 고위험 액션 | 극단 |
| `color-accent-blue` | `#42A5F5` | BET/RAISE 버튼, 정보 | 능동 |
| `color-accent-gold` | `#FFD54F` | GFX 활성 표시, 골드 상태 | 방송 중 |

#### 비활성/중립

| 토큰 | Hex | 용도 |
|------|-----|------|
| `color-neutral-dark` | `#4A4A4A` | Fold/비활성 좌석 배경 |
| `color-neutral-mid` | `#6E6E8E` | 구분선, 테두리 |
| `color-neutral-light` | `#8E8EAE` | 아이콘, 보조 요소 |

> **색맹 대응 원칙**: 색상 단독으로 상태를 전달하지 않는다. 색상 + 아이콘 + 텍스트 3중 표현 (§2.6 참조).

---

### 2.2 타이포그래피

#### 폰트 스택

| 역할 | 폰트 | Fallback | 선택 이유 |
|------|------|----------|----------|
| 숫자/금액 | `JetBrains Mono` | `Consolas`, monospace | 고정폭 — 자릿수 정렬, 숫자 가독성 |
| 상태/레이블 | `IBM Plex Sans Condensed` | `Arial Narrow`, sans-serif | 좁은 폭 — 밀도 높은 UI에 적합 |
| 버튼 텍스트 | `IBM Plex Sans` | `Arial`, sans-serif | 명확성, 중간 굵기 |

> **금지 폰트**: Inter, Roboto, Arial (시스템 기본값), Space Grotesk.

#### 크기 계층

| 토큰 | px | 용도 |
|------|:--:|------|
| `font-size-xs` | 11px | 서브 레이블, 툴팁 |
| `font-size-sm` | 13px | 보조 정보, 좌석 이름 |
| `font-size-base` | 15px | 일반 텍스트 (최소 기준: 14pt = ~19px, 본 문서 14px+ 유지) |
| `font-size-md` | 18px | 버튼 텍스트 |
| `font-size-lg` | 22px | 섹션 헤더, 팟 사이즈 |
| `font-size-xl` | 28px | 스택 금액, 강조 수치 |
| `font-size-2xl` | 36px | 핸드 번호, RFID 등록 카드 |
| `font-size-3xl` | 48px | 현재 액션 플레이어 스택 |

**최소 폰트 크기**: 실제 운영 환경 기준 14pt = 19px. 단, 밀도 높은 통계 테이블 행(§3.4)에서 13px 허용 — 근거: 통계 테이블은 운영자 85% 메인 화면이 아닌 보조 화면이며, 7컬럼×10행 데이터 밀도를 1280px 최소 해상도에서 수용하기 위한 예외. 향후 해상도 대응(§6)에서 1920px 이상 시 15px로 상향.

---

### 2.3 간격/그리드 시스템

#### 간격 토큰 (4px 기준)

| 토큰 | px | 용도 |
|------|:--:|------|
| `space-1` | 4px | 아이콘-텍스트 간격 |
| `space-2` | 8px | 컴포넌트 내부 패딩 |
| `space-3` | 12px | 버튼 수직 패딩 |
| `space-4` | 16px | 섹션 내부 패딩 |
| `space-6` | 24px | 섹션 간 간격 |
| `space-8` | 32px | 주요 영역 구분 |

#### 레이아웃 그리드 (1280×800 기준)

```
+------ 1280px -----------------------------------------------+
|                                                             |
|  StatusBar          [44px 고정 높이]                         |
|  GameConfigBar      [48px 고정 높이]                         |
|  StreetProgressBar  [32px 고정 높이]                         |
|                                                             |
|  TableArea          [flex-grow, 최소 280px]                  |
|                                                             |
|  BoardArea          [120px 고정 높이]                        |
|  PotInfoBar         [44px 고정 높이]                         |
|  ActionPanel        [80px 고정 높이]                         |
|  BetInputPanel      [64px 고정 높이]                         |
|  SpecialActionBar   [52px 고정 높이]                         |
|                                                             |
+-------------------------------------------------------------+

고정 합계:    44+48+32+120+44+80+64+52 = 484px
TableArea:   800 - 484 - 16(padding) = 300px 최소 확보
```

#### 버튼 크기 기준

| 버튼 유형 | 최소 크기 | 권장 크기 |
|----------|:--------:|:--------:|
| 핵심 액션 (FOLD/CHECK/BET 등) | 44×44px | 60×56px |
| 보조 액션 (UNDO, TAG 등) | 44×44px | 52×44px |
| Quick Bet 프리셋 | 44×44px | 80×44px |
| 특수 액션 (HIDE GFX 등) | 44×44px | 100×44px |
| 설정 항목 버튼 | 44×44px | 120×44px |

---

### 2.4 컴포넌트 스타일

#### 버튼 변형

**Primary Action Button** (FOLD, CHECK, CALL, BET, RAISE, ALL-IN)
```
배경:       color-accent-[역할별]
텍스트:     color-text-inverse  /  font-size-md  /  font-weight-700
패딩:       12px 20px
border-radius: 6px
최소 너비:  100px
최소 높이:  56px
hover:      brightness +15%  /  transition 150ms ease
active:     brightness -10%  /  scale 0.97  /  transition 80ms
disabled:   opacity 0.35  /  cursor not-allowed
```

**Secondary Button** (UNDO, TAG HAND, MISS DEAL 등)
```
배경:       color-bg-surface
border:     1px solid color-neutral-mid
텍스트:     color-text-primary  /  font-size-sm  /  font-weight-500
패딩:       8px 16px
border-radius: 6px
hover:      배경 color-bg-hover  /  transition 150ms
```

**Danger Button** (FOLD, CANCEL, MISS DEAL)
```
배경:       color-accent-red
텍스트:     #FFFFFF  /  font-weight-700
hover:      #EF5350
active:     #C62828
```

**Toggle Button** (HIDE GFX, LIVE, AUTO)
```
비활성 상태: 배경 color-bg-surface  /  border color-neutral-mid
활성 상태:   배경 color-accent-amber  /  텍스트 color-text-inverse
전환:       200ms ease-in-out
```

#### 입력 필드

**Bet Amount Input**
```
배경:       color-bg-cell
border:     2px solid color-neutral-mid
포커스:     border color-accent-amber
텍스트:     color-text-primary  /  font-family JetBrains Mono  /  font-size-xl
패딩:       10px 16px
border-radius: 6px
텍스트 정렬: right (금액 우측 정렬)
```

#### 좌석 카드 (Seat Card)

```
크기:       88×72px (1280px 기준)
border-radius: 8px
배경 (Active):    color-bg-surface  /  border 2px solid color-neutral-mid
배경 (Action-on): color-bg-surface  /  border 2px solid color-accent-amber
                  box-shadow: 0 0 12px color-accent-amber (40% opacity)
배경 (Folded):    color-neutral-dark (opacity 0.6)
배경 (Empty):     color-bg-base  /  border 1px dashed color-neutral-mid
배경 (SittingOut):color-bg-surface  /  opacity 0.5
```

#### 커뮤니티 카드 슬롯

```
크기 (빈 슬롯):   52×72px  /  border 1px dashed color-neutral-mid  /  opacity 0.4
크기 (카드 있음): 52×72px  /  카드 이미지 렌더링
border-radius:   6px
간격:            8px (카드 간), 16px (Flop/Turn/River 그룹 간)
```

---

### 2.5 아이콘 시스템

#### 아이콘 라이브러리: Material Symbols (Outlined)

| 아이콘 | Material 심볼 | 크기 | 용도 |
|--------|--------------|:----:|------|
| 연결 상태 | `wifi` / `wifi_off` | 20px | GfxServer 연결 |
| RFID | `nfc` | 20px | RFID 테이블 연결 |
| 방송 | `live_tv` | 20px | 스트림 상태 |
| 녹화 | `fiber_manual_record` | 16px | 녹화 중 (빨간색) |
| UNDO | `undo` | 24px | 이전 액션 취소 |
| TAG | `star_outline` / `star` | 20px | 핸드 태깅 |
| HIDE GFX | `visibility` / `visibility_off` | 20px | 방송 오버레이 |
| 카드 스캔 | `credit_card` / `credit_card_off` | 18px | RFID 카드 상태 |
| 설정 | `settings` | 20px | 설정 진입 |
| DEALER | `person` | 14px | 딜러 뱃지 |

**아이콘 색상 규칙**:
- 정상 상태: `color-accent-green` (#4CAF50)
- 경고 상태: `color-accent-amber` (#F4A228)
- 오류 상태: `color-accent-red` (#E53935)
- 비활성: `color-neutral-light` (#8E8EAE)

---

### 2.6 상태 표현 — 색상 + 아이콘 + 텍스트 3중 표현

색맹 사용자와 저조도 환경 대응을 위해 모든 중요 상태는 3가지 채널로 동시에 표현한다.

#### 연결 상태

| 상태 | 색상 | 아이콘 | 텍스트 |
|------|:----:|:------:|--------|
| Connected | #4CAF50 | `wifi` | "CONNECTED" |
| Connecting | #F4A228 (점멸) | `wifi` (점멸) | "CONNECTING..." |
| Disconnected | #E53935 | `wifi_off` | "DISCONNECTED" |
| Reconnecting | #F4A228 | `sync` (회전) | "RETRY 5s..." |

#### 좌석 상태

| 상태 | 배경색 | 테두리 | 텍스트 스타일 |
|------|:------:|:------:|:------------:|
| Active | #2E2E4A | color-neutral-mid | 정상 |
| Action-on | #2E2E4A | #F4A228 (2px + glow) | **Bold** + Amber |
| Folded | #4A4A4A (dim) | 없음 | 취소선 |
| Empty | #1A1A2E | dashed color-neutral-mid | "EMPTY" italic |
| SittingOut | #2E2E4A | 없음 | opacity 0.5 |

#### RFID 카드 스캔 상태

| 상태 | 아이콘 | 색상 | 설명 |
|------|:------:|:----:|------|
| 미인식 | `credit_card` (outline) | #5A5A7A | 카드 미배분 또는 미감지 |
| 인식 성공 | `credit_card` (filled) | #4CAF50 | RFID 정상 스캔 |
| 오류 | `error_outline` | #E53935 | 스캔 실패 또는 중복 |
| 수동 입력됨 | `edit_note` | #F4A228 | RFID 우회, 수동 입력 |
## 3. 화면 설계 (6개 화면)

### 3.1 메인 액션 화면 (Main Action View)

> 운영자 사용 시간 85%. 가장 중요한 화면.
> **충족 요구사항**: REQ-AT-001~004 (상태 표시), REQ-AT-007 (핸드 번호), REQ-AT-008~011 (테이블 레이아웃), REQ-AT-012~014 (액션 버튼), REQ-AT-015~018 (베팅 입력), REQ-AT-019~020 (보드), REQ-AT-021~026 (특수 액션), REQ-AT-042~043 (동적 UI)

#### 3.1.1 레이아웃 Grid 구조 (1920×1080 권장 기준)

```
+=====================================================================+
| STATUS BAR                                          [고정 44px]     |
| [wifi Connected] [nfc OK 0.3s] [live_tv LIVE] [● REC 01:23:45]    |
+=====================================================================+
| GAME CONFIG BAR                                     [고정 48px]     |
| [HOLDEM v] [SB: 100 / BB: 200 / Ante: 0]  [# HAND 047]  [AUTO]   |
+=====================================================================+
| STREET PROGRESS BAR                                 [고정 32px]     |
|  [PRE-FLOP]---->[FLOP]------>[TURN]------>[RIVER]-->[SHOWDOWN]    |
|       ●              ○             ○             ○           ○     |
+=====================================================================+
|                                                                     |
|   POT INFO:  Pot  1,200,000  |  To Call:  400,000  [고정 44px]    |
|                                                                     |
+---------------------------------------------------------------------+
|                                                                     |
|                    TABLE AREA               [flex, 최소 300px]      |
|                                                                     |
|           [S8 Active]   [S9 Action-on!]   [S10 Active]             |
|                                                                     |
|    [S7 Folded]                                  [S1 Active SB]     |
|                                                                     |
|    [S6 Active]    [  BOARD  ]                   [S2 Active BB]     |
|                   [7♥][6♠][4♥][  ][  ]                            |
|                                                                     |
|    [S5 Active]                                  [S3 Active]        |
|                                                                     |
|           [S4 Active]   [S3 D]      [S2 Active]                    |
|                                                                     |
+---------------------------------------------------------------------+
|                                                                     |
|  CARD SCAN ROW:  [🂠][🂠][  ][  ][  ][  ][  ][  ][  ][  ]         |
|  (S1~S10 각 좌석의 RFID 스캔 상태 아이콘)       [고정 36px]          |
|                                                                     |
+=====================================================================+
| ACTION BUTTONS                                      [고정 80px]     |
|                                                                     |
|  [← UNDO(3)]  [  FOLD  ]  [  CHECK  ]  [   BET   ]  [ ALL-IN ]   |
|                                                                     |
+=====================================================================+
| BET INPUT PANEL                                     [고정 64px]     |
|                                                                     |
|  Amount: [          400,000          ]  [MIN] [1/2P] [POT] [ALL]  |
|  Min: 400,000  Max: 8,400,000                                      |
|                                                                     |
+=====================================================================+
| SPECIAL ACTIONS BAR                                 [고정 52px]     |
|  [HIDE GFX]  [TAG HAND★]  [ADJUST STACK]  [CHOP]  [RIT 2×] [MD]  |
+=====================================================================+
```

#### 3.1.2 정보 계층

**1차 정보** (즉시 인지, 항상 최상위 가시성):
- 현재 Action-on 좌석 (앰버 테두리 + glow)
- 액션 버튼 그룹 (화면 하단 80px 고정)
- 현재 스트리트 (스트리트 진행 바)

**2차 정보** (필요 시 확인):
- 팟 사이즈 / To Call 금액
- 각 좌석의 스택 금액
- 커뮤니티 카드 현황
- RFID 카드 스캔 상태

**3차 정보** (배경 모니터링):
- 연결 상태 (StatusBar)
- 핸드 번호
- 녹화 경과 시간

#### 3.1.3 상세 컴포넌트 설명

**StatusBar (44px)**
```
+---------------------------------------------------------------------+
| [wifi]Connected  [nfc]Table 0.3s ago  [live_tv]LIVE  [●]REC 01:23 |
+---------------------------------------------------------------------+

- [wifi] 아이콘: Connected=#4CAF50, Disconnected=#E53935 (점멸)
- [nfc] 아이콘: heartbeat 5초+ 초과 시 #F4A228 경고
- [live_tv]: LIVE=#4CAF50, Offline=#E53935, Buffering=#F4A228
- [●] 녹화 인디케이터: 빨간 원 + 경과 시간 (JetBrains Mono)
- 배경: color-bg-modal (#0D0D1A)
- 높이: 44px  /  패딩: 0 16px
```

**GameConfigBar (48px)**
```
+---------------------------------------------------------------------+
| [HOLDEM ▾]  SB 100  /  BB 200  /  Ante 0    HAND # 047   [AUTO]   |
+---------------------------------------------------------------------+

- [HOLDEM ▾]: 드롭다운 — HOLDEM / PLO4 / PLO5 / SHORT DECK
  클릭 시 SendGameType 전송 (REQ-AT-005)
- SB/BB/Ante: 클릭 시 인라인 숫자 입력 팝업 (REQ-AT-006)
- HAND #: 자동 증가, 클릭 시 수동 조정 (REQ-AT-007)
- [AUTO]: 토글 버튼 — 활성 시 앰버 배경 (REQ-AT-028)
```

**StreetProgressBar (32px)**
```
+---------------------------------------------------------------------+
|  ●─────────────○────────────○────────────○────────────○            |
|  PRE-FLOP      FLOP         TURN         RIVER     SHOWDOWN        |
+---------------------------------------------------------------------+

- 완료 스트리트: 실선 + 채워진 원 (color-accent-green)
- 현재 스트리트: 앰버 원 (color-accent-amber) + 텍스트 Bold
- 미완료 스트리트: 점선 + 빈 원 (color-neutral-mid)
- 스트리트 전환 시 200ms 트랜지션
```

**PotInfoBar (44px)**
```
+---------------------------------------------------------------------+
|   POT  1,200,000        |        To Call  400,000                  |
+---------------------------------------------------------------------+

- "POT" 레이블: font-size-sm (#9E9E9E)
- 금액: font-size-xl JetBrains Mono (#E0E0E0)
- "To Call" 레이블: font-size-sm (#9E9E9E)
- To Call 금액: font-size-xl JetBrains Mono (#F4A228) — 앰버 강조
- 구분선: 1px solid color-neutral-mid
- 배경: color-bg-surface
```

**TableArea — 좌석 배치**

10인 테이블 포커 레이아웃. 타원형 참조 배치, 좌석 1은 화면 하단 우측 기준 시계 반대 방향.

```
                 [S8]    [S9▶]   [S10]
              (Active) (Action!) (Active)

     [S7]                              [S1]
   (Folded)                          (Active SB)

     [S6]      ┌──────────────┐        [S2]
   (Active)    │  COMMUNITY   │      (Active BB)
               │  [7♥][6♠][4♥]│
     [S5]      │  [  ][  ]    │        [S3]
   (Active)    └──────────────┘      (Active)

                 [S4]   [S3 D]   [S2]
               (Active) (Dealer) (Active)
```

**좌석 카드 상세 (88×72px)**:
```
+------------+
|  SB  [  D] |  <- 포지션 뱃지 (SB, BB, D, STR)
|            |
| Player 3   |  <- 플레이어 이름 (font-size-sm)
| 1,250,000  |  <- 스택 (JetBrains Mono font-size-md)
+------------+
 테두리 컬러: Active=#6E6E8E, Action-on=#F4A228

Action-on 상태 glow 효과:
box-shadow: 0 0 0 2px #F4A228, 0 0 20px rgba(244,162,40,0.4)
```

**커뮤니티 보드 영역**:
```
+----------------------------------------+
|  Flop           Turn    River          |
| [7♥] [6♠] [4♥]  [  ]    [  ]          |
|                                        |
|  (카드 없을 때: 점선 테두리 슬롯)          |
+----------------------------------------+

- 카드 슬롯 크기: 52×72px
- 카드 간격: 8px (Flop 내부), 16px (그룹 간)
- 카드 표시: 실제 카드 SVG 이미지
- 빈 슬롯: 점선 border + opacity 0.3
```

**CardScanRow (36px)**:
```
좌석별 RFID 스캔 상태 아이콘 행:

[S1:🂠✓] [S2:🂠✓] [S3:  ] [S4:  ] [S5:  ] [S6:  ] [S7:  ] [S8:  ] [S9:  ] [S10: ]
  green    green   gray   gray   gray   gray   gray   gray   gray   gray

- 인식 성공: credit_card (filled) + #4CAF50
- 미인식: credit_card (outline) + #5A5A7A
- 오류: error_outline + #E53935
- 수동 입력: edit_note + #F4A228
```

**ActionPanel (80px) — 동적 버튼 전환**:

```
[베팅 없는 상태 — biggest_bet_amt == 0]:
+------------------------------------------------------------------+
| [←UNDO(3)] [  FOLD  ] [   CHECK   ] [    BET    ] [  ALL-IN  ] |
+------------------------------------------------------------------+

[베팅 있는 상태 — biggest_bet_amt > 0]:
+------------------------------------------------------------------+
| [←UNDO(3)] [  FOLD  ] [   CALL   ] [  RAISE-TO  ] [ ALL-IN  ] |
+------------------------------------------------------------------+

버튼별 색상:
- UNDO:      bg color-bg-surface, border color-neutral-mid
- FOLD:      bg #E53935 (color-accent-red)
- CHECK/CALL: bg #4CAF50 (color-accent-green)
- BET/RAISE:  bg #42A5F5 (color-accent-blue)
- ALL-IN:    bg #FF6D00 (color-accent-orange)

UNDO 숫자 배지: UNDO 가능 단계 수 표시 (0이면 비활성)
버튼 높이: 56px, border-radius: 6px
전환 애니메이션: 버튼 라벨 200ms fade-in/out
```

**BetInputPanel (64px)**:
```
+------------------------------------------------------------------+
|  [ -  ]  [         400,000         ]  [ +  ]                    |
|  MIN: 400,000  Max: 8,400,000  [MIN][1/2P][POT][ALL-IN]         |
+------------------------------------------------------------------+

- 금액 입력 필드: JetBrains Mono font-size-xl, 우측 정렬
- [-]/[+] 버튼: smallest_chip 단위 증감 (REQ-AT-016)
- Quick Bet: MIN(최소레이즈) / 1/2 POT / POT / ALL-IN (REQ-AT-017)
- Min/Max 표시: color-text-secondary, font-size-xs
- Enter 키로 베팅 확정 → SendPlayerBet 전송
```

**SpecialActionBar (52px)**:
```
+------------------------------------------------------------------+
| [HIDE GFX] [★ TAG] [ADJUST STACK] [CHOP] [RIT 2×] [MISS DEAL] |
+------------------------------------------------------------------+

- HIDE GFX: 토글 (활성: 앰버 배경, 텍스트 "SHOW GFX")
- TAG: 별 아이콘 + 태그 텍스트 입력 팝업
- ADJUST STACK: 좌석 선택 → 금액 입력 다이얼로그
- CHOP: 분할 대상/비율 입력 다이얼로그
- RIT 2×: Run It Twice 활성화 토글
- MISS DEAL: 빨간 버튼 + 확인 다이얼로그 (2단계 확인)
```

#### 3.1.4 인터랙션 플로우

```
새 핸드 시작:
  [N키 또는 NEW HAND 클릭]
       |
       v
  Settings/Config 화면으로 전환 (딜러/SB/BB 지정)
       |
       v
  게임 시작 → PRE-FLOP 스트리트 바 활성화
       |
       v
  첫 번째 Action-on 좌석에 앰버 glow
       |
       v
  운영자: F=Fold / C=Check or Call / B=Bet or Raise / A=All-in

베팅 입력 흐름:
  [B키 또는 BET 클릭]
       |
       v
  BetInputPanel 포커스 이동 (포커스 링 앰버)
       |
       v
  금액 입력 (숫자키) 또는 Quick Bet 클릭
       |
       v
  [Enter 키] → 금액 확정 → SendPlayerBet
       |
       v
  다음 Action-on으로 자동 이동
```

#### 3.1.5 키보드 단축키 매핑

| 키 | 액션 | 조건 |
|----|------|------|
| `F` | FOLD | Action-on 상태 |
| `C` | CHECK / CALL | Action-on 상태 |
| `B` | BET / RAISE | Action-on 상태 |
| `A` | ALL-IN | Action-on 상태 |
| `U` | UNDO | UNDO 가능 단계 > 0 |
| `N` | NEW HAND | IDLE 또는 HAND_COMPLETE 상태 |
| `Space` | 확인/진행 | 팝업/다이얼로그 열린 경우 |
| `Esc` | 취소/닫기 | 팝업/다이얼로그 열린 경우 |
| `G` | HIDE GFX 토글 | 언제든 |
| `F1` | 단축키 가이드 오버레이 | 언제든 |
| `Tab` | 다음 입력 필드 | 입력 모드 |
| `+` / `-` | 베팅 금액 증감 | BetInput 포커스 시 |

---

### 3.2 설정/구성 화면 (Settings/Configuration View)

> 새 핸드 시작 전 또는 게임 파라미터 변경 시 진입.
> **충족 요구사항**: REQ-AT-005 (게임 타입→SendGameType), REQ-AT-006 (SB/BB/Ante→WriteGameInfo), REQ-AT-027 (Settings 컴팩트 뷰), REQ-AT-028 (AUTO→_auto), REQ-AT-029 (STRADDLE→_third,_pl_third), REQ-AT-030 (3B→_third), REQ-AT-031 (BTN BLIND→_button_blind), REQ-AT-032 (CAP→_cap), REQ-AT-033 (7 DEUCE→_seven_deuce), REQ-AT-034 (BOMB POT→_bomb_pot), REQ-AT-035 (HIT GAME)

#### 3.2.1 ASCII 와이어프레임

```
+=====================================================================+
| STATUS BAR                                          [고정 44px]     |
| [wifi Connected] [nfc OK] [live_tv LIVE] [● REC 01:23:45]         |
+=====================================================================+
| GAME CONFIG BAR                                     [고정 48px]     |
| [HOLDEM ▾]  SB 100  /  BB 200  /  Ante 0    HAND # 047  [AUTO]   |
+=====================================================================+
| SEAT ROW                                            [고정 56px]     |
|  [S1  ][S2  ][S3  ][S4  ][S5  ][S6  ][S7  ][S8  ][S9  ][S10 ]  |
|  [Str1][Str2][Str3][Str4][Str5][Str6][Str7][Str8][Str9][Str10]  |
+=====================================================================+
| CARD SCAN STATUS                                    [고정 36px]     |
| [🂠✓][🂠✓][  ][  ][  ][  ][  ][  ][  ][  ]                      |
+=====================================================================+
|                                                                     |
| POSITION SETUP                                      [고정 80px]     |
| [DEALER ▾]  [SB ▾]  [BB ▾]  [3B ▾]                               |
|  Seat 3      Seat 1   Seat 2  —                                    |
|                                                                     |
+=====================================================================+
|                                                                     |
| GAME RULES                                          [고정 160px]    |
|  +--------+  +--------+  +----------+  +--------+  +---------+   |
|  | CAP    |  | ANTE   |  | BTN BLIND|  | MIN    |  | # BOARDS|   |
|  | 0      |  | 0      |  | 0        |  | CHIP   |  | 1       |   |
|  |        |  |        |  |          |  | 100    |  |         |   |
|  +--------+  +--------+  +----------+  +--------+  +---------+   |
|                                                                     |
|  +--------+  +--------+  +----------+  +---------+               |
|  | 7 DEUCE|  | BOMB   |  | HIT GAME |  | SINGLE  |               |
|  | 0      |  | POT 0  |  | 0        |  | BOARD ▾ |               |
|  |        |  |        |  |          |  |         |               |
|  +--------+  +--------+  +----------+  +---------+               |
|                                                                     |
+=====================================================================+
|                                                                     |
| BOTTOM ACTIONS                                      [고정 64px]     |
|  [SETTINGS]  [START HAND]                                          |
|                                                                     |
+=====================================================================+
```

#### 3.2.2 레이아웃 Grid 구조

- **Seat Row**: 10개 좌석을 균등 분할 (각 124px@1280px). 각 셀에 좌석 번호 + STRADDLE 순서 표시.
- **Position Setup**: 딜러/SB/BB/3B 포지션을 드롭다운으로 좌석에 직접 지정.
- **Game Rules**: 2행 × 5열 그리드. 각 셀은 버튼 + 현재값 인라인 표시.

#### 3.2.3 정보 계층

**1차 정보**: 딜러/SB/BB 포지션 지정, 게임 타입
**2차 정보**: 블라인드 구조 (CAP, ANTE, BTN BLIND), MIN CHIP
**3차 정보**: 특수 사이드 게임 (7 DEUCE, BOMB POT, HIT GAME), # BOARDS

#### 3.2.4 인터랙션 패턴

```
규칙 버튼 클릭 (예: CAP):
  [CAP 버튼 클릭]
       |
       v
  인라인 숫자 키패드 팝업 (버튼 위에 오버레이)
       |
       v
  금액 입력 → Enter 확정
       |
       v
  버튼 내 수치 즉시 갱신 + WriteGameInfo 전송

STRADDLE 설정:
  좌석 행의 [StrN] 클릭
       |
       v
  STRADDLE 순서 드롭다운 (OFF / 1st / 2nd / ...)
       |
       v
  WriteGameInfo(_third, _pl_third 등) 전송
```

---

### 3.3 카드 선택 화면 (Manual Card Selection)

> RFID 실패 또는 수동 모드 진입 시 풀스크린 모달.
> **충족 요구사항**: REQ-AT-020 (수동 카드 선택), REQ-AT-041 (RFID 등록 연계)

#### 3.3.1 ASCII 와이어프레임

```
+=====================================================================+
|  MODAL HEADER                                       [고정 72px]     |
|  [◀ Back]   Selected: [ 7♥ ] [ 6♠ ] [    ] [    ] [    ]  [OK]   |
+=====================================================================+
|  SUIT TABS                                          [고정 44px]     |
|  [ ♠ Spades ]  [ ♥ Hearts ]  [ ♦ Diamonds ]  [ ♣ Clubs ]         |
+=====================================================================+
|                                                                     |
|  CARD GRID (현재 탭: ♥ Hearts)             [flex 영역]             |
|                                                                     |
|  +---+  +---+  +---+  +---+  +---+  +---+  +---+  +---+         |
|  | A |  | K |  | Q |  | J |  |10 |  | 9 |  | 8 |  | 7 |         |
|  | ♥ |  | ♥ |  | ♥ |  | ♥ |  | ♥ |  | ♥ |  | ♥ |  | ♥ |         |
|  +---+  +---+  +---+  +---+  +---+  +---+  +---+  +---+         |
|                                                                     |
|  +---+  +---+  +---+  +---+  +---+                               |
|  | 6 |  | 5 |  | 4 |  | 3 |  | 2 |  (이미 사용: 반투명+취소선)    |
|  | ♥ |  | ♥ |  | ♥ |  | ♥ |  | ♥ |                               |
|  +---+  +---+  +---+  +---+  +---+                               |
|                                                                     |
+=====================================================================+
|  MODAL FOOTER                                       [고정 52px]     |
|  이미 사용된 카드: 3장 사용 불가 (주황 텍스트로 표시)                  |
+=====================================================================+
```

#### 3.3.2 UX 개선 사항 (PokerGFX 대비)

| 항목 | PokerGFX | EBS |
|------|----------|-----|
| 카드 그리드 | 4×13 전체 표시 | 슈트별 탭 분리 (1탭 13장) |
| 카드 크기 | 밀집 소형 | 56×76px 확대 (터치 대응) |
| 사용 카드 | 비활성 처리 방식 미확인 | 반투명 + 취소선 |
| 선택 확인 | 상단 표시 | 헤더 고정 + 슬롯 명확화 |
| 네비게이션 | 단일 화면 | 탭 키로 슈트 전환 가능 |

#### 3.3.3 키보드 단축키

| 키 | 액션 |
|----|------|
| `1~4` | 슈트 탭 전환 (1=♠, 2=♥, 3=♦, 4=♣) |
| `A`, `K`, `Q`, `J`, `T`, `9`~`2` | 현재 탭의 해당 카드 선택 |
| `Backspace` | 마지막 선택 취소 (◀ Back) |
| `Enter` | 선택 확정 (OK) |
| `Esc` | 카드 선택 취소, 메인 화면 복귀 |

---

### 3.4 통계/방송 제어 화면 (Statistics / Broadcast Control)

> 핸드 간 휴식 시간 또는 방송 제어 필요 시 진입.
> **충족 요구사항**: REQ-AT-036~040 (통계 및 방송 제어)

#### 3.4.1 ASCII 와이어프레임

```
+================================================+==============+
| STATUS BAR (공통)                              |              |
+------------------------------------------------+  BROADCAST   |
| HAND # 047          [← 메인 화면으로]          |  CONTROL     |
+================================================+              |
|                                                |              |
| STATISTICS TABLE                               | [LIVE   ]    |
|                                                | LIVE/DELAY   |
| SEAT  STACK      VPIP%  PFR%  AGRFq% WTSD% WIN|              |
| ---- ----------- ------ ----- ------ ----- ---| [GFX ★  ]   |
| S1   1,000,000                            0   | ON/OFF       |
| S2   1,005,000   100    100              +5K  |              |
| S3     995,000   100                    -5K   | HAND #047    |
| S4             —                              |              |
| S5             —                              | [FIELD  ]    |
| S6             —                              | REMAIN  [__] |
| S7             —                              | TOTAL   [__] |
| S8             —                              |              |
| S9             —                              | [STRIP  ]    |
| S10            —                              | STACK / WIN  |
|                                                |              |
| [RESET STATS]  [EXPORT CSV*]                   | [TICKER ]    |
|  * EXPORT CSV: v2.0+ 기능 (PRD 미정의, 추후 REQ 추가 예정)           |
|                                                | [___text___] |
|                                                | [LOOP ON]    |
+================================================+==============+
```

#### 3.4.2 레이아웃 설명

- **통계 테이블** (좌측 70%): 10행 × 7열. STACK 컬럼은 JetBrains Mono + 앰버 하이라이트. WIN 컬럼 양수=#4CAF50, 음수=#E53935.
- **방송 제어 패널** (우측 30%, 240px 고정): 수직 스택. 각 버튼은 현재 상태를 텍스트로 표시.

#### 3.4.3 방송 제어 버튼 동작

| 버튼 | 활성 상태 | 비활성 상태 | 전송 메시지 |
|------|:--------:|:-----------:|-------------|
| LIVE | 앰버 배경 "LIVE" | 회색 "DELAY" | `SendDelayedMode` |
| GFX | 금색 배경 ★ | 회색 | `SendGfxEnable` |
| FIELD | 앰버 배경 "ON" | 회색 "OFF" | `SendFieldVisibility` |
| STRIP | 앰버 + 모드 선택 | 회색 | `SendShowStrip` |
| TICKER | 입력 + 재생 버튼 | — | `SendTicker` + `SendTickerLoop` |

---

### 3.5 RFID 덱 등록 화면 (RFID Deck Registration)

> 덱 교체 또는 초기 설치 시 진입하는 풀스크린 모달.
> **충족 요구사항**: REQ-AT-041 (덱 등록), REQ-AT-044 (덱 검증)

#### 3.5.1 ASCII 와이어프레임

```
+=====================================================================+
|  RFID DECK REGISTRATION                                            |
|  (풀스크린 모달 — 검정 배경 #0D0D1A, 다른 조작 완전 차단)           |
+=====================================================================+
|                                                                     |
|                                                                     |
|         ╔═══════════════════════════════════════╗                  |
|         ║                                       ║                  |
|         ║  PLACE THIS CARD ON ANY ANTENNA       ║                  |
|         ║                                       ║                  |
|         ╚═══════════════════════════════════════╝                  |
|                                                                     |
|                   +------------------+                             |
|                   |                  |                             |
|                   |   A              |                             |
|                   |                  |                             |
|                   |       ♠          |                             |
|                   |                  |                             |
|                   |              A   |                             |
|                   +------------------+                             |
|                      A of Spades                                   |
|                                                                     |
|   PROGRESS:   ▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░  1 / 52        |
|               완료: 1장   남은 카드: 51장                            |
|                                                                     |
|                                                                     |
|         +-----------------------------------------------+          |
|         |                                               |          |
|         |              C A N C E L                      |          |
|         |                                               |          |
|         +-----------------------------------------------+          |
|                                                                     |
+=====================================================================+
```

#### 3.5.2 프로그레스 표현

```
진행 바 구성:
  ▓ = 등록 완료 (#4CAF50)
  ░ = 미등록 (#4A4A4A)
  너비: 600px 고정 중앙 정렬
  높이: 16px, border-radius: 8px

프로그레스 텍스트:
  "N / 52" — JetBrains Mono font-size-lg (#F4A228)
  "완료: N장" — color-accent-green, font-size-sm
  "남은 카드: N장" — color-text-secondary, font-size-sm

카드 등록 완료 시:
  카드 이미지 위에 초록 체크 아이콘 200ms 표시 후
  다음 카드 이미지로 전환 (300ms 슬라이드)

52장 전체 완료:
  "등록 완료! 덱이 준비되었습니다." 메시지
  자동 모달 닫기 (2초 후) + 메인 화면 복귀
```

#### 3.5.3 카드 등록 순서

```
A♠ → K♠ → Q♠ → J♠ → 10♠ → 9♠ → 8♠ → 7♠ → 6♠ → 5♠ → 4♠ → 3♠ → 2♠
A♥ → K♥ → ... → 2♥
A♦ → K♦ → ... → 2♦
A♣ → K♣ → ... → 2♣
```

중복 등록 감지 시: "이미 등록된 카드입니다. 다른 카드를 올려주세요." (앰버 경고)

---

### 3.6 화면 전환 플로우

```
앱 시작
    |
    v
ConnectScreen (서버 IP:Port 입력)
    |
    | [Connect 버튼 / 자동 연결]
    v
메인 액션 화면 (기본 화면)
    |
    +--[탭/버튼]--> 설정/구성 화면
    |                    |
    |              [START HAND]--> 메인 액션 화면
    |
    +--[REGISTER 버튼]--> RFID 덱 등록 (풀스크린 모달)
    |                    |
    |              [CANCEL / 완료]--> 메인 액션 화면
    |
    +--[카드 선택 필요 시]--> 카드 선택 화면 (풀스크린 모달)
    |                    |
    |              [OK / Esc]--> 메인 액션 화면
    |
    +--[통계 탭]--> 통계/방송 제어 화면
                        |
                  [← 뒤로가기]--> 메인 액션 화면
```

**탭 네비게이션 (상단 탭 바)**:
```
[MAIN] [CONFIG] [STATS]

- MAIN: 메인 액션 화면 (기본)
- CONFIG: 설정/구성 화면 (핸드 시작 전)
- STATS: 통계/방송 제어 화면

화면 전환 애니메이션: 200ms horizontal slide
RFID 등록, 카드 선택: 탭 위에 풀스크린 모달 (탭 바 숨김)
```
## 4. 핵심 혁신 (PokerGFX 대비)

### 4.1 팟 정보 상시 표시 (PotInfoBar)

**문제**: PokerGFX Action Tracker는 팟 사이즈와 현재 콜 금액을 표시하지 않는다. BET/RAISE 결정 시 운영자가 게임 상황을 별도로 파악해야 한다.

**해결**: `PotInfoBar` (44px)를 보드 영역 위에 고정 배치.

```
컴포넌트 구성:
  Left:  "POT" 레이블 (font-size-sm, #9E9E9E)
         팟 금액 (font-size-xl, JetBrains Mono, #E0E0E0)

  Right: "To Call" 레이블 (font-size-sm, #9E9E9E)
         콜 금액 (font-size-xl, JetBrains Mono, #F4A228)
         — 콜 없을 때 (체크 상황) 0 표시 또는 숨김

업데이트 소스: OnGameInfoReceived의 pot_amt 및 biggest_bet_amt 필드
```

**REQ 연계**: REQ-AT-018 (최소/최대 베팅 표시), REQ-AT-015 (베팅 입력)

---

### 4.2 스트리트 진행 바 (StreetProgressBar)

**문제**: PokerGFX는 현재 스트리트(Pre-Flop/Flop/Turn/River)를 명시적으로 표시하지 않는다. 운영자는 커뮤니티 카드 수를 보고 유추해야 한다.

**해결**: `StreetProgressBar` (32px)를 항상 화면 상단에 표시.

```
5단계 스텝 인디케이터:

PRE-FLOP  →  FLOP  →  TURN  →  RIVER  →  SHOWDOWN
   ●             ○         ○          ○           ○
(현재)        (미완)     (미완)      (미완)       (미완)

상태별 스타일:
  완료:   ● 채운 원 (#4CAF50) + 실선 연결선
  현재:   ● 앰버 원 (#F4A228) + 텍스트 Bold + 미세 glow
  미완:   ○ 빈 원 (#4A4A4A) + 점선 연결선

전환 애니메이션:
  스트리트 변경 시 왼쪽 원이 초록으로 전환 (300ms)
  새 현재 원이 앰버로 활성화 (200ms delay 후)
```

---

### 4.3 카드 선택 UX 개선

**문제**: PokerGFX의 52장 4×13 그리드는 카드가 작고 밀집되어 빠른 선택이 어렵다. 스튜디오 환경에서 실수 발생 위험이 높다.

**해결**: 슈트별 탭 + 카드 크기 확대.

```
개선 전 (PokerGFX):
  4행 × 13열 = 52장 동시 표시
  카드 크기: 추정 28×40px (소형, 밀집)
  슈트 구분: 행 순서로만

개선 후 (EBS):
  슈트 탭 4개 (♠ / ♥ / ♦ / ♣)
  탭당 13장 표시
  카드 크기: 56×76px (2× 확대)

  빠른 선택 경로:
    키보드: [2키]=♥ 탭 → [K키]=K 선택 → K♥ 즉시 입력
    마우스: 슈트 탭 클릭 → 카드 클릭 (2클릭)

  이미 사용된 카드:
    opacity: 0.3 + 취소선 + cursor not-allowed
    선택 시도 시 경고 툴팁 "이미 사용된 카드"
```

---

### 4.4 RFID 등록 프로그레스 표시

**문제**: PokerGFX RFID 등록 화면은 현재 등록해야 할 카드만 표시한다. 전체 진행률을 알 수 없어 운영자가 완료 시점을 예측하기 어렵다.

**해결**: 프로그레스 바 + 상태 통계 추가.

```
프로그레스 바 컴포넌트:
  +------ 600px -------+
  | ▓▓▓▓▓▓░░░░░░░░░░░  |  <- color-accent-green / color-neutral-dark
  +--------------------+
    완료: N장  남은: M장  예상: ~Xs

  "N / 52" 대형 숫자 (JetBrains Mono font-size-2xl, #F4A228)

카드 완료 애니메이션:
  1. 카드 이미지 위 녹색 체크 (200ms scale-in)
  2. 프로그레스 바 한 칸 증가 (300ms)
  3. 다음 카드 이미지 슬라이드-인 (250ms)

52장 완료:
  전체 프로그레스 바 초록 완성 + 체크 아이콘
  "덱 등록 완료!" 텍스트 (font-size-xl, #4CAF50)
  2초 후 자동 닫기
```

---

### 4.5 신규 운영자 온보딩 레이어

**문제**: PokerGFX에는 단축키 안내 또는 초보 운영자를 위한 가이드가 없다.

**해결**: F1 키로 토글 가능한 단축키 가이드 오버레이.

```
F1 키 → 오버레이 표시 (200ms fade-in)

+-------------------------------------------------------------------+
|  KEYBOARD SHORTCUTS                                  [F1 닫기]   |
+-------------------------------------------------------------------+
|                                                                   |
|  GAME ACTIONS                    NAVIGATION                       |
|  F  =  FOLD                      Tab        =  다음 필드          |
|  C  =  CHECK / CALL              Shift+Tab  =  이전 필드          |
|  B  =  BET / RAISE               1~4        =  슈트 탭 (카드선택) |
|  A  =  ALL-IN                    Esc        =  취소/닫기          |
|  U  =  UNDO (최대 5단계)                                           |
|  N  =  NEW HAND                  BROADCAST                        |
|  G  =  HIDE/SHOW GFX             F1         =  이 화면 토글       |
|  Space = 확인/진행                                                 |
|                                                                   |
|  BET INPUT                                                        |
|  숫자키 = 직접 입력     +/- = Min Chip 단위 증감                    |
|  Enter  = 베팅 확정    Backspace = 지우기                          |
|                                                                   |
+-------------------------------------------------------------------+

배경: #0D0D1A (85% 불투명)
위치: 화면 중앙 모달
최대 크기: 600×400px
```
## 5. 키보드 단축키 전체 매핑

### 5.1 전역 단축키 (모든 화면에서 동작)

| 키 | 액션 | 전송 메시지 | REQ |
|----|------|------------|-----|
| `F1` | 단축키 가이드 오버레이 토글 | — | REQ-AT-014 |
| `G` | HIDE/SHOW GFX 토글 | `SendGfxEnable` | REQ-AT-021 |
| `Esc` | 팝업/다이얼로그 닫기 | — | — |
| `Ctrl+Z` | UNDO (대안 단축키) | — | REQ-AT-013 |

---

### 5.2 메인 액션 화면 단축키

| 키 | 액션 | 조건 | 전송 메시지 |
|----|------|------|------------|
| `F` | FOLD | Action-on 상태, FOLD 가능 | `SendPlayerFold` |
| `C` | CHECK (베팅 없을 때) | Action-on 상태 | `SendPlayerCheckCall` |
| `C` | CALL (베팅 있을 때) | Action-on 상태 | `SendPlayerCheckCall` |
| `B` | BET 입력 모드 (베팅 없을 때) | Action-on 상태 | — → 금액 입력 후 `SendPlayerBet` |
| `B` | RAISE 입력 모드 (베팅 있을 때) | Action-on 상태 | — → 금액 입력 후 `SendPlayerBet` |
| `A` | ALL-IN | Action-on 상태 | `SendPlayerBet` (최대값) |
| `U` | UNDO | UNDO 가능 단계 > 0 | — (로컬 상태 복원) |
| `N` | NEW HAND | IDLE / HAND_COMPLETE | `SendStartHand` |
| `Space` | 팝업 확인/진행 | 팝업 열린 경우 | — |
| `Tab` | 다음 입력 필드 | 입력 모드 | — |
| `+` | 베팅 금액 +smallest_chip | BetInput 포커스 | — |
| `-` | 베팅 금액 -smallest_chip | BetInput 포커스 | — |
| `Enter` | 베팅 확정 | BetInput에 금액 입력됨 | `SendPlayerBet` |
| `Backspace` | 베팅 금액 한 자리 삭제 | BetInput 포커스 | — |
| `M` | MIN 베팅 프리셋 | BetInput 포커스 | — |
| `H` | 1/2 POT 프리셋 | BetInput 포커스 | — |
| `P` | POT 베팅 프리셋 | BetInput 포커스 | — |
| `T` | TAG HAND | 언제든 | `SendTag` |
| `D` | ADJUST STACK 다이얼로그 | 언제든 | `SendPlayerStack` |

---

### 5.3 카드 선택 화면 단축키

| 키 | 액션 |
|----|------|
| `1` | ♠ Spades 탭으로 이동 |
| `2` | ♥ Hearts 탭으로 이동 |
| `3` | ♦ Diamonds 탭으로 이동 |
| `4` | ♣ Clubs 탭으로 이동 |
| `A` | Ace 선택 (현재 탭 슈트) |
| `K` | King 선택 |
| `Q` | Queen 선택 |
| `J` | Jack 선택 |
| `T` | Ten 선택 |
| `9`~`2` | 해당 숫자 카드 선택 |
| `Backspace` | 마지막 선택 카드 취소 |
| `Enter` | 선택 확정 (OK) |
| `Esc` | 카드 선택 취소, 메인 복귀 |

---

### 5.4 단축키 시각적 힌트

모든 버튼 우하단에 단축키 키 표시 (조건: 설정에서 "Show Shortcuts" 활성 시):

```
+------------------+
|                  |
|   F O L D        |
|                  |
|             [F]  |  <- 단축키 힌트 (font-size-xs, #5A5A7A)
+------------------+
```
## 6. 반응형/해상도 대응

### 6.1 지원 해상도 및 레이아웃 변화

| 해상도 | 등급 | 주요 변화 |
|--------|:----:|----------|
| 1280×800 | 최소 지원 | 기본 레이아웃 (모든 컴포넌트 표시) |
| 1366×768 | 일반 노트북 | 좌석 카드 크기 소폭 축소 (80×66px) |
| 1920×1080 | 권장 (Full HD) | 기준 레이아웃. 좌석 카드 88×72px |
| 2560×1440 | 고해상도 | TableArea 확장, 카드/버튼 크기 확대 |

---

### 6.2 1280×800 최소 해상도 대응

```
최소 해상도 레이아웃:

고정 영역 합계: 484px (동일)
TableArea: 800 - 484 - 16 = 300px

좌석 카드: 80×66px (기본 대비 -10%)
커뮤니티 카드: 46×64px
버튼 높이: 52px (기본 56px 대비 -4px)
BetInput font-size: font-size-lg (22px) 적용

절대 축소 불가 요소:
- StatusBar 높이 44px
- ActionPanel 높이 (버튼 44px 최소)
- BetInput 글자 크기 18px+
- 버튼 터치 타깃 44×44px 최소
```

---

### 6.3 1920×1080 권장 해상도 레이아웃

```
전체 높이 1080px:
  StatusBar:        44px
  GameConfigBar:    48px
  StreetProgress:   32px
  PotInfoBar:       44px
  TableArea:       492px  (1080 - 484 - 60 여백)
  BoardArea:       120px
  ActionPanel:      80px
  BetInputPanel:    64px
  SpecialActions:   52px
  여백/패딩:         ~60px
  ───────────────────────
  합계:            1080px (정확)

전체 너비 1920px:
  메인 콘텐츠 최대 너비: 1200px (중앙 정렬)
  좌우 여백: 각 360px (또는 좌측 220px 사이드 패널 확장 가능)
```

---

### 6.4 고해상도 확장 (2560×1440+)

```
Flutter desktop의 MediaQuery.of(context).size를 활용한 반응형:

  breakpoints:
    sm: < 1366px  →  compact 모드
    md: 1366~1919px →  standard 모드
    lg: 1920px+  →  comfortable 모드
    xl: 2560px+  →  spacious 모드

comfortable 모드 (1920px+):
  - 좌석 카드: 88×72px → 100×84px
  - 버튼 높이: 56px → 64px
  - font-size-xl: 28px → 32px

spacious 모드 (2560px+):
  - 좌측에 240px 사이드 패널 (게임 설정 퀵 액세스)
  - 우측에 240px 사이드 패널 (통계 미니뷰)
  - 중앙 1080px 메인 작업 영역
```

---

### 6.5 멀티 모니터 운영 시나리오

**시나리오 A: 듀얼 모니터 (권장)**
```
모니터 1 (운영자 전용, 1920×1080):
  Action Tracker 풀스크린

모니터 2 (방송 프리뷰):
  EBS Server GfxServer
  방송 오버레이 프리뷰
```

**시나리오 B: 단일 모니터**
```
좌측 70%: Action Tracker (창 모드)
우측 30%: GfxServer (창 모드)

최소 사용 가능 폭: 896px (1280px의 70%)
→ compact 모드 자동 적용
```

---

### 6.6 비기능 요구사항 충족 방안

| 요구사항 | 기준 | 구현 방안 |
|----------|:----:|----------|
| 버튼 응답 | 50ms | 버튼 클릭 시 즉시 pressed 스타일 적용 (렌더링 확인), 서버 전송은 비동기 |
| UI 갱신 | 100ms | Riverpod Provider 상태 변경 → 위젯 rebuild 구독 최소화 |
| 연속 운영 | 4~10시간 | 메모리 누수 방지 (dispose 패턴), 자동 재연결 (30초 주기) |
| 다크 스튜디오 환경 | 저조도 | color-bg-base #1A1A2E (순수 검정 회피, 눈 피로 감소) + 밝기 최소 60nit에서 WCAG 4.5:1+ |
---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|---------|
| 1.0.0 | 2026-02-19 | 최초 작성. PRD-AT-001 v2.0.0 기반. 6개 화면 전체 설계. |

---

**Version**: 1.0.0 | **Updated**: 2026-02-19 | **PRD Ref**: PRD-AT-001 v2.0.0
