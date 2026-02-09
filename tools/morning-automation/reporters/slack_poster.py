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
    CATEGORY_A_KEYS = {"sunfly", "angel"}

    # Category C vendors (benchmarks/references, no email needed)
    CATEGORY_C_KEYS = {"pokergfx", "abbiati", "sit_korea"}

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
    }

    def _get_email_status(self, vendor_key: str, list_status: str, gmail_data: dict) -> str:
        """Detect email status for a vendor from List status + Gmail data."""
        domain = self.CATEGORY_A_CONTACTS.get(vendor_key, "")

        # Check Gmail for incoming mail from vendor
        received = False
        delivery_failed = False
        if gmail_data and domain:
            # Check received emails
            for email in gmail_data.get("all_emails", gmail_data.get("emails", [])):
                sender = email.get("from", email.get("sender", ""))
                if isinstance(sender, str) and domain in sender:
                    received = True
                    break

            # Check delivery failures
            for failure in gmail_data.get("delivery_failures", []):
                recipient = failure.get("recipient", "")
                if domain in recipient:
                    delivery_failed = True
                    break

        # Determine status from List status + received flag
        sent = list_status in ("견적요청", "견적수신", "협상중", "계약")

        if delivery_failed:
            return ":x: 전송 실패"
        elif received and sent:
            return ":arrows_counterclockwise: 회신 수신"
        elif received:
            return ":incoming_envelope: 수신"
        elif sent:
            return ":outbox_tray: RFI 발송"
        return ""

    # All vendors that should receive RFI (Category A + B with email)
    ALL_RFI_VENDORS = {
        # Category A (통합 파트너 후보)
        "sunfly": {"name": "Sun-Fly", "email": "susie.su@sun-fly.com", "cat": "A"},
        "angel": {"name": "Angel Playing Cards", "email": "overseas@angel-group.co.jp", "cat": "A"},
        # Category B (부품 공급)
        "gao": {"name": "GAO RFID", "email": "sales@gaorfid.com", "cat": "B"},
        "fadedspade": {"name": "Faded Spade", "email": "sales@fadedspade.com", "cat": "B"},
    }

    def _format_vendor_summary(
        self,
        lists_data: dict,
        slack_data: dict = None,
        gmail_data: dict = None,
    ) -> str:
        """Format concise vendor management summary with RFI stats and replies."""
        items = lists_data.get("items", [])

        # Analyze sent/unsent vendors
        sent_vendors = set()
        failed_vendors = set()
        vendor_replies = []

        if gmail_data:
            # Get sent vendor keys
            vendor_sent = gmail_data.get("vendor_sent", {})
            sent_vendors = set(vendor_sent.keys())

            # Get failed vendor keys from delivery failures
            for failure in gmail_data.get("delivery_failures", []):
                recipient = failure.get("recipient", "")
                for vk, info in self.ALL_RFI_VENDORS.items():
                    if info["email"] in recipient or recipient in info["email"]:
                        failed_vendors.add(vk)

            # Get vendor replies (received emails from vendors)
            vendor_emails = gmail_data.get("vendor_emails", {})
            for vendor, emails in vendor_emails.items():
                if emails:
                    latest = max(emails, key=lambda e: e.get("date", ""))
                    snippet = latest.get("snippet", "")
                    summary = self._extract_reply_summary(vendor, snippet)
                    date = latest.get("date", "")[:10] if latest.get("date") else ""
                    vendor_replies.append({
                        "vendor": vendor,
                        "summary": summary,
                        "date": date,
                    })

        # Calculate unsent vendors
        unsent_vendors = []
        for vk, info in self.ALL_RFI_VENDORS.items():
            if vk not in sent_vendors and vk not in failed_vendors:
                unsent_vendors.append({"key": vk, **info})

        # Sort by category (A first)
        unsent_vendors.sort(key=lambda x: (x["cat"], x["name"]))

        lines = [
            "*EBS 업체 관리 - 통합 파트너 선정*",
            "",
            f":clipboard: <https://slack.com/lists/T03QGJ73GBB/F0ADFE95U00|업체 리스트 보기> ({len(items)}개 업체)",
            "",
            "*RFI 현황:*",
            f"• 발송 완료: {len(sent_vendors)}개 업체",
            f"• 전송 실패: {len(failed_vendors)}개 업체",
            f"• 미발송: {len(unsent_vendors)}개 업체",
        ]

        # Unsent vendors (action needed)
        if unsent_vendors:
            lines.append("")
            lines.append("*:warning: 미발송 업체:*")
            for v in unsent_vendors:
                cat_emoji = ":star:" if v["cat"] == "A" else ""
                lines.append(f"• {v['name']} {cat_emoji} ({v['email']})")

        # Failed vendors
        if failed_vendors:
            lines.append("")
            lines.append("*:x: 전송 실패:*")
            for vk in failed_vendors:
                info = self.ALL_RFI_VENDORS.get(vk, {})
                lines.append(f"• {info.get('name', vk)} ({info.get('email', '')})")

        # Vendor replies section
        if vendor_replies:
            lines.append("")
            lines.append("*:incoming_envelope: 회신 수신:*")
            for reply in vendor_replies:
                vendor_name = reply["vendor"].replace("_", " ").title()
                lines.append(f"• {vendor_name}: {reply['summary']} ({reply['date']})")

        lines.append("")
        lines.append(f"_업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")

        return "\n".join(lines)

    def _extract_reply_summary(self, vendor: str, snippet: str) -> str:
        """Extract meaningful summary from email snippet."""
        # Vendor-specific summaries based on known responses
        snippet_lower = snippet.lower()

        if "interested" in snippet_lower and "cooperat" in snippet_lower:
            return "협력 개발 의향 표명"
        elif "enterprise" in snippet_lower and "license" in snippet_lower:
            return "Enterprise 라이선스 필요 안내"
        elif "quote" in snippet_lower or "price" in snippet_lower:
            return "견적 회신"
        elif "thank" in snippet_lower:
            return "문의 접수 확인"
        else:
            # Generic: first 40 chars
            clean = snippet.replace("&#39;", "'").replace("&amp;", "&")
            return clean[:40] + "..." if len(clean) > 40 else clean


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
