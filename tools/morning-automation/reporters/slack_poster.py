# -*- coding: utf-8 -*-
"""
Slack Channel Poster

Updates existing vendor summary message in #ggpnotice channel.
Does NOT post new messages - only updates existing ones.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "C:/claude")
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.slack.client import SlackClient
from config.settings import SLACK_CHANNEL_ID, GFX_LICENSE_EXPIRY, DATA_DIR

# Store the message timestamp for updates
MESSAGE_TS_FILE = DATA_DIR / "vendor_message_ts.txt"

# Known vendor summary message timestamp (from existing post)
DEFAULT_VENDOR_MESSAGE_TS = "1770011678.051859"


class SlackPoster:
    """Updates existing messages in Slack channel."""

    def __init__(self):
        self.client = SlackClient()
        self.channel_id = SLACK_CHANNEL_ID

    def _get_vendor_message_ts(self) -> str:
        """Get the stored vendor message timestamp."""
        if MESSAGE_TS_FILE.exists():
            return MESSAGE_TS_FILE.read_text(encoding="utf-8").strip()
        return DEFAULT_VENDOR_MESSAGE_TS

    def _save_vendor_message_ts(self, ts: str):
        """Save the vendor message timestamp."""
        MESSAGE_TS_FILE.parent.mkdir(parents=True, exist_ok=True)
        MESSAGE_TS_FILE.write_text(ts, encoding="utf-8")

    def update_vendor_summary(
        self,
        lists_data: dict,
        slack_data: dict = None,
        gmail_data: dict = None,
    ) -> dict:
        """
        Update existing vendor management message (NOT post new).

        Uses chat.update API to modify the existing message in place.

        Args:
            lists_data: Collected lists data
            slack_data: Optional Slack data for briefing stats
            gmail_data: Optional Gmail data for briefing stats

        Returns:
            Update result
        """
        # Format the updated message
        message = self._format_vendor_summary(lists_data, slack_data, gmail_data)

        # Get existing message timestamp
        message_ts = self._get_vendor_message_ts()

        try:
            # Use chat.update to modify existing message
            response = self.client._client.chat_update(
                channel=self.channel_id,
                ts=message_ts,
                text=message,
            )

            if response.data.get("ok"):
                # Save the timestamp (in case it changed)
                new_ts = response.data.get("ts", message_ts)
                self._save_vendor_message_ts(new_ts)

                return {
                    "ok": True,
                    "ts": new_ts,
                    "channel": response.data.get("channel"),
                    "action": "updated",
                }
            else:
                return {
                    "ok": False,
                    "error": response.data.get("error", "Unknown error"),
                }
        except Exception as e:
            error_msg = str(e)

            # If message not found, we might need to create new one
            if "message_not_found" in error_msg:
                print(f"Message {message_ts} not found. Creating new message...")
                return self._post_new_vendor_summary(message)

            return {"ok": False, "error": error_msg}

    def _post_new_vendor_summary(self, message: str) -> dict:
        """Post new vendor summary (fallback if update fails)."""
        try:
            result = self.client.send_message(
                channel=self.channel_id,
                text=message,
            )

            # Save new timestamp
            self._save_vendor_message_ts(result.ts)

            return {
                "ok": result.ok,
                "ts": result.ts,
                "channel": result.channel,
                "action": "created_new",
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _format_vendor_summary(
        self,
        lists_data: dict,
        slack_data: dict = None,
        gmail_data: dict = None,
    ) -> str:
        """Format vendor management summary message with optional briefing stats."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        by_category = lists_data.get("by_category", {})

        rfid = by_category.get("rfid_readers", [])
        casino = by_category.get("casino_solutions", [])
        diy = by_category.get("diy_development", [])
        benchmark = by_category.get("benchmarks", [])

        lines = [
            "*EBS 업체 관리 - RFID 리더/모듈 전문 업체*",
            "",
            "포커 카드 RFID 시스템 구축을 위한 전문 업체 리스트입니다.",
            "",
            f"*리스트 바로가기:* <https://slack.com/lists/T03QGJ73GBB/F0ABWAE20K1|EBS 업체 관리>",
            "",
        ]

        # Add briefing stats if available
        if slack_data or gmail_data:
            # GFX license days
            gfx_expiry = datetime.strptime(GFX_LICENSE_EXPIRY, "%Y-%m-%d")
            gfx_days = (gfx_expiry - datetime.now()).days

            lines.append(f"*Daily Status ({date_str})*")

            if gfx_days <= 60:
                lines.append(f":warning: GFX 라이선스: D-{gfx_days}")

            if gmail_data:
                followup_count = len(gmail_data.get("needs_followup", []))
                if followup_count > 0:
                    lines.append(f":email: Follow-up 필요: {followup_count}건")

            if slack_data:
                pending = [
                    m for m in slack_data.get("mentions_to_me", [])
                    if not m.get("completed", False)
                    and "채널에 참여함" not in m.get("text", "")
                ]
                if pending:
                    lines.append(f":memo: 미완료 작업: {len(pending)}건")

            lines.append("")

        lines.append(f"*RFID 리더/모듈 전문 업체 ({len(rfid)}개)*")

        for item in rfid:
            name = item.get("name", "").split("|")[0].strip()
            url = item.get("url", "")
            # Extract info after the name
            full_text = item.get("name", "")
            info = full_text.split("|")[1].strip() if "|" in full_text else ""
            if url and info:
                lines.append(f"• <{url}|{name}> | {info}")
            elif url:
                lines.append(f"• <{url}|{name}>")
            else:
                lines.append(f"• {name}")

        lines.extend([
            "",
            f"*카지노 통합 솔루션 업체 ({len(casino)}개)*",
        ])
        for item in casino:
            name = item.get("name", "").split("|")[0].strip()
            url = item.get("url", "")
            full_text = item.get("name", "")
            info = full_text.split("|")[1].strip() if "|" in full_text else ""
            if url and info:
                lines.append(f"• <{url}|{name}> | {info}")
            elif url:
                lines.append(f"• <{url}|{name}>")
            else:
                lines.append(f"• {name}")

        lines.extend([
            "",
            f"*DIY/개발 친화 업체 ({len(diy)}개)*",
        ])
        for item in diy:
            name = item.get("name", "").split("|")[0].strip()
            url = item.get("url", "")
            full_text = item.get("name", "")
            info = full_text.split("|")[1].strip() if "|" in full_text else ""
            if url and info:
                lines.append(f"• <{url}|{name}> | {info}")
            elif url:
                lines.append(f"• <{url}|{name}>")
            else:
                lines.append(f"• {name}")

        lines.extend([
            "",
            f"*완제품 벤치마크 업체 ({len(benchmark)}개)*",
        ])
        for item in benchmark:
            name = item.get("name", "").split("|")[0].strip()
            url = item.get("url", "")
            full_text = item.get("name", "")
            info = full_text.split("|")[1].strip() if "|" in full_text else ""
            if url and info:
                lines.append(f"• <{url}|{name}> | {info}")
            elif url:
                lines.append(f"• <{url}|{name}>")
            else:
                lines.append(f"• {name}")

        lines.extend([
            "",
            f"_마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        ])

        return "\n".join(lines)


if __name__ == "__main__":
    import io
    import json

    # Fix Windows encoding
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Load collected data
    data_dir = Path(__file__).parent.parent / "data"

    with open(data_dir / "slack_messages.json", encoding="utf-8") as f:
        slack_data = json.load(f)

    with open(data_dir / "gmail_emails.json", encoding="utf-8") as f:
        gmail_data = json.load(f)

    with open(data_dir / "slack_lists.json", encoding="utf-8") as f:
        lists_data = json.load(f)

    poster = SlackPoster()

    # Preview message (with briefing stats)
    print("=== Vendor Summary with Briefing Stats ===")
    print(poster._format_vendor_summary(lists_data, slack_data, gmail_data))
    print()
    print(f"Current message timestamp: {poster._get_vendor_message_ts()}")
