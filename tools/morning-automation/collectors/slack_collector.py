# -*- coding: utf-8 -*-
"""
Slack Message Collector

Collects and analyzes messages from #ggpnotice channel.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Add lib to path
sys.path.insert(0, "C:/claude")

from lib.slack.client import SlackClient, SlackUserClient
from config.settings import (
    SLACK_CHANNEL_ID,
    SLACK_USER_ID,
    DATA_DIR,
    ACTION_PATTERNS,
    VENDOR_KEYWORDS,
)


class SlackCollector:
    """Collects and analyzes Slack messages."""

    def __init__(self):
        # Use bot token for message history (has channels:history scope)
        self.client = SlackClient()
        # Use user token for Lists API
        self.user_client = SlackUserClient()
        self.data_file = DATA_DIR / "slack_messages.json"
        self.last_ts_file = DATA_DIR / "slack_last_ts.txt"

    def collect_all(self, limit: int = 1000) -> dict:
        """
        Collect all messages from channel (initial collection).

        Args:
            limit: Maximum messages to fetch

        Returns:
            Collection result with messages and analysis
        """
        print(f"Collecting all messages from #{SLACK_CHANNEL_ID}...")

        messages = []
        cursor = None
        total_fetched = 0

        while total_fetched < limit:
            batch_limit = min(200, limit - total_fetched)

            response = self.client._client.conversations_history(
                channel=SLACK_CHANNEL_ID,
                limit=batch_limit,
                cursor=cursor,
            )

            batch = response.data.get("messages", [])
            if not batch:
                break

            messages.extend(batch)
            total_fetched += len(batch)

            # Check for pagination
            cursor = response.data.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break

            print(f"  Fetched {total_fetched} messages...")

        print(f"Total collected: {len(messages)} messages")

        # Analyze messages
        result = self._analyze_messages(messages)

        # Save to file
        self._save_data(result)

        # Update last timestamp
        if messages:
            latest_ts = max(msg["ts"] for msg in messages)
            self._save_last_ts(latest_ts)

        return result

    def collect_incremental(self) -> dict:
        """
        Collect new messages since last collection.

        Returns:
            Collection result with new messages only
        """
        last_ts = self._load_last_ts()

        if not last_ts:
            print("No previous collection found. Running full collection...")
            return self.collect_all()

        print(f"Collecting messages since {last_ts}...")

        response = self.client._client.conversations_history(
            channel=SLACK_CHANNEL_ID,
            oldest=last_ts,
            limit=200,
        )

        messages = response.data.get("messages", [])
        print(f"New messages: {len(messages)}")

        if not messages:
            return {
                "new_messages": 0,
                "action_items": [],
                "vendor_mentions": {},
                "collected_at": datetime.now().isoformat(),
            }

        result = self._analyze_messages(messages)
        result["new_messages"] = len(messages)

        # Merge with existing data
        self._merge_data(result)

        # Update last timestamp
        latest_ts = max(msg["ts"] for msg in messages)
        self._save_last_ts(latest_ts)

        return result

    def _analyze_messages(self, messages: list) -> dict:
        """Analyze messages for action items and vendor mentions."""
        action_items = []
        vendor_mentions = {vendor: [] for vendor in VENDOR_KEYWORDS.keys()}
        mentions_to_me = []

        for msg in messages:
            text = msg.get("text", "").lower()
            ts = msg.get("ts", "")
            user = msg.get("user", "")
            timestamp = datetime.fromtimestamp(float(ts)) if ts else None

            # Check if I'm mentioned
            if SLACK_USER_ID in text or f"<@{SLACK_USER_ID}>" in msg.get("text", ""):
                # Check if completed (has checkmark reaction)
                reactions = msg.get("reactions", [])
                completed = any(
                    r["name"] in ["white_check_mark", "heavy_check_mark", "ballot_box_with_check"]
                    for r in reactions
                )

                mentions_to_me.append({
                    "ts": ts,
                    "text": msg.get("text", ""),
                    "user": user,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "completed": completed,
                    "link": f"slack://channel?team=T05SZ8VE39U&id={SLACK_CHANNEL_ID}&message={ts}",
                })

            # Detect action items
            for pattern in ACTION_PATTERNS:
                matches = re.findall(pattern, msg.get("text", ""), re.IGNORECASE)
                for match in matches:
                    action_items.append({
                        "ts": ts,
                        "action": match.strip(),
                        "user": user,
                        "timestamp": timestamp.isoformat() if timestamp else None,
                    })

            # Detect vendor mentions
            for vendor, keywords in VENDOR_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in text:
                        vendor_mentions[vendor].append({
                            "ts": ts,
                            "context": msg.get("text", "")[:200],
                            "timestamp": timestamp.isoformat() if timestamp else None,
                        })
                        break

        # Filter empty vendor mentions
        vendor_mentions = {k: v for k, v in vendor_mentions.items() if v}

        return {
            "total_messages": len(messages),
            "action_items": action_items,
            "mentions_to_me": mentions_to_me,
            "vendor_mentions": vendor_mentions,
            "collected_at": datetime.now().isoformat(),
        }

    def get_pending_action_items(self) -> list:
        """Get uncompleted action items assigned to me."""
        data = self._load_data()
        if not data:
            return []

        pending = [
            item for item in data.get("mentions_to_me", [])
            if not item.get("completed", False)
        ]

        return pending

    def get_vendor_activity_summary(self) -> dict:
        """Get summary of vendor mentions."""
        data = self._load_data()
        if not data:
            return {}

        return {
            vendor: len(mentions)
            for vendor, mentions in data.get("vendor_mentions", {}).items()
        }

    def _save_data(self, data: dict):
        """Save collected data to JSON file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _load_data(self) -> Optional[dict]:
        """Load existing data from JSON file."""
        if not self.data_file.exists():
            return None
        return json.loads(self.data_file.read_text(encoding="utf-8"))

    def _merge_data(self, new_data: dict):
        """Merge new data with existing data."""
        existing = self._load_data() or {
            "total_messages": 0,
            "action_items": [],
            "mentions_to_me": [],
            "vendor_mentions": {},
        }

        # Merge
        existing["total_messages"] += new_data.get("total_messages", 0)
        existing["action_items"].extend(new_data.get("action_items", []))
        existing["mentions_to_me"].extend(new_data.get("mentions_to_me", []))

        for vendor, mentions in new_data.get("vendor_mentions", {}).items():
            if vendor not in existing["vendor_mentions"]:
                existing["vendor_mentions"][vendor] = []
            existing["vendor_mentions"][vendor].extend(mentions)

        existing["last_updated"] = datetime.now().isoformat()

        self._save_data(existing)

    def _save_last_ts(self, ts: str):
        """Save last processed timestamp."""
        self.last_ts_file.parent.mkdir(parents=True, exist_ok=True)
        self.last_ts_file.write_text(ts, encoding="utf-8")

    def _load_last_ts(self) -> Optional[str]:
        """Load last processed timestamp."""
        if not self.last_ts_file.exists():
            return None
        return self.last_ts_file.read_text(encoding="utf-8").strip()


if __name__ == "__main__":
    import sys
    collector = SlackCollector()

    if len(sys.argv) > 1 and sys.argv[1] == "--incremental":
        result = collector.collect_incremental()
    else:
        result = collector.collect_all()

    print(f"\nResult:")
    print(f"  Total messages: {result.get('total_messages', 0)}")
    print(f"  Action items: {len(result.get('action_items', []))}")
    print(f"  Mentions to me: {len(result.get('mentions_to_me', []))}")
    print(f"  Vendor mentions: {len(result.get('vendor_mentions', {}))}")
