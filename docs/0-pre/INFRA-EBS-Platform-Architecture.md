# EBS Platform Architecture: Infrastructure as Foundation

**Version**: 1.0.0
**Date**: 2026-02-02
**Status**: Draft
**Author**: EBS Architecture Team

---

## 1. Executive Summary

### 1.1 EBS의 새로운 정체성

> **"EBS는 RFID 프로젝트가 아닙니다. 포커 프로덕션의 데이터 중심축입니다."**

EBS의 본질적 가치는 하드웨어에 있지 않습니다. RFID 보드는 전체 시스템의 5%에 불과합니다.
EBS는 **포커 방송 프로덕션을 위한 데이터 인프라스트럭처**로서:

| 역할 | 설명 |
|------|------|
| **데이터 생산** | RFID 카드 인식, Operator 액션 입력, WSOP+ 연동 |
| **데이터 처리** | 승률 계산, 팟 계산, 통계 집계, 이벤트 처리 |
| **데이터 제공** | Viewer Overlay, Operator Console, Analytics, 외부 시스템 |
| **데이터 저장** | 핸드 히스토리, 플레이어 통계, 방송 메타데이터 |

### 1.2 RFID 프로젝트 vs 인프라 관점의 차이

| 관점 | RFID 프로젝트 (좁은 시각) | 인프라 플랫폼 (넓은 시각) |
|------|--------------------------|-------------------------|
| **범위** | ESP32 + RFID 모듈 | 전체 데이터 파이프라인 |
| **성공 기준** | 카드 읽기 성공 | 시스템 가용성 99.9% |
| **확장성** | 단일 테이블 | 동시 10개 테이블 |
| **데이터** | 즉시 소비 | 축적 및 분석 |
| **인터페이스** | 단방향 (RFID→화면) | 다중 소비자 API |
| **운영** | 개발자 관리 | SLA 기반 운영 |

### 1.3 점진적 인프라화 원칙

> **Stage 0-1 일정에 영향을 주지 않으면서, 인프라 기반을 점진적으로 구축합니다.**

```
Stage 0-1: 기능 구현 우선 (인프라 패턴 준비)
     ↓
Stage 2: 인프라 기반 확장 (Message Queue, Multi-table)
     ↓
Stage 3: 완전한 인프라 (Event Sourcing, Data Lake)
```

---

## 2. Architecture Overview

### 2.1 기존 3-Layer vs 목표 5-Layer

#### 현재 아키텍처 (3-Layer)

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Presentation                                      │
│  React Frontend, OBS Overlay                                │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Application                                       │
│  FastAPI Server, WebSocket, Serial Manager                  │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Hardware                                          │
│  ESP32, MFRC522/ST25R3911B                                  │
└─────────────────────────────────────────────────────────────┘
```

**한계점:**
- 단일 진입점 (WebSocket만)
- 데이터 소비자 확장 어려움
- 처리 로직과 API 결합
- 모니터링/관측성 부재

#### 목표 아키텍처 (5-Layer)

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: Presentation Layer                                │
│  Viewer Overlay, Operator Console, Analytics Dashboard      │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: API Layer                                         │
│  REST API, WebSocket Gateway, GraphQL (Future), Auth        │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: Processing Layer                                  │
│  Event Processor, Equity Calculator, Pot Calculator         │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Data Layer                                        │
│  Event Store, Message Queue, Cache, Time-Series DB          │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Hardware Layer                                    │
│  RFID Readers, Serial Communication, Device Management      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 각 Layer 정의

#### Layer 1: Hardware Layer

| 구성요소 | 역할 | Stage |
|----------|------|:-----:|
| **RFID Readers** | 카드 UID 읽기 (MFRC522 → ST25R3911B) | 0+ |
| **Serial Communication** | ESP32 ↔ Server JSON 통신 | 0+ |
| **Device Management** | 리더 상태 모니터링, 자동 재연결 | 1+ |
| **Multi-Reader Support** | 최대 7개 리더 동시 관리 | 1+ |

**책임:**
- 물리적 카드 인식
- UID 추출 및 JSON 직렬화
- 하드웨어 상태 보고

#### Layer 2: Data Layer

| 구성요소 | 역할 | Stage 0-1 | Stage 2+ |
|----------|------|:---------:|:--------:|
| **Primary DB** | 영구 데이터 저장 | SQLite | PostgreSQL |
| **Event Store** | 이벤트 로그 저장 | SQLite Table | Append-only Store |
| **Message Queue** | 이벤트 전파 | In-memory (asyncio) | Redis Streams |
| **Cache** | 핫 데이터 캐싱 | Dict (Python) | Redis |
| **Time-Series** | 메트릭 저장 | 없음 | InfluxDB/TimescaleDB |

**책임:**
- 데이터 영속성 보장
- 이벤트 순서 보장
- 빠른 조회 지원

#### Layer 3: Processing Layer

| 구성요소 | 역할 | 특징 |
|----------|------|------|
| **Event Processor** | 이벤트 라우팅 및 처리 | Stateless, Idempotent |
| **Equity Calculator** | 승률/아웃츠 계산 | Monte Carlo, 병렬 처리 |
| **Pot Calculator** | 팟 사이즈 계산 | 액션 기반 연산 |
| **Statistics Aggregator** | 플레이어 통계 집계 | VPIP, PFR, 3Bet% |
| **Hand Detector** | 핸드 종료 감지 | 규칙 기반 |

**책임:**
- 비즈니스 로직 실행
- 계산 결과 캐싱
- 처리 결과 이벤트 발행

#### Layer 4: API Layer

| 구성요소 | 역할 | 프로토콜 |
|----------|------|----------|
| **REST API** | 동기 요청/응답 | HTTP/HTTPS |
| **WebSocket Gateway** | 실시간 양방향 | WS/WSS |
| **Auth Service** | 인증/인가 | JWT, API Key |
| **Rate Limiter** | 요청 제한 | Token Bucket |
| **API Versioning** | 버전 관리 | URL Path (/api/v1/) |

**책임:**
- 외부 인터페이스 제공
- 인증/인가 처리
- 요청 검증 및 변환

#### Layer 5: Presentation Layer

| 구성요소 | 사용자 | 기능 |
|----------|--------|------|
| **Viewer Overlay** | 시청자 | 홀카드, 승률, 팟 표시 |
| **Operator Console** | 운영자 | 액션 입력, 플레이어 관리 |
| **Admin Dashboard** | 관리자 | 시스템 상태, 설정 |
| **Analytics Platform** | 분석가 | 데이터 조회, 리포트 |

**책임:**
- 사용자별 최적화된 인터페이스
- 실시간 데이터 시각화
- 사용자 입력 처리

---

## 3. Data Flow Diagram

### 3.1 데이터 생산자 (Producers)

```
┌─────────────────────────────────────────────────────────────────┐
│                       DATA PRODUCERS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│  │ RFID Reader │   │  Operator   │   │    WSOP+ API        │   │
│  │   (ESP32)   │   │   Console   │   │   (External)        │   │
│  └──────┬──────┘   └──────┬──────┘   └──────────┬──────────┘   │
│         │                 │                      │              │
│         ▼                 ▼                      ▼              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐   │
│  │ card_read   │   │ action_     │   │ player_sync         │   │
│  │ event       │   │ input       │   │ chip_sync           │   │
│  └─────────────┘   └─────────────┘   └─────────────────────┘   │
│                                                                 │
│  Event Types:                                                   │
│  - card_read: UID, reader_id, timestamp                         │
│  - action_input: player_id, action, amount                      │
│  - player_sync: name, stack, statistics                         │
│  - chip_sync: player_id, new_stack                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 생산자 | 데이터 유형 | 빈도 | Stage |
|--------|------------|:----:|:-----:|
| **RFID Reader** | 카드 UID, 리더 ID, 타임스탬프 | ~50ms 간격 | 0+ |
| **Operator Console** | 액션, 베팅 금액, 플레이어 선택 | 이벤트 기반 | 1+ |
| **WSOP+ API** | 플레이어 정보, 칩 카운트, 토너먼트 정보 | 폴링 (5초) / 이벤트 | 2+ |

### 3.2 데이터 소비자 (Consumers)

```
┌─────────────────────────────────────────────────────────────────┐
│                       DATA CONSUMERS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    EBS API Gateway                       │   │
│  │         (REST + WebSocket + Auth)                        │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │                                    │
│            ┌───────────────┼───────────────┐                    │
│            ▼               ▼               ▼                    │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │   Viewer    │   │  Operator   │   │  Analytics  │           │
│  │  Overlay    │   │   Console   │   │  Platform   │           │
│  │ (시청자)    │   │  (운영자)    │   │  (분석가)    │           │
│  └─────────────┘   └─────────────┘   └─────────────┘           │
│        ▲                   ▲               ▲                    │
│        │                   │               │                    │
│  ┌─────┴─────┐       ┌─────┴─────┐   ┌─────┴─────┐             │
│  │WebSocket  │       │WebSocket  │   │ REST API  │             │
│  │(Real-time)│       │+ REST     │   │(Batch)    │             │
│  └───────────┘       └───────────┘   └───────────┘             │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐                             │
│  │  Content    │   │  External   │                             │
│  │   System    │   │  Partners   │                             │
│  │(콘텐츠 팀)   │   │  (Future)   │                             │
│  └─────────────┘   └─────────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 소비자 | 데이터 요구 | 프로토콜 | 지연 허용 | Stage |
|--------|------------|----------|:--------:|:-----:|
| **Viewer Overlay** | 홀카드, 승률, 팟 | WebSocket | < 200ms | 1+ |
| **Operator Console** | 테이블 상태, 플레이어 | WebSocket + REST | < 100ms | 1+ |
| **Analytics Platform** | 핸드 히스토리, 통계 | REST (Batch) | 분 단위 | 2+ |
| **Content System** | 하이라이트 이벤트 | REST + Webhook | 초 단위 | 3+ |
| **External Partners** | 공개 데이터 | REST API | 분 단위 | Future |

### 3.3 전체 데이터 흐름 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EBS DATA FLOW ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

  PRODUCERS                    PROCESSING                      CONSUMERS
  ═════════                    ══════════                      ═════════

  ┌─────────┐                                                  ┌──────────┐
  │  RFID   │─card_read─┐                              ┌──WS──▶│ Viewer   │
  │ Reader  │           │                              │       │ Overlay  │
  └─────────┘           │   ┌───────────────────────┐  │       └──────────┘
                        ├──▶│                       │  │
  ┌─────────┐           │   │    EVENT PROCESSOR    │  │       ┌──────────┐
  │Operator │─action────┤   │                       │──┼──WS──▶│ Operator │
  │ Console │           │   │  ┌─────────────────┐  │  │       │ Console  │
  └─────────┘           │   │  │ Equity Calc     │  │  │       └──────────┘
                        │   │  │ Pot Calc        │  │  │
  ┌─────────┐           │   │  │ Stats Aggregator│  │  │       ┌──────────┐
  │ WSOP+   │─sync──────┘   │  └─────────────────┘  │──┼─REST─▶│Analytics │
  │  API    │               │                       │  │       │ Platform │
  └─────────┘               └───────────┬───────────┘  │       └──────────┘
                                        │              │
                                        ▼              │       ┌──────────┐
                            ┌───────────────────────┐  └─REST─▶│ Content  │
                            │      DATA LAYER       │          │ System   │
                            │                       │          └──────────┘
                            │  ┌─────┐ ┌─────────┐  │
                            │  │ DB  │ │ Queue   │  │
                            │  └─────┘ └─────────┘  │
                            │  ┌─────┐ ┌─────────┐  │
                            │  │Cache│ │Event Log│  │
                            │  └─────┘ └─────────┘  │
                            └───────────────────────┘

  Legend:
  ─────── : Synchronous flow
  ═══════ : Async message
  WS      : WebSocket (real-time)
  REST    : HTTP REST API (request/response)
```

---

## 4. API Contract

### 4.1 EBS 제공 API

#### 4.1.1 Hands API

```
GET  /api/v1/events/{event_id}/hands
GET  /api/v1/events/{event_id}/hands/{hand_id}
POST /api/v1/events/{event_id}/hands (Admin only)
```

**Response Example:**
```json
{
  "hand_id": "h_2026020215001",
  "event_id": "evt_wsop2026_me",
  "table_id": "table_01",
  "hand_number": 42,
  "timestamp": "2026-02-02T15:00:01Z",
  "players": [
    {
      "seat": 1,
      "player_id": "p_negreanu",
      "name": "Daniel Negreanu",
      "stack": 1245000,
      "hole_cards": ["Ah", "Kh"]
    }
  ],
  "community_cards": ["Qh", "Jh", "Th", "2c", "3d"],
  "actions": [
    {
      "street": "preflop",
      "player_id": "p_negreanu",
      "action": "raise",
      "amount": 25000
    }
  ],
  "pot_total": 125000,
  "winner": "p_negreanu",
  "winning_hand": "Royal Flush"
}
```

#### 4.1.2 Players API

```
GET  /api/v1/events/{event_id}/players
GET  /api/v1/events/{event_id}/players/{player_id}
GET  /api/v1/events/{event_id}/players/{player_id}/statistics
```

**Response Example:**
```json
{
  "player_id": "p_negreanu",
  "name": "Daniel Negreanu",
  "nationality": "CA",
  "current_stack": 1245000,
  "starting_stack": 1000000,
  "statistics": {
    "vpip": 28.5,
    "pfr": 22.1,
    "three_bet": 9.2,
    "fold_to_three_bet": 62.0,
    "c_bet": 71.5,
    "hands_played": 127
  },
  "wsop_profile": {
    "bracelets": 6,
    "career_earnings": 46000000,
    "event_cashes": 89
  }
}
```

#### 4.1.3 Stream API (WebSocket)

```
WS /api/v1/events/{event_id}/stream
```

**Message Types:**

| Type | Direction | Description |
|------|-----------|-------------|
| `card_detected` | Server → Client | 카드 인식 이벤트 |
| `action_recorded` | Server → Client | 액션 기록 이벤트 |
| `equity_update` | Server → Client | 승률 업데이트 |
| `pot_update` | Server → Client | 팟 업데이트 |
| `hand_complete` | Server → Client | 핸드 종료 이벤트 |
| `player_update` | Server → Client | 플레이어 정보 업데이트 |
| `subscribe` | Client → Server | 구독 요청 |
| `ping` | Bidirectional | 연결 상태 확인 |

**Example Message:**
```json
{
  "type": "card_detected",
  "event_id": "evt_wsop2026_me",
  "table_id": "table_01",
  "seat": 1,
  "card": {
    "suit": "hearts",
    "rank": "A",
    "display": "Ah"
  },
  "timestamp": "2026-02-02T15:00:01.123Z"
}
```

#### 4.1.4 Statistics API

```
GET /api/v1/events/{event_id}/statistics
GET /api/v1/events/{event_id}/statistics/summary
GET /api/v1/events/{event_id}/statistics/hands
GET /api/v1/events/{event_id}/statistics/players
```

**Response Example:**
```json
{
  "event_id": "evt_wsop2026_me",
  "period": "2026-02-02T12:00:00Z/2026-02-02T18:00:00Z",
  "hands_played": 342,
  "average_pot": 85000,
  "largest_pot": 1250000,
  "showdowns": 89,
  "players_remaining": 127,
  "average_stack": 985000
}
```

### 4.2 인증/인가 모델

#### 4.2.1 인증 방식

| 방식 | 용도 | Stage |
|------|------|:-----:|
| **API Key** | 외부 시스템 연동 | 2+ |
| **JWT** | 내부 서비스, Operator Console | 1+ |
| **Session** | Admin Dashboard | 1+ |

#### 4.2.2 API Key 인증

```http
GET /api/v1/events/evt_wsop2026_me/hands
Authorization: Bearer ebs_api_1234567890abcdef
```

**API Key 구조:**
```
ebs_api_{random_32_chars}

Permissions:
- read:hands      # 핸드 데이터 조회
- read:players    # 플레이어 데이터 조회
- read:statistics # 통계 조회
- write:actions   # 액션 입력 (Operator only)
```

#### 4.2.3 JWT 인증

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "operator01",
  "password": "..."
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGc..."
}
```

**JWT Claims:**
```json
{
  "sub": "user_id",
  "role": "operator",
  "permissions": ["read:*", "write:actions"],
  "exp": 1738512000,
  "iat": 1738508400
}
```

#### 4.2.4 역할 기반 권한

| Role | Permissions | Description |
|------|-------------|-------------|
| `viewer` | read:hands, read:statistics | 시청자 (공개 데이터만) |
| `operator` | read:*, write:actions | 테이블 운영자 |
| `analyst` | read:* | 데이터 분석가 |
| `admin` | read:*, write:*, manage:* | 시스템 관리자 |

---

## 5. SLA Definition

### 5.1 가용성 (Availability)

| 구성요소 | 목표 | 허용 다운타임/월 | Stage |
|----------|:----:|:---------------:|:-----:|
| **API Gateway** | 99.9% | < 43.8분 | 2+ |
| **WebSocket** | 99.5% | < 3.6시간 | 1+ |
| **Processing Layer** | 99.9% | < 43.8분 | 2+ |
| **Database** | 99.95% | < 21.9분 | 2+ |

**Stage 0-1 목표:**
- 4시간 무중단 테스트 통과
- 수동 복구 허용 (5분 이내)

**Stage 2+ 목표:**
- 99.9% 가용성 (SLA)
- 자동 장애 복구

### 5.2 지연 (Latency)

| 구간 | p50 | p95 | p99 | Stage |
|------|:---:|:---:|:---:|:-----:|
| **카드 인식 → WebSocket** | 100ms | 200ms | 500ms | 1+ |
| **REST API 응답** | 50ms | 200ms | 500ms | 1+ |
| **승률 계산** | 20ms | 50ms | 100ms | 1+ |
| **DB 쿼리** | 10ms | 50ms | 100ms | 1+ |

**Stage 0 목표:**
- E2E 지연: 카드 → 화면 < 1초 (검증 통과 기준)

### 5.3 데이터 복구 목표

| 메트릭 | 정의 | 목표 | Stage |
|--------|------|:----:|:-----:|
| **RPO** (Recovery Point Objective) | 최대 데이터 손실 | 1 핸드 | 2+ |
| **RTO** (Recovery Time Objective) | 서비스 복구 시간 | 5분 | 2+ |

**Stage 0-1:**
- RPO: 세션 데이터 (메모리 기반)
- RTO: 수동 재시작 (5분 이내)

**Stage 2+:**
- RPO: 최대 1핸드 (Event Sourcing)
- RTO: 자동 복구 5분 이내

### 5.4 처리량 (Throughput)

| 메트릭 | 목표 | Stage |
|--------|:----:|:-----:|
| **동시 WebSocket 연결** | 1,000+ | 2+ |
| **초당 이벤트 처리** | 100+ events/sec | 2+ |
| **동시 테이블** | 10개 | 3 |
| **핸드 히스토리 쿼리** | 10,000 rows/sec | 2+ |

---

## 6. Scalability Plan

### 6.1 동시 테이블 지원

| Stage | 테이블 수 | 아키텍처 | 인프라 |
|:-----:|:---------:|----------|--------|
| **0-1** | 1개 | 단일 인스턴스 | SQLite, In-memory |
| **2** | 3개 | 멀티 프로세스 | PostgreSQL, Redis |
| **3** | 10개 | 마이크로서비스 | PostgreSQL Cluster, Redis Cluster |

**확장 전략:**

```
Stage 0-1: Vertical Scaling
┌─────────────────────────────────────┐
│           Single Instance           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │API  │ │WS   │ │Proc │ │DB   │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
└─────────────────────────────────────┘

Stage 2: Process-per-Table
┌─────────────────────────────────────┐
│           API Gateway               │
└───────────────┬─────────────────────┘
        ┌───────┼───────┐
        ▼       ▼       ▼
    ┌───────┐┌───────┐┌───────┐
    │Table 1││Table 2││Table 3│
    │Process││Process││Process│
    └───────┘└───────┘└───────┘
        │       │       │
        └───────┼───────┘
                ▼
    ┌─────────────────────────┐
    │   Shared Database       │
    │   (PostgreSQL + Redis)  │
    └─────────────────────────┘

Stage 3: Microservices
┌─────────────────────────────────────┐
│     Load Balancer / API Gateway     │
└───────────────┬─────────────────────┘
        ┌───────┴───────┐
        ▼               ▼
┌───────────────┐ ┌───────────────┐
│  WebSocket    │ │   REST API    │
│  Service      │ │   Service     │
└───────┬───────┘ └───────┬───────┘
        │                 │
        └────────┬────────┘
                 ▼
┌─────────────────────────────────────┐
│          Message Queue              │
│          (Redis Streams)            │
└───────────────┬─────────────────────┘
        ┌───────┴───────┐
        ▼               ▼
┌───────────────┐ ┌───────────────┐
│   Processor   │ │   Processor   │
│   Instance 1  │ │   Instance 2  │
└───────────────┘ └───────────────┘
```

### 6.2 데이터 보관 전략

| 티어 | 기간 | 저장소 | 접근 속도 | Stage |
|------|:----:|--------|:---------:|:-----:|
| **Hot** | 7일 | PostgreSQL + Redis | < 10ms | 2+ |
| **Warm** | 90일 | PostgreSQL (Archive) | < 100ms | 2+ |
| **Cold** | 무제한 | Object Storage (S3) | < 1초 | 3 |

**데이터 라이프사이클:**

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│     HOT      │     │     WARM     │     │     COLD     │
│   (7 days)   │────▶│   (90 days)  │────▶│  (Archive)   │
│              │     │              │     │              │
│ PostgreSQL   │     │ PostgreSQL   │     │ S3 / Blob    │
│ + Redis      │     │ (Archive)    │     │ (Parquet)    │
└──────────────┘     └──────────────┘     └──────────────┘
     │                     │                    │
  실시간 조회           배치 조회            분석 전용
  (< 10ms)            (< 100ms)           (< 1sec)
```

### 6.3 수평 확장 전략

| 구성요소 | 확장 방식 | 트리거 | Stage |
|----------|----------|--------|:-----:|
| **API Gateway** | 인스턴스 추가 | CPU > 70% | 2+ |
| **WebSocket** | 연결 수 분산 | 연결 > 500/instance | 2+ |
| **Event Processor** | 워커 추가 | 큐 깊이 > 1000 | 2+ |
| **Database** | Read Replica | 읽기 TPS > 5000 | 3 |

---

## 7. Technology Stack by Stage

### 7.1 전체 스택 비교

| Area | Stage 0-1 | Stage 2 | Stage 3 |
|------|-----------|---------|---------|
| **Language** | Python 3.11+ | Python 3.11+ | Python + Go (선택) |
| **Web Framework** | FastAPI | FastAPI | FastAPI + Kong |
| **Database** | SQLite | PostgreSQL | PostgreSQL (Cluster) |
| **Cache** | Dict (In-memory) | Redis | Redis Cluster |
| **Message Queue** | asyncio.Queue | Redis Streams | Redis Streams / Kafka |
| **API Gateway** | FastAPI 내장 | Traefik | Kong / Traefik |
| **Monitoring** | Logs (File) | Prometheus + Grafana | Prometheus + Grafana + Jaeger |
| **Logging** | Python logging | Loki | Loki + ELK |
| **CI/CD** | Manual | GitHub Actions | GitHub Actions + ArgoCD |

### 7.2 Stage별 상세 스택

#### Stage 0-1: 기능 검증 우선

```yaml
# docker-compose.stage1.yml
services:
  api:
    build: ./server
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data  # SQLite
    environment:
      - DATABASE_URL=sqlite:///./data/cards.db
      - LOG_LEVEL=DEBUG

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - api
```

**특징:**
- 단일 컨테이너 (또는 2개: API + Frontend)
- SQLite (파일 기반, 백업 용이)
- 메모리 캐시 (Python dict)
- 파일 기반 로깅

#### Stage 2: 프로덕션 준비

```yaml
# docker-compose.stage2.yml
services:
  api:
    build: ./server
    deploy:
      replicas: 2
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
      - ENABLE_METRICS=true

  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

**특징:**
- PostgreSQL (트랜잭션, 동시성)
- Redis (캐시 + 메시지 큐)
- Prometheus + Grafana (모니터링)
- 다중 API 인스턴스

#### Stage 3: 완전한 인프라

```yaml
# kubernetes/stage3/
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ebs-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ebs-api
  template:
    spec:
      containers:
        - name: api
          image: ebs/api:v3
          resources:
            limits:
              cpu: "1"
              memory: "1Gi"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ebs-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ebs-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**특징:**
- Kubernetes (자동 확장)
- PostgreSQL Cluster (고가용성)
- Redis Cluster (분산 캐시)
- Kong/Istio (API Gateway + Service Mesh)
- Jaeger (분산 추적)

---

## 8. Stage별 인프라 마일스톤

### 8.1 Stage 0: 메트릭 로깅 표준화

| 마일스톤 | 설명 | 완료 기준 |
|----------|------|----------|
| **M0-1** | 로깅 포맷 표준화 | JSON 구조화 로그 적용 |
| **M0-2** | 이벤트 로깅 | 카드 인식 이벤트 로그 기록 |
| **M0-3** | 성능 메트릭 | E2E 지연 시간 측정 |
| **M0-4** | 에러 추적 | 에러 발생 시 컨텍스트 로깅 |

**로그 포맷 예시:**
```json
{
  "timestamp": "2026-02-02T15:00:01.123Z",
  "level": "INFO",
  "event": "card_read",
  "data": {
    "uid": "04:A2:B3:C4",
    "reader_id": 0,
    "latency_ms": 45
  },
  "trace_id": "abc123"
}
```

### 8.2 Stage 1: 이벤트 로깅, API Gateway 패턴

| 마일스톤 | 설명 | 완료 기준 |
|----------|------|----------|
| **M1-1** | 이벤트 스토어 | 모든 이벤트 DB 저장 |
| **M1-2** | API 버전 관리 | /api/v1/ 경로 패턴 |
| **M1-3** | 인증 기반 | JWT 기반 Operator 인증 |
| **M1-4** | 에러 핸들링 | 표준 에러 응답 포맷 |

**API 에러 응답 포맷:**
```json
{
  "error": {
    "code": "CARD_NOT_FOUND",
    "message": "Card with UID 04:A2:B3:C4 not registered",
    "details": {
      "uid": "04:A2:B3:C4"
    }
  },
  "request_id": "req_123",
  "timestamp": "2026-02-02T15:00:01Z"
}
```

### 8.3 Stage 2: Message Queue, Multi-table

| 마일스톤 | 설명 | 완료 기준 |
|----------|------|----------|
| **M2-1** | Redis 도입 | 캐시 + 세션 저장소 |
| **M2-2** | Message Queue | Redis Streams 이벤트 전파 |
| **M2-3** | 멀티 테이블 | 3개 테이블 동시 운영 |
| **M2-4** | PostgreSQL 마이그레이션 | SQLite → PostgreSQL 전환 |
| **M2-5** | 모니터링 대시보드 | Grafana 기본 대시보드 |

### 8.4 Stage 3: Event Sourcing, Data Lake

| 마일스톤 | 설명 | 완료 기준 |
|----------|------|----------|
| **M3-1** | Event Sourcing | 모든 상태 변경 이벤트 기반 |
| **M3-2** | CQRS | 읽기/쓰기 모델 분리 |
| **M3-3** | Data Lake | 핸드 히스토리 Cold Storage |
| **M3-4** | 자동 확장 | HPA 기반 자동 스케일링 |
| **M3-5** | 분산 추적 | Jaeger 통합 |

---

## 9. 관련 문서 링크

### 9.1 비전 및 전략

| 문서 | 용도 |
|------|------|
| [PRD-0003-EBS-RFID-System.md](../PRD-0003-EBS-RFID-System.md) | Master PRD (비전/전략) |
| [CONCEPT-EBS-Vision.md](CONCEPT-EBS-Vision.md) | EBS 컨셉 기획서 |
| [STRATEGY-Lean-Production.md](STRATEGY-Lean-Production.md) | 소수 인원 운영 전략 |

### 9.2 기술 설계

| 문서 | 용도 |
|------|------|
| [ARCHITECTURE-RFID-Software.md](../2-stage1/ARCHITECTURE-RFID-Software.md) | 3-Layer 소프트웨어 아키텍처 |
| [DESIGN-RFID-Hardware.md](../1-stage0/DESIGN-RFID-Hardware.md) | 하드웨어 설계 |
| [DESIGN-Card-API.md](../design/DESIGN-Card-API.md) | Card API 설계 |
| [DESIGN-Database-Schema.md](../design/DESIGN-Database-Schema.md) | 데이터베이스 스키마 |

### 9.3 Stage별 PRD

| 문서 | 용도 |
|------|------|
| [PRD-0003-Stage0-RFID-Connection.md](../1-stage0/PRD-0003-Stage0-RFID-Connection.md) | Stage 0: RFID 연결 검증 |
| [PRD-0003-Stage1-PokerGFX-Clone.md](../2-stage1/PRD-0003-Stage1-PokerGFX-Clone.md) | Stage 1: PokerGFX 복제 |
| [PRD-0003-Stage2-WSOP-Integration.md](../3-stage2/PRD-0003-Stage2-WSOP-Integration.md) | Stage 2: WSOP+ 연동 |
| [PRD-0003-Stage3-EBS-Automation.md](../4-stage3/PRD-0003-Stage3-EBS-Automation.md) | Stage 3: 자동화 |

---

## 10. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|:----:|------|----------|--------|
| 1.0.0 | 2026-02-02 | 초안 - 5-Layer 아키텍처, API Contract, SLA 정의 | EBS Architecture Team |

---

**문서 종료**
