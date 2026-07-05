"""
============================================================

                    STACKED ONE

                ENGINE REGISTRY

------------------------------------------------------------

Central registry for all analytics engines.

AnalyticsManager creates every engine from here.

============================================================
"""

from __future__ import annotations

from app.analytics.absorption_engine import AbsorptionEngine
from app.analytics.base_engine import AnalyticsEngine
from app.analytics.cvd_engine import CVDEngine
from app.analytics.iceberg_engine import IcebergEngine
from app.analytics.large_trade_engine import LargeTradeEngine
from app.analytics.order_flow_engine import OrderFlowEngine

type AnalyticsEngineType = type[AnalyticsEngine]

ENGINE_REGISTRY: tuple[AnalyticsEngineType, ...] = (
    OrderFlowEngine,
    CVDEngine,
    LargeTradeEngine,
    AbsorptionEngine,
    IcebergEngine,
)