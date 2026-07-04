"""
============================================================

                    STACKED ONE

        COMPOSITE ANALYTICS ENGINE REGISTRY

------------------------------------------------------------

Central registry for all composite analytics engines.

============================================================
"""

from app.analytics.liquidity_engine import LiquidityEngine
from app.analytics.exhaustion_engine import ExhaustionEngine
from app.analytics.smart_money_engine import SmartMoneyEngine
from app.analytics.regime_engine import RegimeEngine

COMPOSITE_ENGINE_REGISTRY = [

    LiquidityEngine,

    ExhaustionEngine,

    SmartMoneyEngine,

    RegimeEngine,

]