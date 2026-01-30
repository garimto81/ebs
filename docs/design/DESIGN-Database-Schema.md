# Database Schema Design

**Version**: 1.0.0
**Last Updated**: 2026-01-30
**Stage**: Stage 0 (RFID Connection Validation)

## Overview

EBS 백오피스 데이터베이스는 RFID 태그와 포커 카드의 매핑 정보를 관리합니다. SQLite 기반으로 경량화되었으며, 향후 PostgreSQL 마이그레이션을 고려한 표준 SQL 구조를 따릅니다.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    EBS Backend                          │
│  ┌─────────────┐    ┌─────────────┐   ┌─────────────┐ │
│  │   ESP32     │───▶│FastAPI      │──▶│  SQLite DB  │ │
│  │ (RFID Read) │    │  (Server)   │   │  (cards.db) │ │
│  └─────────────┘    └─────────────┘   └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Table Schemas

### `cards` 테이블

카드 덱의 물리적 RFID 태그와 논리적 카드 정보를 매핑합니다.

```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE,                    -- RFID UID (예: "04:A2:B3:C4:D5:E6:F7")
    suit TEXT NOT NULL,                 -- spades, hearts, diamonds, clubs, joker
    rank TEXT NOT NULL,                 -- A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, JOKER
    display TEXT NOT NULL,              -- "A♠", "K♥", "JOKER"
    value INTEGER NOT NULL,             -- 1-14 (Ace low=1, high=14, Joker=0)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_suit CHECK (suit IN ('spades', 'hearts', 'diamonds', 'clubs', 'joker')),
    CONSTRAINT chk_value CHECK (value >= 0 AND value <= 14)
);
```

#### 컬럼 설명

| 컬럼 | 타입 | 제약 | 설명 |
|------|------|------|------|
| `id` | INTEGER | PK, AUTO_INCREMENT | 내부 식별자 |
| `uid` | TEXT | UNIQUE, NULLABLE | RFID 태그 UID (초기값 NULL, 매핑 후 업데이트) |
| `suit` | TEXT | NOT NULL, CHECK | 카드 무늬 (4가지 + joker) |
| `rank` | TEXT | NOT NULL | 카드 숫자/문자 (A, 2-10, J, Q, K, JOKER) |
| `display` | TEXT | NOT NULL | UI 표시용 문자열 (유니코드 심볼 포함) |
| `value` | INTEGER | NOT NULL, CHECK | 카드 숫자 값 (정렬/비교용, Joker=0) |
| `created_at` | TIMESTAMP | DEFAULT NOW | 레코드 생성 시각 |
| `updated_at` | TIMESTAMP | DEFAULT NOW | 최종 수정 시각 |

#### 인덱스 전략

```sql
CREATE UNIQUE INDEX idx_cards_uid ON cards(uid) WHERE uid IS NOT NULL;
CREATE INDEX idx_cards_suit_rank ON cards(suit, rank);
CREATE INDEX idx_cards_value ON cards(value);
```

- **`idx_cards_uid`**: RFID UID 기반 빠른 조회 (Partial Index로 NULL 제외)
- **`idx_cards_suit_rank`**: 무늬+숫자 복합 조회
- **`idx_cards_value`**: 값 기반 정렬 쿼리

## ER Diagram

```
┌─────────────────────────────────────┐
│            cards                    │
├─────────────────────────────────────┤
│ PK  id          INTEGER             │
│ UK  uid         TEXT                │
│     suit        TEXT (NOT NULL)     │
│     rank        TEXT (NOT NULL)     │
│     display     TEXT (NOT NULL)     │
│     value       INTEGER (NOT NULL)  │
│     created_at  TIMESTAMP           │
│     updated_at  TIMESTAMP           │
└─────────────────────────────────────┘
             │
             │ (Stage 1 확장)
             ▼
┌─────────────────────────────────────┐
│          card_reads                 │ (예정)
├─────────────────────────────────────┤
│ PK  id          INTEGER             │
│ FK  card_id     INTEGER             │
│     reader_id   INTEGER             │
│     timestamp   TIMESTAMP           │
└─────────────────────────────────────┘
```

## Data Dictionary

### Suit Values

| suit | 한글 | 유니코드 | 색상 |
|------|------|----------|------|
| `spades` | 스페이드 | ♠ (U+2660) | 검정 |
| `hearts` | 하트 | ♥ (U+2665) | 빨강 |
| `diamonds` | 다이아몬드 | ♦ (U+2666) | 빨강 |
| `clubs` | 클럽 | ♣ (U+2663) | 검정 |
| `joker` | 조커 | 🃏 (U+1F0CF) | 특수 |

### Rank Values

| rank | value | 설명 |
|------|-------|------|
| `JOKER` | 0 | 조커 (2장) |
| `A` | 1 또는 14 | Ace (맥락에 따라 low/high) |
| `2`-`10` | 2-10 | 숫자 카드 |
| `J` | 11 | Jack |
| `Q` | 12 | Queen |
| `K` | 13 | King |

## Initial Data

초기 데이터는 표준 54장 포커 덱입니다:

- 스페이드 A-K (13장)
- 하트 A-K (13장)
- 다이아몬드 A-K (13장)
- 클럽 A-K (13장)
- 조커 2장

모든 카드의 `uid`는 NULL로 초기화되며, Stage 0 매핑 작업에서 실제 RFID 태그를 스캔하여 업데이트됩니다.

## Migration Strategy

### Stage 0 → Stage 1 확장 예정

```sql
-- Stage 1: 핸드 히스토리 추적
CREATE TABLE hands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    hand_number INTEGER NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP
);

CREATE TABLE hand_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hand_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    position TEXT NOT NULL,  -- 'board', 'player1', 'player2'
    FOREIGN KEY (hand_id) REFERENCES hands(id),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

-- Stage 2: 플레이어 정보
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    avatar_url TEXT
);
```

### PostgreSQL 마이그레이션 고려사항

현재 SQLite 스키마는 PostgreSQL로 이전 가능하도록 설계되었습니다:

- `AUTOINCREMENT` → `SERIAL` 또는 `GENERATED ALWAYS AS IDENTITY`
- `TIMESTAMP` → `TIMESTAMPTZ`
- `CHECK` 제약은 동일하게 지원

## Backup Strategy

```bash
# SQLite 백업
sqlite3 server/db/cards.db ".backup server/db/cards-backup-$(date +%Y%m%d).db"

# CSV 내보내기 (데이터 감사용)
sqlite3 server/db/cards.db ".mode csv" ".output cards.csv" "SELECT * FROM cards;"
```

## Security Considerations

### Stage 0 (개발 환경)
- Local SQLite 파일 기반
- 파일 권한: 600 (소유자만 읽기/쓰기)

### Stage 2+ (프로덕션)
- PostgreSQL + SSL/TLS
- RLS (Row Level Security) 정책
- 백업 암호화

## Query Examples

### 카드 매핑 업데이트
```sql
UPDATE cards
SET uid = '04:A2:B3:C4:D5:E6:F7', updated_at = CURRENT_TIMESTAMP
WHERE suit = 'spades' AND rank = 'A';
```

### UID로 카드 조회
```sql
SELECT suit, rank, display, value
FROM cards
WHERE uid = '04:A2:B3:C4:D5:E6:F7';
```

### 매핑되지 않은 카드 목록
```sql
SELECT id, suit, rank, display
FROM cards
WHERE uid IS NULL
ORDER BY suit, value;
```

### 무늬별 통계
```sql
SELECT suit, COUNT(*) as count
FROM cards
WHERE uid IS NOT NULL
GROUP BY suit;
```

## References

- SQLite Documentation: https://www.sqlite.org/docs.html
- PostgreSQL Migration Guide: https://wiki.postgresql.org/wiki/Converting_from_other_Databases_to_PostgreSQL
- ISO 8601 Timestamp Format: https://en.wikipedia.org/wiki/ISO_8601

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-30 | 초기 스키마 설계 (Stage 0) |
