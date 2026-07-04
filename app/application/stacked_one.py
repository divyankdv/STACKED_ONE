"""
============================================================

                    STACKED ONE

                 APPLICATION API

------------------------------------------------------------

Public API for the entire trading framework.

============================================================
"""

from __future__ import annotations

from app.application.bootstrap import Bootstrap


class StackedOne:
    """
    Main application façade.
    """

    # =====================================================

    def __init__(self):

        self._container = Bootstrap.build()

        self.market_pipeline = self._container.resolve(

            "market_pipeline"

        )

        self.decision_pipeline = self._container.resolve(

            "decision_pipeline"

        )

        self.event_bus = self._container.resolve(

            "event_bus"

        )

        self._running = False

    # =====================================================

    def start(self):

        self._running = True

    # =====================================================

    def stop(self):

        self._running = False

    # =====================================================

    @property
    def running(self):

        return self._running

    # =====================================================

    def process_tick(

        self,

        tick,

    ):
        """
        Main application entry point.

        Tick
            ↓
        MarketPipeline
            ↓
        DecisionPipeline
        """

        completed = self.market_pipeline.process_tick(

            tick,

        )

        #
        # No completed candle yet.
        #

        if completed is None:

            return None

        #
        # TODO
        #
        # When AnalyticsManager becomes candle-aware,
        # DecisionPipeline will process the completed
        # market snapshot here.
        #

        return completed

    # =====================================================

    def reset(self):

        self.market_pipeline.reset()

        self.decision_pipeline.reset()

    # =====================================================

    def status(self):

        return {

            "running": self.running,

            "market_pipeline": str(

                self.market_pipeline,

            ),

            "decision_pipeline": str(

                self.decision_pipeline,

            ),

            "event_bus": str(

                self.event_bus,

            ),

        }

    # =====================================================

    def __str__(self):

        return (

            "StackedOne("

            f"running={self.running}"

            ")"

        )

    __repr__ = __str__