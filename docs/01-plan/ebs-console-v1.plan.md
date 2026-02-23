---
doc_type: "plan"
doc_id: "EBS-CONSOLE-V1-PLAN"
version: "1.0.0"
status: "draft"
owner: "BRACELET STUDIO"
created: "2026-02-23"
last_updated: "2026-02-23"
phase: "phase-1"
priority: "critical"

depends_on:
  - "docs/00-prd/ebs-console.prd.md"
  - "docs/01_PokerGFX_Analysis/ebs-console-feature-triage.md"
---

# EBS console v1.0 개발 계획서

> **목표**: EBS console v1.0 Broadcast Ready — 라이브 포커 방송 가능한 최소 완성품

---

## 1. 전제 조건

v1.0 개발을 시작하기 전 충족되어야 하는 조건:

| 전제 조건 | 상태 | 담당 |
|----------|:----:|------|
| RFID 업체 선정 (Phase 0) | 진행 중 | 운영팀 |
| POC 하드웨어 확보 (MFRC522) | 미착수 | 기술팀 |
| PokerGFX 기능 분석 완료 | **완료** | Phase 0 |
| EBS console 기획서 확정 | **완료** | Phase 0 |
| 개발 환경 설정 | 미착수 | 기술팀 |

**v1.0 RFID 정책**: RFID 미연결 시 수동 카드 입력 폴백으로 운영. v1.0은 RFID 없이도 동작해야 한다.

---

## 2. v1.0 개발 범위 (65개 기능)

| 카테고리 | v1.0 개수 | 핵심 목적 |
|----------|:---------:|---------|
| Action Tracker | 22 | 실시간 게임 추적, 액션/베팅 입력 |
| Pre-Start Setup | 10 | 이벤트 설정, 플레이어/스택 입력 |
| Viewer Overlay | 12 | OBS 방송 오버레이 출력 |
| Security | 7 | Realtime/Trustless Mode, WebSocket TLS |
| GFX Console | 3 | 기본 현황 (플레이어 수, 스택) |
| Equity & Stats | 1 | 핸드 카운터 |
| Hand History | 1 | 현재 세션 핸드 상세 뷰 |
| Server 관리 | 9 | 출력 설정, 크로마키, 레이아웃 |
| **합계** | **65** | |

---

## 3. 6-Layer 개발 계획

65개 기능을 의존성 순서로 6개 레이어로 분류. 각 레이어는 이전 레이어 완료 후 시작.

### Layer 1: 인프라 (6주 예상)

> 방송 시작 전 필수 기반 구조. 다른 모든 레이어가 이에 의존.

| 기능 ID | 기능명 | 설명 |
|---------|-------|------|
| SEC-009 | WebSocket 암호화 | Server↔Frontend WSS(TLS) 기반 |
| SV-006 | Live/Delay 이중 출력 | 출력 파이프라인 기반 |
| SV-007 | Secure Delay 설정 | 딜레이 버퍼 구조 |
| SV-008 | Video Size / Frame Rate | 출력 해상도/프레임레이트 |

**추가 인프라 작업 (기능 ID 외):**
- DB 스키마: cards, hands, sessions, players 테이블
- Serial 통신 레이어: USB Serial 수신 → WebSocket 브로드캐스트
- OBS Browser Source 연동 기반 (HTTP 서버)

**병렬 개발 가능:** 서버 코드와 프론트엔드 기반 UI 동시 진행

---

### Layer 2: 게임 설정 (4주 예상)

> 방송 전 설정 화면. Pre-Start Setup 완성.

| 기능 ID | 기능명 | 비고 |
|---------|-------|------|
| PS-001 | Event Name 입력 | |
| PS-002 | Game Type 선택 | HOLDEM / PLO4 / PLO5 / SHORT DECK |
| PS-003 | Min Chip 설정 | |
| PS-004 | 플레이어 이름 입력 | 자동완성 지원 |
| PS-005 | 칩 스택 입력 | 숫자 검증 포함 |
| PS-006 | 포지션 할당 | Dealer 버튼 위치 |
| PS-007 | RFID 카드 감지 상태 | 수동 입력 폴백 포함 |
| PS-008 | Ante/SB/BB 설정 | |
| PS-010 | Dealer 위치 조정 | 드래그 앤 드롭 |
| PS-012 | TRACK THE ACTION 버튼 | 화면 전환 트리거 |

**결과물:** 설정 완료 후 Action Tracker 화면으로 전환되는 완성된 Pre-Start Setup 화면

---

### Layer 3: 액션 추적 (8주 예상)

> v1.0 핵심. 실시간 게임 진행 추적 및 액션 입력.

#### 3.1 게임 상태 + 좌석 (Layer 3a)

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| AT-005 | 게임 타입 선택 | Layer 2 완료 |
| AT-006 | Blinds 표시 | Layer 2 완료 |
| AT-007 | Hand 번호 추적 | |
| AT-008 | 10인 좌석 레이아웃 | |
| AT-009 | 플레이어 상태 표시 | AT-008 |
| AT-010 | Action-on 하이라이트 | AT-009 |
| AT-011 | 포지션 표시 | AT-008 |

#### 3.2 액션 입력 (Layer 3b)

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| AT-012 | 기본 액션 버튼 | AT-009 |
| AT-013 | UNDO 버튼 | AT-012 |
| AT-014 | 키보드 단축키 | AT-012 |
| AT-015 | 베팅 금액 직접 입력 | AT-012 |
| AT-016 | +/- 조정 버튼 | AT-015 |
| AT-017 | Quick Bet 버튼 | AT-015 |
| AT-018 | Min/Max 범위 표시 | AT-015 |
| AT-021 | HIDE GFX | |
| AT-023 | ADJUST STACK | AT-009 |

#### 3.3 보드 카드 (Layer 3c)

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| AT-019 | Community Cards 표시 | |
| AT-020 | 보드 카드 업데이트 | AT-019, RFID or 수동 |

---

### Layer 4: 오버레이 출력 (6주 예상)

> OBS Browser Source로 방송에 송출되는 시청자용 오버레이.

#### 4.1 플레이어 정보 오버레이

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| VO-002 | Blinds 정보 | Layer 3a |
| VO-003 | Chip Counts | Layer 3a |
| VO-005 | Hole Cards 표시 | AT-020 |
| VO-006 | Player Name + Stack | Layer 2, 3a |
| VO-007 | 마지막 액션 표시 | AT-012 |
| VO-009 | Board Cards | AT-019, AT-020 |
| VO-010 | Pot Display | AT-015 |
| VO-012 | Street 표시 | AT-019 |
| VO-013 | To Act 표시 | AT-010 |
| VO-014 | Folded Player 스타일 | AT-009 |

#### 4.2 이벤트 정보 오버레이

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| VO-001 | Event Logo | Layer 2 (PS-001) |
| VO-011 | Event Info | Layer 2 (PS-001) |

#### 4.3 GFX 레이아웃 설정

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| SV-005 | Chroma Key | Layer 1 |
| SV-012 | Board Position | Layer 1 |
| SV-013 | Player Layout | Layer 1 |
| SV-017 | Action Clock | Layer 3b |
| SV-019 | BB 표시 모드 | VO-003 |
| SV-020 | 통화 기호 설정 | VO-003 |

---

### Layer 5: 보안 + 딜레이 (4주 예상)

> Trustless/Realtime Mode 전환. 홀카드 딜레이 방송.

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| SEC-001 | 30초 딜레이 버퍼링 | Layer 1 (SV-006, SV-007) |
| SEC-002 | 카운트다운 표시 | SEC-001 |
| SEC-003 | DB 조회 지연 | SEC-001 |
| SEC-004 | 즉시 카드 표시 | Layer 4 (VO-005) |
| SEC-005 | 모드 표시 | SEC-001, SEC-004 |
| SEC-010 | Trustless/Realtime 토글 | SEC-001, SEC-004 |

---

### Layer 6: 마무리 + 모니터링 (2주 예상)

> 상태 표시, 기본 현황 패널. Layer 1~5 이후 통합.

| 기능 ID | 기능명 | 의존 |
|---------|-------|------|
| AT-001 | Network 연결 상태 | Layer 1 |
| AT-002 | Table 연결 상태 | Layer 1 |
| AT-003 | Stream 상태 | OBS 연동 |
| AT-004 | Record 상태 | OBS 연동 |
| GC-013 | Total Players | Layer 2 |
| GC-014 | Remaining Players | Layer 3a |
| GC-015 | Average Stack | Layer 3a |
| ST-007 | Hands Played | AT-007 |
| HH-008 | 핸드 상세 뷰 | Layer 3 |

---

## 4. 마일스톤

| 마일스톤 | 완료 기준 | 목표 시기 |
|---------|---------|---------|
| **M1** — 인프라 완성 | WebSocket 서버 + DB + OBS 연동 동작 확인 | Layer 1 완료 |
| **M2** — 설정 완성 | Pre-Start Setup 화면 완성 + 데이터 저장 | Layer 2 완료 |
| **M3** — 액션 추적 | Action Tracker 65% 기능 동작 | Layer 3 완료 |
| **M4** — 방송 오버레이 | OBS Browser Source에 오버레이 정상 출력 | Layer 4 완료 |
| **M5** — 보안 완성 | Trustless/Realtime Mode 전환 검증 | Layer 5 완료 |
| **M6** — v1.0 완성 | 라이브 방송 시뮬레이션 1회 성공 | Layer 6 완료 |

**전체 예상 기간**: 30주 (약 7.5개월)
**병렬 개발 시**: 20~24주로 단축 가능 (Layer 3a/3b/3c + Layer 4 UI 동시 진행)

---

## 5. 기술 스택 (미정 사항)

| 레이어 | 선택지 | 결정 기준 |
|-------|-------|---------|
| Frontend | React + Electron, Flutter Desktop, Tauri | UI 복잡도, 팀 역량 |
| Backend | Node.js, Python FastAPI, Go | WebSocket 성능, 팀 역량 |
| DB | SQLite (로컬), PostgreSQL | 동시 접속 수, 확장성 |
| RFID | MFRC522 (POC), ST25R3911B (프로덕션) | Phase 0 업체 선정 결과 |

> 기술 스택은 Phase 0 완료 후 별도 기술 결정 문서에서 확정한다.

---

## 6. 리스크

| 리스크 | 가능성 | 영향 | 완화 방법 |
|-------|:----:|:----:|---------|
| RFID 업체 선정 지연 | 중 | 중 | v1.0은 수동 입력 폴백으로 RFID 없이도 진행 |
| 기술 스택 결정 지연 | 저 | 고 | Phase 0 종료 전 기술 결정 문서 작성 |
| 65개 기능 범위 크리프 | 중 | 중 | 트리아지 문서가 배제 기준 역할, 변경 시 PRD 개정 필요 |
| Layer 3 복잡도 과소평가 | 중 | 고 | 게임 규칙/엣지케이스 상세 명세 사전 작성 |
| OBS Browser Source 호환성 | 저 | 중 | 사전 POC로 OBS 연동 방식 확인 |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0.0 | 2026-02-23 | 최초 작성 (ebs-console.prd.md 기반) |

---
**Version**: 1.0.0 | **Updated**: 2026-02-23
