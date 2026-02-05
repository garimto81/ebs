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
from config.settings import SLACK_CHANNEL_ID, DATA_DIR

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

    # Category A vendors (integrated partner candidates: RFID card + reader)
    CATEGORY_A_KEYS = {"sunfly", "angel", "emfoplus"}

    # Category C vendors (benchmarks/references, no email needed)
    CATEGORY_C_KEYS = {"pokergfx", "rfpoker", "abbiati", "matsui", "sit_korea"}

    def _classify_vendor(self, vendor_key: str) -> str:
        """Classify vendor into A/B/C category."""
        if vendor_key in self.CATEGORY_A_KEYS:
            return "A"
        if vendor_key in self.CATEGORY_C_KEYS:
            return "C"
        return "B"

    def _format_vendor_item(self, item: dict) -> str:
        """Format a single vendor item as a Slack line."""
        vendor_key = item.get("vendor_key", "")
        url = item.get("url", "")
        # Extract vendor name from the raw 'name' field (last segment)
        raw_name = item.get("name", "")
        # Try to find fields for cleaner data
        fields = {f.get("key"): f.get("text", "") for f in item.get("raw_fields", [])}
        display_name = fields.get("name", "") or vendor_key.replace("_", " ").title()
        contact = fields.get("contact", "")
        description = fields.get("description", "")

        parts = []
        if url:
            parts.append(f"<{url}|{display_name}>")
        else:
            parts.append(display_name)
        if description:
            parts.append(description)

        return "• " + " | ".join(parts)

    # Email contacts for Category A vendors (for status detection)
    CATEGORY_A_CONTACTS = {
        "sunfly": "sun-fly.com",
        "angel": "angel-group.co.jp",
        "emfoplus": "emfoplus.co.kr",
    }

    def _get_email_status(self, vendor_key: str, list_status: str, gmail_data: dict) -> str:
        """Detect email status for a vendor from List status + Gmail data."""
        domain = self.CATEGORY_A_CONTACTS.get(vendor_key, "")

        # Check Gmail for incoming mail from vendor
        received = False
        if gmail_data and domain:
            for email in gmail_data.get("all_emails", gmail_data.get("emails", [])):
                sender = email.get("from", email.get("sender", ""))
                if isinstance(sender, str) and domain in sender:
                    received = True
                    break

        # Determine status from List status + received flag
        sent = list_status in ("견적요청", "견적수신", "협상중", "계약")

        if received and sent:
            return ":arrows_counterclockwise: 회신 수신"
        elif received:
            return ":incoming_envelope: 수신"
        elif sent:
            return ":outbox_tray: RFI 발송"
        return ""

    def _format_vendor_summary(
        self,
        lists_data: dict,
        slack_data: dict = None,
        gmail_data: dict = None,
    ) -> str:
        """Format concise vendor management summary with List link and email status."""
        items = lists_data.get("items", [])

        # Classify items
        cat_a = []
        counts = {"A": 0, "B": 0, "C": 0}
        for item in items:
            vk = item.get("vendor_key", "")
            cat = self._classify_vendor(vk)
            counts[cat] = counts.get(cat, 0) + 1
            if cat == "A":
                cat_a.append(item)

        lines = [
            "*EBS 업체 관리 - 통합 파트너 선정*",
            "",
            f":clipboard: <https://slack.com/lists/T03QGJ73GBB/F0ADFE95U00|업체 리스트 보기> ({len(items)}개 업체)",
            f"카테고리 A: {counts['A']}개 | B: {counts['B']}개 | C: {counts['C']}개",
        ]

        # Category A email status
        if cat_a:
            lines.append("")
            lines.append("*RFI 현황:*")
            for item in cat_a:
                vk = item.get("vendor_key", "")
                fields = {f.get("key"): f.get("text", "") for f in item.get("raw_fields", [])}
                name = fields.get("name", vk.replace("_", " ").title())
                status = fields.get("status", "후보")
                email_status = self._get_email_status(vk, status, gmail_data)
                lines.append(f"• {name}: {status} {email_status}")

        lines.append("")
        lines.append(f"_업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

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
