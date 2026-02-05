---
doc_type: "prd"
doc_id: "PRD-0003-EBS-Master"
version: "9.0.0"
status: "approved"
owner: "BRACELET STUDIO"
last_updated: "2026-02-05"
next_review: "2026-07-01"
phase: "master"
priority: "critical"

depends_on: []

related_docs:
  - "docs/1-phase-0/VENDOR-SELECTION-CHECKLIST.md"
  - "docs/2-phase-1/PRD-0003-Phase1-PokerGFX-Clone.md"
  - "docs/2-phase-1/PokerGFX-Feature-Checklist.md"
  - "docs/2-phase-1/reference/"
  - "docs/3-phase-2/PRD-0003-Phase2-WSOP-Integration.md"
  - "docs/4-phase-3/PRD-0003-Phase3-EBS-Automation.md"
  - "docs/5-operations/PHASE-PROGRESSION.md"
  - "docs/5-operations/VENDOR-MANAGEMENT.md"

stakeholders:
  - "방송팀"
  - "기술팀"
  - "운영팀"
  - "경영진"

approvals:
  - reviewer: "EBS Team Lead"
    date: "2026-02-05"
    status: "approved"
---

# PRD-0003: EBS Event Broadcasting System

# 1. 비전과 목적

## 1.1 제품 비전

> **"WSOP STUDIO의 DB 자산을 내재화하여, 데이터 기반 방송과 사업 확장을 실현한다"**

EBS는 RFID 기반 포커 카드 인식 시스템을 통해 다음 세 가지를 실현합니다:

1. **DB 자산 완전 소유**: 핸드 히스토리, 플레이어 통계를 자체 DB로 축적
2. **데이터 기반 확장**: 방송 콘텐츠, 비즈니스, 분석 역량 강화
3. **운영 자동화**: 시청자 정보 즉시 제공, 운영자 간편 입력, 전 과정 자동화

## 1.2 왜 EBS를 만드는가

핸드 히스토리와 플레이어 통계는 방송 품질과 사업 확장의 핵심 자산입니다. 현재 이 데이터를 외부 시스템에 의존하고 있어 활용에 제약이 있습니다. EBS를 통해 데이터를 자체 소유하고, 커스텀 분석과 콘텐츠 생산을 자유롭게 수행합니다.

> 경쟁사 분석은 [Phase 1 PRD](2-phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)를 참조하세요.

## 1.3 핵심 가치 제안

| 핵심 가치 | 설명 | 고객 혜택 |
|-----------|------|----------|
| **DB 자산 내재화** | 핸드 히스토리, 플레이어 통계 자체 소유 | 데이터 독립성, 분석 자유도, 비즈니스 확장 |
| **시청자 중심 정보 전달** | 핸드, 팟, 확률, 액션을 실시간 표시 | 몰입감 있는 시청 경험 |
| **간편한 운영자 입력** | 최소 클릭으로 모든 정보 입력 | 운영 부담 80% 감소 |
| **완전 자동화** | 카드 인식 → 그래픽 → 팟 계산 자동 | 인력/실수 최소화 |

## 1.4 문서 정체성

> **본 문서는 비전/전략 문서입니다. 상세 설계 명세는 Phase별 문서를 참조하세요.**

| 문서 유형 | 역할 | 상세 수준 |
|----------|------|----------|
| **Master PRD (본 문서)** | 비전, 전략, 로드맵 | 고수준 개요 |
| **Phase PRD** | 구현 계획, 기능 명세 | 상세 설계 |

Phase 0 진행 중이므로 상세 스펙은 Phase PRD에 위임합니다.

---

# 2. 타겟 사용자

## 2.1 사용자 분류

EBS는 **DB 자산을 활용**하는 네 가지 핵심 역할을 위해 설계됩니다:

| 역할 | 소속 | 핵심 목표 | EBS 제공 가치 |
|------|------|----------|--------------|
| **시청자** | 외부 | 정보 소비 | 실시간 홀카드, 승률, 통계 |
| **테이블 운영** | Table Operations | 데이터 입력 | 스마트 입력, 자동 팟 계산 |
| **콘텐츠 PD** | Content Team | 콘텐츠 제작 | 하이라이트 자동 생성 |
| **데이터 분석** | Analytics Team | 인사이트 도출 | SQL 쿼리, 데이터 내보내기 |

## 2.2 페르소나 요약

### 시청자 (김철수)
- **목표:** 몰입감 있는 시청, 플레이어 스타일 파악, 핸드 복기
- **활용:** 실시간 홀카드/승률, VPIP/PFR 통계, 히스토리

### 테이블 운영자 (박준영)
- **목표:** 최소 클릭으로 액션 입력, RFID 안정 운영, 팟/베팅 토큰 관리
- **활용:** 원클릭 입력, RFID→카드 매핑, 드래그 앤 드롭 설정

### 콘텐츠 PD (김영호)
- **목표:** 하이라이트 자동화, 해설 콘텐츠, 데이터 기반 기획
- **활용:** 핸드 데이터 태깅, 콘텐츠 API, 통계 공개

### 데이터 분석가 (박지원)
- **목표:** 플레이어 패턴, A/B 테스트, 예측 모델
- **활용:** SQL 인터페이스, Jupyter 통합, CSV/Parquet 내보내기

---

# 3. 핵심 기능 개요

## 3.1 Phase 1 기능 (확정)

Phase 1은 **PokerGFX 100% 복제**가 목표입니다. 복제 대상 기능 전체 목록은 [PokerGFX Feature Checklist (119개)](2-phase-1/PokerGFX-Feature-Checklist.md)를 참조하세요.

**카테고리별 요약:**

| 카테고리 | 기능 |
|----------|------|
| **카드 표시** | 실시간 홀카드 표시, 승률/아웃츠 자동 계산, 팟 사이즈, 플레이어 통계 (VPIP, PFR), 핸드 히스토리 |
| **운영자 입력** | 원클릭 액션 입력, 스마트 베팅 예측, 드래그 앤 드롭 플레이어 관리, Stream Deck |
| **프로덕션 통합** | OBS Browser Source, NDI 출력, Chroma Key, 다중 테이블 |
| **보안** | Realtime Mode + Trustless Mode (PokerGFX 동일) |
| **커스터마이징** | TBD |

> 상세 기능 명세는 [Phase 1 PRD](2-phase-1/PRD-0003-Phase1-PokerGFX-Clone.md)를 참조하세요.

## 3.2 Phase 2/3 기능 (TBD)

Phase 1 완료 후 실제 운영 경험을 바탕으로 설계합니다.

| 기능 | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| 카드 인식 | RFID 자동 | TBD | TBD |
| 팟 계산 | 수동 입력 | TBD | TBD |
| 플레이어 통계 | 수동 설정 | TBD | TBD |
| 입력 방식 | 원클릭 | TBD | TBD |

---

# 4. 보안 원칙

## 4.1 Phase 1 보안 (PokerGFX 동일)

PokerGFX도 **Realtime Mode**로 운영합니다. 카드 스캔 즉시 시스템에 반영하고, 방송 딜레이는 스튜디오(OBS/하드웨어)에서 처리합니다.

| 모드 | 설명 | 운영 방식 |
|------|------|----------|
| **Realtime Mode** | 카드 스캔 즉시 시스템에 반영 | **실제 운영에 사용**. 방송 딜레이는 OBS/하드웨어에서 처리 |
| **Trustless Mode** | 딜레이 후 카드 공개 | PokerGFX에 기능으로 존재하므로 **복제 대상**. 실제 운영은 Realtime Mode |

**모드 전환:** 운영자 설정에서 토글 가능

## 4.2 Phase 2+ 보안 (TBD)

Phase 1 완료 후 실제 운영 경험을 바탕으로 재설계합니다.

---

# 5. 개발 로드맵

## 5.1 Phase 마스터 테이블

> Phase 로드맵 정의는 이 섹션이 **단일 진실 공급원**입니다.

| Phase | 완료 | 핵심 목표 | 성공 지표 | 슬로건 |
|-------|:----:|----------|----------|--------|
| **0** | Q2 2026 | RFID 업체 선정 + POC + PokerGFX 기능 분석/기획 | 계약 + POC 통과 + 기능 체크리스트 확정 | "준비 완료" |
| **1** | Q4 2026 | PokerGFX 100% 복제 (순수 개발) | 운영자 2명+ "동일" 승인 | "동일하게" |
| **2** | Q4 2027 | WSOPLIVE DB 수작업을 자동화 처리 | TBD | "자동화한다" |
| **3** | Q4 2028 | 자동화 프로토콜 | TBD | "프로덕션 최적화" |

**총 개발 기간**: 3년 (2026-2028)

## 5.2 Phase 0/1 병렬 진행

| Week | Phase 0 (비즈니스 + 기획) | Phase 1 (순수 개발) |
|:----:|--------------------------|-------------------|
| 1-2 | 업체 연락, 견적 요청 + PokerGFX 기능 분석 | - |
| 3-6 | 샘플 검토, 발주 + UI 분석, 기능 체크리스트 확정 | - |
| 7-12 | 하드웨어 도착 + Phase 1 상세 설계 | UI 프로토타입, 오버레이 개발 시작 |
| 13-24 | RFID 통합 테스트 | Action Tracker 개발, 전체 시스템 검증 |

**이점:** SW 선개발로 전체 일정 4-6주 단축

## 5.3 Phase별 상세 문서

| Phase | 문서 | 주요 내용 |
|-------|------|----------|
| 0 | [VENDOR-SELECTION-CHECKLIST.md](1-phase-0/VENDOR-SELECTION-CHECKLIST.md) | 업체 선정 기준, 체크리스트 |
| 1 | [PRD-0003-Phase1-PokerGFX-Clone.md](2-phase-1/PRD-0003-Phase1-PokerGFX-Clone.md) | 기능 매핑, 주차별 계획, Gate 조건 |
| 2 | [PRD-0003-Phase2-WSOP-Integration.md](3-phase-2/PRD-0003-Phase2-WSOP-Integration.md) | API 명세, 동기화 로직, 에러 핸들링 |
| 3 | [PRD-0003-Phase3-EBS-Automation.md](4-phase-3/PRD-0003-Phase3-EBS-Automation.md) | 자동화 알고리즘, 성능 요구사항 |

---

# 6. 문서 정보

## 6.1 메타데이터

| 항목 | 내용 |
|------|------|
| **문서 버전** | 9.0.0 |
| **작성일** | 2026-02-05 |
| **작성자** | BRACELET STUDIO |
| **검토자** | Technical Architect |
| **승인자** | Product Owner |
| **상태** | **Draft** |
| **분류** | Confidential |

## 6.2 v3.0 vs v4.0 방향 전환

| 영역 | v3.0 (이전) | v4.0 (현재) |
|------|-------------|-------------|
| **핵심 목적** | 보안 (Trustless Security) | **WSOP STUDIO DB 자산 내재화** |
| **핵심 초점** | 기술적 암호화 | **데이터 소유 + 방송 워크플로우** |
| **타겟 사용자** | 운영자 중심 | **방송 확장 / 사업 확장 / 데이터 분석** |
| **설계 원칙** | 보안 우선 | 데이터 축적 + 보안 + 자동화 균형 |

## 6.3 변경 이력

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
| **9.0.0** | **2026-02-05** | **구조 전면 재설계: Section 2/5/8/9 삭제, Section 1/4/6/7 통합/축소, Phase 0 확장(PokerGFX 기획 포함), Phase 2 슬로건 변경, 보안 섹션 수정(Trustless 오해 교정)** | BRACELET STUDIO |

---

**Version**: 9.0.0 | **Updated**: 2026-02-05 | **BRACELET STUDIO**
