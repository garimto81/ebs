# -*- coding: utf-8 -*-
"""
Gmail Email Collector

Collects and analyzes emails from EBS-Project label.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List

# Add lib to path
sys.path.insert(0, "C:/claude")

from lib.gmail.client import GmailClient
from config.settings import (
    GMAIL_LABELS,
    GMAIL_EBS_LABEL_ID,
    DATA_DIR,
    FOLLOWUP_THRESHOLD_HOURS,
    VENDOR_KEYWORDS,
)


class GmailCollector:
    """Collects and analyzes Gmail emails."""

    def __init__(self):
        self.client = GmailClient()
        self.data_file = DATA_DIR / "gmail_emails.json"
        self.last_date_file = DATA_DIR / "gmail_last_date.txt"

    def collect_all(self, max_results: int = 100) -> dict:
        """
        Collect all emails from EBS-Project label (initial collection).

        Args:
            max_results: Maximum emails to fetch

        Returns:
            Collection result with emails and analysis
        """
        print("Collecting all emails from EBS label...")

        # Use configured label ID
        ebs_label_id = GMAIL_EBS_LABEL_ID

        # Collect emails
        query = "label:EBS"
        emails = self.client.list_emails(query=query, max_results=max_results)

        print(f"Total collected: {len(emails)} emails")

        # Analyze emails
        result = self._analyze_emails(emails)

        # Save to file
        self._save_data(result)

        # Update last date
        if emails:
            latest_date = max(
                (e.date for e in emails if e.date),
                default=datetime.now()
            )
            self._save_last_date(latest_date)

        return result

    def collect_incremental(self) -> dict:
        """
        Collect new emails since last collection.

        Returns:
            Collection result with new emails only
        """
        last_date = self._load_last_date()

        if not last_date:
            print("No previous collection found. Running full collection...")
            return self.collect_all()

        # Format date for Gmail query
        date_str = last_date.strftime("%Y/%m/%d")
        query = f"label:EBS after:{date_str}"

        print(f"Collecting emails since {date_str}...")

        emails = self.client.list_emails(query=query, max_results=50)
        print(f"New emails: {len(emails)}")

        if not emails:
            return {
                "new_emails": 0,
                "awaiting_reply": [],
                "needs_followup": [],
                "vendor_emails": {},
                "collected_at": datetime.now().isoformat(),
            }

        result = self._analyze_emails(emails)
        result["new_emails"] = len(emails)

        # Merge with existing data
        self._merge_data(result)

        # Update last date
        latest_date = max(
            (e.date for e in emails if e.date),
            default=datetime.now()
        )
        self._save_last_date(latest_date)

        return result

    def _analyze_emails(self, emails: list) -> dict:
        """Analyze emails for status and vendor classification."""
        email_data = []
        awaiting_reply = []
        needs_followup = []
        vendor_emails = {vendor: [] for vendor in VENDOR_KEYWORDS.keys()}

        now = datetime.now()
        followup_threshold = timedelta(hours=FOLLOWUP_THRESHOLD_HOURS)

        for email in emails:
            # Detect vendor from sender/subject
            detected_vendor = self._detect_vendor(email)

            email_info = {
                "id": email.id,
                "thread_id": email.thread_id,
                "subject": email.subject,
                "sender": email.sender,
                "date": email.date.isoformat() if email.date else None,
                "is_unread": email.is_unread,
                "labels": email.labels,
                "snippet": email.snippet,
                "vendor": detected_vendor,
            }
            email_data.append(email_info)

            # Check if awaiting reply
            if "SENT" not in email.labels and email.is_unread:
                awaiting_reply.append(email_info)

            # Check if needs follow-up (sent by me, no reply for X hours)
            if "SENT" in email.labels:
                if email.date and (now - email.date) > followup_threshold:
                    # Check if there's a reply in the thread
                    thread = self.client.get_thread(email.thread_id)
                    has_reply = any(
                        msg.sender != email.sender
                        for msg in thread.messages
                        if msg.date and msg.date > email.date
                    )

                    if not has_reply:
                        days_elapsed = (now - email.date).days
                        needs_followup.append({
                            **email_info,
                            "days_elapsed": days_elapsed,
                        })

            # Categorize by vendor
            if detected_vendor:
                vendor_emails[detected_vendor].append(email_info)

        # Filter empty vendor categories
        vendor_emails = {k: v for k, v in vendor_emails.items() if v}

        return {
            "total_emails": len(emails),
            "emails": email_data,
            "awaiting_reply": awaiting_reply,
            "needs_followup": needs_followup,
            "vendor_emails": vendor_emails,
            "collected_at": datetime.now().isoformat(),
        }

    def _detect_vendor(self, email) -> Optional[str]:
        """Detect vendor from email sender or subject."""
        text_to_search = f"{email.sender} {email.subject}".lower()

        for vendor, keywords in VENDOR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_to_search:
                    return vendor

        return None

    def get_pending_emails(self) -> dict:
        """Get emails that need attention."""
        data = self._load_data()
        if not data:
            return {"awaiting_reply": [], "needs_followup": []}

        return {
            "awaiting_reply": data.get("awaiting_reply", []),
            "needs_followup": data.get("needs_followup", []),
        }

    def get_vendor_email_summary(self) -> dict:
        """Get summary of emails by vendor."""
        data = self._load_data()
        if not data:
            return {}

        return {
            vendor: len(emails)
            for vendor, emails in data.get("vendor_emails", {}).items()
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
            "total_emails": 0,
            "emails": [],
            "awaiting_reply": [],
            "needs_followup": [],
            "vendor_emails": {},
        }

        # Get existing email IDs
        existing_ids = {e["id"] for e in existing.get("emails", [])}

        # Add only new emails
        for email in new_data.get("emails", []):
            if email["id"] not in existing_ids:
                existing["emails"].append(email)
                existing["total_emails"] += 1

        # Update awaiting/followup (replace with fresh data)
        existing["awaiting_reply"] = new_data.get("awaiting_reply", [])
        existing["needs_followup"] = new_data.get("needs_followup", [])

        # Merge vendor emails
        for vendor, emails in new_data.get("vendor_emails", {}).items():
            if vendor not in existing["vendor_emails"]:
                existing["vendor_emails"][vendor] = []

            existing_vendor_ids = {e["id"] for e in existing["vendor_emails"][vendor]}
            for email in emails:
                if email["id"] not in existing_vendor_ids:
                    existing["vendor_emails"][vendor].append(email)

        existing["last_updated"] = datetime.now().isoformat()

        self._save_data(existing)

    def _save_last_date(self, date: datetime):
        """Save last processed date."""
        self.last_date_file.parent.mkdir(parents=True, exist_ok=True)
        self.last_date_file.write_text(date.isoformat(), encoding="utf-8")

    def _load_last_date(self) -> Optional[datetime]:
        """Load last processed date."""
        if not self.last_date_file.exists():
            return None
        try:
            return datetime.fromisoformat(
                self.last_date_file.read_text(encoding="utf-8").strip()
            )
        except ValueError:
            return None


if __name__ == "__main__":
    import sys
    collector = GmailCollector()

    if len(sys.argv) > 1 and sys.argv[1] == "--incremental":
        result = collector.collect_incremental()
    else:
        result = collector.collect_all()

    print(f"\nResult:")
    print(f"  Total emails: {result.get('total_emails', 0)}")
    print(f"  Awaiting reply: {len(result.get('awaiting_reply', []))}")
    print(f"  Needs follow-up: {len(result.get('needs_followup', []))}")
    print(f"  Vendor emails: {len(result.get('vendor_emails', {}))}")
