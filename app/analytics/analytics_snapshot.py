"""
============================================================

                    STACKED ONE

                ANALYTICS SNAPSHOT

------------------------------------------------------------

Aggregates every analytics engine snapshot into one object.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.iceberg_snapshot import IcebergSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.order_flow_snapshot import OrderFlowSnapshot


@dataclass(frozen=True)
class AnalyticsSnapshot:

    order_flow: OrderFlowSnapshot

    cvd: CVDSnapshot

    large_trades: LargeTradeSnapshot

    absorption: AbsorptionSnapshot

    iceberg: IcebergSnapshot