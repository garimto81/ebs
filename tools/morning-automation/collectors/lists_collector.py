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
from config.settings import SLACK_LIST_ID, SLACK_LIST_COLUMNS, DATA_DIR, VENDOR_KEYWORDS


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
            "A": [],
            "B": [],
            "C": [],
            "uncategorized": [],
        }

        cat_a = {"sunfly", "angel", "emfoplus"}
        cat_c = {"pokergfx", "rfpoker", "abbiati", "matsui", "sit_korea"}

        for item in items:
            vendor_key = item.get("vendor_key")

            if vendor_key in cat_a:
                categories["A"].append(item)
            elif vendor_key in cat_c:
                categories["C"].append(item)
            elif vendor_key:
                categories["B"].append(item)
            else:
                categories["uncategorized"].append(item)

        return categories

    def _build_rich_text_cell(self, column_id: str, row_id: str, text: str) -> dict:
        """Build a rich_text cell payload for Slack Lists API."""
        return {
            "column_id": column_id,
            "row_id": row_id,
            "rich_text": [{
                "type": "rich_text",
                "elements": [{
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": text}
                    ]
                }]
            }]
        }

    def update_item_fields(
        self,
        item_id: str,
        fields: Dict[str, str],
    ) -> bool:
        """
        Update multiple fields of an item in the list.

        Args:
            item_id: Item ID (row_id)
            fields: Dict of field_name -> value.
                     Keys: "status", "category", "contact", "description"

        Returns:
            True if successful
        """
        cells = []
        for field_name, value in fields.items():
            column_id = SLACK_LIST_COLUMNS.get(field_name)
            if not column_id:
                print(f"Unknown field: {field_name}")
                continue
            cells.append(self._build_rich_text_cell(column_id, item_id, value))

        if not cells:
            print("No valid fields to update")
            return False

        try:
            response = self.client._client.api_call(
                "slackLists.items.update",
                json={
                    "list_id": self.list_id,
                    "cells": cells,
                }
            )
            success = response.data.get("ok", False)
            if success:
                print(f"Updated item {item_id}: {list(fields.keys())}")
            else:
                print(f"Failed to update {item_id}: {response.data}")
            return success
        except Exception as e:
            print(f"Error updating item {item_id}: {e}")
            return False

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
            status: New status (후보, 견적요청, 견적수신, 협상중, 계약, 보류, 제외)
            notes: Optional notes

        Returns:
            True if successful
        """
        return self.update_item_fields(item_id, {"status": status})

    def update_item_text(
        self,
        item_id: str,
        name: str,
        url: str,
        info: str,
    ) -> bool:
        """
        Update an item's text content in the list.

        Args:
            item_id: Item ID (e.g., "Rec0AC9422B7X") - this is the row_id
            name: Vendor name (link text)
            url: Vendor website URL
            info: Description text after the link

        Returns:
            True if successful
        """
        try:
            response = self.client._client.api_call(
                "slackLists.items.update",
                json={
                    "list_id": self.list_id,
                    "cells": [{
                        "column_id": "Col0AD62WARNC",  # Primary column
                        "row_id": item_id,  # Row ID is the item_id
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
            success = response.data.get("ok", False)
            if success:
                print(f"Successfully updated item {item_id}")
            else:
                print(f"Failed to update item {item_id}: {response.data}")
            return success
        except Exception as e:
            print(f"Error updating item: {e}")
            return False

    def add_vendor(
        self,
        name: str,
        url: str,
        info: str,
        category: str = "",
        contact: str = "",
        status: str = "후보",
    ) -> Optional[str]:
        """
        Add a new vendor to the list with all fields.

        Args:
            name: Vendor name
            url: Vendor website URL
            info: Brief info/description
            category: Category (e.g., "카테고리 A")
            contact: Contact email or info
            status: Initial status (default: "후보")

        Returns:
            New item ID if successful, None otherwise
        """
        def _text_field(column_id: str, text: str) -> dict:
            return {
                "column_id": column_id,
                "rich_text": [{
                    "type": "rich_text",
                    "elements": [{
                        "type": "rich_text_section",
                        "elements": [{"type": "text", "text": text}]
                    }]
                }]
            }

        def _link_field(column_id: str, url: str, text: str) -> dict:
            return {
                "column_id": column_id,
                "rich_text": [{
                    "type": "rich_text",
                    "elements": [{
                        "type": "rich_text_section",
                        "elements": [{"type": "link", "url": url, "text": text}]
                    }]
                }]
            }

        try:
            fields = [
                _link_field(SLACK_LIST_COLUMNS["name"], url, name),
            ]
            if status:
                fields.append(_text_field(SLACK_LIST_COLUMNS["status"], status))
            if category:
                fields.append(_text_field(SLACK_LIST_COLUMNS["category"], category))
            if contact:
                fields.append(_text_field(SLACK_LIST_COLUMNS["contact"], contact))
            if info:
                fields.append(_text_field(SLACK_LIST_COLUMNS["description"], info))

            response = self.client._client.api_call(
                "slackLists.items.create",
                json={
                    "list_id": self.list_id,
                    "initial_fields": fields,
                }
            )
            if response.data.get("ok"):
                item_id = response.data.get("item", {}).get("id", "")
                print(f"Added vendor '{name}' (ID: {item_id})")
                return item_id
            else:
                print(f"Failed to add vendor '{name}': {response.data}")
                return None
        except Exception as e:
            print(f"Error adding vendor '{name}': {e}")
            return None

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
            "A": len(by_category.get("A", [])),
            "B": len(by_category.get("B", [])),
            "C": len(by_category.get("C", [])),
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
    print(f"  Category A (통합 파트너): {len(by_cat.get('A', []))}")
    print(f"  Category B (부품 공급): {len(by_cat.get('B', []))}")
    print(f"  Category C (벤치마크): {len(by_cat.get('C', []))}")
    print(f"  Uncategorized: {len(by_cat.get('uncategorized', []))}")
