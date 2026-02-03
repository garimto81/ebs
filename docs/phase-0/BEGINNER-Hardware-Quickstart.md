# 하드웨어 연결 초보자 가이드

> **BRACELET STUDIO** | EBS Project

**대상**: 전자공학 경험 없는 개발자, 소프트웨어 엔지니어
**예상 시간**: 2~3시간 (첫 설정 기준)
**난이도**: 초급 (납땜 불필요)

이 가이드는 RFID 카드 리더 하드웨어를 처음 다루는 분을 위한 상세 실습 가이드입니다. 모든 단계를 따라하면 ESP32로 RFID 카드를 읽을 수 있습니다.

---

## 목차

1. [준비물 체크리스트](#1-준비물-체크리스트)
2. [핵심 용어 이해](#2-핵심-용어-이해)
3. [하드웨어 배선](#3-하드웨어-배선)
4. [소프트웨어 설치](#4-소프트웨어-설치)
5. [코드 업로드 및 테스트](#5-코드-업로드-및-테스트)
6. [문제 해결 가이드](#6-문제-해결-가이드)
7. [다음 단계](#7-다음-단계)

---

## 1. 준비물 체크리스트

### 1.1 필수 부품

| 부품 | 수량 | 예상 가격 | 구매처 | 체크 |
|------|:----:|----------:|--------|:----:|
| ESP32-WROOM-32 DevKit | 1개 | $5-10 | AliExpress, Coupang | [ ] |
| MFRC522 RFID 모듈 | 1개 | $2-5 | AliExpress, Coupang | [ ] |
| MIFARE Classic 1K 카드 | 5장 | $2-3 | AliExpress, Coupang | [ ] |
| 점퍼 와이어 (Female-Female) | 7개+ | $1-2 | AliExpress, Coupang | [ ] |
| USB 데이터 케이블 (Micro-B) | 1개 | $2-3 | 다이소, 온라인 | [ ] |

**예상 총 비용**: $15-25 (배송비 제외)

### 1.2 ESP32 구매 시 주의사항

```
✅ 올바른 모델 (호환됨)
─────────────────────────────
• ESP32-WROOM-32 DevKit
• ESP32 DevKit V1
• ESP32-WROOM-32D
• NodeMCU-32S

⚠️ 주의할 모델 (핀 배치 다름)
─────────────────────────────
• ESP32-S2 (USB 네이티브, 다른 핀 배치)
• ESP32-S3 (USB 네이티브, 다른 핀 배치)
• ESP32-C3 (RISC-V 기반, 다른 핀 배치)
• ESP32-C6 (WiFi 6 지원, 다른 핀 배치)
```

**구매 키워드**: "ESP32 DevKit V1" 또는 "ESP32-WROOM-32 개발보드"

### 1.3 USB 케이블 주의사항

```
⚠️ 충전 전용 케이블은 데이터 전송 불가!

데이터 케이블 확인 방법:
1. 케이블 연결 후 PC에서 새 드라이브/장치 인식 확인
2. 장치 관리자(Windows)에서 COM 포트 나타나는지 확인
3. 인식 안 되면 다른 케이블로 교체
```

---

## 2. 핵심 용어 이해

RFID 프로젝트에서 자주 등장하는 용어를 먼저 이해합니다.

### 2.1 하드웨어 용어

| 용어 | 의미 | 비유 |
|------|------|------|
| **ESP32** | 마이크로컨트롤러 보드 | 작은 컴퓨터 본체 |
| **MFRC522** | RFID 리더 모듈 | 교통카드 리더기 |
| **MIFARE** | RFID 카드 규격 | 교통카드 종류 |
| **UID** | 카드 고유 식별번호 | 주민등록번호 |

### 2.2 전기 용어

| 용어 | 의미 | 주의사항 |
|------|------|----------|
| **VCC** | 전원 공급 (+) | MFRC522는 반드시 3.3V! |
| **GND** | 접지 (Ground, -) | 모든 GND는 연결해야 함 |
| **3.3V** | 3.3볼트 전원 | MFRC522 전원 |
| **5V** | 5볼트 전원 | ⚠️ MFRC522에 연결 금지! |
| **GPIO** | 범용 입출력 핀 | ESP32의 다목적 핀 |

### 2.3 통신 용어

| 용어 | 의미 | EBS에서의 역할 |
|------|------|----------------|
| **SPI** | 직렬 주변 장치 인터페이스 | ESP32 ↔ MFRC522 통신 |
| **Serial** | 직렬 통신 | ESP32 ↔ PC 통신 |
| **MOSI** | Master Out Slave In | ESP32 → MFRC522 데이터 |
| **MISO** | Master In Slave Out | MFRC522 → ESP32 데이터 |
| **SCK** | Serial Clock | 통신 타이밍 신호 |
| **SDA/SS** | Slave Select | 장치 선택 신호 |

### 2.4 SPI 통신 이해

```
ESP32 (Master)                MFRC522 (Slave)
     │                              │
     │──────── MOSI ───────────────▶│  데이터 전송 (ESP32 → RFID)
     │◀─────── MISO ────────────────│  데이터 수신 (RFID → ESP32)
     │──────── SCK ────────────────▶│  클럭 신호 (동기화)
     │──────── SS/SDA ─────────────▶│  장치 선택 (LOW=활성)
     │                              │
```

---

## 3. 하드웨어 배선

### 3.1 배선 전 경고

```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️ 중요 경고 - 반드시 읽어주세요!                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. MFRC522의 VCC 핀에 5V 연결 금지!                         ║
║     → 3.3V만 연결 (5V 연결 시 칩 손상)                       ║
║                                                              ║
║  2. 배선 전 ESP32 전원 분리                                  ║
║     → USB 케이블 뽑은 상태에서 작업                          ║
║                                                              ║
║  3. 점퍼 와이어 색상 통일 권장                               ║
║     → 나중에 디버깅할 때 편함                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### 3.2 배선표 (7개 연결)

| # | ESP32 핀 | MFRC522 핀 | 기능 | 권장 색상 | 체크 |
|:-:|----------|------------|------|:---------:|:----:|
| 1 | **3.3V** | VCC | 전원 (+) | 🔴 빨강 | [ ] |
| 2 | **GND** | GND | 접지 (-) | ⚫ 검정 | [ ] |
| 3 | GPIO5 | SDA | SPI Slave Select | 🟡 노랑 | [ ] |
| 4 | GPIO18 | SCK | SPI Clock | 🟢 초록 | [ ] |
| 5 | GPIO23 | MOSI | SPI Master Out | 🔵 파랑 | [ ] |
| 6 | GPIO19 | MISO | SPI Master In | 🟠 주황 | [ ] |
| 7 | GPIO4 | RST | Reset | ⚪ 흰색 | [ ] |

> **IRQ 핀**: 연결하지 않음 (인터럽트 미사용)

### 3.3 배선 다이어그램

```
                    ESP32 DevKit
              ┌───────────────────────┐
              │    [USB 포트]         │
              │                       │
         3.3V │●                     ●│ VIN
          GND │●                     ●│ GND
              │                       │
        GPIO5 │●  ← SDA (노랑) ──────────┐
              │                       │  │
       GPIO18 │●  ← SCK (초록) ──────────┤
              │                       │  │
       GPIO23 │●  ← MOSI (파랑) ─────────┤
              │                       │  │
       GPIO19 │●  ← MISO (주황) ─────────┤
              │                       │  │
        GPIO4 │●  ← RST (흰색) ──────────┤
              │                       │  │
         3.3V │●  ← VCC (빨강) ──────────┤
              │                       │  │
          GND │●  ← GND (검정) ──────────┤
              │                       │  │
              └───────────────────────┘  │
                                         │
                                         ▼
                              ┌──────────────────┐
                              │   MFRC522 모듈   │
                              ├──────────────────┤
                              │ SDA  ← GPIO5     │
                              │ SCK  ← GPIO18    │
                              │ MOSI ← GPIO23    │
                              │ MISO ← GPIO19    │
                              │ IRQ  (미연결)    │
                              │ GND  ← GND       │
                              │ RST  ← GPIO4     │
                              │ VCC  ← 3.3V      │
                              └──────────────────┘
```

### 3.4 배선 단계별 가이드

**Step 1: 전원 연결 (가장 중요)**

```
1. ESP32의 3.3V 핀 찾기
   → 보통 보드 가장자리, "3V3" 또는 "3.3V" 라벨

2. MFRC522의 VCC 핀에 빨간 점퍼 와이어 연결
   → 절대로 5V 핀에 연결하지 말 것!

3. ESP32의 GND 핀을 MFRC522의 GND 핀에 연결
   → 검정 점퍼 와이어 사용
```

**Step 2: SPI 데이터 라인 연결**

```
4. GPIO5 → MFRC522 SDA (노랑)
   → Slave Select 핀

5. GPIO18 → MFRC522 SCK (초록)
   → Clock 핀

6. GPIO23 → MFRC522 MOSI (파랑)
   → 데이터 출력

7. GPIO19 → MFRC522 MISO (주황)
   → 데이터 입력
```

**Step 3: 리셋 핀 연결**

```
8. GPIO4 → MFRC522 RST (흰색)
   → 리셋 제어
```

### 3.5 배선 체크리스트

배선 완료 후 전원 연결 전 확인:

- [ ] VCC가 3.3V에 연결됨 (5V 아님!)
- [ ] GND가 GND에 연결됨
- [ ] 모든 7개 와이어 연결됨
- [ ] 와이어가 단단히 꽂혀 있음
- [ ] 와이어끼리 쇼트 없음 (닿지 않음)

---

## 4. 소프트웨어 설치

### 4.1 Arduino IDE 설치

**Step 1: 다운로드**

```
1. https://www.arduino.cc/en/software 접속
2. "SOFTWARE" 메뉴 클릭
3. "Windows Win 10 and newer, 64 bits" 선택
4. "JUST DOWNLOAD" 클릭 (기부 선택사항)
5. 다운로드된 exe 파일 실행
```

**Step 2: 설치**

```
1. 설치 마법사 "I Agree" 클릭
2. 모든 구성 요소 체크 상태로 "Next"
3. 설치 경로 기본값 유지 "Install"
4. 완료 후 "Close"
```

### 4.2 ESP32 보드 매니저 추가

**Step 1: Preferences 열기**

```
1. Arduino IDE 실행
2. File → Preferences (또는 Ctrl+,)
```

**Step 2: 보드 매니저 URL 추가**

```
1. "Additional boards manager URLs" 필드 찾기
2. 다음 URL 입력 (또는 복사-붙여넣기):

   https://dl.espressif.com/dl/package_esp32_index.json

3. "OK" 클릭
```

**Step 3: ESP32 보드 설치**

```
1. Tools → Board → Boards Manager...
2. 검색창에 "ESP32" 입력
3. "esp32 by Espressif Systems" 찾기
4. "Install" 클릭 (약 200MB, 수 분 소요)
5. 설치 완료 후 창 닫기
```

### 4.3 라이브러리 설치

**필요한 라이브러리:**

| 라이브러리 | 버전 | 용도 |
|------------|------|------|
| MFRC522 | 1.4.10+ | RFID 리더 제어 |
| ArduinoJson | 6.x | JSON 직렬화 (선택) |

**Step 1: MFRC522 설치**

```
1. Sketch → Include Library → Manage Libraries...
2. 검색창에 "MFRC522" 입력
3. "MFRC522 by GithubCommunity" 찾기
4. "Install" 클릭
```

**Step 2: ArduinoJson 설치 (선택)**

```
1. 동일한 Library Manager에서
2. 검색창에 "ArduinoJson" 입력
3. "ArduinoJson by Benoit Blanchon" 찾기
4. "Install" 클릭
```

### 4.4 USB 드라이버 설치

ESP32 DevKit의 USB-Serial 칩에 따라 드라이버가 필요합니다.

**칩 확인 방법:**

```
1. ESP32 보드의 USB 포트 근처 큰 칩 확인
2. 칩에 새겨진 글자 읽기:
   - "CP2102" → Silicon Labs 드라이버
   - "CH340" 또는 "CH341" → WCH 드라이버
```

**드라이버 다운로드:**

| 칩 | 다운로드 URL | 설치 방법 |
|-----|-------------|----------|
| CP2102 | https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers | CP210x Windows Drivers 다운로드 후 설치 |
| CH340 | https://www.wch.cn/download/CH341SER_EXE.html | EXE 실행 후 "INSTALL" 클릭 |

**드라이버 설치 확인:**

```
1. ESP32를 USB로 PC에 연결
2. Windows 키 + X → 장치 관리자
3. "포트 (COM & LPT)" 확장
4. "Silicon Labs CP210x" 또는 "USB-SERIAL CH340" 확인
5. COM 포트 번호 기억 (예: COM3)
```

---

## 5. 코드 업로드 및 테스트

### 5.1 테스트 코드

새 Arduino 스케치를 만들고 다음 코드를 복사합니다.

```cpp
/*
 * EBS RFID Test - MFRC522 카드 읽기 테스트
 *
 * 배선:
 *   ESP32  →  MFRC522
 *   3.3V   →  VCC
 *   GND    →  GND
 *   GPIO5  →  SDA
 *   GPIO18 →  SCK
 *   GPIO23 →  MOSI
 *   GPIO19 →  MISO
 *   GPIO4  →  RST
 */

#include <SPI.h>
#include <MFRC522.h>

// 핀 정의
#define SS_PIN   5    // SDA/SS 핀
#define RST_PIN  4    // RST 핀

// MFRC522 인스턴스 생성
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  // 시리얼 통신 초기화 (115200 baud)
  Serial.begin(115200);
  while (!Serial) {
    ; // 시리얼 포트 대기 (USB 연결 대기)
  }

  // SPI 버스 초기화
  SPI.begin();

  // MFRC522 초기화
  mfrc522.PCD_Init();

  // 초기화 완료 대기
  delay(100);

  // 시작 메시지 출력
  Serial.println();
  Serial.println("========================================");
  Serial.println("   EBS RFID Reader Test v1.0");
  Serial.println("========================================");
  Serial.println();

  // MFRC522 버전 확인
  Serial.print("MFRC522 Firmware Version: ");
  byte version = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  Serial.print("0x");
  Serial.println(version, HEX);

  if (version == 0x91) {
    Serial.println("→ v1.0 감지됨");
  } else if (version == 0x92) {
    Serial.println("→ v2.0 감지됨");
  } else if (version == 0x00 || version == 0xFF) {
    Serial.println("→ 오류: MFRC522 연결 확인 필요!");
    Serial.println("   - 배선을 다시 확인하세요");
    Serial.println("   - VCC가 3.3V에 연결되어 있는지 확인하세요");
  }

  Serial.println();
  Serial.println("카드를 리더기에 가까이 대세요...");
  Serial.println();
}

void loop() {
  // 새 카드 감지 확인
  if (!mfrc522.PICC_IsNewCardPresent()) {
    delay(50);  // CPU 부하 감소
    return;
  }

  // 카드 UID 읽기 시도
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // UID 출력
  Serial.print("카드 감지! UID: ");
  printUID(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();

  // 카드 타입 확인
  MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
  Serial.print("카드 타입: ");
  Serial.println(mfrc522.PICC_GetTypeName(piccType));

  // 구분선
  Serial.println("----------------------------------------");
  Serial.println();

  // 카드 통신 종료
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  // 중복 읽기 방지 딜레이
  delay(500);
}

// UID를 HEX 형식으로 출력하는 함수
void printUID(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    // 1자리 HEX인 경우 앞에 0 추가
    if (buffer[i] < 0x10) {
      Serial.print("0");
    }
    Serial.print(buffer[i], HEX);

    // 마지막이 아니면 콜론 추가
    if (i < bufferSize - 1) {
      Serial.print(":");
    }
  }
}
```

### 5.2 업로드 설정

**Step 1: 보드 선택**

```
1. Tools → Board → ESP32 Arduino → "ESP32 Dev Module" 선택
```

**Step 2: 포트 선택**

```
1. Tools → Port → COM 포트 선택 (예: COM3)
   → 장치 관리자에서 확인한 포트 번호
```

**Step 3: 업로드 설정 확인**

```
Tools 메뉴에서 다음 설정 확인:

Board: "ESP32 Dev Module"
Upload Speed: "921600" (또는 115200)
CPU Frequency: "240MHz (WiFi/BT)"
Flash Frequency: "80MHz"
Flash Mode: "QIO"
Flash Size: "4MB (32Mb)"
Partition Scheme: "Default 4MB with spiffs"
PSRAM: "Disabled"
```

### 5.3 업로드 실행

**Step 1: 컴파일**

```
1. Sketch → Verify/Compile (또는 Ctrl+R)
2. 하단 콘솔에 "Done compiling." 확인
```

**Step 2: 업로드**

```
1. Sketch → Upload (또는 Ctrl+U)
2. "Connecting..." 메시지가 나오면:
   → ESP32의 BOOT 버튼을 누른 상태로 대기
   → "Writing..." 시작되면 BOOT 버튼 놓기

3. "Done uploading." 확인
```

### 5.4 결과 확인

**Step 1: Serial Monitor 열기**

```
1. Tools → Serial Monitor (또는 Ctrl+Shift+M)
2. 우측 하단 보드레이트: "115200 baud" 선택
```

**Step 2: 정상 출력 예시**

```
========================================
   EBS RFID Reader Test v1.0
========================================

MFRC522 Firmware Version: 0x92
→ v2.0 감지됨

카드를 리더기에 가까이 대세요...

카드 감지! UID: 04:A2:B3:C4
카드 타입: MIFARE 1KB
----------------------------------------

카드 감지! UID: 53:2E:7F:01
카드 타입: MIFARE 1KB
----------------------------------------
```

**성공 기준:**

- [ ] "EBS RFID Reader Test" 메시지 출력
- [ ] Firmware Version 0x91 또는 0x92 표시
- [ ] 카드 대면 UID 출력

---

## 6. 문제 해결 가이드

### 6.1 ESP32 인식 문제

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| COM 포트 안 보임 | 드라이버 미설치 | 4.4 USB 드라이버 설치 참조 |
| COM 포트 안 보임 | 충전 전용 케이블 | 데이터 케이블로 교체 |
| COM 포트 안 보임 | USB 포트 불량 | 다른 USB 포트 시도 |
| 장치 인식됐다 끊김 | 전원 불안정 | USB 허브 대신 PC 직접 연결 |

### 6.2 업로드 실패

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| "Connecting..." 멈춤 | BOOT 모드 미진입 | BOOT 버튼 누른 상태로 업로드 |
| "Failed to connect" | 시리얼 충돌 | Serial Monitor 닫고 재시도 |
| "Wrong boot mode" | EN 리셋 필요 | EN 버튼 누르고 다시 시도 |
| Timeout error | Upload Speed 너무 높음 | 115200으로 낮추기 |

**BOOT 버튼 강제 부트 모드 진입:**

```
1. ESP32의 BOOT 버튼을 누르고 있기
2. EN (또는 RST) 버튼을 한번 눌렀다 놓기
3. BOOT 버튼 계속 누른 상태에서 Upload 시작
4. "Writing..." 시작되면 BOOT 버튼 놓기
```

### 6.3 Serial Monitor 문제

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| 아무것도 안 나옴 | 보드레이트 불일치 | 115200으로 변경 |
| 이상한 글자 출력 | 보드레이트 불일치 | 115200으로 변경 |
| 포트 접근 오류 | 다른 프로그램 사용 중 | 다른 시리얼 프로그램 종료 |

### 6.4 MFRC522 인식 문제

| 증상 | 원인 | 해결 방법 |
|------|------|----------|
| Firmware: 0x00 | 연결 안됨 | 모든 배선 재확인 |
| Firmware: 0xFF | 연결 불량 | 점퍼 와이어 다시 꽂기 |
| 카드 인식 안됨 | VCC 전압 문제 | 3.3V 연결 확인 (5V 아님!) |
| 카드 인식 안됨 | MFRC522 손상 | 새 모듈로 교체 |
| 간헐적 인식 | 접촉 불량 | 와이어 연결부 확인 |

**MFRC522 자가 진단:**

```
Firmware Version 의미:
- 0x91: MFRC522 v1.0 (정상)
- 0x92: MFRC522 v2.0 (정상)
- 0x00: 통신 실패 (배선 문제)
- 0xFF: 전원 문제 (3.3V 확인)
- 0x12: 복제품 가능성 (동작은 할 수 있음)
```

### 6.5 자주 묻는 질문

**Q: 5V를 연결했는데 동작하지 않아요**

```
A: MFRC522가 손상되었을 가능성이 높습니다.
   → 새 MFRC522 모듈 구매 권장
   → 다시 할 때는 반드시 3.3V 연결
```

**Q: 여러 장의 카드 UID가 같아요**

```
A: 저가 카드는 UID가 중복될 수 있습니다.
   → 각 카드를 개별 구매처에서 구매
   → 또는 프리미엄 MIFARE 카드 사용
```

**Q: ESP32가 계속 재부팅돼요**

```
A: 전원 공급 문제입니다.
   → USB 허브 대신 PC 직접 연결
   → 다른 USB 케이블 시도
   → 외부 3.3V 전원 공급 고려
```

---

## 7. 다음 단계

이 가이드를 완료하면 다음 단계로 진행할 수 있습니다.

### 7.1 Phase 0 진행 경로

```
현재 완료: 기초 RFID 테스트
    │
    ▼
다음 단계: 카드-UID 매핑
    │
    ├── 54장 카드 UID 등록
    ├── SQLite DB 저장
    └── Python 서버 연동
    │
    ▼
이후 단계: 10-Reader 시스템
    │
    ├── 다중 RFID 리더 연결
    ├── 좌석별 카드 인식
    └── 실시간 WebSocket 전송
```

### 7.2 관련 문서

| 문서 | 내용 | 경로 |
|------|------|------|
| Phase 0 PRD | 전체 기획 | `docs/phase-0/PRD-0003-Phase0-PokerGFX-Clone.md` |
| 기능 체크리스트 | 구현 목록 | `docs/phase-0/PokerGFX-Feature-Checklist.md` |
| 프로덕션 RFID | ST25R3911B 스펙 | Phase 0 완료 후 |

### 7.3 참고 자료

**공식 문서:**

| 자료 | URL |
|------|-----|
| ESP32 Datasheet | https://www.espressif.com/en/products/socs/esp32 |
| MFRC522 Datasheet | https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf |
| Arduino-ESP32 | https://docs.espressif.com/projects/arduino-esp32 |
| MFRC522 라이브러리 | https://github.com/miguelbalboa/rfid |

---

**Version**: 3.0.0 | **Updated**: 2026-02-03
