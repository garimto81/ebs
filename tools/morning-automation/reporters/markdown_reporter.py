# -*- coding: utf-8 -*-
"""
Markdown Report Generator

Generates daily briefing reports in Markdown format.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import OUTPUT_DIR


class MarkdownReporter:
    """Generates markdown briefing reports."""

    def __init__(self):
        self.output_dir = OUTPUT_DIR

    def generate(
        self,
        slack_data: dict,
        gmail_data: dict,
        lists_data: dict,
        date: Optional[datetime] = None,
    ) -> str:
        """
        Generate daily briefing report.

        Args:
            slack_data: Collected Slack data
            gmail_data: Collected Gmail data
            lists_data: Collected Lists data
            date: Report date (default: today)

        Returns:
            Path to generated report file
        """
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y-%m-%d")
        filename = f"{date_str}.md"
        filepath = self.output_dir / filename

        # Generate content
        content = self._generate_content(slack_data, gmail_data, lists_data, date)

        # Write file
        self.output_dir.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")

        print(f"Report generated: {filepath}")
        return str(filepath)

    def _generate_content(
        self,
        slack_data: dict,
        gmail_data: dict,
        lists_data: dict,
        date: datetime,
    ) -> str:
        """Generate report content."""
        date_str = date.strftime("%Y-%m-%d")
        time_str = date.strftime("%H:%M")

        lines = [
            f"# EBS 아침 브리핑 - {date_str}",
            "",
            f"**생성 시각**: {date_str} {time_str} KST",
            "**자동 생성**: morning-automation v1.0.0",
            "",
            "---",
            "",
        ]

        # Urgent alerts section
        alerts = self._generate_alerts(gmail_data)
        if alerts:
            lines.extend([
                "## 🚨 긴급 알림",
                "",
                *alerts,
                "",
                "---",
                "",
            ])

        # Gmail section
        lines.extend(self._generate_gmail_section(gmail_data))

        # Slack section
        lines.extend(self._generate_slack_section(slack_data))

        # Lists section
        lines.extend(self._generate_lists_section(lists_data))

        # Today's tasks
        lines.extend(self._generate_tasks_section(slack_data, gmail_data))

        # Footer
        next_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")
        lines.extend([
            "---",
            "",
            f"**다음 브리핑**: {next_date} 09:00",
        ])

        return "\n".join(lines)

    def _generate_alerts(self, gmail_data: dict) -> list:
        """Generate urgent alerts."""
        alerts = []

        # Follow-up needed
        needs_followup = gmail_data.get("needs_followup", [])
        for item in needs_followup[:3]:  # Top 3
            vendor = item.get("vendor", "Unknown")
            days = item.get("days_elapsed", 0)
            alerts.append(f"- 🔴 Follow-up 필요: {vendor} ({days}일 무응답)")

        # Delivery failures
        delivery_failures = gmail_data.get("delivery_failures", [])
        for item in delivery_failures[:3]:
            recipient = item.get("recipient", "Unknown")
            alerts.append(f"- ❌ 메일 전송 실패: {recipient}")

        return alerts

    def _generate_gmail_section(self, gmail_data: dict) -> list:
        """Generate Gmail section."""
        lines = [
            "## 📧 Gmail 현황",
            "",
        ]

        # Sent emails by vendor
        vendor_sent = gmail_data.get("vendor_sent", {})
        sent_emails = gmail_data.get("sent_emails", [])
        if sent_emails:
            lines.extend([
                "### 📤 발송 현황",
                "",
                "| 수신 업체 | 수신자 | 제목 | 발송일 |",
                "|----------|--------|------|--------|",
            ])
            for email in sent_emails[:15]:
                # Get recipient vendor (detected from email domain)
                recipient_vendor = email.get("recipient_vendor") or "-"

                # Format recipients (first recipient email)
                recipients = email.get("recipients", [])
                recipient_display = "-"
                if recipients:
                    # Extract email from "Name <email>" format
                    import re
                    first_recipient = recipients[0]
                    email_match = re.search(r'<([^>]+)>', first_recipient)
                    recipient_display = email_match.group(1) if email_match else first_recipient
                    # Truncate if too long
                    if len(recipient_display) > 30:
                        recipient_display = recipient_display[:27] + "..."

                subject = email.get("subject", "")[:35]
                date = email.get("date", "")[:10] if email.get("date") else "-"
                lines.append(f"| {recipient_vendor} | {recipient_display} | {subject} | {date} |")
            lines.append("")

        # Delivery failures
        failures = gmail_data.get("delivery_failures", [])
        if failures:
            lines.extend([
                "### ❌ 전송 실패",
                "",
                "| 수신자 | 날짜 |",
                "|--------|------|",
            ])
            for email in failures[:5]:
                recipient = email.get("recipient", "-")
                date = email.get("date", "")[:10] if email.get("date") else "-"
                lines.append(f"| {recipient} | {date} |")
            lines.append("")

        # Vendor received emails
        vendor_emails = gmail_data.get("vendor_emails", {})
        if vendor_emails:
            lines.extend([
                "### 📥 업체 수신 메일",
                "",
                "| 업체 | 발신자 | 제목 | 수신일 |",
                "|------|--------|------|--------|",
            ])
            for vendor, emails in sorted(vendor_emails.items()):
                for email in emails[:3]:
                    sender = email.get("sender", "-")
                    # Extract name from "Name <email>" format
                    import re
                    name_match = re.match(r'^([^<]+)<', sender)
                    sender_display = name_match.group(1).strip().strip('"') if name_match else sender[:25]
                    subject = email.get("subject", "")[:35]
                    date = email.get("date", "")[:10] if email.get("date") else "-"
                    lines.append(f"| {vendor} | {sender_display} | {subject} | {date} |")
            lines.append("")

        # Awaiting reply (received emails needing response)
        awaiting = gmail_data.get("awaiting_reply", [])
        if awaiting:
            lines.extend([
                "### 📬 회신 필요",
                "",
                "| 업체 | 제목 | 수신일 |",
                "|------|------|--------|",
            ])
            for email in awaiting[:10]:
                vendor = email.get("vendor", "-")
                subject = email.get("subject", "")[:40]
                date = email.get("date", "")[:10] if email.get("date") else "-"
                lines.append(f"| {vendor} | {subject} | {date} |")
            lines.append("")

        # Needs follow-up
        followup = gmail_data.get("needs_followup", [])
        if followup:
            lines.extend([
                "### ⚠️ Follow-up 필요 (72시간+ 무응답)",
                "",
                "| 업체 | 제목 | 발송일 | 경과일 |",
                "|------|------|--------|--------|",
            ])
            for email in followup[:10]:
                vendor = email.get("recipient_vendor") or email.get("vendor", "-")
                subject = email.get("subject", "")[:30]
                date = email.get("date", "")[:10] if email.get("date") else "-"
                days = email.get("days_elapsed", 0)
                lines.append(f"| {vendor} | {subject} | {date} | {days}일 |")
            lines.append("")

        # Statistics
        total = gmail_data.get("total_emails", 0)
        lines.extend([
            "### 통계",
            "",
            f"- 전체 이메일: {total}건",
            f"- 발송: {len(sent_emails)}건",
            f"- 전송 실패: {len(failures)}건",
            f"- 응답 대기: {len(awaiting)}건",
            f"- Follow-up 필요: {len(followup)}건",
            "",
            "---",
            "",
        ])

        return lines

    def _generate_slack_section(self, slack_data: dict) -> list:
        """Generate Slack section."""
        lines = [
            "## 📋 Slack 액션 아이템",
            "",
        ]

        # Pending items (mentions to me, not completed)
        mentions = slack_data.get("mentions_to_me", [])
        # Filter out system messages
        pending = [
            m for m in mentions
            if not m.get("completed", False)
            and "채널에 참여함" not in m.get("text", "")
            and "has joined the channel" not in m.get("text", "")
        ]
        completed = [m for m in mentions if m.get("completed", False)]

        if pending:
            lines.extend([
                "### 미완료 작업 (✅ 없음)",
                "",
                "| 날짜 | 내용 | 링크 |",
                "|------|------|------|",
            ])
            for item in pending[:10]:
                date = item.get("timestamp", "")[:10] if item.get("timestamp") else "-"
                text = self._extract_display_text(item.get("text", ""), max_len=50)
                link = item.get("link", "#")
                lines.append(f"| {date} | {text} | [바로가기]({link}) |")
            lines.append("")
        else:
            lines.append("✅ 모든 작업 완료!")
            lines.append("")

        # Statistics
        lines.extend([
            "### 통계",
            "",
            f"- 미완료: {len(pending)}건",
            f"- 완료: {len(completed)}건",
            "",
        ])

        # Vendor mentions
        vendor_mentions = slack_data.get("vendor_mentions", {})
        if vendor_mentions:
            lines.extend([
                "### 업체 언급 현황",
                "",
            ])
            for vendor, mentions in sorted(vendor_mentions.items(), key=lambda x: -len(x[1])):
                lines.append(f"- {vendor}: {len(mentions)}회")
            lines.append("")

        lines.extend([
            "---",
            "",
        ])

        return lines

    def _generate_lists_section(self, lists_data: dict) -> list:
        """Generate Lists section."""
        lines = [
            "## 🏢 업체 관리 현황",
            "",
        ]

        by_category = lists_data.get("by_category", {})

        # RFID Readers
        rfid = by_category.get("rfid_readers", [])
        if rfid:
            lines.extend([
                "### RFID 리더/모듈 업체",
                "",
            ])
            for item in rfid[:5]:
                name = item.get("name", "")[:30]
                lines.append(f"- {name}")
            lines.append("")

        # Casino Solutions
        casino = by_category.get("casino_solutions", [])
        if casino:
            lines.extend([
                "### 카지노 통합 솔루션",
                "",
            ])
            for item in casino[:5]:
                name = item.get("name", "")[:30]
                lines.append(f"- {name}")
            lines.append("")

        # DIY/Development
        diy = by_category.get("diy_development", [])
        if diy:
            lines.extend([
                "### DIY/개발 업체",
                "",
            ])
            for item in diy[:5]:
                name = item.get("name", "")[:30]
                lines.append(f"- {name}")
            lines.append("")

        # Summary
        total = lists_data.get("total_items", 0)
        lines.extend([
            "### 요약",
            "",
            f"**총 {total}개 업체 등록됨**",
            "",
            f"- RFID 리더: {len(rfid)}개",
            f"- 카지노 솔루션: {len(casino)}개",
            f"- DIY/개발: {len(diy)}개",
            f"- 벤치마크: {len(by_category.get('benchmarks', []))}개",
            "",
            "---",
            "",
        ])

        return lines

    def _extract_display_text(self, text: str, max_len: int = 50) -> str:
        """Extract displayable text, handling URLs and special chars."""
        import re

        # Extract document title from Slack link format: <URL|Title>
        link_match = re.search(r'<[^|]+\|([^>]+)>', text)
        if link_match:
            text = link_match.group(1)

        # Remove user mentions like <@U12345>
        text = re.sub(r'<@[A-Z0-9]+>', '', text)

        # Clean up extra whitespace
        text = ' '.join(text.split())

        # Escape pipe chars for markdown tables
        text = text.replace("|", "\\|")

        # Truncate
        if len(text) > max_len:
            text = text[:max_len-3] + "..."

        return text.strip()

    # All vendors that should receive RFI (same as slack_poster.py)
    ALL_RFI_VENDORS = {
        # Category A (통합 파트너 후보)
        "sunfly": {"name": "Sun-Fly", "email": "susie.su@sun-fly.com", "cat": "A"},
        "angel": {"name": "Angel Playing Cards", "email": "overseas@angel-group.co.jp", "cat": "A"},
        "emfoplus": {"name": "엠포플러스", "email": "biz@emfoplus.co.kr", "cat": "A"},
        # Category B (부품 공급)
        "feig": {"name": "FEIG", "email": "info@feig.de", "cat": "B"},
        "gao": {"name": "GAO RFID", "email": "sales@gaorfid.com", "cat": "B"},
        "identiv": {"name": "Identiv", "email": "sales@identiv.com", "cat": "B"},
        "pongee": {"name": "PONGEE", "email": "pongee@pongee.com.tw", "cat": "B"},
        "waveshare": {"name": "Waveshare", "email": "service@waveshare.com", "cat": "B"},
        "sparkfun": {"name": "SparkFun", "email": "sales@sparkfun.com", "cat": "B"},
        "adafruit": {"name": "Adafruit", "email": "support@adafruit.com", "cat": "B"},
        "fadedspade": {"name": "Faded Spade", "email": "sales@fadedspade.com", "cat": "B"},
    }

    def _generate_tasks_section(self, slack_data: dict, gmail_data: dict) -> list:
        """Generate today's tasks section."""
        lines = [
            "## 📅 오늘 할 일 제안",
            "",
        ]

        task_num = 1

        # Analyze sent/failed/unsent vendors
        sent_vendors = set(gmail_data.get("vendor_sent", {}).keys())
        failed_vendors = set()
        for failure in gmail_data.get("delivery_failures", []):
            recipient = failure.get("recipient", "")
            for vk, info in self.ALL_RFI_VENDORS.items():
                if info["email"] in recipient or recipient in info["email"]:
                    failed_vendors.add(vk)

        # Priority 1: Unsent Category A vendors (CRITICAL)
        for vk, info in self.ALL_RFI_VENDORS.items():
            if info["cat"] == "A" and vk not in sent_vendors and vk not in failed_vendors:
                lines.append(f"{task_num}. [ ] **[CRITICAL]** {info['name']} RFI 발송 ({info['email']})")
                task_num += 1

        # Priority 2: Failed deliveries (need alternative email)
        for vk in failed_vendors:
            info = self.ALL_RFI_VENDORS.get(vk, {})
            lines.append(f"{task_num}. [ ] {info.get('name', vk)} 대체 이메일 확인 및 재발송")
            task_num += 1

        # Priority 3: Follow-up emails
        for email in gmail_data.get("needs_followup", [])[:3]:
            vendor = email.get("vendor", "Unknown")
            lines.append(f"{task_num}. [ ] {vendor} Follow-up 메일 발송")
            task_num += 1

        # Priority 4: Pending Slack items
        mentions = slack_data.get("mentions_to_me", [])
        pending = [m for m in mentions if not m.get("completed", False)]
        for item in pending[:3]:
            text = item.get("text", "")[:30]
            lines.append(f"{task_num}. [ ] Slack 요청 처리: {text}...")
            task_num += 1

        # Default task
        if task_num == 1:
            lines.append("1. [ ] EBS-WORK-DASHBOARD.md 업데이트")

        lines.append("")

        return lines


if __name__ == "__main__":
    # Test with sample data
    reporter = MarkdownReporter()

    sample_slack = {
        "mentions_to_me": [
            {"timestamp": "2026-02-01", "text": "RFID 모듈 검토", "completed": False, "link": "#"},
        ],
        "vendor_mentions": {"feig": [1, 2], "waveshare": [1]},
    }

    sample_gmail = {
        "total_emails": 15,
        "awaiting_reply": [],
        "needs_followup": [
            {"vendor": "FEIG", "subject": "Quote Request", "date": "2026-01-28", "days_elapsed": 5},
        ],
    }

    sample_lists = {
        "total_items": 16,
        "by_category": {
            "rfid_readers": [{"name": "FEIG"}, {"name": "GAO RFID"}],
            "casino_solutions": [{"name": "S.I.T. Korea"}],
            "diy_development": [{"name": "ST Micro"}],
            "benchmarks": [{"name": "PokerGFX"}],
        },
    }

    path = reporter.generate(sample_slack, sample_gmail, sample_lists)
    print(f"Generated: {path}")
