# -*- coding: utf-8 -*-
"""
EBS Morning Automation - Main Entry Point

Usage:
    # Full collection (initial)
    python main.py --full

    # Incremental collection (daily)
    python main.py

    # With Slack DM notification
    python main.py --notify

    # Specific date report
    python main.py --date 2026-02-01
"""

import argparse
import sys
import io
from datetime import datetime
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "C:/claude")

from collectors import SlackCollector, GmailCollector, ListsCollector
from reporters import MarkdownReporter, SlackNotifier, SlackPoster
from config.settings import DATA_DIR


def print_banner():
    """Print startup banner."""
    print("=" * 50)
    print("  EBS Morning Automation v1.0.0")
    print("=" * 50)
    print()


def run_full_collection():
    """Run full initial collection."""
    print("📊 Running FULL collection (initial)...")
    print()

    results = {}

    # 1. Slack Messages
    print("1️⃣ Collecting Slack messages...")
    slack_collector = SlackCollector()
    results["slack"] = slack_collector.collect_all()
    print(f"   ✅ {results['slack'].get('total_messages', 0)} messages collected")
    print()

    # 2. Gmail Emails
    print("2️⃣ Collecting Gmail emails...")
    try:
        gmail_collector = GmailCollector()
        results["gmail"] = gmail_collector.collect_all()
        print(f"   ✅ {results['gmail'].get('total_emails', 0)} emails collected")
    except Exception as e:
        print(f"   ⚠️ Gmail collection failed: {e}")
        results["gmail"] = {
            "total_emails": 0,
            "awaiting_reply": [],
            "needs_followup": [],
            "vendor_emails": {},
        }
    print()

    # 3. Slack Lists
    print("3️⃣ Collecting Slack Lists...")
    lists_collector = ListsCollector()
    results["lists"] = lists_collector.collect()
    print(f"   ✅ {results['lists'].get('total_items', 0)} items collected")
    print()

    return results


def run_incremental_collection():
    """Run incremental daily collection."""
    print("📊 Running INCREMENTAL collection (daily)...")
    print()

    results = {}

    # 1. Slack Messages
    print("1️⃣ Collecting new Slack messages...")
    slack_collector = SlackCollector()
    results["slack"] = slack_collector.collect_incremental()
    new_msgs = results["slack"].get("new_messages", results["slack"].get("total_messages", 0))
    print(f"   ✅ {new_msgs} new messages")
    print()

    # 2. Gmail Emails
    print("2️⃣ Collecting new Gmail emails...")
    try:
        gmail_collector = GmailCollector()
        results["gmail"] = gmail_collector.collect_incremental()
        new_emails = results["gmail"].get("new_emails", results["gmail"].get("total_emails", 0))
        print(f"   ✅ {new_emails} new emails")
    except Exception as e:
        print(f"   ⚠️ Gmail collection failed: {e}")
        results["gmail"] = {
            "total_emails": 0,
            "awaiting_reply": [],
            "needs_followup": [],
            "vendor_emails": {},
        }
    print()

    # 3. Slack Lists
    print("3️⃣ Collecting Slack Lists...")
    lists_collector = ListsCollector()
    results["lists"] = lists_collector.collect()
    print(f"   ✅ {results['lists'].get('total_items', 0)} items")
    print()

    return results


def generate_report(results: dict, date: datetime = None) -> str:
    """Generate markdown report."""
    print("4️⃣ Generating report...")

    reporter = MarkdownReporter()
    report_path = reporter.generate(
        results["slack"],
        results["gmail"],
        results["lists"],
        date=date,
    )

    print(f"   ✅ Report: {report_path}")
    print()

    return report_path


def send_notification(results: dict, report_path: str) -> bool:
    """Send Slack DM notification."""
    print("5️⃣ Sending Slack notification...")

    notifier = SlackNotifier()
    success = notifier.send_briefing(
        results["slack"],
        results["gmail"],
        results["lists"],
        report_path,
    )

    if success:
        print("   ✅ Notification sent")
    else:
        print("   ⚠️ Notification failed")
    print()

    return success


def post_to_channel(results: dict, post_type: str = "vendors") -> bool:
    """Update existing Slack channel message (NOT post new)."""
    print(f"6️⃣ Updating channel message ({post_type})...")

    poster = SlackPoster()

    # Always use update_vendor_summary - it updates existing message
    result = poster.update_vendor_summary(
        results["lists"],
        slack_data=results.get("slack"),
        gmail_data=results.get("gmail"),
    )

    action = result.get("action", "unknown")
    if result.get("ok"):
        print(f"   ✅ Message {action} (ts: {result.get('ts', 'N/A')})")
    else:
        print(f"   ⚠️ Update failed: {result.get('error', 'Unknown')}")
    print()

    return result.get("ok", False)


def print_summary(results: dict):
    """Print collection summary."""
    print("=" * 50)
    print("  📋 SUMMARY")
    print("=" * 50)
    print()

    # Slack
    slack = results.get("slack", {})
    pending = [m for m in slack.get("mentions_to_me", []) if not m.get("completed", False)]
    print(f"📬 Slack:")
    print(f"   - Total messages: {slack.get('total_messages', 0)}")
    print(f"   - Pending tasks: {len(pending)}")
    print(f"   - Vendor mentions: {len(slack.get('vendor_mentions', {}))}")
    print()

    # Gmail
    gmail = results.get("gmail", {})
    print(f"📧 Gmail:")
    print(f"   - Total emails: {gmail.get('total_emails', 0)}")
    print(f"   - Awaiting reply: {len(gmail.get('awaiting_reply', []))}")
    print(f"   - Follow-up needed: {len(gmail.get('needs_followup', []))}")
    print()

    # Lists
    lists = results.get("lists", {})
    by_cat = lists.get("by_category", {})
    print(f"🏢 Vendors:")
    print(f"   - Total: {lists.get('total_items', 0)}")
    print(f"   - RFID Readers: {len(by_cat.get('rfid_readers', []))}")
    print(f"   - Casino Solutions: {len(by_cat.get('casino_solutions', []))}")
    print(f"   - DIY/Development: {len(by_cat.get('diy_development', []))}")
    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="EBS Morning Automation")
    parser.add_argument("--full", action="store_true", help="Run full initial collection")
    parser.add_argument("--notify", action="store_true", help="Send Slack DM notification")
    parser.add_argument("--post", action="store_true", help="Update existing channel message")
    parser.add_argument("--date", type=str, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--no-report", action="store_true", help="Skip report generation")

    args = parser.parse_args()

    print_banner()

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Run collection
    if args.full:
        results = run_full_collection()
    else:
        results = run_incremental_collection()

    # Generate report
    report_path = None
    if not args.no_report:
        report_date = None
        if args.date:
            report_date = datetime.strptime(args.date, "%Y-%m-%d")
        report_path = generate_report(results, report_date)

    # Send notification
    if args.notify and report_path:
        send_notification(results, report_path)

    # Update channel message
    if args.post:
        post_to_channel(results)

    # Print summary
    print_summary(results)

    print("✅ Done!")


if __name__ == "__main__":
    main()
