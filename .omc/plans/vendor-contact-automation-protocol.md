# Vendor Contact Automation Protocol

**Version**: 1.1.0
**Created**: 2026-02-04
**Status**: READY FOR EXECUTION
**Parent**: `daily-intelligence-system.md`

---

## Context

### Original Request

업무 자동화 프로토콜 설계:
1. DM 알림 비활성화 (scope 문제) → Slack List 포스팅만 갱신
2. 후보 업체들 메일 발신 여부 확인 후 처리 프로토콜
3. 회신 draft 자동 작성 + 검토 요청 (질문 없이)
4. 사용자 수정 시 문서 반영

---

## Part 1: /daily 스킬 수정 규칙

### DM 알림 비활성화 (CRITICAL)

**현재 문제**: `chat:write:bot` scope 부족으로 DM 실패

**해결 방안**: `--notify` 플래그 사용 금지

| 기존 | 변경 |
|------|------|
| `python main.py --notify --post` | `python main.py --post` |

### /daily 실행 플래그 규칙

```
/daily                    → python main.py --post        (DM 없음, 채널만)
/daily --collect-only     → python main.py               (수집만)
/daily --no-post          → python main.py               (수집만)
/daily --full             → python main.py --full --post (전체 재수집 + 채널)
```

**절대 금지**: `--notify` 플래그 사용

### 채널 메시지 갱신 실패 시

1. 오류 메시지 출력
2. 코드 수정 시도 **금지**
3. Slack List만 업데이트 (별도 명령)

```bash
# 채널 갱신 실패 시 대안
/auto --update slacklist sync
```

---

## Part 2: 업체 컨택 현황 추적

### Source of Truth

**Single Source of Truth**: `VENDOR-MANAGEMENT.md` (docs/operations/)
- 이 문서의 컨택 현황은 Gmail/Slack 분석 결과를 **반영**한 것
- 상태 변경 시 `VENDOR-MANAGEMENT.md`를 **먼저** 업데이트
- Slack List는 `VENDOR-MANAGEMENT.md` 기준으로 동기화

### 현재 업체 목록 (16개) - Gmail 기반 분석

> **참고**: 아래 테이블은 Gmail 메일함 분석 결과입니다.
> `VENDOR-MANAGEMENT.md` 상태(참조/후보/조사중)와 다를 수 있으며,
> 실제 컨택 진행 시 해당 문서를 업데이트해야 합니다.

| 카테고리 | 업체 | Contact | Gmail 기반 상태 | VENDOR-MGMT 상태 |
|---------|------|---------|:---------------:|:----------------:|
| **RFID Hardware** | FEIG Electronic | info@feig.de | ❌ 미발신 | 조사중 |
| | Pongee Industries | pongee@pongee.com.tw | ❌ 미발신 | 후보 |
| | Identiv | sales@identiv.com | ❌ 미발신 | 후보 |
| | GAO RFID | sales@gaorfid.com | ❌ 미발신 | 후보 |
| **Casino Solutions** | Abbiati | info@abbiati.com | ❌ 미발신 | 참조 |
| | Matsui | N/A | ⚪ 연락처 없음 | 참조 |
| | **SUN-FLY** | susie.su@sun-fly.com | 🔴 **회신필요** | 참조 |
| | S.I.T Korea | N/A | ⚪ 연락처 없음 | 참조 |
| **DIY/Development** | SparkFun | N/A | ⚪ 학습용 | 학습용 |
| | Adafruit | N/A | ⚪ 학습용 | 학습용 |
| | Waveshare | service@waveshare.com | ❌ 미발신 | 조사중 |
| | ST Micro | N/A | ⚪ 부품 제조사 | 핵심 |
| **Benchmark** | RF Poker | N/A | ⚪ 벤치마크 | 벤치마크 |
| | Faded Spade | service@fadedspade.com | ❌ 미발신 | 조사중 |
| | **PokerGFX** | support@pokergfx.io | ✅ 정보확인완료 | 벤치마크 |
| | Angel Cards | N/A | ⚪ 벤치마크 | 조사중 |

### 컨택 상태 정의

| 상태 | 아이콘 | 설명 |
|------|:-----:|------|
| 미발신 | ❌ | 연락처 있음, 아직 메일 안 보냄 |
| 발신완료 | 📤 | 메일 발송함, 회신 대기 |
| 회신받음 | ✅ | 업체에서 회신함 |
| 회신필요 | 🔴 | 우리가 회신해야 함 |
| 완료 | ✔️ | 진행 완료 또는 Drop |
| 연락처없음 | ⚪ | 연락처 확보 필요 |

---

## Part 3: 업체별 처리 프로토콜

### 즉시 처리 필요 (🔴 회신필요)

#### SUN-FLY (susie.su@sun-fly.com)

**받은 메일 요약**:
> "We are interested in cooperating with you to develop a Poker RFID GFX system although we have no direct delivery experience yet, we can customize a workable solution"

**필요 액션**: 협력 조건 협의 회신

**회신 Draft**:
```
Subject: RE: Inquiry regarding Poker RFID GFX development experience

Dear Susie,

Thank you for your prompt response and interest in cooperating on the Poker RFID GFX system.

We would like to discuss the following points:

1. **Technical Specifications**
   - What RFID protocols does your solution support? (ISO 15693, ISO 14443, etc.)
   - What is the typical read range and multi-card reading capability?

2. **Customization Scope**
   - Can you provide a sample module for evaluation?
   - What is the estimated lead time for customization?

3. **Commercial Terms**
   - Could you share preliminary pricing for a sample order?
   - What MOQ would apply for production orders?

We are targeting Q2 2026 for our POC phase and would appreciate your earliest convenience.

Best regards,
Aiden Kim
GGPoker Technical Team
```

**검토 요청**: 위 내용으로 회신해도 될까요? 수정이 필요하면 말씀해 주세요.

**승인 후 저장 위치**: `docs/operations/email-drafts/SUN-FLY-reply-v1.md`

---

#### PokerGFX (support@pokergfx.io)

**받은 메일 요약**:
> "The PokerGFX live hand API is no longer available by request. This feature is now only available with an Enterprise license."

**필요 액션**: Enterprise 라이선스 비용 확인 (정보 수집)

**상태**: ⚪ 정보 확인 완료 (회신 불필요)
- Enterprise 전용 = 비용 부담 → 자체 개발 방향 확정
- 추가 컨택 보류

---

### 신규 컨택 필요 (❌ 미발신)

#### RFID Hardware 업체 (우선순위 HIGH)

| 업체 | Email | 발송 우선순위 |
|------|-------|:------------:|
| FEIG Electronic | info@feig.de | 1 |
| GAO RFID | sales@gaorfid.com | 2 |
| Identiv | sales@identiv.com | 3 |
| Pongee | pongee@pongee.com | 4 |

**공통 문의 Draft**:
```
Subject: Inquiry: Custom RFID Reader for Poker Card Tracking System

Dear Sales Team,

We are GGPoker, an online poker platform exploring RFID technology for our live event broadcasting system (Event Broadcasting System - EBS).

We are looking for an RFID reader/module solution with the following requirements:

**Technical Requirements:**
- Protocol: ISO 15693 or compatible (for NXP ICODE SLIX2 tags)
- Read Range: 5-10cm minimum
- Multi-card Reading: Capable of reading 2-5 cards simultaneously
- Interface: USB or SPI for integration with custom hardware

**Application:**
- Real-time poker card detection for live streaming
- Integration with custom broadcast graphics system
- Deployment in professional poker tournament environment

**Questions:**
1. Do you have existing products that meet these specifications?
2. Can you provide evaluation samples for our POC phase?
3. What customization options are available?
4. What is the typical lead time for sample delivery?

We are targeting Q2 2026 for initial POC testing.

Thank you for your time. We look forward to your response.

Best regards,
Aiden Kim
GGPoker Technical Team
```

**검토 요청**: 위 템플릿으로 4개 RFID Hardware 업체에 발송해도 될까요?

**승인 후 저장 위치**: `docs/operations/email-drafts/RFID-Hardware-inquiry-template-v1.md`

---

## Part 4: 자동화 워크플로우

### /daily 실행 시 처리 흐름

```
┌─────────────────────────────────────────────────────────────┐
│  /daily 실행                                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Python 자동화                                       │
│  python main.py --post  (DM 없음!)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Gmail 분석 (Claude)                                 │
│  - 신규 메일 확인                                             │
│  - 업체별 분류                                                │
│  - 회신 필요 여부 판단                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: 회신 필요 시 (자동)                                  │
│  - Draft 자동 작성                                           │
│  - 사용자에게 검토 요청                                       │
│  - "이 내용으로 회신할까요?" (Yes/No만)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: 사용자 피드백                                        │
│  - 승인 → 발송 (또는 클립보드 복사)                           │
│  - 수정 → 이 문서에 Draft 업데이트                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: 컨택 상태 업데이트                                   │
│  - Part 2 테이블 갱신                                        │
│  - Slack List 상태 변경 (필요 시)                            │
└─────────────────────────────────────────────────────────────┘
```

### 회신 Draft 작성 규칙

1. **질문 금지**: "작성할까요?" 묻지 말고 무조건 작성
2. **검토 요청 필수**: "이 내용으로 회신할까요?" (승인/거절만)
3. **수정 반영 필수**: 사용자가 수정하면 이 문서의 Draft 섹션 업데이트
4. **발송은 수동**: 자동 발송 기능 없음, 사용자가 직접 발송

---

## Part 5: Slack List 상태 업데이트 규칙

### 컨택 진행 시 상태 변경

| 액션 | 상태 변경 | 명령어 |
|------|----------|--------|
| 첫 메일 발송 | 후보 → 컨택중 | `/auto --update slacklist status {RecID} 컨택중` |
| 회신 받음 | 컨택중 → 검토중 | `/auto --update slacklist status {RecID} 검토중` |
| 샘플 요청 | 검토중 → 샘플대기 | `/auto --update slacklist status {RecID} 샘플대기` |
| 최종 선정 | 샘플대기 → 확정 | `/auto --update slacklist status {RecID} 확정` |
| 탈락 | Any → 탈락 | `/auto --update slacklist status {RecID} 탈락` |

### 상태 정의

| 상태 | 설명 |
|------|------|
| 후보 | 초기 등록, 컨택 전 |
| 컨택중 | 메일 발송함, 회신 대기 |
| 검토중 | 회신 받고 검토 진행 |
| 샘플대기 | 샘플/견적 요청 후 대기 |
| 확정 | 최종 선정 |
| 탈락 | 부적합 판정 |

---

## Part 6: /daily 스킬 업데이트 (COMPLETED ✅)

### 완료된 수정

**파일**: `C:\claude\ebs\.claude\skills\daily\SKILL.md` (v2.1.0)

| 항목 | Before | After | 상태 |
|------|--------|-------|:----:|
| Step 1 플래그 | `--notify --post` | `--post` | ✅ |
| Step 2 명령 | `python main.py --notify --post` | `python main.py --post` | ✅ |
| CRITICAL 경고 | 없음 | `--notify` 사용 금지 명시 | ✅ |

### 검증 방법

```bash
# 1. SKILL.md 확인
grep "notify" C:\claude\ebs\.claude\skills\daily\SKILL.md
# 예상 결과: "⚠️ CRITICAL: --notify 플래그 사용 금지" 만 출력

# 2. 테스트 실행
/daily --collect-only
# 예상 결과: DM 전송 시도 없이 수집만 완료
```

### 추가 구현 필요 (향후)

- [ ] Step 5: 회신 필요 메일 Draft 자동 생성
- [ ] Step 6: 사용자 검토 요청 (승인/거절)

---

## Execution Order

```
┌────────────────────────────────────────────────────────────────┐
│  순서 1: /daily 스킬 업데이트 ✅ COMPLETED                        │
│  └─ --notify 플래그 제거 완료                                    │
├────────────────────────────────────────────────────────────────┤
│  순서 2: SUN-FLY 회신 Draft 검토 요청                            │
│  └─ 사용자 승인 시 → docs/operations/email-drafts/ 저장          │
│  └─ 사용자가 직접 발송 (자동 발송 없음)                           │
├────────────────────────────────────────────────────────────────┤
│  순서 3: RFID Hardware 업체 문의 메일 검토 요청                   │
│  └─ 사용자 승인 시 → docs/operations/email-drafts/ 저장          │
│  └─ 4개 업체에 순차 발송 (사용자 수동)                           │
├────────────────────────────────────────────────────────────────┤
│  순서 4: 컨택 상태 업데이트 (순서 중요!)                          │
│  └─ Step 4.1: VENDOR-MANAGEMENT.md 상태 변경                    │
│  └─ Step 4.2: Slack List 상태 동기화 (/auto --update slacklist) │
│  └─ Step 4.3: 이 문서 Part 2 테이블은 참조용 (deprecated)        │
└────────────────────────────────────────────────────────────────┘
```

### 상태 업데이트 순서 (CRITICAL)

| 순서 | 대상 | 역할 |
|:----:|------|------|
| 1 | `VENDOR-MANAGEMENT.md` | **Primary Source of Truth** |
| 2 | Slack List | 팀 공유용 (동기화) |
| 3 | 이 문서 Part 2 | 참조용 (deprecated after sync) |

---

## Change History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-04 | 1.1.0 | Critic 피드백 반영: Source of Truth 명시, 저장 위치 추가, 실행 순서 명확화 |
| 2026-02-04 | 1.0.0 | Initial protocol document |

---

**Version**: 1.1.0 | **Updated**: 2026-02-04
