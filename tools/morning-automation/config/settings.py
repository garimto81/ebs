# -*- coding: utf-8 -*-
"""
EBS Morning Automation - Configuration
"""

from pathlib import Path

# ===========================================
# Paths
# ===========================================
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = Path("C:/claude/ebs/docs/5-operations/daily-briefings")

# ===========================================
# Slack Configuration
# ===========================================
SLACK_CHANNEL_ID = "C09N8J3UJN9"  # #ggpnotice
SLACK_CHANNEL_NAME = "ggpnotice"
SLACK_LIST_ID = "F0ADFE95U00"  # EBS 업체 관리 (5컬럼)
SLACK_LIST_ID_ARCHIVED = [
    "F0ABWAE20K1",  # v0: 단일컬럼
    "F0ACJPEE52S",  # v1: 4컬럼 (설명 없음)
]

# Multi-Column List Schema (v2)
SLACK_LIST_COLUMNS = {
    "name": "Col0ACQP79Y1J",        # 업체명 (primary)
    "category": "Col0ACEPEKNRZ",    # 카테고리
    "description": "Col0ACM5EBF1Q", # 설명
    "contact": "Col0ACHNF1G93",     # 연락처
    "status": "Col0AC5MSUPPZ",      # 상태
}
SLACK_USER_ID = "U05U07C2EAV"  # Aiden

# ===========================================
# Gmail Configuration
# ===========================================
GMAIL_LABELS = {
    "awaiting": "EBS/Status/⏳-Awaiting-Reply",
    "replied": "EBS/Status/✅-Replied",
    "ebs": "EBS",
}
GMAIL_EBS_LABEL_ID = "Label_4886549615727008050"

# ===========================================
# Analysis Settings
# ===========================================
FOLLOWUP_THRESHOLD_HOURS = 72  # 무응답 Follow-up 알림 기준
GFX_LICENSE_EXPIRY = "2026-03-17"  # PokerGFX 라이선스 만료일

# ===========================================
# Vendor Keywords for Detection
# ===========================================
VENDOR_KEYWORDS = {
    # RFID Readers/Modules
    "feig": ["feig", "feig electronic"],
    "gao": ["gao rfid", "gao-rfid"],
    "pongee": ["pongee", "pongee industries"],
    "identiv": ["identiv", "utrust"],

    # Casino Solutions
    "sit_korea": ["s.i.t", "sit korea", "에스아이티"],
    "sunfly": ["sun-fly", "sunfly", "선플라이"],
    "matsui": ["matsui", "마츠이"],
    "abbiati": ["abbiati", "아비아티"],

    # DIY/Development
    "st_micro": ["st25r3911b", "stm", "st micro", "stmicroelectronics"],
    "waveshare": ["waveshare", "웨이브쉐어"],
    "adafruit": ["adafruit", "pn532"],
    "sparkfun": ["sparkfun"],

    # Integrated Partner Candidates (Category A)
    "emfoplus": ["엠포플러스", "emfoplus", "emfo plus"],

    # Benchmarks
    "pokergfx": ["pokergfx", "poker gfx", "videopokertable"],
    "rfpoker": ["rfpoker", "rf poker"],
    "fadedspade": ["faded spade", "fadedspade", "genesis"],
    "angel": ["angel playing cards", "angel cards"],
}

# ===========================================
# Action Item Detection Patterns
# ===========================================
ACTION_PATTERNS = [
    r"@\w+\s+(.+?)(?:해주세요|해줘|부탁|확인|검토)",
    r"TODO:?\s*(.+)",
    r"\[ \]\s*(.+)",
    r"Action:?\s*(.+)",
]
