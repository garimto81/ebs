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

from config.settings import OUTPUT_DIR, GFX_LICENSE_EXPIRY


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

        # Calculate GFX license days remaining
        gfx_expiry = datetime.strptime(GFX_LICENSE_EXPIRY, "%Y-%m-%d")
        gfx_days = (gfx_expiry - date).days

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
        alerts = self._generate_alerts(gmail_data, gfx_days)
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

    def _generate_alerts(self, gmail_data: dict, gfx_days: int) -> list:
        """Generate urgent alerts."""
        alerts = []

        # GFX license alert
        if gfx_days <= 60:
            emoji = "🔴" if gfx_days <= 30 else "⚠️"
            alerts.append(f"- {emoji} GFX 라이선스 만료: **D-{gfx_days}**")

        # Follow-up needed
        needs_followup = gmail_data.get("needs_followup", [])
        for item in needs_followup[:3]:  # Top 3
            vendor = item.get("vendor", "Unknown")
            days = item.get("days_elapsed", 0)
            alerts.append(f"- 🔴 Follow-up 필요: {vendor} ({days}일 무응답)")

        return alerts

    def _generate_gmail_section(self, gmail_data: dict) -> list:
        """Generate Gmail section."""
        lines = [
            "## 📧 Gmail 현황",
            "",
        ]

        # Awaiting reply
        awaiting = gmail_data.get("awaiting_reply", [])
        if awaiting:
            lines.extend([
                "### 새 메일 (응답 대기)",
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
                vendor = email.get("vendor", "-")
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

    def _generate_tasks_section(self, slack_data: dict, gmail_data: dict) -> list:
        """Generate today's tasks section."""
        lines = [
            "## 📅 오늘 할 일 제안",
            "",
        ]

        task_num = 1

        # Follow-up emails
        for email in gmail_data.get("needs_followup", [])[:3]:
            vendor = email.get("vendor", "Unknown")
            lines.append(f"{task_num}. [ ] {vendor} Follow-up 메일 발송")
            task_num += 1

        # Pending Slack items
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
