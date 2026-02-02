# -*- coding: utf-8 -*-
"""EBS Morning Automation - Collectors"""

from .slack_collector import SlackCollector
from .gmail_collector import GmailCollector
from .lists_collector import ListsCollector

__all__ = ["SlackCollector", "GmailCollector", "ListsCollector"]
