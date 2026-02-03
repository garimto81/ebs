# RFID 하드웨어 참조 가이드

> **BRACELET STUDIO** | EBS Project

**문서 성격**: Phase 0 하드웨어 연동 참조 문서
**대상**: 개발팀 (RFID 하드웨어 연동 시 참조)

---

## 개요

EBS는 두 가지 RFID 모듈을 사용합니다:

| 용도 | 모듈 | Phase | 비고 |
|------|------|:-----:|------|
| **개발/테스트** | MFRC522 | 0-1, 0-2 | 저가, 학습용 |
| **프로덕션** | ST25R3911B | 0-3+ | 고성능, 다중 리더 |

> **참고**: 상세 프로덕션 스펙은 [DESIGN-RFID-Hardware.md](DESIGN-RFID-Hardware.md) 참조

---

## 1. 개발용 하드웨어 (MFRC522)

### 1.1 부품 목록

| 부품 | 수량 | 비고 |
|------|:----:|------|
| ESP32-WROOM-32 DevKit | 1 | ESP32-S2/S3/C3 아님 |
| MFRC522 RFID 모듈 | 1 | 13.56MHz |
| MIFARE Classic 1K 카드 | 5+ | 테스트용 |
| 점퍼 와이어 (F-F) | 7 | - |
| USB 데이터 케이블 | 1 | 충전 전용 불가 |

### 1.2 배선표

| ESP32 | MFRC522 | 기능 |
|-------|---------|------|
| **3.3V** | VCC | 전원 ⚠️ 5V 금지 |
| GND | GND | 접지 |
| GPIO5 | SDA | SPI SS |
| GPIO18 | SCK | SPI Clock |
| GPIO23 | MOSI | SPI Out |
| GPIO19 | MISO | SPI In |
| GPIO4 | RST | Reset |

### 1.3 핵심 코드

```cpp
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN   5
#define RST_PIN  4

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();

  // 버전 확인 (0x91/0x92 = 정상, 0x00/0xFF = 연결 문제)
  byte v = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  Serial.printf("Firmware: 0x%02X\n", v);
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial())
    return;

  // UID 출력
  Serial.print("UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++)
    Serial.printf("%02X%s", mfrc522.uid.uidByte[i],
                  i < mfrc522.uid.size - 1 ? ":" : "\n");

  mfrc522.PICC_HaltA();
  delay(500);
}
```

---

## 2. 소프트웨어 설정

### 2.1 Arduino IDE

1. **ESP32 보드 URL**: `https://dl.espressif.com/dl/package_esp32_index.json`
2. **보드 선택**: ESP32 Dev Module
3. **라이브러리**: MFRC522 by GithubCommunity

### 2.2 USB 드라이버

| 칩 | 드라이버 |
|----|---------|
| CP2102 | Silicon Labs VCP |
| CH340 | WCH CH341SER |

---

## 3. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| Firmware 0x00/0xFF | 배선 오류 | 3.3V 확인, 재연결 |
| COM 포트 없음 | 드라이버/케이블 | 드라이버 설치, 데이터 케이블 |
| 업로드 실패 | BOOT 모드 | BOOT 버튼 누른 채 업로드 |
| 카드 미인식 | VCC 5V 연결 | 모듈 손상, 교체 필요 |

---

## 4. Phase 0 하드웨어 마일스톤

| 단계 | 목표 | 하드웨어 |
|:----:|------|----------|
| 0-1 | 기본 RFID 읽기 | MFRC522 1개 |
| 0-2 | 카드 DB 매핑 | MFRC522 + SQLite |
| 0-3 | 프로덕션 모듈 통합 | ST25R3911B |
| 0-4 | 10-Reader 시스템 | ST25R3911B × 10 |

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [DESIGN-RFID-Hardware.md](DESIGN-RFID-Hardware.md) | 프로덕션 RFID 설계 |
| [PRD-0003-Phase0-PokerGFX-Clone.md](PRD-0003-Phase0-PokerGFX-Clone.md) | Phase 0 전체 계획 |
| [PokerGFX-Feature-Checklist.md](PokerGFX-Feature-Checklist.md) | 기능 체크리스트 |

---

**Version**: 4.0.0 | **Updated**: 2026-02-03

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 3.0.0 | 2026-02-03 | 초보자 상세 가이드 버전 |
| **4.0.0** | **2026-02-03** | **Phase 0 참조 문서로 전면 재구성 (705줄 → 130줄)** |
