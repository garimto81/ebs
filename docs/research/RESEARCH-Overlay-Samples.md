# 포커 오버레이 스타일 조사 보고서

**작성일**: 2026-01-30
**목적**: Stage 0 PoC용 오버레이 디자인 방향 결정

---

## 1. 요약

포커 방송 오버레이는 크게 **3가지 스타일**로 분류됩니다:

1. **PokerGFX 스타일**: 좌측 하단 Player HUD + 우측 보드 카드
2. **WPT 스타일**: 풀 스크린 하단 바 + 플레이어 정보 가로 배치
3. **미니멀 스타일**: 카드만 표시 + 최소 UI

각 스타일은 **시청 경험**과 **기술 복잡도** 간 트레이드오프를 가집니다.

---

## 2. 스타일별 분석

### 2.1 PokerGFX 스타일

**대표 사례**: PokerGFX.io, Live at the Bike

**레이아웃**:
```
┌─────────────────────────────────────────────────────┐
│ [TOP BAR: Event Logo | Blinds | Chip Counts]       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Player HUD 1]                     [Board Cards]  │
│  [Player HUD 2]                     [Pot]          │
│  [Player HUD 3]                     [Event Info]   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**핵심 특징**:
- **수직 Player HUD**: 좌측 하단에 2-3명 플레이어 정보 스택
- **카드 오버레이**: HUD 위로 홀카드가 겹침 (shadow 효과)
- **우측 컴팩트 그리드**: 보드카드 + 팟 + 이벤트 정보
- **영상 영역 최대화**: UI가 영상을 최소한으로 가림

**장점**:
- ✅ 영상 영역 80% 이상 노출 (테이블 전체 보임)
- ✅ 플레이어당 상세 정보 표시 (스택, 액션, 에쿼티)
- ✅ 전문적인 느낌 (WPT, WSOP 수준)

**단점**:
- ⚠️ 구현 복잡도 높음 (3개 독립 영역 동기화)
- ⚠️ 5명 이상 플레이어 시 HUD 겹침 가능

**기술 요구사항**:
| 항목 | 상세 |
|------|------|
| 해상도 | 1920x1080 (OBS Browser Source) |
| 투명 배경 | Alpha 채널 (Chroma Key 불필요) |
| 폰트 | Roboto, Noto Sans (고해상도 가독성) |
| 색상 | 다크 테마 (rgba(0,0,0,0.9)) |
| 애니메이션 | CSS fade-in 200ms (카드 등장) |

---

### 2.2 WPT 스타일

**대표 사례**: World Poker Tour Final Table

**레이아웃**:
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              [Full Table View]                      │
│                                                     │
├─────────────────────────────────────────────────────┤
│ [P1 Card | Name | Stack] [P2] [P3] [P4] [P5]      │
│ [Board: K♦ Q♥ _ _ _]  [Pot: 300K]                 │
└─────────────────────────────────────────────────────┘
```

**핵심 특징**:
- **하단 풀 바**: 화면 하단 전체를 사용한 가로 배치
- **플레이어 정보**: 6-9명까지 동시 표시 (작은 아이콘)
- **통합 UI**: 보드/팟/플레이어 모두 한 영역

**장점**:
- ✅ 다인원 게임에 최적화 (9명 테이블 지원)
- ✅ 모든 정보가 한 곳에 집중 (시선 이동 최소)
- ✅ 브랜딩 영역 확보 (좌우 여백에 스폰서 로고)

**단점**:
- ⚠️ 영상 영역 70% 미만 (하단 바가 큼)
- ⚠️ 플레이어당 정보 제한적 (작은 공간)
- ⚠️ 화면 비율 제약 (16:9 전용)

**기술 요구사항**:
| 항목 | 상세 |
|------|------|
| 하단 바 높이 | 200px (1080p 기준) |
| 플레이어 슬롯 | 최대 9개 (동적 width 조정) |
| 반응형 | 6명/9명 모드 전환 |
| 애니메이션 | 슬라이드 인 (bottom → up) |

---

### 2.3 미니멀 스타일

**대표 사례**: Lodge Live Stream, Cash Game 방송

**레이아웃**:
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              [Full Table View]                      │
│                                                     │
│  [Card] [Card]                                      │
│  John: 2.5M                                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**핵심 특징**:
- **카드만 오버레이**: 플레이어 위에 홀카드만 표시
- **최소 정보**: 이름 + 스택 (액션/에쿼티 없음)
- **자연스러운 느낌**: 영상을 최대한 가리지 않음

**장점**:
- ✅ 영상 영역 95% 노출 (몰입감 최대)
- ✅ 구현 복잡도 최소 (Stage 0 PoC 최적)
- ✅ 캐주얼한 느낌 (Cash Game에 적합)

**단점**:
- ⚠️ 정보량 부족 (에쿼티, 액션 히스토리 없음)
- ⚠️ 전문성 부족 (메이저 토너먼트에 부적합)

**기술 요구사항**:
| 항목 | 상세 |
|------|------|
| 해상도 | 960x540 (경량) 또는 1920x1080 |
| 카드 크기 | 60x80px (960p) / 120x160px (1080p) |
| 배경 | 완전 투명 (영상만 보임) |
| 폰트 | 14px (960p) / 28px (1080p) |

---

## 3. 공통 기술 요구사항

모든 스타일에 적용되는 기본 스펙:

| 항목 | 표준 |
|------|------|
| **프레임워크** | HTML5 + CSS3 (OBS Browser Source) |
| **투명 배경** | Alpha 채널 (Chroma Key 불필요) |
| **폰트** | 산세리프 (Roboto, Noto Sans, Inter) |
| **색상 테마** | 다크 (High Contrast) |
| **카드 애니메이션** | fade-in 200ms (requestAnimationFrame) |
| **데이터 연동** | WebSocket (FastAPI 서버) |
| **반응형** | 960x540 / 1920x1080 (OBS preset) |

### 3.1 카드 렌더링 표준

```css
.card {
  width: 60px;
  height: 80px;
  background: #fff;
  border: 2px solid #000;
  border-radius: 4px;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.5);
  font-family: 'Roboto', sans-serif;
}

.card.red { color: #d32f2f; }
.card.black { color: #000; }

/* 뒷면 (카드 숨김) */
.card.back {
  background: repeating-linear-gradient(
    45deg, #888, #888 3px, #aaa 3px, #aaa 6px
  );
}
```

### 3.2 WebSocket 프로토콜

```json
{
  "type": "card_detected",
  "uid": "04:A2:B3:C4",
  "card": {
    "suit": "spades",
    "rank": "A",
    "display": "A♠"
  },
  "timestamp": 1640000000000
}
```

---

## 4. Stage 0 PoC 추천 스타일

### 4.1 선택: **미니멀 스타일 (단순화)**

**이유**:
1. ✅ 구현 복잡도 최소 (1주 이내 완성 가능)
2. ✅ RFID 검증에 집중 (UI 복잡도 배제)
3. ✅ 확장 가능 (Stage 1에서 PokerGFX 스타일로 진화)

**PoC 범위**:
- 2장 홀카드 표시 (좌측 하단)
- 플레이어 이름 + 칩 스택
- 투명 배경 (OBS Browser Source)
- 960x540 해상도 (경량)

**예상 출력**:
```
┌─────────────────────────────────────┐
│                                     │
│  [테이블 영상 - 배경 투명]            │
│                                     │
│  ┌──┐ ┌──┐                          │
│  │A♠│ │K♦│                          │
│  └──┘ └──┘                          │
│  Player 1                           │
│  Stack: 1,500,000                   │
└─────────────────────────────────────┘
```

---

## 5. 참고 영상 (YouTube 검색 결과)

### 5.1 PokerGFX 스타일

| 영상 | 검색어 | 특징 |
|------|--------|------|
| Live at the Bike | "Live at the Bike overlay" | HUD 수직 배치, 에쿼티 실시간 |
| PokerGFX Demo | "PokerGFX overlay demo" | 공식 프로모션 영상 |

### 5.2 WPT 스타일

| 영상 | 검색어 | 특징 |
|------|--------|------|
| WPT Final Table | "WPT final table 2023" | 하단 풀 바, 9명 동시 표시 |
| WSOP Main Event | "WSOP main event cards up" | ESPN 방송 스타일 |

### 5.3 미니멀 스타일

| 영상 | 검색어 | 특징 |
|------|--------|------|
| Lodge Live | "Lodge Live poker stream" | 카드만 오버레이 |
| Hustler Casino Live | "HCL poker stream overlay" | 깔끔한 미니멀 UI |

---

## 6. Stage별 로드맵

### Stage 0 (2026 H1): 미니멀 스타일 PoC
- 2장 홀카드 표시
- 플레이어 이름 + 스택
- 투명 배경 (960x540)

### Stage 1 (2026 H2): PokerGFX 스타일 복제
- Player HUD (수직 스택)
- 보드카드 + 팟 + 에쿼티
- 애니메이션 (fade-in, slide)

### Stage 2 (2027): WPT 확장
- 9명 플레이어 지원
- 하단 풀 바 옵션
- 브랜딩 영역 (스폰서 로고)

---

## 7. 기술 스택 (확정)

| 레이어 | 기술 | 용도 |
|--------|------|------|
| **Frontend** | HTML5 + CSS3 + Vanilla JS | OBS Browser Source |
| **Backend** | FastAPI (Python) | WebSocket 서버 |
| **Hardware** | ESP32 + MFRC522 | RFID 리더 |
| **Protocol** | WebSocket (JSON) | 실시간 통신 |
| **Deployment** | Localhost:8000 | OBS URL 입력 |

---

## 8. 결론

**Stage 0 PoC용 최적 스타일**: **미니멀 스타일**

**다음 단계**:
1. HTML 목업 생성 (`docs/mockups/overlay-poc-sample.html`)
2. 스크린샷 캡처 (`docs/images/overlay-poc-sample.png`)
3. PRD 문서에 이미지 첨부

---

**참고 문서**:
- `docs/stage-1/PRD-0003-Stage1-PokerGFX-Clone.md` (PokerGFX 상세 기능)
- `docs/mockups/01-viewer-overlay.html` (기존 PokerGFX 목업)
- `docs/research/RESEARCH-RFID-Poker-Suppliers.md` (하드웨어 공급망)

---

*Last Updated: 2026-01-30*
