"""
============================================================

                    STACKED ONE

                  EVENT TYPES

============================================================
"""

from __future__ import annotations

from enum import Enum


class EventType(str, Enum):

    #
    # Market
    #

    TRADE = "TRADE"

    ORDERBOOK = "ORDERBOOK"

    TICK = "TICK"

    #
    # Analytics
    #

    ANALYTICS_UPDATED = "ANALYTICS_UPDATED"

    COMPOSITE_UPDATED = "COMPOSITE_UPDATED"

    #
    # Strategy
    #

    STRATEGY_UPDATED = "STRATEGY_UPDATED"

    #
    # Confluence
    #

    CONFLUENCE_UPDATED = "CONFLUENCE_UPDATED"

    #
    # Risk
    #

    RISK_UPDATED = "RISK_UPDATED"

    #
    # Execution
    #

    EXECUTION = "EXECUTION"

    #
    # Journal
    #

    DECISION_RECORDED = "DECISION_RECORDED"

    TRADE_RECORDED = "TRADE_RECORDED"

    #
    # Performance
    #

    PERFORMANCE_UPDATED = "PERFORMANCE_UPDATED"

    #
    # Dashboard

    DASHBOARD_UPDATED = "DASHBOARD_UPDATED"

    #
    # AI

    FEATURE_VECTOR = "FEATURE_VECTOR"

    AI_SIGNAL = "AI_SIGNAL"

    #
    # System

    ERROR = "ERROR"

    WARNING = "WARNING"

    INFO = "INFO"