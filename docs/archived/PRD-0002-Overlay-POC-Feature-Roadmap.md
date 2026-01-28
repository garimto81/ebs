# PRD-0002: EBS 오버레이 POC 기능 로드맵

**Version**: 1.0.0
**작성일**: 2026-01-26
**관련 PRD**: PRD-0001-RFID-Poker-Card-Reader-MVP

---

## 1. PokerGFX 오버레이 기능 분석

### 1.1 PokerGFX 핵심 기능 목록

[PokerGFX](https://www.pokergfx.io/)는 업계 표준 포커 방송 소프트웨어로, WSOP 2024, PokerGO Studios, Live at the Bike 등에서 사용됩니다.

#### 그래픽 오버레이 요소

| 요소 | 설명 | 우선순위 |
|------|------|----------|
| **Hole Cards** | 플레이어 홀카드 표시 | 필수 |
| **Community Cards** | 플랍/턴/리버 커뮤니티 카드 | 필수 |
| **Player Names** | 플레이어 이름 표시 | 필수 |
| **Chip Counts** | 플레이어 칩 수량 | 필수 |
| **Pot Size** | 현재 팟 크기 | 필수 |
| **Blind Levels** | 블라인드 레벨 (SB/BB) | 필수 |
| **Timer** | 게임 타이머 / 샷클럭 | 중요 |
| **Leaderboard** | 토너먼트 리더보드 | 선택 |
| **Player Photos** | 플레이어 사진 | 선택 |
| **Country Flags** | 국가 플래그 아이콘 | 선택 |
| **Win Probability** | 승률 퍼센트 표시 | 선택 |

#### 스킨 시스템 (PRO 기능)

| 기능 | 설명 |
|------|------|
| **Fully Customizable Images** | 모든 그래픽 요소 커스터마이징 |
| **Customizable Fonts** | 폰트 변경 지원 |
| **Multi-lingual Text** | 다국어 텍스트 지원 |
| **Animation Transitions** | 요소별 애니메이션 전환 정의 |
| **Custom Animation Sequences** | 커스텀 애니메이션 시퀀스 |
| **Skin Packaging** | 스킨 파일 내보내기/가져오기 |
| **Skin Download Centre** | 프리메이드 스킨 라이브러리 |

#### 방송 기능

| 기능 | 설명 |
|------|------|
| **4K UHD Output** | 4K 해상도 출력 |
| **Auto Camera Switching** | 자동 카메라 전환 |
| **Time Delay (Secure Delay)** | 보안 딜레이 기능 |
| **NDI Output** | NDI 네이티브 출력 |
| **SDI/HDMI Output** | Blackmagic Decklink 지원 |
| **Fill & Key Output** | 외부 키잉용 분리 출력 |
| **Dynamic Delay** | 휴식 시간 자동 감지/단축 |

#### 통합 기능

| 기능 | 설명 |
|------|------|
| **Action Clock Integration** | 샷클럭 앱 연동 |
| **Stream Deck Integration** | Elgato Stream Deck 지원 |
| **Hand History Database** | 핸드 히스토리 DB |
| **Studio Mode** | 포스트 프로덕션 컨트롤 |

---

## 2. EBS 제품 단계별 기능 정의

### 2.1 Phase 개요

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    EBS Overlay Product Roadmap                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Phase 1: POC (Proof of Concept)                                       │
│   ═══════════════════════════════                                       │
│   목표: 기본 카드 표시 + 간단한 오버레이                                │
│   기간: 2주                                                             │
│                                                                         │
│   Phase 2: MVP (Minimum Viable Product)                                 │
│   ══════════════════════════════════════                                │
│   목표: 홈게임 스트리밍 가능 수준                                       │
│   기간: 4주                                                             │
│                                                                         │
│   Phase 3: Beta                                                         │
│   ══════════════                                                        │
│   목표: 카드룸 수준 기능 + 커스터마이징                                 │
│   기간: 6주                                                             │
│                                                                         │
│   Phase 4: Production                                                   │
│   ═══════════════════                                                   │
│   목표: 상용 방송 수준                                                  │
│   기간: 8주+                                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1: POC (Proof of Concept)

### 3.1 목표

- RFID 카드 인식 → 웹 오버레이 표시 검증
- 기본 애니메이션 효과 구현
- OBS Browser Source 연동 확인

### 3.2 기능 목록

#### 필수 기능 (Must Have)

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P1-01 | **Hole Cards Display** | 2장 홀카드 표시 (1개 슬롯) | 중 |
| P1-02 | **Card Animation** | 카드 등장 애니메이션 | 중 |
| P1-03 | **Transparent Background** | 크로마키/투명 배경 | 하 |
| P1-04 | **WebSocket Realtime** | 실시간 카드 업데이트 | 중 |
| P1-05 | **OBS Compatibility** | Browser Source 호환 | 하 |

#### 선택 기능 (Nice to Have)

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P1-06 | Card Flip Animation | 카드 뒤집기 효과 | 중 |
| P1-07 | Card Highlight | 핸드 완성 시 하이라이트 | 하 |

### 3.3 UI 컴포넌트

```
┌─────────────────────────────────────────────────────────────┐
│                      POC Overlay Layout                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                 Transparent Canvas                   │  │
│   │                 (1920 x 1080)                        │  │
│   │                                                      │  │
│   │                                                      │  │
│   │                                                      │  │
│   │                                                      │  │
│   │   ┌───────────────────────────────────────────┐     │  │
│   │   │            Player Hole Cards               │     │  │
│   │   │   ┌─────────┐    ┌─────────┐              │     │  │
│   │   │   │   A ♠   │    │   K ♠   │              │     │  │
│   │   │   │         │    │         │              │     │  │
│   │   │   │         │    │         │              │     │  │
│   │   │   └─────────┘    └─────────┘              │     │  │
│   │   │       Player Name: "Player 1"             │     │  │
│   │   └───────────────────────────────────────────┘     │  │
│   │                                                      │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 애니메이션 스펙

| 애니메이션 | 트리거 | 지속시간 | 이징 |
|-----------|--------|---------|------|
| Card Appear | 카드 인식 | 300ms | ease-out |
| Card Flip | 카드 공개 | 400ms | cubic-bezier |
| Card Highlight | 핸드 완성 | 500ms | pulse |
| Card Fade Out | 카드 제거 | 200ms | ease-in |

### 3.5 기술 스택

| 영역 | 기술 | 이유 |
|------|------|------|
| Frontend | React + TypeScript | 컴포넌트 기반, 실시간 UI |
| Animation | Framer Motion | React 최적화, 선언적 애니메이션 |
| Styling | CSS-in-JS (Emotion) | 동적 스타일, 투명 배경 |
| Communication | WebSocket | 실시간 양방향 통신 |
| Output | HTML/CSS | OBS Browser Source 호환 |

### 3.6 산출물

- `/overlay` 엔드포인트 (투명 배경 오버레이)
- 카드 컴포넌트 + 애니메이션
- WebSocket 연동 테스트

---

## 4. Phase 2: MVP

### 4.1 목표

- 다중 플레이어 지원 (최대 10명)
- 커뮤니티 카드 표시
- 기본 게임 정보 표시
- 홈게임 스트리밍 가능

### 4.2 기능 목록

#### 그래픽 요소

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P2-01 | **Multi-Player Slots** | 최대 10명 플레이어 슬롯 | 상 |
| P2-02 | **Community Cards** | 플랍/턴/리버 표시 | 중 |
| P2-03 | **Player Names** | 플레이어 이름 표시 | 하 |
| P2-04 | **Chip Counts** | 칩 수량 표시 | 중 |
| P2-05 | **Pot Size Display** | 팟 크기 표시 | 하 |
| P2-06 | **Blind Levels** | SB/BB 레벨 표시 | 하 |

#### 애니메이션

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P2-07 | **Community Card Deal** | 플랍/턴/리버 딜 애니메이션 | 중 |
| P2-08 | **Pot Update Animation** | 팟 증가 애니메이션 | 하 |
| P2-09 | **Player Action Indicator** | 액션 표시 (Bet, Raise, Fold) | 중 |
| P2-10 | **Winning Hand Highlight** | 승리 핸드 하이라이트 | 중 |

#### 레이아웃

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P2-11 | **Table Layout Presets** | 6/8/9/10인 테이블 프리셋 | 중 |
| P2-12 | **Position Auto-Arrangement** | 플레이어 위치 자동 배치 | 중 |

### 4.3 UI 레이아웃

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MVP Overlay Layout (9-Max)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│        [P1]              [P2]              [P3]                         │
│       ┌────┐            ┌────┐            ┌────┐                        │
│       │A♠K♠│            │??  │            │??  │                        │
│       └────┘            └────┘            └────┘                        │
│       Player1           Player2           Player3                       │
│       $1,200            $850              $2,100                        │
│                                                                         │
│   [P9]                                              [P4]                │
│   ┌────┐                                            ┌────┐              │
│   │??  │        ┌─────────────────────────┐         │??  │              │
│   └────┘        │     Community Cards      │         └────┘              │
│   Player9       │   [A♥] [K♦] [Q♣] [?] [?] │         Player4            │
│   $500          │                          │         $1,800              │
│                 │       POT: $450          │                            │
│   [P8]          │       Blinds: 5/10       │         [P5]               │
│   ┌────┐        └─────────────────────────┘         ┌────┐              │
│   │??  │                                            │??  │              │
│   └────┘                                            └────┘              │
│   Player8                                           Player5             │
│   $950                                              $1,500              │
│                                                                         │
│        [P7]              [P6]                                           │
│       ┌────┐            ┌────┐                                          │
│       │??  │            │??  │                                          │
│       └────┘            └────┘                                          │
│       Player7           Player6                                         │
│       $1,100            $750                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Phase 3: Beta

### 5.1 목표

- 스킨 시스템 (기본)
- 보안 딜레이 기능
- 승률 계산/표시
- 카드룸 수준 품질

### 5.2 기능 목록

#### 스킨 시스템

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P3-01 | **Theme Presets** | 3-5개 테마 프리셋 | 중 |
| P3-02 | **Color Customization** | 주요 색상 커스터마이징 | 중 |
| P3-03 | **Font Selection** | 폰트 선택 (3-5개) | 하 |
| P3-04 | **Card Style Options** | 카드 디자인 옵션 | 중 |
| P3-05 | **Layout Position Editor** | 요소 위치 조정 | 상 |

#### 고급 기능

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P3-06 | **Secure Delay** | 5-60초 보안 딜레이 | 상 |
| P3-07 | **Win Probability** | 실시간 승률 계산 | 상 |
| P3-08 | **Hand Strength Meter** | 핸드 강도 시각화 | 중 |
| P3-09 | **Action History** | 최근 액션 히스토리 | 중 |
| P3-10 | **Timer/Shot Clock** | 액션 타이머 | 중 |

#### 애니메이션 고급

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P3-11 | **Custom Transitions** | 요소별 전환 효과 선택 | 중 |
| P3-12 | **Animation Timing Control** | 애니메이션 속도 조절 | 하 |
| P3-13 | **Particle Effects** | 승리 시 파티클 효과 | 중 |

### 5.3 스킨 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Skin System Architecture                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   skin.json                                                             │
│   ├── meta                                                              │
│   │   ├── name: "Dark Professional"                                    │
│   │   ├── version: "1.0.0"                                             │
│   │   └── author: "EBS Team"                                           │
│   │                                                                     │
│   ├── colors                                                            │
│   │   ├── primary: "#1a1a2e"                                           │
│   │   ├── secondary: "#16213e"                                         │
│   │   ├── accent: "#e94560"                                            │
│   │   ├── text: "#ffffff"                                              │
│   │   └── card_bg: "#0f3460"                                           │
│   │                                                                     │
│   ├── fonts                                                             │
│   │   ├── primary: "Roboto"                                            │
│   │   ├── secondary: "Roboto Condensed"                                │
│   │   └── mono: "Roboto Mono"                                          │
│   │                                                                     │
│   ├── cards                                                             │
│   │   ├── style: "modern" | "classic" | "minimal"                      │
│   │   ├── size: { width: 80, height: 112 }                             │
│   │   └── border_radius: 8                                             │
│   │                                                                     │
│   ├── animations                                                        │
│   │   ├── card_appear: { duration: 300, easing: "ease-out" }           │
│   │   ├── card_flip: { duration: 400, easing: "cubic-bezier" }         │
│   │   └── pot_update: { duration: 500, easing: "ease-in-out" }         │
│   │                                                                     │
│   └── layout                                                            │
│       ├── player_slots: [{ x: 10%, y: 20% }, ...]                      │
│       ├── community: { x: 50%, y: 40% }                                │
│       └── pot: { x: 50%, y: 55% }                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Phase 4: Production

### 6.1 목표

- 상용 방송 수준 품질
- 완전한 스킨 커스터마이징
- 다중 출력 지원
- 통합 기능 (Stream Deck 등)

### 6.2 기능 목록

#### 프로덕션 기능

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P4-01 | **4K UHD Output** | 4K 해상도 지원 | 중 |
| P4-02 | **NDI Output** | NDI 네이티브 출력 | 상 |
| P4-03 | **Fill & Key Output** | 외부 키잉용 분리 출력 | 상 |
| P4-04 | **Multi-Table Support** | 다중 테이블 동시 관리 | 상 |
| P4-05 | **Dynamic Delay** | 휴식 자동 감지/단축 | 상 |

#### 통합

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P4-06 | **Stream Deck Plugin** | Elgato Stream Deck 연동 | 상 |
| P4-07 | **Action Clock API** | 외부 샷클럭 연동 | 중 |
| P4-08 | **Leaderboard System** | 토너먼트 리더보드 | 중 |
| P4-09 | **Hand History Export** | 핸드 히스토리 내보내기 | 중 |

#### 스킨 고급

| ID | 기능 | 설명 | 복잡도 |
|----|------|------|--------|
| P4-10 | **Full Skin Editor** | 비주얼 스킨 에디터 | 상 |
| P4-11 | **Skin Import/Export** | 스킨 패키징 | 중 |
| P4-12 | **Animation Sequences** | 커스텀 시퀀스 편집 | 상 |
| P4-13 | **Multi-lingual Support** | 다국어 텍스트 | 중 |

---

## 7. 애니메이션 상세 스펙

### 7.1 카드 애니메이션

| 애니메이션 | CSS/JS | 설명 |
|-----------|--------|------|
| **Card Appear** | `transform: scale(0.5) → scale(1)` | 카드 등장 |
| **Card Flip** | `rotateY(0) → rotateY(180deg)` | 카드 뒤집기 |
| **Card Slide** | `translateX(-100px) → translateX(0)` | 카드 슬라이드 |
| **Card Glow** | `box-shadow` pulse | 핸드 완성 강조 |
| **Card Fade** | `opacity: 1 → 0` | 카드 제거 |

### 7.2 UI 애니메이션

| 애니메이션 | 트리거 | 효과 |
|-----------|--------|------|
| **Pot Increase** | 베팅 시 | 숫자 카운트업 + 스케일 |
| **Player Action** | 액션 시 | 플레이어 슬롯 하이라이트 |
| **Winning Flash** | 승리 시 | 골드 글로우 + 파티클 |
| **Deal Animation** | 딜 시 | 카드 순차 등장 |

### 7.3 이징 함수

```css
/* 기본 이징 */
--ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0.0, 1, 1);
--ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);

/* 커스텀 이징 */
--bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--smooth: cubic-bezier(0.25, 0.1, 0.25, 1);
--snappy: cubic-bezier(0.5, 0, 0.5, 1);
```

---

## 8. 기술 구현 가이드

### 8.1 프론트엔드 구조

```
frontend/
├── src/
│   ├── components/
│   │   ├── Card/
│   │   │   ├── Card.tsx
│   │   │   ├── CardAnimation.tsx
│   │   │   └── CardStyles.ts
│   │   ├── PlayerSlot/
│   │   │   ├── PlayerSlot.tsx
│   │   │   └── PlayerInfo.tsx
│   │   ├── CommunityCards/
│   │   │   └── CommunityCards.tsx
│   │   ├── PotDisplay/
│   │   │   └── PotDisplay.tsx
│   │   └── Overlay/
│   │       ├── OverlayCanvas.tsx
│   │       └── OverlayController.tsx
│   ├── hooks/
│   │   ├── useWebSocket.ts
│   │   ├── useAnimation.ts
│   │   └── useSkin.ts
│   ├── themes/
│   │   ├── default.json
│   │   ├── dark.json
│   │   └── broadcast.json
│   └── pages/
│       ├── overlay.tsx      # /overlay (투명 배경)
│       └── control.tsx      # /control (컨트롤 패널)
```

### 8.2 WebSocket 이벤트

```typescript
// Server → Client
interface OverlayEvent {
  type: 'card_dealt' | 'card_revealed' | 'pot_updated' | 'action' | 'hand_complete';
  payload: {
    playerId?: number;
    cards?: Card[];
    pot?: number;
    action?: 'fold' | 'check' | 'call' | 'bet' | 'raise';
    amount?: number;
    winner?: number;
  };
  timestamp: number;
}
```

---

## 9. Phase별 체크리스트

### Phase 1: POC

```markdown
- [ ] 카드 컴포넌트 구현
- [ ] 카드 등장 애니메이션
- [ ] 투명 배경 캔버스
- [ ] WebSocket 연동
- [ ] OBS Browser Source 테스트
- [ ] 카드 뒤집기 애니메이션 (선택)
```

### Phase 2: MVP

```markdown
- [ ] 다중 플레이어 슬롯 (10개)
- [ ] 커뮤니티 카드 표시
- [ ] 플레이어 이름/칩 표시
- [ ] 팟 크기 표시
- [ ] 테이블 레이아웃 프리셋
- [ ] 딜 애니메이션
- [ ] 액션 인디케이터
```

### Phase 3: Beta

```markdown
- [ ] 테마 프리셋 3-5개
- [ ] 색상 커스터마이징
- [ ] 보안 딜레이 (5-60초)
- [ ] 승률 계산/표시
- [ ] 액션 타이머
- [ ] 커스텀 전환 효과
```

### Phase 4: Production

```markdown
- [ ] 4K 출력
- [ ] NDI 출력
- [ ] Stream Deck 연동
- [ ] 비주얼 스킨 에디터
- [ ] 다중 테이블 지원
- [ ] 핸드 히스토리 내보내기
```

---

## 10. 참고 자료

### 10.1 PokerGFX 관련

| 리소스 | URL |
|--------|-----|
| PokerGFX 공식 | https://www.pokergfx.io/ |
| PokerGFX Features | https://videopokertable.net/features.aspx |
| PokerGFX PRO | https://www.videopokertable.net/pro.aspx |

### 10.2 애니메이션 라이브러리

| 라이브러리 | URL | 용도 |
|-----------|-----|------|
| Framer Motion | https://www.framer.com/motion/ | React 애니메이션 |
| GSAP | https://greensock.com/gsap/ | 고급 애니메이션 |
| Lottie | https://airbnb.io/lottie/ | 벡터 애니메이션 |

### 10.3 경쟁 제품

| 제품 | URL | 특징 |
|------|-----|------|
| RF Poker | https://rfpoker.com/ | AI 기반 분석 |
| DIY Solutions | Poker Chip Forum | 오픈소스 대안 |

---

**문서 끝**
