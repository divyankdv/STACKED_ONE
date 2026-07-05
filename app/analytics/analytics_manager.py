"""
============================================================

                    STACKED ONE

                ANALYTICS MANAGER

------------------------------------------------------------

Central coordinator for every analytics engine.

New engines register once and automatically receive
every trade.

============================================================
"""

from __future__ import annotations

from typing import cast

from app.analytics.order_flow_snapshot import OrderFlowSnapshot
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.iceberg_snapshot import IcebergSnapshot

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.engine_registry import ENGINE_REGISTRY


class AnalyticsManager:

    """
    Central analytics manager.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.engines = []

        for engine_cls in ENGINE_REGISTRY:

            self.register(

                engine_cls()

            )

    # =====================================================
    # Register Engine
    # =====================================================

    def register(

        self,

        engine,

    ):

        if not hasattr(

            engine,

            "snapshot_name",

        ):

            raise TypeError(

                f"{engine.__class__.__name__} "

                "does not define snapshot_name."

            )

        self.engines.append(

            engine

        )

    # =====================================================
    # Update Trade
    # =====================================================

    def update_trade(

        self,

        trade,

    ):

        for engine in self.engines:

            engine.update_trade(

                trade

            )
    
    # =====================================================
    # Update + Snapshot
    # =====================================================

    def update(

        self,

        trade,

    ) -> AnalyticsSnapshot:

        """
        High-level API.

        Processes one trade through every analytics engine
        and returns the latest AnalyticsSnapshot.
        """

        self.update_trade(

            trade,

        )

        return self.snapshot()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        for engine in self.engines:

            engine.reset()

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self) -> AnalyticsSnapshot:

        snapshots: dict[str, object] = {}

        for engine in self.engines:

            snapshots[engine.snapshot_name] = engine.snapshot()

        return AnalyticsSnapshot(

            order_flow=cast(
                OrderFlowSnapshot,
                snapshots["order_flow"],
            ),

            cvd=cast(
                CVDSnapshot,
                snapshots["cvd"],
            ),

            large_trades=cast(
                LargeTradeSnapshot,
                snapshots["large_trades"],
            ),

            absorption=cast(
                AbsorptionSnapshot,
                snapshots["absorption"],
            ),

            iceberg=cast(
                IcebergSnapshot,
                snapshots["iceberg"],
            ),

        )

    # =====================================================
    # Get Engine
    # =====================================================

    def get_engine(

        self,

        engine_type,

    ):

        for engine in self.engines:

            if isinstance(

                engine,

                engine_type,

            ):

                return engine

        return None

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            f"AnalyticsManager("

            f"engines={len(self.engines)})"

        )

    __repr__ = __str__