# PRD-0003-Stage2: WSOP+ DB 연동

**버전**: 1.0.0
**생성일**: 2026-01-28
**상위 문서**: [PRD-0003-EBS-RFID-System.md](PRD-0003-EBS-RFID-System.md)
**전제조건**: Stage 1 Gate 통과 (2026년 12월)
**목표 기간**: 2027년 전체 (12개월)

---

## 1. Stage 2 개요

### 1.1 목표

> **"WSOP+ 데이터베이스와 완전 연동하여 수동 입력 30% 감소"**

Stage 2는 WSOP+ 시스템과 데이터를 동기화하여 중복 입력을 제거하고
"Single Source of Truth" 원칙을 구현합니다.

### 1.2 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **Single Source of Truth** | WSOP+가 마스터 데이터 |
| **양방향 동기화** | EBS ↔ WSOP+ 데이터 흐름 |
| **Graceful Degradation** | 연결 실패 시 Stage 1 모드 폴백 |

### 1.3 전제조건

- [ ] Stage 1 Gate 100% 통과
- [ ] WSOP+ API 문서 확보
- [ ] API 접근 권한 획득
- [ ] 테스트 환경 구축

---

## 2. 연동 범위

### 2.1 동기화 대상 데이터

| 데이터 | 방향 | 마스터 | 동기화 타이밍 |
|--------|------|--------|--------------|
| **플레이어 정보** | WSOP+ → EBS | WSOP+ | 토너먼트 시작 시 |
| **칩 카운트** | 양방향 | WSOP+ (브레이크) | 브레이크/핸드 종료 |
| **핸드 히스토리** | EBS → WSOP+ | EBS | 핸드 종료 시 |
| **플레이어 통계** | WSOP+ → EBS | WSOP+ | 요청 시 |

### 2.2 동기화 제외 항목

| 항목 | 이유 |
|------|------|
| 카드 정보 | 보안 (EBS 독점) |
| 실시간 베팅 | 지연 이슈 (수동 입력 유지) |
| 스킨/설정 | EBS 로컬 관리 |

---

## 3. 데이터 동기화 상세

### 3.1 칩 카운트 동기화

```
[WSOP+] ─────────────────────────────────────────> [EBS]
          토너먼트 시작: 초기 스택 PULL
                    │
[WSOP+] <────────── │ ────────────────────────────> [EBS]
                    │ 브레이크: 양방향 보정
                    │
[WSOP+] <───────────┴───────────────────────────── [EBS]
          핸드 종료: 칩 변동 PUSH
```

| 이벤트 | 소스 | 타겟 | 방식 | 설명 |
|--------|------|------|------|------|
| 토너먼트 시작 | WSOP+ | EBS | Pull | 초기 스택 가져오기 |
| 핸드 종료 | EBS | WSOP+ | Push | 칩 변동 전송 |
| 브레이크 시작 | WSOP+ | EBS | Push | 공식 칩 카운트로 보정 |
| 리바이/애드온 | WSOP+ | EBS | Push | 칩 추가 반영 |

### 3.2 플레이어 정보 동기화

| 필드 | 소스 | 초기화 | 업데이트 |
|------|------|--------|----------|
| 이름 | WSOP+ | 토너먼트 시작 | - |
| 국적 | WSOP+ | 토너먼트 시작 | - |
| 시트 번호 | WSOP+ | 테이블 배정 | 테이블 이동 |
| 통계 (VPIP 등) | WSOP+ | 요청 시 | 실시간 |

### 3.3 핸드 히스토리 동기화

**EBS → WSOP+ 전송 데이터**:

```json
{
  "hand_id": "EBS-2026012800001",
  "wsop_table_id": "TABLE-42",
  "timestamp": "2026-01-28T14:30:00Z",
  "players": [...],
  "actions": [...],
  "board": [...],
  "pot": 150000,
  "winners": [{"seat": 3, "amount": 150000}]
}
```

---

## 4. API 설계

### 4.1 WSOP+ API 엔드포인트 (예상)

| Endpoint | Method | 용도 |
|----------|--------|------|
| `/api/tournaments/{id}/players` | GET | 플레이어 목록 |
| `/api/tournaments/{id}/tables/{table_id}/chips` | GET/PUT | 칩 카운트 |
| `/api/players/{id}/stats` | GET | 플레이어 통계 |
| `/api/hands` | POST | 핸드 히스토리 전송 |

### 4.2 EBS API 엔드포인트 (신규)

| Endpoint | Method | 용도 |
|----------|--------|------|
| `/api/sync/init` | POST | 동기화 초기화 |
| `/api/sync/status` | GET | 동기화 상태 확인 |
| `/api/sync/chips` | POST | 칩 동기화 트리거 |
| `/api/sync/players` | POST | 플레이어 동기화 |

### 4.3 인증/권한

| 항목 | 방식 |
|------|------|
| 인증 | OAuth 2.0 (예상) |
| 권한 | 테이블별 scope |
| 토큰 갱신 | Refresh Token |
| 암호화 | TLS 1.3 |

---

## 5. DB 스키마 확장

### 5.1 동기화 상태 테이블

```sql
CREATE TABLE sync_status (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL,  -- 'player', 'chips', 'hand'
    entity_id TEXT NOT NULL,
    wsop_id TEXT,
    last_sync_at TIMESTAMP,
    sync_direction TEXT,  -- 'pull', 'push', 'bidirectional'
    status TEXT DEFAULT 'pending',  -- 'pending', 'synced', 'conflict', 'error'
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 충돌 로그 테이블

```sql
CREATE TABLE sync_conflicts (
    id INTEGER PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    ebs_value TEXT,
    wsop_value TEXT,
    resolution TEXT,  -- 'ebs_wins', 'wsop_wins', 'manual'
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. 에러 핸들링

### 6.1 연결 실패 시 폴백

```
연결 상태 감지 (5초 간격)
        │
        ├── Connected: 정상 동기화
        │
        └── Disconnected:
            ├── 경고 UI 표시 ("WSOP+ 연결 끊김")
            ├── Stage 1 모드 전환 (수동 입력)
            ├── 로컬 큐에 변경사항 저장
            └── 재연결 시 큐 자동 동기화
```

### 6.2 데이터 불일치 알림

| 불일치 유형 | 감지 방법 | 알림 | 자동 해결 |
|------------|----------|------|----------|
| 칩 카운트 차이 > 5% | 브레이크 비교 | 운영자 경고 | WSOP+ 값 사용 |
| 플레이어 누락 | 목록 비교 | 운영자 경고 | WSOP+ 추가 |
| 핸드 전송 실패 | ACK 타임아웃 | 시스템 로그 | 재전송 (3회) |

### 6.3 롤백 절차

1. 동기화 실패 감지
2. 로컬 트랜잭션 롤백
3. 이전 상태 복원
4. 운영자 알림
5. 수동 재동기화 옵션 제공

---

## 7. 분기별 개발 계획

**전체 기간**: 2027년 1월 - 12월 (12개월)

| 분기 | 마일스톤 | 기능 | Definition of Done |
|------|----------|------|-------------------|
| Q1 (1-3월) | Alpha | WSOP+ API 연동 | 연결 상태 모니터링 UI, 인증 구현 |
| Q2 (4-6월) | Beta | 칩 동기화 | 브레이크 시 자동 보정, 양방향 동기화 |
| Q3 (7-9월) | RC | 플레이어 정보 동기화 | 자동 시트 배정, 통계 가져오기 |
| Q4 (10-12월) | Release | 히스토리 공유 + 안정화 | 양방향 동기화 확인, 24시간 안정성 테스트 |

---

## 8. 성공 기준

### 8.1 핵심 지표

| 지표 | 목표 |
|------|------|
| 수동 입력 감소 | Stage 1 대비 30% |
| 데이터 정합성 | 100% (칩 카운트) |
| 동기화 지연 | < 5초 (95th percentile) |
| 연결 가동률 | 99%+ (24시간 기준) |

### 8.2 수동 입력 감소 항목

| 항목 | Stage 1 | Stage 2 | 감소율 |
|------|---------|---------|--------|
| 플레이어 이름 입력 | 수동 | 자동 | 100% |
| 초기 칩 입력 | 수동 | 자동 | 100% |
| 통계 설정 | 수동 | 자동 | 100% |
| 칩 보정 (브레이크) | 수동 | 자동 | 100% |
| **베팅 액션** | **수동** | **수동** | 0% |

---

## 9. Stage 2 Gate (정량적 전환 조건)

**Gate 시기**: 2027년 12월

Stage 3 착수를 위해 다음 조건을 **모두** 충족해야 합니다:

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| 연결 안정성 | 24시간 모니터링 99%+ 가동률 | 모니터링 로그 |
| 데이터 정합성 | WSOP+ vs EBS 칩 카운트 100% 일치 | 비교 테스트 |
| 동기화 성능 | 지연 < 5초 (95 percentile) | 성능 테스트 |
| 수동 입력 감소 | Stage 1 대비 30% 이상 감소 | 입력 횟수 비교 |

**Gate 통과 시**: Stage 3 착수 가능 (2028년 1월)

---

## 10. Definition of Done

### 개발

- [ ] WSOP+ API 연동 완료
- [ ] 칩 카운트 양방향 동기화
- [ ] 플레이어 정보 자동 가져오기
- [ ] 핸드 히스토리 전송
- [ ] 폴백 모드 구현

### 검증

- [ ] 24시간 연속 안정성 테스트
- [ ] 데이터 정합성 100% 확인
- [ ] 수동 입력 30% 감소 측정

---

## 11. 위험 요소 및 대응

| 위험 | 영향도 | 대응 |
|------|--------|------|
| WSOP+ API 미확정 | 고 | Stage 1 Week 4까지 확보 필수 |
| API 변경 | 중 | 버전 관리 + 어댑터 패턴 |
| 네트워크 불안정 | 중 | 로컬 큐 + 자동 재연결 |

---

## 12. 문서 정보

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0.0 |
| **작성일** | 2026-01-28 |
| **상태** | Draft |

