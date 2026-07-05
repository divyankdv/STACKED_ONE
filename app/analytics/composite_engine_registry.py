"""
============================================================

                    STACKED ONE

        COMPOSITE ANALYTICS ENGINE REGISTRY

============================================================
"""

from __future__ import annotations

from typing import TypeAlias

from app.analytics.base_composite_engine import CompositeAnalyticsEngine
from app.analytics.exhaustion_engine import ExhaustionEngine
from app.analytics.liquidity_engine import LiquidityEngine
from app.analytics.regime_engine import RegimeEngine
from app.analytics.smart_money_engine import SmartMoneyEngine

CompositeEngineType: TypeAlias = type[CompositeAnalyticsEngine]

COMPOSITE_ENGINE_REGISTRY: tuple[CompositeEngineType, ...] = (
    LiquidityEngine,
    ExhaustionEngine,
    SmartMoneyEngine,
    RegimeEngine,
)