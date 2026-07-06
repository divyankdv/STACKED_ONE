"""
============================================================

                    STACKED ONE

                  REPLAY ENGINE

------------------------------------------------------------

Consumes any MarketDataSource and replays market events
through the complete STACKED ONE trading pipeline.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.pipeline.decision_pipeline import DecisionPipeline
from app.pipeline.market_pipeline import MarketPipeline
from app.simulator.market_data_source import MarketDataSource
from app.simulator.market_event import MarketEvent


@dataclass(slots=True)
class ReplayStatistics:
    events_processed: int = 0

    candles_completed: int = 0

    decisions_generated: int = 0


class ReplayEngine:
    """
    Generic replay engine.

    Works with any MarketDataSource.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        source: MarketDataSource,
        market_pipeline: MarketPipeline,
        decision_pipeline: DecisionPipeline,
    ):

        self.source = source

        self.market_pipeline = market_pipeline

        self.decision_pipeline = decision_pipeline

        self.statistics = ReplayStatistics()

    # =====================================================
    # Run
    # =====================================================

    def run(self):
        """
        Replay every market event.
        """

        self.statistics = ReplayStatistics()

        self.source.reset()

        for event in self.source:
            self.process_event(event)

        return self.statistics

    # =====================================================
    # Process One Event
    # =====================================================

    def process_event(
        self,
        event: MarketEvent,
    ):

        self.statistics.events_processed += 1

        #
        # Feed Market Pipeline
        #

        completed = self.market_pipeline.process_tick(event)

        if completed is None:
            return

        self.statistics.candles_completed += 1

        #
        # Feed Decision Pipeline
        #
        # NOTE:
        # DecisionPipeline will eventually consume a
        # MarketSnapshot instead of raw candles.
        #

        self.decision_pipeline.process_trade(event)

        self.statistics.decisions_generated += 1

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.statistics = ReplayStatistics()

        self.market_pipeline.reset()

        self.decision_pipeline.reset()

        self.source.reset()

    # =====================================================
    # Properties
    # =====================================================

    @property
    def progress(self):

        return self.source.progress

    @property
    def finished(self):

        return self.source.finished

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return f"ReplayEngine({self.statistics.events_processed} events)"

    __repr__ = __str__
