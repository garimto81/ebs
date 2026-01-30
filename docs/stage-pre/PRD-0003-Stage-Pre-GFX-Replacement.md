# PRD-0003-Stage-Pre: PokerGFX 대체 준비

**Version**: 1.0.0
**Date**: 2026-01-30
**Author**: EBS Project Team
**Status**: Draft
**Parent Document**: [PRD-0003-EBS-RFID-System.md](../PRD-0003-EBS-RFID-System.md)

---

## 1. Executive Summary

### 1.1 Stage-Pre 정의

> **"PokerGFX를 EBS로 대체하기 위한 모든 사전 준비를 완료한다"**

Stage-Pre는 본격적인 RFID 개발(Stage 0)에 앞서 **부품 선정, 공급망 확보, 기술 기반 구축**을 완료하는 준비 단계입니다.

| 항목 | 내용 |
|------|------|
| **목적** | PokerGFX 대체를 위한 모든 사전 준비 완료 |
| **기간** | 2026년 1월 - 2026년 2월 (약 4-6주) |
| **위치** | Stage 0 이전 |
| **산출물** | 결정 문서, 조달 계획, 기술 설계, UI 목업 |

### 1.2 Stage-Pre 목표 요약

| # | 목표 | 상태 | 관련 문서 |
|---|------|------|----------|
| 1 | RFID 모듈 정하기 | **완료** | DECISION-RFID-Module.md |
| 2 | 구매처 및 공급원 확정 | **완료** | PROCUREMENT-RFID-Parts.md |
| 3 | 지속적 공급원 정하기 | **완료** | PROCUREMENT-RFID-Parts.md |
| 4 | RFID 통신 성공 검증 | **Stage 0** | (Stage 0에서 검증) |
| 5 | 오버레이 샘플 및 에디터 기반 | **완료** | RESEARCH-Overlay-Samples.md |
| 6 | 에디터 UI 구성 | **완료** | mockups/card-editor.html |
| 7 | WSOP+ 데이터 연동 방안 | **완료** | PLAN-WSOP-Integration.md |

---

## 2. Stage 구조 업데이트

### 2.1 기존 Stage 구조

| Stage | 기간 | 핵심 목표 |
|-------|------|----------|
| Stage 0 | 2026 H1 | RFID 연결 검증 |
| Stage 1 | 2026 H2 | PokerGFX 100% 복제 |
| Stage 2 | 2027 | WSOP+ DB 연동 |
| Stage 3 | 2028 | EBS 독창적 자동화 |

### 2.2 신규 Stage 구조 (Stage-Pre 추가)

| Stage | 기간 | 핵심 목표 | 슬로건 |
|-------|------|----------|--------|
| **Stage-Pre** | **2026년 1-2월** | **PokerGFX 대체 준비** | **"준비 완료"** |
| Stage 0 | 2026 H1 | RFID 연결 검증 | "연결 증명" |
| Stage 1 | 2026 H2 | PokerGFX 100% 복제 | "동일하게" |
| Stage 2 | 2027 | WSOP+ DB 연동 | "연결한다" |
| Stage 3 | 2028 | EBS 독창적 자동화 | "80% 감소" |

---

## 3. 완료된 작업 (Goals 매핑)

### 3.1 Goal 1: RFID 모듈 정하기 (**완료**)

**결정 문서**: `docs/decisions/DECISION-RFID-Module.md`

| 항목 | 결정 내용 |
|------|----------|
| **선택 모듈** | MFRC522 (RC522) |
| **가격** | $1-5 (AliExpress), 5,000-15,000원 (국내) |
| **읽기 거리** | 3-5cm |
| **인터페이스** | SPI / I2C |
| **프로토콜** | ISO 14443A |
| **카드 호환** | MIFARE Classic / Ultralight |
| **ESP32 호환** | 완벽 |

**선택 근거**:
1. 최저 비용 - DIY 진입장벽 최소화
2. 최다 튜토리얼 & 커뮤니티 라이브러리 (miguelbalboa/rfid 13.8K+ stars)
3. ESP32 3.3V 직접 연결 (레벨 변환 불필요)

**업그레이드 경로**:
```
Stage 0: MFRC522 ($1-5)
    ↓ (성능 요구 시)
Stage 1-2: ST25R3911B ($25-40)
    ↓ (산업용 수준 필요 시)
Stage 3: ST25R3916 또는 커스텀 PCB
```

---

### 3.2 Goal 2-3: 구매처 및 지속 공급원 확정 (**완료**)

**조달 문서**: `docs/procurement/PROCUREMENT-RFID-Parts.md`

#### BOM (Bill of Materials)

| 부품 | 수량 | 단가 (USD) | 소계 | 비고 |
|------|------|-----------|------|------|
| ESP32-WROOM-32 DevKit | 1 | $5-10 | $5-10 | 30핀 권장 |
| MFRC522 모듈 | 2 | $1-5/ea | $2-10 | 여분 1개 |
| MIFARE Classic 1K 카드 | 10 | $0.50/ea | $5 | 테스트용 |
| 점퍼 와이어 (F-F) | 10 | $1/세트 | $1 | 20cm 권장 |
| USB-C 케이블 | 1 | $2 | $2 | 데이터 전송 지원 |
| 브레드보드 (선택) | 1 | $2-3 | $2-3 | 프로토타이핑 |
| **총계** | - | - | **$17-31** | 여유 예산: $50 |

#### 구매처 우선순위

| 순위 | 구매처 | 배송 기간 | 장점 |
|------|--------|----------|------|
| 1순위 | 국내 (디바이스마트, 엘레파츠) | 2-3일 | 품질 보증, 빠른 배송 |
| 2순위 | Amazon | 5-7일 | 반품 용이, 키트 상품 |
| 3순위 | AliExpress | 2-4주 | 최저가, 대량 구매 할인 |

#### 대량 구매 (WSOP 정식 계약 확대 시)

| 업체 | 전문 분야 | MOQ | 연락처 |
|------|----------|-----|--------|
| RFIDup.com | RFID 카드 OEM | 500장+ | director@rfidup.com |
| TP-RFID | 산업용 RFID 모듈 | 100개+ | sales@tp-rfid.com |
| Seeed Studio | ESP32 모듈 | 500개+ | partners@seeed.cc |

---

### 3.3 Goal 4: RFID 통신 성공 (**Stage 0 이관**)

> **참고**: 실제 RFID 통신 검증은 Stage 0에서 수행됩니다.

**Stage 0 목표 (재확인)**:
- MFRC522 - ESP32 SPI 통신 안정화
- 5장 카드 100% 인식
- E2E 지연 < 1초
- 4시간 무중단 운영

**Stage-Pre에서 완료한 준비**:
- [x] 하드웨어 설계 문서 완료 (`docs/stage-0/DESIGN-RFID-Hardware.md`)
- [x] 배선도 및 핀 매핑 정의
- [x] 구현 가이드 작성 (`docs/stage-0/GUIDE-RFID-Implementation.md`)

---

### 3.4 Goal 5: 오버레이 샘플 및 기술 기반 (**완료**)

**리서치 문서**: `docs/research/RESEARCH-Overlay-Samples.md`

#### 3종 오버레이 스타일 분석 완료

| 스타일 | 대표 사례 | 영상 영역 | 구현 복잡도 | Stage |
|--------|----------|----------|------------|-------|
| **미니멀** | Lodge Live, HCL | 95% | 낮음 | **Stage 0** |
| PokerGFX | Live at the Bike | 80% | 높음 | Stage 1 |
| WPT | World Poker Tour | 70% | 중간 | Stage 2 |

#### Stage 0 PoC 오버레이 선택: **미니멀 스타일**

**목업 완료**: `docs/mockups/overlay-poc-sample.html`

| 항목 | 사양 |
|------|------|
| 해상도 | 960x540 (경량) / 1920x1080 (Full HD) |
| 배경 | 투명 (OBS Browser Source) |
| 구성요소 | 2장 홀카드 + 플레이어 이름 + 칩 스택 |
| 애니메이션 | fade-in 400ms |
| 데이터 연동 | WebSocket (ws://localhost:8000/ws) |

#### 오버레이 기술 스택 확정

| 레이어 | 기술 | 용도 |
|--------|------|------|
| Frontend | HTML5 + CSS3 + Vanilla JS | OBS Browser Source |
| Backend | FastAPI (Python) | WebSocket 서버 |
| Hardware | ESP32 + MFRC522 | RFID 리더 |
| Protocol | WebSocket (JSON) | 실시간 통신 |
| Deployment | Localhost:8000 | OBS URL 입력 |

---

### 3.5 Goal 6: 에디터 UI 구성 (**완료**)

**목업**: `docs/mockups/card-editor.html`

#### Card-UID Mapping Editor 기능

| 기능 | 설명 | 상태 |
|------|------|------|
| 카드 목록 | 54장 카드 테이블 (52장 + 조커 2장) | 완료 |
| 상태 표시 | Mapped / Unmapped / Learning | 완료 |
| 학습 모드 | 개별 카드 UID 학습 | 완료 |
| 배치 학습 | Learn All (Sequential) | 완료 |
| Import/Export | JSON 형식 매핑 데이터 | 완료 |
| 필터 | Suit / Status / Search | 완료 |
| RFID 상태 | Reader Connected 인디케이터 | 완료 |

#### 에디터 API 설계 완료

**설계 문서**: `docs/design/DESIGN-Card-API.md`

| Endpoint | Method | 용도 |
|----------|--------|------|
| `/api/cards` | GET | 전체 카드 목록 조회 |
| `/api/cards/{id}` | GET | 개별 카드 조회 |
| `/api/cards/{id}/uid` | PUT | UID 매핑 업데이트 |
| `/api/cards/{id}/uid` | DELETE | UID 매핑 삭제 |
| `/api/cards/learn` | POST | 학습 모드 시작 |
| `/api/cards/export` | POST | JSON 내보내기 |
| `/api/cards/import` | POST | JSON 가져오기 |

#### 데이터베이스 스키마 완료

**설계 문서**: `docs/design/DESIGN-Database-Schema.md`
**초기 데이터**: `server/db/init.sql`

```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE,           -- RFID UID (초기값 NULL)
    suit TEXT NOT NULL,        -- spades, hearts, diamonds, clubs, joker
    rank TEXT NOT NULL,        -- A, 2-10, J, Q, K, JOKER
    display TEXT NOT NULL,     -- "A♠", "K♥"
    value INTEGER NOT NULL,    -- 0-14
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

### 3.6 Goal 7: WSOP+ 데이터 연동 방안 (**완료**)

**리서치 문서**: `docs/research/RESEARCH-WSOP-Integration.md`
**계획 문서**: `docs/plans/PLAN-WSOP-Integration.md`

#### 조사 결과 요약

| 항목 | 결과 |
|------|------|
| WSOP 공개 API | **미확인** (공개 개발자 API 없음) |
| 파트너 API | NDA + 데이터 라이센스 계약 필요 (추정 $10K-100K/년) |
| 권장 방식 | Stage 0-1: 수동 입력 / CSV Import |

#### 3단계 연동 시나리오

| 시나리오 | 적용 Stage | 복잡도 | 권장 |
|----------|-----------|--------|------|
| **1. 완전 수동 입력** | Stage 0-1 | 낮음 | **권장** |
| **2. CSV Import + 반자동** | Stage 1 | 중간 | **권장** |
| 3. 파트너 API 연동 | Stage 2+ | 높음 | 협의 필요 |

#### 필요 데이터 포인트

| 데이터 | 우선순위 | Stage 0-1 대응 | Stage 2+ |
|--------|----------|----------------|----------|
| 플레이어명 | P0 | 수동 입력 | API/CSV |
| 칩 카운트 | P0 | 수동 입력 | 실시간 API |
| 현재 액션 | P1 | EBS 자체 기록 | WebSocket |
| 핸드 히스토리 | P1 | EBS 자체 기록 | 배치 API |
| 대회 정보 | P2 | 수동 입력 | CSV Import |

#### Stage 2 로드맵 (WSOP 협의)

| 시점 | 작업 |
|------|------|
| 2027 Q1 | WSOP 담당자 컨택, CSV 포맷 협의 |
| 2027 Q2 | API 스펙 획득 (협의 성공 시), 칩 동기화 구현 |
| 2027 Q3 | 플레이어/핸드 히스토리 동기화 |
| 2027 Q4 | 안정화, Stage 2 Gate 검증 |

---

## 4. PokerGFX 대체 준비 체크리스트

### 4.1 하드웨어 준비

| 항목 | 상태 | 담당 | 비고 |
|------|------|------|------|
| [x] RFID 모듈 선정 (MFRC522) | 완료 | - | DECISION-RFID-Module.md |
| [x] MCU 선정 (ESP32-WROOM-32) | 완료 | - | DESIGN-RFID-Hardware.md |
| [x] 부품 BOM 작성 | 완료 | - | PROCUREMENT-RFID-Parts.md |
| [x] 구매처 목록 확정 | 완료 | - | PROCUREMENT-RFID-Parts.md |
| [x] 배선도 작성 | 완료 | - | DESIGN-RFID-Hardware.md |
| [ ] 부품 구매 | **대기** | 담당자 | Stage 0 시작 시 |
| [ ] 하드웨어 조립 | **대기** | 담당자 | Stage 0 Phase 0-1 |

### 4.2 소프트웨어 준비

| 항목 | 상태 | 담당 | 비고 |
|------|------|------|------|
| [x] DB 스키마 설계 | 완료 | - | DESIGN-Database-Schema.md |
| [x] 초기 데이터 SQL | 완료 | - | server/db/init.sql |
| [x] REST API 설계 | 완료 | - | DESIGN-Card-API.md |
| [x] WebSocket 프로토콜 정의 | 완료 | - | DESIGN-Card-API.md |
| [x] Card Editor UI 목업 | 완료 | - | mockups/card-editor.html |
| [x] Overlay PoC 목업 | 완료 | - | mockups/overlay-poc-sample.html |
| [ ] 서버 구현 (FastAPI) | **대기** | 백엔드 | Stage 0 Phase 0-3 |
| [ ] 프론트엔드 구현 (React) | **대기** | 프론트 | Stage 0 Phase 0-4 |

### 4.3 데이터 준비

| 항목 | 상태 | 담당 | 비고 |
|------|------|------|------|
| [x] WSOP+ API 조사 | 완료 | - | RESEARCH-WSOP-Integration.md |
| [x] 연동 시나리오 정의 | 완료 | - | PLAN-WSOP-Integration.md |
| [x] CSV Import 포맷 설계 | 완료 | - | PLAN-WSOP-Integration.md |
| [ ] 플레이어 샘플 데이터 | **대기** | 담당자 | Stage 1 |
| [ ] WSOP 담당자 컨택 | **2027** | 담당자 | Stage 2 |

### 4.4 운영 준비

| 항목 | 상태 | 담당 | 비고 |
|------|------|------|------|
| [x] 오버레이 스타일 결정 | 완료 | - | RESEARCH-Overlay-Samples.md |
| [x] Stage별 로드맵 정의 | 완료 | - | PRD-0003-EBS-RFID-System.md |
| [ ] 운영자 교육 자료 | **대기** | 담당자 | Stage 1 Gate |
| [ ] OBS 연동 테스트 | **대기** | 담당자 | Stage 1 |

---

## 5. 추가 필요 기능 (GFX 개선 희망)

### 5.1 PokerGFX 대비 EBS 개선 목표

| 영역 | PokerGFX 현황 | EBS 개선 목표 | Stage |
|------|--------------|--------------|-------|
| **운영 복잡도** | 높음 (전담 인력) | 80% 간편화 | Stage 3 |
| **정보 입력** | 수동 중심 | 스마트 예측 + 최소 수동 | Stage 2-3 |
| **시청자 정보** | 기본 | 풍부 (통계, 확률, 히스토리) | Stage 2 |
| **WSOP+ 연동** | 없음 | 완전 통합 | Stage 2 |
| **DB 소유권** | 외부 의존 | 자체 완전 소유 | **핵심** |

### 5.2 사용자 요청 기반 추가 기능

#### 5.2.1 백오피스 기능 (Stage 1)

| 기능 | 설명 | 우선순위 |
|------|------|----------|
| **Card-UID 매핑 에디터** | RFID ↔ 카드 매핑 관리 | P0 (완료) |
| **학습 모드** | 새 카드 덱 자동 학습 | P0 |
| **매핑 Export/Import** | JSON 기반 백업/복원 | P1 |
| **다중 덱 관리** | 여러 RFID 덱 관리 | P2 (Stage 2) |

#### 5.2.2 오버레이 기능 (Stage 1-2)

| 기능 | 설명 | 우선순위 |
|------|------|----------|
| **홀카드 표시** | 2장 카드 실시간 표시 | P0 |
| **플레이어 HUD** | 이름, 칩, 액션 표시 | P0 |
| **보드카드 표시** | Flop/Turn/River | P1 |
| **팟 크기 표시** | 실시간 팟 계산 | P1 |
| **승률 계산** | 에쿼티 자동 계산 | P2 (Stage 2) |
| **플레이어 통계** | VPIP, PFR, 3Bet% | P2 (Stage 2) |
| **핸드 히스토리** | 과거 핸드 재생 | P3 (Stage 3) |

#### 5.2.3 자동화 기능 (Stage 2-3)

| 기능 | 설명 | 우선순위 |
|------|------|----------|
| **자동 팟 계산** | 베팅 액션 기반 자동 계산 | P1 (Stage 2) |
| **자동 칩 추적** | 컴퓨터 비전 기반 | P2 (Stage 3) |
| **스마트 베팅 예측** | 이전 액션 기반 예측 | P2 (Stage 3) |
| **핸드 종료 자동 감지** | 쇼다운/폴드 감지 | P2 (Stage 3) |
| **하이라이트 자동 태깅** | 빅 팟, 블러프, 배드빗 | P3 (Stage 3) |

---

## 6. WSOP+ 데이터 활용 방안

### 6.1 데이터 소스

| 데이터 소스 | 현재 상태 | 활용 방안 |
|------------|----------|----------|
| **WSOP.com** | 공개 페이지 (읽기 전용) | 플레이어 프로필 참조 |
| **WSOP+ 앱** | API 비공개 | 파트너십 체결 시 연동 |
| **CSV 명단** | WSOP 내부 제공 (예상) | Stage 1 CSV Import |
| **EBS 자체 DB** | 신규 구축 | **Single Source of Truth** |

### 6.2 활용 시나리오

#### 시나리오 A: 토너먼트 시작 전

```
1. WSOP 공식 명단 CSV 다운로드 (또는 수동 입력)
2. EBS CSV Import 도구로 플레이어 일괄 등록
3. 시작 칩 카운트 입력
4. RFID 카드 덱 확인 (매핑 상태)
5. 방송 준비 완료
```

#### 시나리오 B: 토너먼트 진행 중

```
1. RFID가 홀카드 자동 감지 → 오버레이 표시
2. 운영자가 액션 입력 (원클릭)
3. EBS가 팟 자동 계산
4. 핸드 히스토리 자동 기록
5. 칩 카운트 수동 업데이트 (브레이크 시)
```

#### 시나리오 C: 토너먼트 종료 후 (Stage 2+)

```
1. 핸드 히스토리 Export (Pokerstars HH 포맷)
2. 플레이어 통계 집계
3. 하이라이트 자동 생성
4. 데이터 아카이브
5. (Stage 2+) WSOP+ DB 동기화
```

### 6.3 데이터 흐름도

```
┌─────────────────────────────────────────────────────────────┐
│                    Stage 0-1 (2026)                         │
└─────────────────────────────────────────────────────────────┘

[RFID 카드] ──▶ [ESP32] ──▶ [Python Server] ──▶ [EBS DB]
                                    │
                                    ▼
[운영자 입력] ────────────────▶ [EBS DB] ──▶ [오버레이 UI]
                                    │
                                    ▼
[CSV Import] ─────────────────▶ [EBS DB]

┌─────────────────────────────────────────────────────────────┐
│                    Stage 2+ (2027+)                         │
└─────────────────────────────────────────────────────────────┘

[WSOP+ API] ◀───────▶ [EBS Sync Service] ◀───────▶ [EBS DB]
                            │
                            ▼
                     [양방향 동기화]
                     - 플레이어 정보
                     - 칩 카운트
                     - 핸드 히스토리
```

---

## 7. Stage-Pre Gate (완료 조건)

### 7.1 체크리스트

| 조건 | 상태 | 검증 방법 |
|------|------|----------|
| RFID 모듈 선정 완료 | **완료** | DECISION-RFID-Module.md |
| 구매처 및 BOM 확정 | **완료** | PROCUREMENT-RFID-Parts.md |
| 오버레이 스타일 결정 | **완료** | RESEARCH-Overlay-Samples.md |
| 에디터 UI 목업 완료 | **완료** | mockups/card-editor.html |
| 오버레이 PoC 목업 완료 | **완료** | mockups/overlay-poc-sample.html |
| DB 스키마 설계 완료 | **완료** | DESIGN-Database-Schema.md |
| API 설계 완료 | **완료** | DESIGN-Card-API.md |
| WSOP+ 연동 방안 수립 | **완료** | PLAN-WSOP-Integration.md |
| 부품 구매 준비 | **대기** | Stage 0 시작 시 |

### 7.2 Gate 통과 조건

**모든 문서 완료** + **팀 합의** = Stage 0 착수 가능

### 7.3 프로덕션 RFID 모듈 스펙 (신규)

> **"RFID 통신 성공 = 프로덕션 스펙을 충족하는 모듈에서의 성공"**

**스펙 문서**: `docs/specs/SPEC-RFID-Production-Module.md`

| 항목 | 정의 |
|------|------|
| **최종 사양 모듈** | ST25R3911B (또는 동등 스펙 충족 모듈) |
| **학습용 모듈** | MFRC522 (Stage 0 초기) |
| **검증 방법** | SPEC 문서 P0 요구사항 10항목 PASS |

**Stage 0 Gate 추가 조건**:
- [ ] ST25R3911B로 프로덕션 스펙 검증 완료
- [ ] 10/10 P0 요구사항 PASS

### 7.4 Stage-Pre 완료 선언

> **Stage-Pre Gate 통과: 2026-01-30**

| 항목 | 결과 |
|------|:----:|
| 문서 완료율 | **100%** (9/9 완료) |
| 프로덕션 스펙 정의 | **완료** |
| Architect 검증 | **APPROVED** |
| Gate 조건 충족 | **YES** |

**다음 단계**: Stage 0 착수 (하드웨어 구매 시작)

---

## 8. 산출물 목록

### 8.1 결정 문서

| 문서 | 경로 | 상태 |
|------|------|------|
| RFID 모듈 선택 | `docs/decisions/DECISION-RFID-Module.md` | 완료 |

### 8.2 조달 문서

| 문서 | 경로 | 상태 |
|------|------|------|
| 부품 조달 계획 | `docs/procurement/PROCUREMENT-RFID-Parts.md` | 완료 |

### 8.3 리서치 문서

| 문서 | 경로 | 상태 |
|------|------|------|
| WSOP+ 연동 가능성 조사 | `docs/research/RESEARCH-WSOP-Integration.md` | 완료 |
| 오버레이 스타일 조사 | `docs/research/RESEARCH-Overlay-Samples.md` | 완료 |

### 8.4 설계 문서

| 문서 | 경로 | 상태 |
|------|------|------|
| 데이터베이스 스키마 | `docs/design/DESIGN-Database-Schema.md` | 완료 |
| Card API 설계 | `docs/design/DESIGN-Card-API.md` | 완료 |

### 8.5 계획 문서

| 문서 | 경로 | 상태 |
|------|------|------|
| WSOP+ 연동 계획 | `docs/plans/PLAN-WSOP-Integration.md` | 완료 |

### 8.6 목업

| 목업 | 경로 | 상태 |
|------|------|------|
| Card-UID Mapping Editor | `docs/mockups/card-editor.html` | 완료 |
| Overlay PoC (Minimal) | `docs/mockups/overlay-poc-sample.html` | 완료 |

### 8.7 초기 데이터

| 파일 | 경로 | 상태 |
|------|------|------|
| DB 초기화 스크립트 | `server/db/init.sql` | 완료 |

---

## 9. 다음 단계 (Stage 0 착수)

### 9.1 즉시 실행 (2026년 2월)

1. **부품 구매**
   - 국내 쇼핑몰 (디바이스마트, 엘레파츠)에서 시나리오 B ($50) 구매
   - 예상 도착: 2-3일

2. **환경 설정**
   - Arduino IDE 설치
   - ESP32 보드 패키지 추가
   - MFRC522 라이브러리 설치

3. **하드웨어 조립**
   - 배선도 (`docs/stage-0/DESIGN-RFID-Hardware.md`) 참조
   - ESP32 + MFRC522 연결

### 9.2 Stage 0 Phase 진행

| Phase | 기간 | 목표 |
|-------|------|------|
| Phase 0-1 | 2주 | 환경 설정, Blink 예제 |
| Phase 0-2 | 4주 | RFID 읽기, 카드 인식 |
| Phase 0-3 | 4주 | Serial 통신, JSON 포맷 |
| Phase 0-4 | 6주 | UI 연동, WebSocket |
| Phase 0-5 | 4주 | 안정화, Gate 검증 |

### 9.3 참조 문서

- Stage 0 PRD: `docs/stage-0/PRD-0003-Stage0-RFID-Connection.md`
- 하드웨어 설계: `docs/stage-0/DESIGN-RFID-Hardware.md`
- 구현 가이드: `docs/stage-0/GUIDE-RFID-Implementation.md`

---

## 10. 문서 정보

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0.0 |
| **작성일** | 2026-01-30 |
| **상태** | Draft |
| **작성자** | EBS Project Team |
| **검토자** | - |
| **승인자** | - |

### 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2026-01-30 | 초안 작성 | EBS Team |

---

**문서 종료**
