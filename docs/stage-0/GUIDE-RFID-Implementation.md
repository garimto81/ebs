# EBS - Stage 0 RFID 연결 검증 구현 가이드

**Version**: 2.1.0
**작성일**: 2026-01-22
**수정일**: 2026-01-29
**관련 문서**:
- [PRD-0003-Stage0-RFID-Connection.md](PRD-0003-Stage0-RFID-Connection.md) - Stage 0 PRD
- [DESIGN-RFID-Hardware.md](DESIGN-RFID-Hardware.md) - 하드웨어 설계

---

## 1. Stage 0 개요

### 1.1 목표

> **"하드웨어 연결 가능성 검증"** - MVP가 아닌 기술 탐색 단계

| 목표 | 설명 |
|------|------|
| 하드웨어 학습 | ESP32 + MFRC522 기초 습득 |
| 연결 검증 | RFID → 서버 → 화면 파이프라인 증명 |
| 리스크 조기 발견 | 기술적 장벽 사전 파악 |

### 1.2 Stage 0 범위 (Scope)

**포함 (In Scope):**
- 단일 RFID 리더 연결 (ESP32 + MFRC522 1개)
- 카드 UID 읽기 (기본 MIFARE 카드)
- Serial 통신 (ESP32 → PC USB)
- 기본 Python 서버 (Serial 수신)
- 단순 UI (카드 UID 화면 표시)

**제외 (Out of Scope):**
- 카드-포커정보 매핑 (Stage 1)
- 다중 리더 (Stage 1+)
- 프로덕션 UI (Stage 1)
- 보안 기능 (Stage 1)
- OBS 연동 (Stage 1)

### 1.3 일정 개요 (20주, 5개월)

| Phase | 기간 | 목표 |
|-------|------|------|
| Phase 0-1 | 2주 | 환경 설정 |
| Phase 0-2 | 4주 | RFID 읽기 |
| Phase 0-3 | 4주 | Serial 통신 |
| Phase 0-4 | 6주 | UI 연동 |
| Phase 0-5 | 4주 | 안정화 |

---

## 2. Phase 0-1: 환경 설정 (2주)

### 2.1 필요 부품

| 부품 | 수량 | 예상 비용 |
|------|------|----------|
| ESP32-WROOM-32 DevKit | 1 | $5 |
| MFRC522 모듈 | 1 | $2 |
| MIFARE Classic 1K 카드 | 5 | $2.50 |
| 점퍼 와이어 (F-F) | 10 | $1 |
| USB-C 케이블 | 1 | $2 |

**총 비용**: 약 $15-20

### 2.2 소프트웨어 설치

```
□ Arduino IDE 2.0+ 설치
  - ESP32 보드 매니저 추가
  - URL: https://dl.espressif.com/dl/package_esp32_index.json

□ MFRC522 라이브러리 설치
  - Library Manager → "MFRC522" 검색

□ ArduinoJson 라이브러리 설치
  - Library Manager → "ArduinoJson" 검색

□ USB 드라이버 설치
  - CP2102 또는 CH340 (보드에 따라)

□ Python 3.11+ 설치
□ VS Code 설치 (선택)
```

### 2.3 완료 기준

- [ ] ESP32가 Arduino IDE에서 인식됨
- [ ] Blink 예제 업로드 성공
- [ ] Serial Monitor에서 출력 확인

---

## 3. Phase 0-2: RFID 읽기 (4주)

### 3.1 배선 연결

```
ESP32          MFRC522
─────          ───────
3.3V    ────── VCC      (빨강)
GND     ────── GND      (검정)
GPIO5   ────── SDA (SS) (노랑)
GPIO18  ────── SCK      (초록)
GPIO23  ────── MOSI     (파랑)
GPIO19  ────── MISO     (주황)
GPIO4   ────── RST      (흰색)
        (IRQ 미사용)
```

**⚠️ 주의: VCC는 반드시 3.3V! 5V 연결 시 모듈 손상**

### 3.1.1 바이패스 커패시터 연결 (권장)

전원 안정화를 위해 100nF (0.1µF) 세라믹 커패시터를 추가합니다.

```
MFRC522 VCC ●────┬────● ESP32 3.3V
                 │
               ═══ 100nF (0.1µF)
                 │
MFRC522 GND ●────┴────● ESP32 GND
```

**설치 팁:**
- 커패시터는 MFRC522 모듈 VCC-GND 핀 가까이 배치
- 극성 없음 (세라믹 커패시터)
- 효과: 고주파 노이즈 제거, 카드 인식 안정성 향상

> 💡 **선택 사항**: 커패시터 없이도 동작하지만, 간헐적 인식 실패 시 추가 권장

### 3.2 테스트 펌웨어

```cpp
// firmware/rfid_reader/rfid_reader.ino

#include <SPI.h>
#include <MFRC522.h>
#include <ArduinoJson.h>

#define SS_PIN  5
#define RST_PIN 4

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();

  // 초기화 완료 메시지 (JSON)
  StaticJsonDocument<128> doc;
  doc["type"] = "init";
  doc["status"] = "ready";
  doc["reader_id"] = 0;
  serializeJson(doc, Serial);
  Serial.println();
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) {
    delay(50);
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // UID를 문자열로 변환
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (i > 0) uid += ":";
    if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();

  // JSON 출력
  StaticJsonDocument<128> doc;
  doc["type"] = "card_read";
  doc["uid"] = uid;
  doc["reader_id"] = 0;
  doc["timestamp"] = millis();

  serializeJson(doc, Serial);
  Serial.println();

  mfrc522.PICC_HaltA();
  delay(500);
}
```

### 3.3 테스트 방법

1. 코드를 Arduino IDE에 붙여넣기
2. Tools → Board → ESP32 Dev Module
3. Tools → Port → (해당 COM 포트)
4. Upload 버튼 클릭
5. Serial Monitor 열기 (115200 baud)
6. RFID 카드를 리더에 가져다 대기

**예상 출력:**
```json
{"type":"init","status":"ready","reader_id":0}
{"type":"card_read","uid":"04:A2:B3:C4","reader_id":0,"timestamp":1234}
```

### 3.4 완료 기준

- [ ] 5장 MIFARE 카드 모두 인식
- [ ] UID가 Serial Monitor에 JSON으로 출력
- [ ] 1시간 연속 운영 안정

---

## 4. Phase 0-3: Serial 통신 (4주)

### 4.1 Python Serial 수신

```python
# server/stage0/serial_reader.py

import serial
import json
from datetime import datetime

def read_serial(port: str = "COM3", baud: int = 115200):
    """ESP32로부터 Serial 데이터 수신"""

    ser = serial.Serial(port, baud, timeout=1)
    print(f"Connected to {port}")

    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        data = json.loads(line)
                        handle_event(data)
                    except json.JSONDecodeError as e:
                        print(f"JSON Error: {e}")
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        ser.close()

def handle_event(data: dict):
    """이벤트 처리"""
    event_type = data.get("type")

    if event_type == "init":
        print(f"Reader initialized: {data.get('status')}")

    elif event_type == "card_read":
        uid = data.get("uid")
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Card: {uid}")

    else:
        print(f"Unknown event: {data}")

if __name__ == "__main__":
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "COM3"
    read_serial(port)
```

### 4.2 테스트 실행

```bash
# 가상환경 생성 (최초 1회)
python -m venv venv
.\venv\Scripts\activate  # Windows

# 패키지 설치
pip install pyserial

# 실행 (Arduino Serial Monitor는 닫아야 함!)
python server/stage0/serial_reader.py COM3
```

### 4.3 에러 핸들링 추가

```python
# server/stage0/serial_reader_robust.py

import serial
import serial.tools.list_ports
import json
import time
from datetime import datetime

class SerialReader:
    def __init__(self, port: str = None, baud: int = 115200):
        self.port = port
        self.baud = baud
        self.ser = None
        self.reconnect_delay = 2  # seconds

    def find_esp32_port(self) -> str:
        """ESP32 포트 자동 탐지"""
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if "CP210" in p.description or "CH340" in p.description:
                return p.device
        return None

    def connect(self):
        """연결 (재시도 포함)"""
        while True:
            try:
                port = self.port or self.find_esp32_port()
                if not port:
                    print("ESP32 not found. Retrying...")
                    time.sleep(self.reconnect_delay)
                    continue

                self.ser = serial.Serial(port, self.baud, timeout=1)
                print(f"Connected to {port}")
                return
            except serial.SerialException as e:
                print(f"Connection failed: {e}. Retrying...")
                time.sleep(self.reconnect_delay)

    def read_loop(self):
        """메인 읽기 루프"""
        self.connect()

        while True:
            try:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        self.handle_line(line)
            except serial.SerialException:
                print("Connection lost. Reconnecting...")
                self.connect()
            except KeyboardInterrupt:
                break

        if self.ser:
            self.ser.close()

    def handle_line(self, line: str):
        """라인 처리"""
        try:
            data = json.loads(line)
            event_type = data.get("type")

            if event_type == "card_read":
                uid = data.get("uid")
                ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                print(f"[{ts}] Card UID: {uid}")
            else:
                print(f"Event: {data}")

        except json.JSONDecodeError:
            print(f"Raw: {line}")

if __name__ == "__main__":
    reader = SerialReader()
    reader.read_loop()
```

### 4.4 완료 기준

- [ ] Python에서 Serial 데이터 수신
- [ ] JSON 파싱 성공
- [ ] 연결 끊김 시 자동 재연결

---

## 5. Phase 0-4: UI 연동 (6주)

### 5.1 WebSocket 서버 (FastAPI)

```python
# server/stage0/main.py

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import serial
import json
import asyncio
from typing import List

app = FastAPI(title="EBS Stage 0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket 클라이언트 목록
clients: List[WebSocket] = []

# 최근 카드 정보
last_card = {"uid": None, "timestamp": None}

@app.get("/api/status")
async def status():
    return {"status": "running", "last_card": last_card}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지 대기 (keep-alive)
            await websocket.receive_text()
    except:
        clients.remove(websocket)

async def broadcast(message: dict):
    """모든 WebSocket 클라이언트에 브로드캐스트"""
    for client in clients.copy():
        try:
            await client.send_json(message)
        except:
            clients.remove(client)

async def serial_reader(port: str = "COM3"):
    """Serial 읽기 (비동기)"""
    import serial.tools.list_ports

    # 포트 자동 탐지
    if port == "auto":
        for p in serial.tools.list_ports.comports():
            if "CP210" in p.description or "CH340" in p.description:
                port = p.device
                break

    ser = serial.Serial(port, 115200, timeout=0.1)
    print(f"Serial connected: {port}")

    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    data = json.loads(line)
                    if data.get("type") == "card_read":
                        last_card["uid"] = data.get("uid")
                        last_card["timestamp"] = data.get("timestamp")
                        await broadcast({
                            "type": "card_detected",
                            "uid": data.get("uid")
                        })
                except json.JSONDecodeError:
                    pass
        await asyncio.sleep(0.01)

@app.on_event("startup")
async def startup():
    asyncio.create_task(serial_reader("COM3"))  # 포트 수정 필요

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5.2 React 프론트엔드

```tsx
// frontend/stage0/src/App.tsx

import { useState, useEffect, useRef } from 'react';

function App() {
  const [connected, setConnected] = useState(false);
  const [lastCard, setLastCard] = useState<string | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // WebSocket 연결
    const connect = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws');

      ws.current.onopen = () => {
        setConnected(true);
        console.log('WebSocket connected');
      };

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'card_detected') {
          setLastCard(data.uid);
          setHistory(prev => [data.uid, ...prev.slice(0, 9)]);
        }
      };

      ws.current.onclose = () => {
        setConnected(false);
        setTimeout(connect, 2000);  // 재연결
      };
    };

    connect();

    return () => {
      ws.current?.close();
    };
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>EBS Stage 0 - RFID Test</h1>

      <div style={{ marginBottom: '20px' }}>
        Status: {connected ? '🟢 Connected' : '🔴 Disconnected'}
      </div>

      <div style={{
        fontSize: '48px',
        padding: '40px',
        border: '2px solid black',
        textAlign: 'center',
        marginBottom: '20px'
      }}>
        {lastCard || 'Waiting for card...'}
      </div>

      <h2>History</h2>
      <ul>
        {history.map((uid, i) => (
          <li key={i}>{uid}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

### 5.3 실행 방법

```bash
# 서버 실행
cd server/stage0
pip install fastapi uvicorn pyserial websockets
uvicorn main:app --reload --port 8000

# 프론트엔드 실행 (별도 터미널)
cd frontend/stage0
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

### 5.4 완료 기준

- [ ] WebSocket으로 실시간 브로드캐스트
- [ ] React에서 카드 UID 표시
- [ ] E2E 지연 < 1초

---

## 6. Phase 0-5: 안정화 (4주)

### 6.1 테스트 항목

| 테스트 | 방법 | 기준 |
|--------|------|------|
| 연속 운영 | 4시간 무중단 | 에러 0회 |
| 인식률 | 100회 연속 스캔 | 100% 성공 |
| 지연 시간 | 타임스탬프 측정 | < 1초 |
| 재연결 | USB 분리/연결 | 자동 복구 |

### 6.2 에러 로깅

```python
# server/stage0/logger.py

import logging
from datetime import datetime

logging.basicConfig(
    filename=f'logs/stage0_{datetime.now():%Y%m%d}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('stage0')
```

### 6.3 완료 기준 (Stage 0 Gate)

| 조건 | 기준 | 검증 방법 |
|------|------|----------|
| RFID 읽기 | 5장 카드 100% 인식 | 테스트 로그 |
| E2E 지연 | 카드→화면 < 1초 | 타임스탬프 |
| 연속 운영 | 4시간 무중단 | 모니터링 |
| 팀 자신감 | "Stage 1 진행 가능" 합의 | 팀 회의록 |

**Gate 통과 시**: Stage 1 착수 (2026년 하반기)

---

## 7. 트러블슈팅

### 7.1 하드웨어 문제

| 증상 | 원인 | 해결 |
|------|------|------|
| ESP32 인식 안됨 | 드라이버 미설치 | CP2102/CH340 설치 |
| 업로드 실패 | 잘못된 포트 | Tools → Port 확인 |
| RFID 초기화 실패 | SPI 배선 오류 | 핀 연결 재확인 |
| 카드 인식 안됨 | 전원 부족 | 3.3V 확인 |
| 간헐적 인식 | 접촉 불량 | 점퍼 교체 |

### 7.2 소프트웨어 문제

| 증상 | 원인 | 해결 |
|------|------|------|
| Serial 연결 실패 | 포트 사용 중 | Arduino Monitor 닫기 |
| JSON 파싱 오류 | 불완전 데이터 | 버퍼 비우기 |
| WebSocket 끊김 | 서버 오류 | 로그 확인 |

---

## 8. 참고 자료

| 리소스 | URL |
|--------|-----|
| ESP32 공식 문서 | espressif.com |
| MFRC522 라이브러리 | github.com/miguelbalboa/rfid |
| FastAPI 문서 | fastapi.tiangolo.com |
| Random Nerd Tutorials | randomnerdtutorials.com |

---

## 9. 문서 정보

| 항목 | 내용 |
|------|------|
| **문서 버전** | 2.1.0 |
| **작성일** | 2026-01-22 |
| **수정일** | 2026-01-29 |
| **상태** | Active |
| **변경 사항** | 바이패스 커패시터 연결 가이드 추가 (Section 3.1.1) |

---

**문서 끝**
