# -*- coding: utf-8 -*-
"""
Gmail Email Collector

Collects and analyzes emails from EBS-Project label.
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
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
    VENDOR_EMAIL_DOMAINS,
)


class GmailCollector:
    """Collects and analyzes Gmail emails."""

    def __init__(self):
        self.client = GmailClient()
        self.data_file = DATA_DIR / "gmail_emails.json"
        self.last_date_file = DATA_DIR / "gmail_last_date.txt"

    def _build_vendor_domain_query(self, date_filter: str = "") -> str:
        """Build Gmail query from VENDOR_EMAIL_DOMAINS."""
        all_domains = []
        for domains in VENDOR_EMAIL_DOMAINS.values():
            all_domains.extend(domains)
        from_parts = " OR ".join(f"from:{d}" for d in all_domains)
        return f"{date_filter} ({from_parts})".strip()

    def _collect_vendor_replies(self, existing_ids: set, emails: list, date_filter: str = ""):
        """Collect vendor replies via domain search and thread tracking."""
        # Path 1: Vendor domain search
        domain_query = self._build_vendor_domain_query(date_filter)
        vendor_inbox = self.client.list_emails(query=domain_query, max_results=50)
        added = 0
        for email in vendor_inbox:
            if email.id not in existing_ids:
                emails.append(email)
                existing_ids.add(email.id)
                added += 1
        print(f"  Vendor domain search: +{added} emails")

        # Path 2: Thread-based reply detection
        sent_thread_ids = {e.thread_id for e in emails if "SENT" in e.labels}
        thread_added = 0
        for tid in sent_thread_ids:
            try:
                thread = self.client.get_thread(tid)
                for msg in thread.messages:
                    if msg.id not in existing_ids:
                        emails.append(msg)
                        existing_ids.add(msg.id)
                        thread_added += 1
            except Exception:
                pass
        print(f"  Thread reply detection: +{thread_added} emails")

    def _auto_label_ebs(self, emails: list):
        """Auto-add EBS label to emails that don't have it."""
        ebs_label_id = GMAIL_EBS_LABEL_ID
        labeled = 0
        for email in emails:
            if ebs_label_id not in email.labels:
                try:
                    self.client.modify_labels(email.id, add_labels=[ebs_label_id])
                    labeled += 1
                except Exception:
                    pass
        if labeled > 0:
            print(f"  Auto-labeled {labeled} emails with EBS label")

    def collect_all(self, max_results: int = 100) -> dict:
        """
        Collect all emails from EBS-Project label (initial collection).

        Args:
            max_results: Maximum emails to fetch

        Returns:
            Collection result with emails and analysis
        """
        print("Collecting all emails from EBS label...")

        # Path 0: EBS label emails
        query = "label:EBS"
        emails = self.client.list_emails(query=query, max_results=max_results)
        existing_ids = {e.id for e in emails}
        print(f"  EBS labeled: {len(emails)} emails")

        # Path 1: Sent emails with EBS keywords (English + Korean)
        sent_query = "in:sent (RFID OR poker OR card recognition OR playing cards OR 포커 OR 카드 인식)"
        sent_emails = self.client.list_emails(query=sent_query, max_results=50)
        sent_added = 0
        for sent in sent_emails:
            if sent.id not in existing_ids:
                emails.append(sent)
                existing_ids.add(sent.id)
                sent_added += 1
        print(f"  Sent keyword search: +{sent_added} emails")

        # Path 2+3: Vendor domain + Thread replies
        self._collect_vendor_replies(existing_ids, emails)

        # Auto-label unlabeled emails
        self._auto_label_ebs(emails)

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
        date_filter = f"after:{date_str}"

        print(f"Collecting emails since {date_str}...")

        # Path 0: EBS label emails
        query = f"label:EBS {date_filter}"
        emails = self.client.list_emails(query=query, max_results=50)
        existing_ids = {e.id for e in emails}
        print(f"  EBS labeled: {len(emails)} emails")

        # Path 1: Sent emails with EBS keywords (English + Korean)
        sent_query = f"in:sent {date_filter} (RFID OR poker OR card recognition OR playing cards OR 포커 OR 카드 인식)"
        sent_emails = self.client.list_emails(query=sent_query, max_results=50)
        sent_added = 0
        for sent in sent_emails:
            if sent.id not in existing_ids:
                emails.append(sent)
                existing_ids.add(sent.id)
                sent_added += 1
        print(f"  Sent keyword search: +{sent_added} emails")

        # Path 2+3: Vendor domain + Thread replies
        self._collect_vendor_replies(existing_ids, emails, date_filter)

        # Auto-label unlabeled emails
        self._auto_label_ebs(emails)

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
        sent_emails = []  # Track sent emails
        delivery_failures = []  # Track delivery failures
        vendor_emails = {vendor: [] for vendor in VENDOR_KEYWORDS.keys()}
        vendor_sent = {}  # Track sent emails by vendor/recipient

        now = datetime.now(timezone.utc)
        followup_threshold = timedelta(hours=FOLLOWUP_THRESHOLD_HOURS)

        for email in emails:
            # Detect vendor from sender/subject
            detected_vendor = self._detect_vendor(email)

            # Check for delivery failure
            is_delivery_failure = (
                "mailer-daemon" in email.sender.lower() or
                "delivery" in email.subject.lower() and "failure" in email.subject.lower()
            )

            # Extract recipients for sent emails
            recipients = email.to if hasattr(email, 'to') else []
            recipient_vendor = None

            # Detect vendor from recipient email domain
            if "SENT" in email.labels and recipients:
                recipient_vendor = self._detect_vendor_from_recipients(recipients)

            email_info = {
                "id": email.id,
                "thread_id": email.thread_id,
                "subject": email.subject,
                "sender": email.sender,
                "recipients": recipients,  # Add recipients list
                "date": email.date.isoformat() if email.date else None,
                "is_unread": email.is_unread,
                "labels": email.labels,
                "snippet": email.snippet,
                "vendor": detected_vendor,
                "recipient_vendor": recipient_vendor,  # Add recipient vendor
                "is_sent": "SENT" in email.labels,
                "is_delivery_failure": is_delivery_failure,
            }
            email_data.append(email_info)

            # Track delivery failures
            if is_delivery_failure:
                # Extract failed recipient from snippet
                recipient = self._extract_failed_recipient(email.snippet)
                delivery_failures.append({
                    **email_info,
                    "recipient": recipient,
                })
                continue

            # Check if awaiting reply (received email from vendor)
            if "SENT" not in email.labels and detected_vendor:
                awaiting_reply.append(email_info)

            # Track sent emails
            if "SENT" in email.labels:
                sent_emails.append(email_info)

                # Use recipient_vendor detected from email domain
                if recipient_vendor:
                    if recipient_vendor not in vendor_sent:
                        vendor_sent[recipient_vendor] = []
                    vendor_sent[recipient_vendor].append(email_info)

                # Check if needs follow-up (no reply for X hours)
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
                            "recipient_vendor": recipient_vendor,
                        })

            # Categorize received emails by vendor
            if detected_vendor and "SENT" not in email.labels:
                vendor_emails[detected_vendor].append(email_info)

        # Filter empty vendor categories
        vendor_emails = {k: v for k, v in vendor_emails.items() if v}
        vendor_sent = {k: v for k, v in vendor_sent.items() if v}

        return {
            "total_emails": len(emails),
            "emails": email_data,
            "awaiting_reply": awaiting_reply,
            "needs_followup": needs_followup,
            "sent_emails": sent_emails,
            "delivery_failures": delivery_failures,
            "vendor_emails": vendor_emails,  # Received emails by vendor
            "vendor_sent": vendor_sent,  # Sent emails by vendor
            "collected_at": datetime.now().isoformat(),
        }

    def _extract_failed_recipient(self, snippet: str) -> str:
        """Extract failed recipient email from delivery failure snippet."""
        import re
        # Match email pattern
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
        return match.group(0) if match else "Unknown"

    def _detect_vendor_from_text(self, text: str) -> Optional[str]:
        """Detect vendor from arbitrary text (subject, snippet)."""
        text_lower = text.lower()
        for vendor, keywords in VENDOR_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return vendor
        return None

    def _detect_vendor_from_recipients(self, recipients: List[str]) -> Optional[str]:
        """Detect vendor from recipient email addresses."""
        for recipient in recipients:
            # Extract email address from "Name <email>" format
            email_match = re.search(r'<([^>]+)>', recipient)
            email = email_match.group(1) if email_match else recipient

            # Extract domain
            if '@' in email:
                domain = email.split('@')[1].lower()

                # Check against vendor email domains
                for vendor, domains in VENDOR_EMAIL_DOMAINS.items():
                    if domain in domains:
                        return vendor

        return None

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
            "sent_emails": [],
            "delivery_failures": [],
            "vendor_emails": {},
            "vendor_sent": {},
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

        # Replace sent_emails and delivery_failures with fresh data
        existing["sent_emails"] = new_data.get("sent_emails", [])
        existing["delivery_failures"] = new_data.get("delivery_failures", [])

        # Merge vendor emails (received)
        if "vendor_emails" not in existing:
            existing["vendor_emails"] = {}
        for vendor, emails in new_data.get("vendor_emails", {}).items():
            if vendor not in existing["vendor_emails"]:
                existing["vendor_emails"][vendor] = []

            existing_vendor_ids = {e["id"] for e in existing["vendor_emails"][vendor]}
            for email in emails:
                if email["id"] not in existing_vendor_ids:
                    existing["vendor_emails"][vendor].append(email)

        # Merge vendor_sent
        if "vendor_sent" not in existing:
            existing["vendor_sent"] = {}
        for vendor, emails in new_data.get("vendor_sent", {}).items():
            if vendor not in existing["vendor_sent"]:
                existing["vendor_sent"][vendor] = []

            existing_sent_ids = {e["id"] for e in existing["vendor_sent"][vendor]}
            for email in emails:
                if email["id"] not in existing_sent_ids:
                    existing["vendor_sent"][vendor].append(email)

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
