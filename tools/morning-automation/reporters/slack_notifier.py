# -*- coding: utf-8 -*-
"""
Slack DM Notifier

Sends daily briefing summary via Slack DM.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "C:/claude")

from lib.slack.client import SlackUserClient
from config.settings import SLACK_USER_ID, GFX_LICENSE_EXPIRY


class SlackNotifier:
    """Sends notifications via Slack DM."""

    def __init__(self):
        self.client = SlackUserClient()

    def send_briefing(
        self,
        slack_data: dict,
        gmail_data: dict,
        lists_data: dict,
        report_path: str,
    ) -> bool:
        """
        Send briefing summary via DM.

        Args:
            slack_data: Collected Slack data
            gmail_data: Collected Gmail data
            lists_data: Collected Lists data
            report_path: Path to full report file

        Returns:
            True if sent successfully
        """
        message = self._format_message(slack_data, gmail_data, lists_data, report_path)

        try:
            # Send DM to self
            response = self.client._client.chat_postMessage(
                channel=SLACK_USER_ID,
                text=message,
                mrkdwn=True,
            )
            return response.data.get("ok", False)
        except Exception as e:
            print(f"Error sending DM: {e}")
            return False

    def _format_message(
        self,
        slack_data: dict,
        gmail_data: dict,
        lists_data: dict,
        report_path: str,
    ) -> str:
        """Format briefing message."""
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Calculate alerts
        alerts = []

        # GFX license
        gfx_expiry = datetime.strptime(GFX_LICENSE_EXPIRY, "%Y-%m-%d")
        gfx_days = (gfx_expiry - datetime.now()).days
        if gfx_days <= 60:
            alerts.append(f"GFX 라이선스 D-{gfx_days}")

        # Follow-up needed
        followup_count = len(gmail_data.get("needs_followup", []))
        if followup_count > 0:
            alerts.append(f"Follow-up 필요 {followup_count}건")

        # Pending items
        mentions = slack_data.get("mentions_to_me", [])
        pending_count = len([m for m in mentions if not m.get("completed", False)])

        # Format message
        lines = [
            f"🌅 *EBS 아침 브리핑 - {date_str}*",
            "",
        ]

        if alerts:
            lines.append(f"🚨 *긴급*: {' / '.join(alerts)}")
            lines.append("")

        lines.extend([
            f"📧 Gmail: {gmail_data.get('total_emails', 0)}건 (대기 {len(gmail_data.get('awaiting_reply', []))}건)",
            f"📋 미완료: {pending_count}건",
            f"🏢 업체: {lists_data.get('total_items', 0)}개",
            "",
            f"📄 상세 리포트: `{report_path}`",
        ])

        return "\n".join(lines)

    def send_alert(self, message: str) -> bool:
        """
        Send an alert message via DM.

        Args:
            message: Alert message

        Returns:
            True if sent successfully
        """
        try:
            response = self.client._client.chat_postMessage(
                channel=SLACK_USER_ID,
                text=f"🚨 *EBS 알림*\n\n{message}",
                mrkdwn=True,
            )
            return response.data.get("ok", False)
        except Exception as e:
            print(f"Error sending alert: {e}")
            return False


if __name__ == "__main__":
    # Test notification
    notifier = SlackNotifier()

    sample_slack = {"mentions_to_me": [{"completed": False}]}
    sample_gmail = {"total_emails": 10, "awaiting_reply": [], "needs_followup": []}
    sample_lists = {"total_items": 16}

    result = notifier.send_briefing(
        sample_slack,
        sample_gmail,
        sample_lists,
        "C:/claude/ebs/docs/operations/daily-briefings/test.md"
    )
    print(f"Sent: {result}")
