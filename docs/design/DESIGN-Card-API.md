# Card Management REST API 설계

**Version**: 1.0.0
**Date**: 2026-01-30
**Status**: Draft

---

## 1. 개요

EBS 백오피스용 Card-UID 매핑 관리 REST API 설계 문서.

### 1.1 범위

- Stage 0: 기본 CRUD + 학습 모드
- Stage 1+: 보안 기능, 다중 리더 지원

### 1.2 기술 스택

- **Framework**: FastAPI 0.100+
- **Database**: SQLite → PostgreSQL (Stage 1+)
- **Protocol**: REST + WebSocket

---

## 2. Base URL

```
Development: http://localhost:8000/api
Production:  https://ebs.example.com/api
```

---

## 3. CRUD Endpoints

### 3.1 GET /api/cards

전체 카드 목록 조회.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| suit | string | No | 무늬 필터 (spades, hearts, diamonds, clubs, joker) |
| mapped | boolean | No | true=매핑됨, false=미매핑 |

**Response 200:**

```json
{
  "cards": [
    {
      "id": 1,
      "uid": "04:A2:B3:C4",
      "suit": "spades",
      "rank": "A",
      "display": "A♠",
      "value": 14,
      "status": "mapped",
      "created_at": "2026-01-30T12:00:00Z",
      "updated_at": "2026-01-30T12:00:00Z"
    }
  ],
  "total": 54,
  "mapped_count": 42,
  "unmapped_count": 12
}
```

---

### 3.2 GET /api/cards/{id}

개별 카드 조회.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | 카드 ID (1-54) |

**Response 200:**

```json
{
  "id": 1,
  "uid": "04:A2:B3:C4",
  "suit": "spades",
  "rank": "A",
  "display": "A♠",
  "value": 14,
  "status": "mapped",
  "created_at": "2026-01-30T12:00:00Z",
  "updated_at": "2026-01-30T12:00:00Z"
}
```

**Response 404:**

```json
{
  "error": {
    "code": "E_CARD_NOT_FOUND",
    "message": "Card with id 99 not found"
  }
}
```

---

### 3.3 PUT /api/cards/{id}/uid

UID 업데이트.

**Request Body:**

```json
{
  "uid": "04:A2:B3:C4"
}
```

**Validation:**
- UID format: `XX:XX:XX:XX` (4-byte) 또는 `XX:XX:XX:XX:XX:XX:XX` (7-byte)
- UID uniqueness: 중복 불가

**Response 200:**

```json
{
  "id": 1,
  "uid": "04:A2:B3:C4",
  "status": "mapped",
  "message": "UID updated successfully"
}
```

**Response 409 (Conflict):**

```json
{
  "error": {
    "code": "E_UID_DUPLICATE",
    "message": "UID 04:A2:B3:C4 is already assigned to card id 5 (5♥)"
  }
}
```

---

### 3.4 DELETE /api/cards/{id}/uid

UID 삭제 (null로 설정).

**Response 204:** No Content

---

## 4. Batch Operations

### 4.1 POST /api/cards/learn

학습 모드 시작.

**Request Body:**

```json
{
  "card_id": 1,
  "timeout_seconds": 30
}
```

또는 전체 학습:

```json
{
  "mode": "sequential",
  "start_id": 1,
  "end_id": 54
}
```

**Response 200:**

```json
{
  "session_id": "learn_2026-01-30_001",
  "status": "waiting",
  "card_id": 1,
  "card_display": "A♠",
  "message": "Scan card A♠ within 30 seconds"
}
```

**Response 409:**

```json
{
  "error": {
    "code": "E_LEARN_IN_PROGRESS",
    "message": "Learning session already active for card id 3"
  }
}
```

---

### 4.2 DELETE /api/cards/learn

학습 모드 취소.

**Response 200:**

```json
{
  "message": "Learning session cancelled",
  "session_id": "learn_2026-01-30_001"
}
```

---

### 4.3 POST /api/cards/export

JSON 내보내기.

**Response 200:**

```json
{
  "version": "1.0",
  "exported_at": "2026-01-30T12:00:00Z",
  "mappings": [
    {"id": 1, "uid": "04:A2:B3:C4", "display": "A♠"},
    {"id": 2, "uid": "04:B3:C4:D5", "display": "2♠"}
  ],
  "total_mapped": 42
}
```

---

### 4.4 POST /api/cards/import

JSON 가져오기.

**Request Body:**

```json
{
  "version": "1.0",
  "mappings": [
    {"id": 1, "uid": "04:A2:B3:C4"},
    {"id": 2, "uid": "04:B3:C4:D5"}
  ],
  "mode": "merge"
}
```

**mode 옵션:**
- `merge`: 기존 매핑 유지, 새 매핑 추가
- `replace`: 모든 매핑 교체

**Response 200:**

```json
{
  "imported": 42,
  "skipped": 3,
  "errors": [
    {"id": 5, "reason": "UID format invalid"}
  ]
}
```

---

## 5. WebSocket Events

### 5.1 Connection

```
ws://localhost:8000/ws
```

### 5.2 Events (Server → Client)

#### card_scanned

```json
{
  "type": "card_scanned",
  "uid": "04:A2:B3:C4",
  "reader_id": 0,
  "timestamp": 1706619600000
}
```

#### learn_progress

```json
{
  "type": "learn_progress",
  "session_id": "learn_2026-01-30_001",
  "status": "completed",
  "card_id": 1,
  "uid": "04:A2:B3:C4",
  "display": "A♠"
}
```

#### reader_status

```json
{
  "type": "reader_status",
  "connected": true,
  "port": "COM3",
  "reader_id": 0
}
```

#### card_updated

```json
{
  "type": "card_updated",
  "id": 1,
  "uid": "04:A2:B3:C4",
  "status": "mapped"
}
```

---

## 6. Error Codes

| Code | Name | HTTP Status | Description |
|------|------|-------------|-------------|
| 1001 | E_CARD_NOT_FOUND | 404 | 카드 ID 없음 |
| 1002 | E_UID_DUPLICATE | 409 | UID 중복 |
| 1003 | E_INVALID_SUIT | 400 | 잘못된 무늬 값 |
| 1004 | E_INVALID_UID_FORMAT | 400 | UID 형식 오류 |
| 1005 | E_LEARN_IN_PROGRESS | 409 | 학습 세션 진행 중 |
| 1006 | E_NO_LEARN_SESSION | 400 | 활성 학습 세션 없음 |
| 1007 | E_READER_DISCONNECTED | 503 | 리더 연결 끊김 |

---

## 7. Security (Stage 1+)

### 7.1 CORS

```python
# FastAPI CORS 설정
origins = [
    "http://localhost:5173",    # Vite dev
    "http://localhost:3000",    # React dev
    "https://ebs.example.com"   # Production
]
```

### 7.2 Rate Limiting

- 60 requests/minute per IP
- 10 requests/second burst

---

## 8. Performance

| Endpoint | Target Response Time |
|----------|---------------------|
| GET /api/cards | < 50ms |
| GET /api/cards/{id} | < 20ms |
| PUT /api/cards/{id}/uid | < 100ms |
| POST /api/cards/import | < 500ms |

---

## 9. 다음 단계

1. FastAPI routes 구현 (`server/app/api/routes.py`)
2. WebSocket handlers 구현 (`server/app/api/websocket.py`)
3. Pydantic models 정의 (`server/app/models/`)
4. Unit tests 작성
5. OpenAPI/Swagger 문서 자동 생성
