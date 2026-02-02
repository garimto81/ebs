# -*- coding: utf-8 -*-
"""
Slack Lists Collector and Updater

Collects vendor status from Slack Lists and updates based on analysis.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Add lib to path
sys.path.insert(0, "C:/claude")

from lib.slack.client import SlackUserClient
from config.settings import SLACK_LIST_ID, DATA_DIR, VENDOR_KEYWORDS


class ListsCollector:
    """Collects and updates Slack Lists vendor data."""

    def __init__(self):
        self.client = SlackUserClient()
        self.data_file = DATA_DIR / "slack_lists.json"
        self.list_id = SLACK_LIST_ID

    def collect(self) -> dict:
        """
        Collect all items from EBS vendor management list.

        Returns:
            Collection result with items and analysis
        """
        print(f"Collecting items from Slack List {self.list_id}...")

        response = self.client.get_list_items(self.list_id, limit=100)
        items = response.get("items", [])

        print(f"Total items: {len(items)}")

        # Parse items
        parsed_items = []
        for item in items:
            parsed = self._parse_item(item)
            if parsed:
                parsed_items.append(parsed)

        result = {
            "total_items": len(parsed_items),
            "items": parsed_items,
            "by_category": self._categorize_items(parsed_items),
            "collected_at": datetime.now().isoformat(),
        }

        # Save to file
        self._save_data(result)

        return result

    def _parse_item(self, item: dict) -> Optional[dict]:
        """Parse a Slack List item into structured data."""
        item_id = item.get("id")
        fields = item.get("fields", [])

        # Extract text from primary column
        text_content = ""
        url = ""

        for field in fields:
            column_id = field.get("column_id", "")

            # Primary text column
            if "Col0" in column_id:
                rich_text = field.get("rich_text", [])
                for block in rich_text:
                    elements = block.get("elements", [])
                    for elem in elements:
                        inner_elems = elem.get("elements", [])
                        for inner in inner_elems:
                            if inner.get("type") == "link":
                                text_content += inner.get("text", "")
                                url = inner.get("url", "")
                            elif inner.get("type") == "text":
                                text_content += inner.get("text", "")

        if not text_content.strip():
            return None

        # Detect vendor from text
        vendor_key = self._detect_vendor_key(text_content)

        return {
            "id": item_id,
            "name": text_content.strip(),
            "url": url,
            "vendor_key": vendor_key,
            "raw_fields": fields,
        }

    def _detect_vendor_key(self, text: str) -> Optional[str]:
        """Detect vendor key from text."""
        text_lower = text.lower()

        for vendor, keywords in VENDOR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return vendor

        return None

    def _categorize_items(self, items: list) -> dict:
        """Categorize items by type."""
        categories = {
            "rfid_readers": [],
            "casino_solutions": [],
            "diy_development": [],
            "benchmarks": [],
            "uncategorized": [],
        }

        rfid_readers = ["feig", "gao", "pongee", "identiv"]
        casino_solutions = ["sit_korea", "sunfly", "matsui", "abbiati"]
        diy_development = ["st_micro", "waveshare", "adafruit", "sparkfun"]
        benchmarks = ["pokergfx", "rfpoker", "fadedspade", "angel"]

        for item in items:
            vendor_key = item.get("vendor_key")

            if vendor_key in rfid_readers:
                categories["rfid_readers"].append(item)
            elif vendor_key in casino_solutions:
                categories["casino_solutions"].append(item)
            elif vendor_key in diy_development:
                categories["diy_development"].append(item)
            elif vendor_key in benchmarks:
                categories["benchmarks"].append(item)
            else:
                categories["uncategorized"].append(item)

        return categories

    def update_item_status(
        self,
        item_id: str,
        status: str,
        notes: str = None,
    ) -> bool:
        """
        Update an item's status in the list.

        Args:
            item_id: Item ID
            status: New status (candidate, rfp_sent, quote_received, etc.)
            notes: Optional notes

        Returns:
            True if successful
        """
        # Note: Slack Lists API for updating items requires specific column IDs
        # This is a placeholder for actual implementation
        print(f"Updating item {item_id} status to {status}...")
        return True

    def add_vendor(
        self,
        name: str,
        url: str,
        info: str,
    ) -> bool:
        """
        Add a new vendor to the list.

        Args:
            name: Vendor name
            url: Vendor website URL
            info: Brief info/description

        Returns:
            True if successful
        """
        try:
            response = self.client._client.api_call(
                "slackLists.items.create",
                json={
                    "list_id": self.list_id,
                    "initial_fields": [{
                        "column_id": "Col0AD62WARNC",  # Primary column
                        "rich_text": [{
                            "type": "rich_text",
                            "elements": [{
                                "type": "rich_text_section",
                                "elements": [
                                    {"type": "link", "url": url, "text": name},
                                    {"type": "text", "text": f" | {info}"}
                                ]
                            }]
                        }]
                    }]
                }
            )
            return response.data.get("ok", False)
        except Exception as e:
            print(f"Error adding vendor: {e}")
            return False

    def sync_from_analysis(
        self,
        slack_data: dict,
        gmail_data: dict,
    ) -> dict:
        """
        Sync list based on collected Slack and Gmail data.

        Args:
            slack_data: Collected Slack message data
            gmail_data: Collected Gmail email data

        Returns:
            Sync result with changes made
        """
        changes = {
            "new_vendors": [],
            "status_updates": [],
            "activity_updates": [],
        }

        # Get current list items
        current_items = self.collect()
        existing_vendors = {
            item["vendor_key"]
            for item in current_items.get("items", [])
            if item.get("vendor_key")
        }

        # Check for new vendors mentioned in communications
        slack_vendors = set(slack_data.get("vendor_mentions", {}).keys())
        gmail_vendors = set(gmail_data.get("vendor_emails", {}).keys())
        all_mentioned = slack_vendors | gmail_vendors

        # New vendors to potentially add
        new_vendors = all_mentioned - existing_vendors
        if new_vendors:
            print(f"Found {len(new_vendors)} new vendors mentioned: {new_vendors}")
            changes["new_vendors"] = list(new_vendors)

        # Check email activity to update status
        for vendor, emails in gmail_data.get("vendor_emails", {}).items():
            if vendor in existing_vendors and emails:
                latest_email = max(emails, key=lambda e: e.get("date", ""))
                changes["activity_updates"].append({
                    "vendor": vendor,
                    "latest_activity": latest_email.get("date"),
                    "email_count": len(emails),
                })

        return changes

    def get_summary(self) -> dict:
        """Get summary of current list status."""
        data = self._load_data()
        if not data:
            return {"error": "No data collected yet"}

        by_category = data.get("by_category", {})

        return {
            "total": data.get("total_items", 0),
            "rfid_readers": len(by_category.get("rfid_readers", [])),
            "casino_solutions": len(by_category.get("casino_solutions", [])),
            "diy_development": len(by_category.get("diy_development", [])),
            "benchmarks": len(by_category.get("benchmarks", [])),
            "uncategorized": len(by_category.get("uncategorized", [])),
            "collected_at": data.get("collected_at"),
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


if __name__ == "__main__":
    collector = ListsCollector()
    result = collector.collect()

    print(f"\nResult:")
    print(f"  Total items: {result.get('total_items', 0)}")

    by_cat = result.get("by_category", {})
    print(f"  RFID Readers: {len(by_cat.get('rfid_readers', []))}")
    print(f"  Casino Solutions: {len(by_cat.get('casino_solutions', []))}")
    print(f"  DIY/Development: {len(by_cat.get('diy_development', []))}")
    print(f"  Benchmarks: {len(by_cat.get('benchmarks', []))}")
    print(f"  Uncategorized: {len(by_cat.get('uncategorized', []))}")
