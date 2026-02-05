# Work Plan: AliExpress 제품 목록화

**Version**: 1.1.0
**Created**: 2026-01-29
**Revised**: 2026-01-29 (Critic 피드백 반영)
**Target Document**: `C:\claude\ebs\docs\stage-0\DESIGN-RFID-Hardware.md`
**Status**: Ready for Execution

---

## 1. Context

### 1.1 Original Request

EBS Stage 0 하드웨어 문서에서 참조하는 MCU와 RFID 리더 모듈들의 실제 AliExpress 판매 제품 링크를 조사하고 문서에 추가.

### 1.2 Interview Summary

- **범위**: MCU 5종 + RFID 모듈 5종 + 부품류 4종 = 총 14개 카테고리
- **현재 상태**: 검색 URL만 존재 (예: `https://www.aliexpress.com/w/wholesale-esp32-wroom-32.html`)
- **목표**: 검증된 판매자의 실제 제품 페이지 URL로 교체
- **제약**: 일부 항목(Raspberry Pi Pico W, uFR Zero)은 AliExpress에서 미판매

### 1.3 Research Findings

문서 분석 결과:
- **Section 1.3.6 (MCU 구매 링크 모음)**: 라인 221-227 (5개 MCU)
- **Section 1.4.10 (RFID 모듈 구매 링크 모음)**: 라인 571-577 (5개 모듈)
- **Section 9.1 (부품 구매 체크리스트)**: 라인 1137-1163 (체크리스트 형식)

현재 테이블 형식 (Section 1.3.6, 1.4.10):
```markdown
| MCU | AliExpress | Amazon | 국내 |
|-----|------------|--------|------|
| **ESP32-WROOM-32** | [$4-6](검색URL) | ... | ... |
```

현재 체크리스트 형식 (Section 9.1):
```markdown
□ ESP32 DevKit V1 (또는 V2) x1
  └── 가격: ₩15,000-25,000
  └── 구매: Coupang, 디바이스마트
```

---

## 2. Work Objectives

### 2.1 Core Objective

WebSearch 도구를 사용하여 AliExpress에서 검증된 판매자의 실제 제품 URL을 조사하고, 문서의 구매 링크 섹션을 업데이트.

### 2.2 Deliverables

| # | Deliverable | Location |
|---|-------------|----------|
| 1 | MCU 제품 링크 테이블 업데이트 (5개) | Section 1.3.6 (Lines 221-227) |
| 2 | RFID 모듈 제품 링크 테이블 업데이트 (5개) | Section 1.4.10 (Lines 571-577) |
| 3 | 부품류 구매 링크 체크리스트 업데이트 | Section 9.1 (Lines 1137-1163) |
| 4 | 가격 변동 면책 조항 추가 | 각 테이블/섹션 하단 |

### 2.3 Definition of Done

- [ ] AliExpress 판매 제품의 URL이 검색 URL에서 실제 제품 URL로 교체됨
- [ ] URL 형식 검증 완료 (`aliexpress.com/item/[ID].html` 형식)
- [ ] AliExpress 미판매 항목("-" 표시)은 유지하고 대안 구매처 안내
- [ ] 가격은 조사 시점 기준 표기 + 변동 가능 면책 조항 포함
- [ ] 부품류(카드, 점퍼 와이어, 브레드보드, 케이블) 링크 추가됨

---

## 3. Guardrails

### 3.1 Must Have

- WebSearch 결과에서 AliExpress 공식 도메인(`aliexpress.com`) 링크만 사용
- URL 형식 검증: `https://www.aliexpress.com/item/[숫자ID].html` 또는 `https://www.aliexpress.us/item/[숫자ID].html`
- 가격 변동 면책 조항 포함
- AliExpress 미판매 제품은 "-" 유지 + 대안 구매처 명시

### 3.2 Must NOT Have

- 검색 URL 형식(`/w/wholesale-*.html`) 그대로 유지
- AliExpress 외 도메인 (가짜 사이트 주의)
- 광고성 또는 스폰서 링크
- 가격을 확정적으로 표기 (변동 가능 명시 필수)

### 3.3 Fallback Procedures

| 상황 | 대응 |
|------|------|
| WebSearch에서 제품 URL 미발견 | 기존 검색 URL 유지 + 주석 추가 |
| AliExpress 미판매 (Pico W, uFR Zero) | "-" 유지, Amazon/공식몰 링크 안내 |
| URL 형식이 표준과 다름 | Clean URL로 변환 (spm 파라미터 제거) |

---

## 4. Task Flow

```
[Research Phase]
    |
    v
+-------------------+     +-------------------+     +-------------------+
| Task 1: MCU       | --> | Task 2: RFID      | --> | Task 3: Parts     |
| 제품 조사         |     | 모듈 조사         |     | 조사              |
+-------------------+     +-------------------+     +-------------------+
    |                         |                         |
    v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| Task 4: Section   | --> | Task 5: Section   | --> | Task 6: Section 9 |
| 1.3.6 업데이트    |     | 1.4.10 업데이트   |     | 업데이트          |
+-------------------+     +-------------------+     +-------------------+
    |
    v
[Documentation Update Phase]
    |
    v
+-------------------+
| Task 7: 면책      |
| 조항 추가         |
+-------------------+
    |
    v
[Verification Phase]
    |
    v
+-------------------+
| Task 8: URL       |
| 검증 및 최종 확인 |
+-------------------+
```

---

## 5. Detailed TODOs

### Task 1: MCU 제품 조사 (WebSearch 사용)

**Method:**
WebSearch 도구로 각 MCU의 AliExpress 제품 페이지 검색

**Search Queries:**
```
"ESP32-WROOM-32 DevKit site:aliexpress.com"
"ESP32-C3 DevKit site:aliexpress.com"
"ESP32-S3 DevKit site:aliexpress.com"
"STM32 Blue Pill F103C8T6 site:aliexpress.com"
```

**Acceptance Criteria:**
- 5개 MCU 중 AliExpress 판매 제품(4개)의 실제 URL 확보
- URL 형식 검증 (`/item/[숫자].html`)
- Raspberry Pi Pico W는 "-" 유지 (AliExpress 미판매)

**Target Products (문서 Section 1.3.6 기준):**
| # | MCU | AliExpress 상태 | Priority |
|---|-----|-----------------|----------|
| 1 | ESP32-WROOM-32 | 검색 URL → 실제 URL | HIGH |
| 2 | ESP32-C3 | 검색 URL → 실제 URL | MEDIUM |
| 3 | ESP32-S3 | 검색 URL → 실제 URL | MEDIUM |
| 4 | Raspberry Pi Pico W | "-" 유지 (미판매) | SKIP |
| 5 | STM32 Blue Pill | 검색 URL → 실제 URL | LOW |

**File Reference:** `DESIGN-RFID-Hardware.md` Section 1.3.6 (Lines 221-227)

---

### Task 2: RFID 모듈 제품 조사 (WebSearch 사용)

**Method:**
WebSearch 도구로 각 RFID 모듈의 AliExpress 제품 페이지 검색

**Search Queries:**
```
"MFRC522 RC522 RFID module site:aliexpress.com"
"PN5180 RFID NFC module site:aliexpress.com"
"PN532 NFC module site:aliexpress.com"
"ST25R3911B NFC reader site:aliexpress.com"
```

**Acceptance Criteria:**
- 5개 RFID 모듈 중 AliExpress 판매 제품(4개)의 실제 URL 확보
- URL 형식 검증 (`/item/[숫자].html`)
- uFR Zero는 "-" 유지 (AliExpress 미판매, D-Logic 직구만)

**Target Products (문서 Section 1.4.10 기준):**
| # | Module | AliExpress 상태 | Priority |
|---|--------|-----------------|----------|
| 1 | MFRC522 | 검색 URL → 실제 URL | HIGH |
| 2 | PN5180 | 실제 URL 존재 (검증 필요) | MEDIUM |
| 3 | PN532 | 가격만 표시 → 실제 URL | MEDIUM |
| 4 | ST25R3911B | "-" → 검색 또는 유지 | LOW |
| 5 | uFR Zero | "-" 유지 (미판매) | SKIP |

**File Reference:** `DESIGN-RFID-Hardware.md` Section 1.4.10 (Lines 571-577)

---

### Task 3: 부품류 제품 조사 (WebSearch 사용)

**Method:**
WebSearch 도구로 각 부품의 AliExpress 제품 페이지 검색

**Search Queries:**
```
"MIFARE Classic 1K card NFC site:aliexpress.com"
"jumper wire female 20cm dupont site:aliexpress.com"
"breadboard 400 830 pin site:aliexpress.com"
"USB micro cable data site:aliexpress.com"
```

**Acceptance Criteria:**
- 4개 부품 카테고리별 최소 1개 AliExpress URL 확보
- URL 형식 검증

**Target Products:**
| # | Part | Priority |
|---|------|----------|
| 1 | MIFARE Classic 1K 카드/태그 | HIGH |
| 2 | 점퍼 와이어 (F-F, 20cm) | MEDIUM |
| 3 | 브레드보드 (400 또는 830핀) | MEDIUM |
| 4 | USB-C/Micro 케이블 | LOW |

**File Reference:** `DESIGN-RFID-Hardware.md` Section 9.1 (Lines 1137-1163)

---

### Task 4: Section 1.3.6 업데이트

**Acceptance Criteria:**
- 기존 검색 URL을 실제 제품 URL로 교체
- 판매자 정보 컬럼 추가 (선택적)
- 가격 조사 시점 명시

**Before:**
```markdown
| **ESP32-WROOM-32** | [$4-6](https://www.aliexpress.com/w/wholesale-esp32-wroom-32.html) | ... |
```

**After:**
```markdown
| **ESP32-WROOM-32** | [$4-6](https://www.aliexpress.com/item/실제제품ID.html) | ... |
```

**File Reference:** `DESIGN-RFID-Hardware.md` Lines 219-228

---

### Task 5: Section 1.4.10 업데이트

**Acceptance Criteria:**
- 기존 검색 URL을 실제 제품 URL로 교체
- 판매자 정보 추가 (선택적)

**File Reference:** `DESIGN-RFID-Hardware.md` Lines 569-577

---

### Task 6: Section 9.1 부품 체크리스트에 AliExpress 링크 추가

**Current Format (체크리스트):**
```markdown
□ ESP32 DevKit V1 (또는 V2) x1
  └── 가격: ₩15,000-25,000
  └── 구매: Coupang, 디바이스마트
```

**Target Format (AliExpress 추가):**
```markdown
□ ESP32 DevKit V1 (또는 V2) x1
  └── 가격: ₩15,000-25,000 / $4-6 (AliExpress)
  └── 국내: Coupang, 디바이스마트
  └── AliExpress: [제품 링크](https://www.aliexpress.com/item/...)
```

**Acceptance Criteria:**
- 체크리스트 형식 유지
- AliExpress 링크를 새 줄로 추가
- 국내/AliExpress 구분 명확

**File Reference:** `DESIGN-RFID-Hardware.md` Section 9.1 (Lines 1137-1163)

---

### Task 7: 면책 조항 추가

**Acceptance Criteria:**
- 각 구매 링크 테이블 하단에 면책 조항 추가

**Template:**
```markdown
> **주의**: 가격은 2026-01-29 기준이며 변동될 수 있습니다.
> 링크가 유효하지 않은 경우 제품명으로 검색하세요.
> 판매자 평점과 리뷰를 반드시 확인 후 구매하세요.
```

---

### Task 8: URL 형식 검증 및 최종 확인

**Acceptance Criteria:**
- URL 형식 검증 (HTTP 요청 불가, 형식만 확인):
  - Valid: `https://www.aliexpress.com/item/1005001234567890.html`
  - Valid: `https://www.aliexpress.us/item/3256801234567890.html`
  - Invalid: `https://www.aliexpress.com/w/wholesale-*.html` (검색 URL)
- 문서 형식 일관성 확인
- 버전 번호 업데이트 (v2.2.0 → v2.3.0)

**Validation Regex:**
```
^https://(www\.)?aliexpress\.(com|us)/item/\d+\.html$
```

**Note:** HTTP 200 검증은 불가능하므로 URL 형식 검증으로 대체

---

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AliExpress 제품 URL 변경 | 링크 깨짐 | 제품명 검색 가이드 병기 |
| 판매자 폐점 | 링크 무효 | 다중 대안 판매자 기록 |
| 가격 변동 | 정보 outdated | 면책 조항 + 조사 시점 명시 |
| 배송비 미포함 | 실제 비용 오해 | 배송비 별도 안내 |

---

## 7. Commit Strategy

| Commit # | Scope | Message |
|----------|-------|---------|
| 1 | Research | `docs(ebs): MCU/RFID AliExpress 제품 조사 완료` |
| 2 | Update | `docs(ebs): 구매 링크 섹션 실제 제품 URL로 업데이트` |
| 3 | Final | `docs(ebs): 가격 면책 조항 및 문서 버전 업데이트` |

---

## 8. Success Criteria

- [ ] AliExpress 판매 제품(MCU 4개 + RFID 4개 + 부품 4개 = 12개)의 실제 URL 확보
- [ ] AliExpress 미판매 제품(Raspberry Pi Pico W, uFR Zero)은 "-" 유지 + 대안 안내
- [ ] 모든 URL이 표준 형식 준수 (`/item/[숫자].html`)
- [ ] 가격 변동 면책 조항 포함
- [ ] Section 9.1 체크리스트에 AliExpress 링크 추가됨
- [ ] 문서 버전 v2.3.0으로 업데이트

---

## 9. Implementation Notes

### 9.1 Research Method (WebSearch Tool)

**도구**: Claude Code의 WebSearch 도구 사용 (웹 브라우징 불가)

**검색 프로세스:**
1. WebSearch 도구로 `"[제품명] site:aliexpress.com"` 쿼리 실행
2. 검색 결과에서 제품 페이지 URL 추출
3. URL 형식 검증 (`/item/[숫자].html`)
4. Clean URL로 변환 (tracking 파라미터 제거)

**예시:**
```
Query: "ESP32-WROOM-32 DevKit site:aliexpress.com"
Result: https://www.aliexpress.com/item/1005001234567890.html?spm=...
Clean:  https://www.aliexpress.com/item/1005001234567890.html
```

### 9.2 URL Format

AliExpress 제품 URL 형식:
- Standard: `https://www.aliexpress.com/item/[ITEM_ID].html`
- US domain: `https://www.aliexpress.us/item/[ITEM_ID].html`
- Clean URL 사용 (spm, aff_fcid 등 파라미터 제거)

**URL Cleanup:**
```
Input:  https://www.aliexpress.com/item/123.html?spm=a2g0o&aff_fcid=abc
Output: https://www.aliexpress.com/item/123.html
```

### 9.3 Documentation Update

문서 수정 시:
1. 기존 테이블 구조 유지 (Section 1.3.6, 1.4.10)
2. AliExpress 컬럼만 URL 교체
3. Amazon/국내 링크는 변경 없음
4. "-" 표시된 항목은 그대로 유지

### 9.4 Section 9.1 체크리스트 업데이트

기존 체크리스트 형식에 AliExpress 라인 추가:
```markdown
□ [부품명] x[수량]
  └── 가격: [국내가격] / [AliExpress가격]
  └── 국내: [국내 구매처]
  └── AliExpress: [링크](URL)  ← 신규 추가
```

### 9.5 AliExpress 미판매 제품 처리

| 제품 | 현재 상태 | 대응 |
|------|----------|------|
| Raspberry Pi Pico W | "-" | 유지, Amazon 링크 안내 |
| uFR Zero | "-" | 유지, D-Logic 공식몰 안내 |
| ST25R3911B | "-" | WebSearch 시도, 미발견 시 유지 |

---

**PLAN_READY**
