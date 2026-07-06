"""
============================================================

                    STACKED ONE

                  TRADE RECORD

------------------------------------------------------------

Stores every completed trade together with
the analytics that generated it.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.risk.trade_plan import TradePlan


@dataclass(slots=True)
class TradeRecord:
    trade_id: str

    symbol: str

    opened_at: datetime

    closed_at: datetime | None

    trade_plan: TradePlan

    analytics: AnalyticsSnapshot

    pnl: float = 0.0

    r_multiple: float = 0.0

    winner: bool = False
