---
doc_type: "prd"
doc_id: "PRD-0003-EBS-Master"
version: "8.0.0"
status: "approved"
owner: "BRACELET STUDIO"
last_updated: "2026-01-15"
next_review: "2026-07-01"
phase: "master"
priority: "critical"

depends_on: []

related_docs:
  - "docs/phase-0/VENDOR-SELECTION-CHECKLIST.md"
  - "docs/phase-1/PRD-0003-Phase1-PokerGFX-Clone.md"
  - "docs/phase-1/PokerGFX-Feature-Checklist.md"
  - "docs/phase-1/reference/"
  - "docs/phase-2/PRD-0003-Phase2-WSOP-Integration.md"
  - "docs/phase-3/PRD-0003-Phase3-EBS-Automation.md"
  - "docs/operations/PHASE-PROGRESSION.md"
  - "docs/operations/VENDOR-MANAGEMENT.md"

stakeholders:
  - "방송팀"
  - "기술팀"
  - "운영팀"
  - "경영진"

approvals:
  - reviewer: "EBS Team Lead"
    date: "2026-01-15"
    status: "approved"
---

# PRD-0003: EBS Event Broadcasting System

# 1. Executive Summary

## 1.1 제품 비전

> **"WSOP STUDIO의 DB 자산을 내재화하여, 데이터 기반 방송과 사업 확장을 실현한다"**

EBS(Event Broadcasting System)는 **WSOP STUDIO에서 축적된 핸드 히스토리와 플레이어 통계 데이터를 자체 시스템으로 내재화**하는 것을 핵심 목표로 합니다. RFID 기반 포커 카드 인식 시스템을 통해:

1. **DB 자산 완전 소유**: 핸드 히스토리, 플레이어 통계를 자체 DB로 축적
2. **데이터 기반 확장**: 방송 콘텐츠, 비즈니스, 분석 역량 강화
3. **운영 자동화**: 시청자 정보 즉시 제공, 운영자 간편 입력, 전 과정 자동화

를 실현하는 시스템입니다.

## 1.1.1 Infrastructure Perspective

> **"EBS는 포커 프로덕션의 데이터 중심축이다"**

EBS는 단순한 RFID 카드 인식 시스템이 아닙니다. EBS는:

| 역할 | 설명 |
|------|------|
| **데이터 생산자** | 핸드, 액션, 팟 이벤트 생성 |
| **듀얼 소스 통합** | EBS + WSOPLIVE 두 소스를 연결하는 브릿지 역할 |
| **API 제공자** | 외부 시스템에 실시간/배치 데이터 제공 |
| **분석 기반** | 콘텐츠, 통계, 인사이트의 원천 |

상세 비전은 본 문서 Section 1을 참조하세요.

## 1.2 핵심 가치 제안 (Value Proposition)

| 핵심 가치 | 설명 | 고객 혜택 |
|-----------|------|----------|
| **DB 자산 내재화** | 핸드 히스토리, 플레이어 통계 자체 소유 | 데이터 독립성, 분석 자유도, 비즈니스 확장 |
| **시청자 중심 정보 전달** | 핸드, 팟, 확률, 액션을 실시간 표시 | 몰입감 있는 시청 경험 |
| **간편한 운영자 입력** | 최소 클릭으로 모든 정보 입력 | 운영 부담 80% 감소 |
| **완전 자동화** | 카드 인식 → 그래픽 → 팟 계산 자동 | 인력/실수 최소화 |
| **Trustless Security** | 운영자조차 실시간 카드 정보 접근 불가 | 게임 무결성 100% 보장 |

## 1.3 4단계 개발 전략

EBS는 **하드웨어 검증과 소프트웨어 개발의 병렬 진행**을 통해 안정적으로 발전합니다:

| Phase | 완료 시점 | 핵심 전략 | 슬로건 |
|-------|:--------:|----------|--------|
| **Phase 0** | 2026 Q2 | RFID 업체 선정 + POC 검증 | "준비 완료" |
| **Phase 1** | 2026 Q4 | PokerGFX 100% 복제 | "동일하게" |
| **Phase 2** | 2027 Q4 | WSOPLIVE DB 연동 | "연결한다" |
| **Phase 3** | 2028 Q4 | 자동화 프로토콜 | "프로덕션 최적화" |

**총 개발 기간**: 3년 (2026-2028)

### Phase 0과 Phase 1 병렬 진행

**Phase 0 (비즈니스)**와 **Phase 1 (개발)**은 동시에 시작 가능:

| 담당 | Phase 0 (4-6주) | Phase 1 (6개월) |
|------|-----------------|-----------------|
| **비즈니스팀** | 업체 연락, 견적, 발주 | RFID 하드웨어 도착 대기 |
| **개발팀** | 관리 체계 구축 | PokerGFX 복제 시작 (소프트웨어) |

**병렬 진행 이점:**
- RFID 하드웨어 도착 전에 소프트웨어 개발 착수
- Phase 1 중반에 실제 하드웨어로 통합 테스트
- 전체 일정 단축 (약 4-6주 절감)

**상세 기획서:**
- [Phase 1: PokerGFX 완전 복제](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)
- [Phase 2: WSOPLIVE DB 연동](phase-2/PRD-0003-Phase2-WSOP-Integration.md)
- [Phase 3: EBS 자동화 프로토콜](phase-3/PRD-0003-Phase3-EBS-Automation.md)

## 1.4 주요 기능 요약

| 카테고리 | 기능 |
|----------|------|
| **시청자 정보** | 실시간 홀카드 표시, 승률/아웃츠 자동 계산, 팟 사이즈, 플레이어 통계 (VPIP, PFR), 핸드 히스토리 |
| **운영자 입력** | 원클릭 액션 입력, 스마트 베팅 예측, 드래그 앤 드롭 플레이어 관리, 음성 입력 (선택), Stream Deck |
| **자동화** | 카드 인식→그래픽, 액션→팟 계산, 핸드 종료 감지, 딜러 버튼 이동, 핸드 히스토리 저장 |
| **보안** | Trustless Mode, Realtime Mode, AES-256 DB 암호화, TLS 1.3, HSM (Enterprise) |
| **프로덕션** | OBS Browser Source, NDI 출력, Chroma Key, 다중 테이블 |
| **커스터마이징** | 스킨 시스템, 다국어, 커스텀 애니메이션, 레이아웃 에디터 |

## 1.5 문서 정체성

> **본 문서는 비전/전략 문서입니다. 상세 설계 명세는 Phase별 문서를 참조하세요.**

| 문서 유형 | 역할 | 상세 수준 |
|----------|------|----------|
| **Master PRD (본 문서)** | 비전, 전략, 로드맵 | 고수준 개요 |
| **Phase PRD** | 구현 계획, 기능 명세 | 상세 설계 |

Phase 0 (PokerGFX 복제) 완료 시점에 개발 명세가 명확해지며, 이후 상세 설계 문서가 산출됩니다.

---

# 2. 제작 의도 및 목적

## 2.1 왜 EBS를 만드는가

EBS의 핵심 목적은 **WSOP STUDIO DB 자산 내재화**입니다. 이는 Section 1.1에서 정의한 제품 비전을 실현하는 것입니다.

### 내재화 대상

| 자산 유형 | 현황 | EBS 목표 |
|----------|------|----------|
| 핸드 히스토리 | 외부 시스템 의존 | 자체 DB 완전 소유 |
| 플레이어 통계 | 제한된 API 의존 | 커스텀 통계 무제한 |
| 방송 메타데이터 | 플랫폼 종속 | 독립적 저장/활용 |

### 부차적 목적: 시장 문제점 해결

| 문제점 | EBS 솔루션 |
|--------|-----------|
| 운영 복잡성 | 자동화 + 간편 UI |
| 시청자 경험 부족 | 실시간 정보 |
| 보안 취약점 | Trustless Mode |

## 2.2 경쟁사 분석 (PokerGFX)

| 항목 | PokerGFX | EBS | 차별점 |
|------|----------|-----|--------|
| 운영 복잡도 | 높음 (전담 인력) | 낮음 (자동화) | 80% 간편화 |
| 정보 입력 | 수동 중심 | 자동 + 최소 수동 | 스마트 입력 |
| 시청자 정보 | 기본 | 풍부 (통계, 확률) | 시청자 중심 |
| WSOPLIVE 연동 | 없음 | 완전 통합 | DB 동기화 |
| DB 소유권 | 외부 의존 | 자체 완전 소유 | 데이터 독립 |

**PokerGFX 강점:** 10년+ 경험, WSOP/WPT 공식 파트너, Secure Delay
**PokerGFX 약점:** 복잡한 UI, 느린 지원 (72시간), 아시아 지원 미흡

---

# 3. 타겟 사용자

## 3.1 사용자 분류

EBS는 **DB 자산을 활용**하는 네 가지 핵심 역할을 위해 설계됩니다:

| 역할 | 소속 | 핵심 목표 | EBS 제공 가치 |
|------|------|----------|--------------|
| **시청자** | 외부 | 정보 소비 | 실시간 홀카드, 승률, 통계 |
| **테이블 운영** | Table Operations | 데이터 입력 | 스마트 입력, 자동 팟 계산 |
| **콘텐츠 PD** | Content Team | 콘텐츠 제작 | 하이라이트 자동 생성 |
| **데이터 분석** | Analytics Team | 인사이트 도출 | SQL 쿼리, 데이터 내보내기 |

## 3.2 페르소나 요약

### 시청자 (김철수)
- **목표:** 몰입감 있는 시청, 플레이어 스타일 파악, 핸드 복기
- **활용:** 실시간 홀카드/승률, VPIP/PFR 통계, 히스토리

### 테이블 운영자 (박준영)
- **목표:** 최소 클릭으로 액션 입력, RFID 안정 운영, 팟/칩 관리
- **활용:** 원클릭 입력, RFID→카드 매핑, 드래그 앤 드롭 설정

### 콘텐츠 PD (김영호)
- **목표:** 하이라이트 자동화, 해설 콘텐츠, 데이터 기반 기획
- **활용:** 핸드 데이터 태깅, 콘텐츠 API, 통계 공개

### 데이터 분석가 (박지원)
- **목표:** 플레이어 패턴, A/B 테스트, 예측 모델
- **활용:** SQL 인터페이스, Jupyter 통합, CSV/Parquet 내보내기

---

# 4. 핵심 기능 개요

> **상세 기능 명세는 Phase 1 완료 후 확정됩니다.**
> 본 섹션은 비전 수준의 기능 목표만 제시합니다.

## 4.1 기능 비전

EBS는 세 가지 핵심 기능 영역을 제공합니다:

| 영역 | 비전 | 상세 명세 |
|------|------|----------|
| **시청자 정보 표시** | 홀카드, 승률, 통계를 실시간 표시 | [Phase 1 PRD §2](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) |
| **운영자 입력** | 최소 클릭으로 액션 입력 | [Phase 1 PRD §2.1](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) |
| **프로덕션 통합** | OBS, NDI 출력 지원 | [Phase 1 PRD §2.3](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) |

## 4.2 Phase별 기능 확장 요약

| 기능 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| 카드 인식 | RFID 자동 | 동일 | 동일 |
| 팟 계산 | 수동 입력 | DB 동기화 | 자동 계산 |
| 플레이어 통계 | 수동 설정 | WSOPLIVE 연동 | 실시간 자동 |
| 입력 방식 | 원클릭 | 30% 감소 | 80% 감소 |

## 4.3 컨셉 목업 (비전 전달용)

다음 목업은 **최종 스펙이 아닌 비전 전달 목적**입니다.
Phase 0 개발 중 변경될 수 있습니다.

### 컨셉 목업 (Phase 0 개발 시 정의)

Phase 0 개발 중 다음 목업이 작성됩니다:
- **Viewer Overlay**: 시청자 화면 레이아웃
- **Action Tracker**: 운영자 입력 화면
- **Production Dashboard**: 프로덕션 통합

> **상세 UI 명세, 워크플로우, 성능 목표**는 Phase PRD를 참조하세요.

---

# 5. 자동화 목표

> **상세 자동화 시나리오는 Phase 1 개발 중 정의됩니다.**

## 5.1 자동화 비전

EBS의 궁극적 목표는 **수동 입력 80% 감소** (Phase 3 완료 시)입니다.

| Phase | 자동화 수준 | 수동 입력 |
|-------|------------|----------|
| Phase 1 | 카드 인식만 자동 | 액션/베팅 수동 |
| Phase 2 | DB 동기화 추가 | 30% 감소 |
| Phase 3 | 팟/칩 자동 추적 | 80% 감소 |

## 5.2 핵심 자동화 영역

| 영역 | 자동화 방식 |
|------|------------|
| **항상 자동** | 카드 인식, 승률 계산, 핸드 히스토리 저장, 버튼 이동 |
| **점진적 자동화** | 팟 계산, 칩 카운트, 플레이어 통계 |
| **수동 유지** | 베팅 액션 입력 (Phase 3에서 옵션으로 자동화) |

> **상세 자동화 시나리오, 흐름도, 데이터 스키마**는 [Phase 1 PRD](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)를 참조하세요.

---

# 6. 보안 원칙

> **상세 암호화 스펙, 워크플로우는 Phase 1 보안 설계 문서에서 정의됩니다.**

## 6.1 Dual Mode 개념

EBS는 사용 시나리오에 따라 두 가지 보안 모드를 지원합니다:

| 모드 | 용도 | 원칙 |
|------|------|------|
| **Realtime Mode** | 녹화, 테스트 | 카드 즉시 공개 |
| **Trustless Mode** | 라이브 방송 | 딜레이 후 공개 |

## 6.2 보안 원칙

| 원칙 | 설명 |
|------|------|
| **Trustless** | 운영자 포함 누구도 딜레이 전 카드 정보 접근 불가 |
| **전 구간 암호화** | RFID, 통신, DB 모든 구간 암호화 |
| **역할 기반 접근** | 역할별 권한 분리 |

> **상세 암호화 스펙 (알고리즘, 키 관리), Trustless Mode 워크플로우**는
> [Phase 1 PRD](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) 및 보안 설계 문서를 참조하세요.

---

# 7. 개발 로드맵 (2026-2028)

## 7.1 Phase 마스터 테이블

> Phase 로드맵 정의는 이 섹션이 **단일 진실 공급원**입니다.
> Section 1.3은 이 테이블을 요약한 것입니다.

| Phase | 완료 | 핵심 목표 | 성공 지표 | 슬로건 |
|-------|:----:|----------|----------|--------|
| **0** | Q2 2026 | RFID 업체 선정 + POC | 계약 + POC 통과 | "준비 완료" |
| **1** | Q4 2026 | PokerGFX 100% 복제 | 운영자 2명+ "동일" 승인 | "동일하게" |
| **2** | Q4 2027 | WSOPLIVE DB 연동 | 입력 30% 감소 | "연결한다" |
| **3** | Q4 2028 | 자동화 프로토콜 | 입력 80% 감소 | "프로덕션 최적화" |

**진행 원칙**: Gate 조건 만족 시에만 다음 Phase로 진행

## 7.2 Phase 0/1 병렬 진행

| Week | Phase 0 (비즈니스) | Phase 1 (개발) |
|:----:|-------------------|---------------|
| 1-2 | 업체 연락, 견적 요청 | PokerGFX 기능 분석 |
| 3-6 | 샘플 검토, 발주 | UI 프로토타입, 오버레이 |
| 7-12 | 하드웨어 도착 대기 | Action Tracker 개발 |
| 13-24 | RFID 통합 테스트 | 전체 시스템 검증 |

**이점:** SW 선개발로 전체 일정 4-6주 단축

## 7.3 Phase별 상세 문서

| Phase | 문서 | 주요 내용 |
|-------|------|----------|
| 0 | [VENDOR-SELECTION-CHECKLIST.md](phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 기준, 체크리스트 |
| 1 | [PRD-0003-Phase1-PokerGFX-Clone.md](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) | 기능 매핑, 주차별 계획, Gate 조건 |
| 2 | [PRD-0003-Phase2-WSOP-Integration.md](phase-2/PRD-0003-Phase2-WSOP-Integration.md) | API 명세, 동기화 로직, 에러 핸들링 |
| 3 | [PRD-0003-Phase3-EBS-Automation.md](phase-3/PRD-0003-Phase3-EBS-Automation.md) | 자동화 알고리즘, 성능 요구사항 |

## 7.4 Phase Gate 조건

### Phase 0 완료 조건 (2026년 Q2)

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| 업체 선정 | ST25R3911B 공급 업체 확정 | 계약서 |
| 발주 완료 | RFID 하드웨어 주문 완료 | 발주서 |
| 관리 체계 | PRD, 업무 대시보드 완성 | 문서 검토 |
| PDCA 시스템 | Snapshot 자동화 가동 | 실행 로그 |

### Phase 1 → Phase 2 Gate (2026년 Q4)

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| 기능 구현 | PokerGFX-Feature-Checklist.md 100% | 체크리스트 검토 |
| 방송 테스트 | 4시간 연속 운영, 에러 0건 | 로그 검증 |
| 운영자 승인 | 2명+ "동일 수준" 서명 | 서명 문서 |
| 성능 | 카드 < 200ms, 승률 < 100ms | 성능 테스트 |
| RFID 통합 | 5장 카드 100% 인식 | 테스트 로그 |

### Phase 2 → Phase 3 Gate (2027년 Q4)

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| 연결 안정성 | 24시간 99%+ 가동률 | 모니터링 로그 |
| 데이터 정합성 | WSOPLIVE vs EBS 100% 일치 | 비교 테스트 |
| 동기화 성능 | 지연 < 5초 (95th) | 성능 테스트 |
| 입력 감소 | Phase 1 대비 30%+ | 입력 횟수 비교 |

### Phase 3 완료 조건 (2028년 Q4)

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| 자동화율 | 입력 80% 감소 (Phase 1 대비) | 입력 횟수 비교 |
| 팟 계산 | 100% 정확도 (100핸드) | 수동 검증 |
| 시스템 안정성 | 8시간 99.9% 가동률 | 모니터링 |
| 성능 | 팟 < 100ms, 칩 동기화 < 500ms | 성능 테스트 |

## 7.5 연간 마일스톤

### 2026년

| 분기 | Phase | 목표 |
|------|-------|------|
| Q1-Q2 | Phase 0 | RFID 업체 선정, POC 검증 완료 |
| Q3 | Phase 1 | PokerGFX 기능 분석, UI 프로토타입 |
| Q4 | Phase 1 | PokerGFX 복제 완료, Gate 통과 |

### 2027년

| 분기 | Phase | 목표 |
|------|-------|------|
| Q1-Q2 | Phase 2 | WSOPLIVE API 연동 기초, 데이터 구조 분석 |
| Q3 | Phase 2 | 칩/플레이어 동기화 구현 |
| Q4 | Phase 2 | WSOPLIVE DB 연동 완료, Gate 통과 |

### 2028년

| 분기 | Phase | 목표 |
|------|-------|------|
| Q1-Q2 | Phase 3 | 자동화 프로토콜 설계/구현 |
| Q3 | Phase 3 | 프로덕션 최적화 적용 |
| Q4 | Phase 3 | 최종 검증, 프로젝트 완료 |

---

# 8. Infrastructure Vision

## 8.1 RFID 프로젝트 vs 인프라

| 관점 | RFID 프로젝트 | 인프라스트럭처 |
|------|-------------|---------------|
| 핵심 목표 | 카드 → 화면 | 데이터 흐름 중심 |
| API 방향 | 소비 (WSOPLIVE → EBS) | **제공 (EBS → 외부)** |
| SLA | 4시간 무중단 | 99.9% 가용성 |
| 확장성 | 단일 테이블 | 동시 10개 테이블 |

## 8.2 Phase별 인프라 마일스톤

| Phase | 인프라 목표 | 기능 목표와 연계 |
|-------|-----------|----------------|
| Pre | 문서화 시스템, PDCA | 프로젝트 관리 |
| 0 | 메트릭 로깅, API Gateway | PokerGFX 복제 + RFID 통합 |
| 1 | Message Queue, Multi-table | WSOPLIVE 동기화 |
| 2 | Event Sourcing, Data Lake | 자동화 학습 데이터 |

## 8.3 SLA 정의

| 지표 | 목표 | 측정 |
|------|------|------|
| 가용성 | 99.9% | 월 다운타임 < 43.8분 |
| API 응답 | p95 < 500ms | 모니터링 |
| RPO | 1핸드 | 최대 데이터 손실 |
| RTO | 5분 | 복구 시간 |

상세는 본 문서 Section 8을 참조하세요.

---

# 9. 부록

## 9.1 용어 정의

| 용어 | 정의 |
|------|------|
| **Trustless Mode** | 운영자 포함 누구도 딜레이 전 카드 정보에 접근할 수 없는 보안 모드 |
| **Realtime Mode** | 카드 스캔 즉시 정보가 공개되는 일반 모드 |
| **Action Tracker** | 베팅 액션을 입력하는 운영자용 인터페이스 |
| **Pot Equity** | 현재 상황에서 각 플레이어의 승리 확률 |
| **Outs** | 상대방을 역전할 수 있는 남은 카드 |
| **VPIP** | Voluntarily Put $ In Pot, 자발적으로 팟에 참여한 비율 |
| **PFR** | Pre-Flop Raise, 프리플랍에서 레이즈한 비율 |

## 9.2 참조 문서

| 유형 | 문서 | 용도 |
|------|------|------|
| **Phase PRD** | [Phase1-PokerGFX-Clone](phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) | Phase 1 계획 |
| | [Phase2-WSOP-Integration](phase-2/PRD-0003-Phase2-WSOP-Integration.md) | Phase 2 계획 |
| | [Phase3-EBS-Automation](phase-3/PRD-0003-Phase3-EBS-Automation.md) | Phase 3 계획 |
| **운영** | [PHASE-PROGRESSION](operations/PHASE-PROGRESSION.md) | Phase 진행 가이드 |
| | [VENDOR-MANAGEMENT](operations/VENDOR-MANAGEMENT.md) | 업체 관리 |
| | [EBS-WORK-DASHBOARD](operations/EBS-WORK-DASHBOARD.md) | 업무 현황 |
| **기능** | [PokerGFX-Feature-Checklist](phase-1/PokerGFX-Feature-Checklist.md) | 기능 체크리스트 |
| | [VENDOR-SELECTION-CHECKLIST](phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 체크리스트 |

---

# 10. 문서 정보

## 10.1 문서 메타데이터

| 항목 | 내용 |
|------|------|
| **문서 버전** | 8.0.0 |
| **작성일** | 2026-02-03 |
| **작성자** | BRACELET STUDIO |
| **검토자** | Technical Architect |
| **승인자** | Product Owner |
| **상태** | **Draft** |
| **분류** | 기밀 (Confidential) |

## 10.2 v3.0 vs v4.0 방향 전환

| 영역 | v3.0 (이전) | v4.0 (현재) |
|------|-------------|-------------|
| **핵심 목적** | 보안 (Trustless Security) | **WSOP STUDIO DB 자산 내재화** |
| **핵심 초점** | 기술적 암호화 | **데이터 소유 + 방송 워크플로우** |
| **타겟 사용자** | 운영자 중심 | **방송 확장 / 사업 확장 / 데이터 분석** |
| **설계 원칙** | 보안 우선 | 데이터 축적 + 보안 + 자동화 균형 |

## 10.3 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0.0 | 2026-01-22 | 초안 (MVP 중심) | EBS Team |
| 2.0.0 | 2026-01-25 | 상용 솔루션 + TLEK 기반 | EBS Team |
| 2.1.0 | 2026-01-26 | Retrospective Overlay 패턴 전환 | Architect |
| 2.2.0 | 2026-01-26 | Dual Mode 아키텍처 추가 | Architect |
| 3.0.0 | 2026-01-27 | 완전한 PRD 재작성: 페르소나, 사용자 스토리, 비즈니스 모델 포함 | Product Team |
| 4.0.0 | 2026-01-27 | 방송 워크플로우 최적화 + 자동화 시스템 중심 전면 재설계 | Product Team |
| 5.0.0 | 2026-01-27 | 3단계 개발 전략 추가, Stage별 구현 수준 분리, 가격 정보 제거 | Product Team |
| 5.1.0 | 2026-01-28 | Stage 0 추가 (하드웨어 학습 단계), 연간 타임라인 (2026-2028) 명시 | Product Team |
| 5.2.0 | 2026-01-28 | Master PRD 정체성 재정립: 비전/전략 문서로 전환, 상세 설계 명세 Stage 문서로 위임 | Product Team |
| 5.3.0 | 2026-01-28 | Section 4-6 경량화: 상세 스펙 제거, 비전/목표 요약만 유지, Stage PRD 참조로 전환 | Product Team |
| 5.4.0 | 2026-01-28 | Section 7 (기술 스택) 제거: Stage PRD로 위임, 섹션 번호 재정렬 (7→8→9) | Product Team |
| 5.5.0 | 2026-01-28 | 문서 제목 변경 (Secure Poker → Event), 수평선 정리, Appendix 제거 | Product Team |
| 5.6.0 | 2026-02-02 | Section 8 Infrastructure Vision 추가, 인프라 관점 명시, related_docs 업데이트 | Product Team |
| **6.0.0** | **2026-02-03** | **Stage → Phase 전환, 5단계 → 4단계 통합 (Phase-Pre/0 병렬 진행), 하드웨어 검증 Phase-Pre로 흡수** | Product Team |
| **6.1.0** | **2026-02-03** | **회사명 BRACELET STUDIO 통일** | BRACELET STUDIO |
| **7.0.0** | **2026-02-03** | **일정 전면 수정 (Q2/Q4 마일스톤), WSOP+ → WSOPLIVE 변경, 듀얼 소스 아키텍처 정의** | BRACELET STUDIO |
| **7.1.0** | **2026-02-03** | **끊어진 링크 정리, 삭제된 문서 참조 제거, related_docs 업데이트** | BRACELET STUDIO |
| 7.2.0 | 2026-02-03 | 섹션 1.4 "v3.0 vs v4.0 방향 전환"을 부록(10.2)으로 이동, 문서 업데이트 내용 최하단 배치 원칙 적용 | BRACELET STUDIO |
| **8.0.0** | **2026-02-03** | **중복 제거 리팩터링: Section 2 통합(38줄→15줄), 페르소나 압축(100줄→30줄), Phase 테이블 단일화(§7.1), 참조문서 통합** | BRACELET STUDIO |
| **8.1.0** | **2026-02-04** | **문서 정합성 수정: YAML 중복 키 제거, 끊어진 CONCEPT 링크 수정, Phase 테이블 링크 업데이트** | BRACELET STUDIO |

---

**Version**: 8.1.0 | **Updated**: 2026-02-04 | **BRACELET STUDIO**
