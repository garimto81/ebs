# Stage 0 이미지 리소스

이 디렉토리는 Stage 0 하드웨어 문서에 사용되는 이미지를 저장합니다.

## 현재 상태

**온라인 참조 사용 중**: 문서에서 외부 URL을 직접 참조합니다.

## 이미지 목록

### 외부 참조 이미지 (현재 사용)

| 파일명 (다운로드 시) | 원본 URL | 출처 |
|---------------------|----------|------|
| `esp32-devkit-v1-pinout.jpg` | https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg | Random Nerd Tutorials |
| `esp32-wroom32-pinout.png` | https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/esp32-pinout-chip-ESP-WROOM-32.png | Random Nerd Tutorials |
| `mfrc522-module-with-tags.jpg` | https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-with-Tag-Card-and-FOB-Key-Tag.jpg | Last Minute Engineers |
| `mfrc522-pinout.png` | https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-Pinout.png | Last Minute Engineers |
| `esp32-mfrc522-wiring.jpg` | https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Board-Circuit.jpg | Random Nerd Tutorials |
| `esp32-mfrc522-setup.jpg` | https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Card-Reader-Keychain.jpg | Random Nerd Tutorials |

### 로컬 이미지

| 파일명 | 설명 | 상태 |
|--------|------|------|
| `beginner-00-system-flow.png` | RFID 시스템 데이터 흐름 다이어그램 | ✅ 완료 |
| `beginner-01-parts-overview.png` | 부품 전체 사진 | 대기 |
| `beginner-02-esp32-pins.png` | ESP32 핀 위치 (라벨) | 대기 |
| `beginner-03-mfrc522-pins.png` | MFRC522 핀 위치 (라벨) | 대기 |
| `beginner-04-wiring-color.png` | ESP32-MFRC522 배선도 (색상별) | ✅ 완료 |
| `beginner-05-success-screen.png` | 성공 화면 스크린샷 | 대기 |

## 이미지 다운로드 방법

### PowerShell 스크립트

```powershell
# 이미지 디렉토리로 이동
cd C:\claude\ebs\docs\images\stage-0

# 이미지 다운로드
$images = @{
    "esp32-devkit-v1-pinout.jpg" = "https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg"
    "esp32-wroom32-pinout.png" = "https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/esp32-pinout-chip-ESP-WROOM-32.png"
    "mfrc522-module-with-tags.jpg" = "https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-with-Tag-Card-and-FOB-Key-Tag.jpg"
    "mfrc522-pinout.png" = "https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-Pinout.png"
    "esp32-mfrc522-wiring.jpg" = "https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Board-Circuit.jpg"
    "esp32-mfrc522-setup.jpg" = "https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Card-Reader-Keychain.jpg"
}

foreach ($file in $images.Keys) {
    Write-Host "Downloading $file..."
    Invoke-WebRequest -Uri $images[$file] -OutFile $file
}

Write-Host "Download complete!"
```

### curl 명령 (Git Bash)

```bash
cd /c/claude/ebs/docs/images/stage-0

curl -O https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/ESP32-DOIT-DEVKIT-V1-Board-Pinout-36-GPIOs-updated.jpg
curl -O https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2018/08/esp32-pinout-chip-ESP-WROOM-32.png
curl -O https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-with-Tag-Card-and-FOB-Key-Tag.jpg
curl -O https://lastminuteengineers.com/wp-content/uploads/arduino/RC522-RFID-Reader-Writer-Module-Pinout.png
curl -O https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Board-Circuit.jpg
curl -O https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2024/11/Reader-Writer-RFID-MFRC522-Module-ESP32-Card-Reader-Keychain.jpg
```

## 로컬 이미지로 전환하기

이미지를 다운로드한 후, 문서의 외부 URL을 로컬 경로로 변경:

```markdown
# 변경 전 (외부 URL)
![ESP32 핀아웃](https://i0.wp.com/randomnerdtutorials.com/...)

# 변경 후 (로컬)
![ESP32 핀아웃](../images/stage-0/esp32-wroom32-pinout.png)
```

## 라이선스 및 저작권

이 이미지들은 교육 목적으로 참조됩니다. 원본 저작권은 각 출처에 있습니다:

- **Random Nerd Tutorials**: https://randomnerdtutorials.com
- **Last Minute Engineers**: https://lastminuteengineers.com

상업적 사용 시 원저작자에게 허가를 받으세요.

---

*Last Updated: 2026-01-30*
