from __future__ import annotations

from dataclasses import dataclass

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.liquidity_snapshot import LiquiditySnapshot
from app.analytics.exhaustion_snapshot import ExhaustionSnapshot
from app.analytics.smart_money_snapshot import SmartMoneySnapshot
from app.analytics.regime_snapshot import RegimeSnapshot


@dataclass(slots=True)
class CompositeAnalyticsContext:

    #
    # Primary Analytics
    #

    analytics: AnalyticsSnapshot

    #
    # Composite Analytics
    #

    liquidity: LiquiditySnapshot | None = None

    exhaustion: ExhaustionSnapshot | None = None

    smart_money: SmartMoneySnapshot | None = None

    regime: RegimeSnapshot | None = None