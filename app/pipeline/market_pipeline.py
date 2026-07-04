"""
============================================================

                STACKED QUANT AI V6

                MARKET PIPELINE

------------------------------------------------------------

Central market data pipeline.

Responsibilities
----------------
✓ Process live ticks
✓ Process historical candles
✓ Store 1m candles
✓ Aggregate higher timeframes
✓ Store aggregated candles

============================================================
"""

from app.data.tick_engine import TickEngine
from app.data.timeframe_manager import TimeframeManager
from app.data.timeframe_aggregator import TimeframeAggregator
from app.models.candle import Candle


class MarketPipeline:

    def __init__(self):

        self.tick_engine = TickEngine()

        self.timeframe_manager = TimeframeManager()

        self.timeframe_aggregator = TimeframeAggregator()

    # =====================================================
    # Live Tick
    # =====================================================

    def process_tick(self, tick):

        completed = self.tick_engine.update(tick)

        if completed is None:

            return None

        return self._process_completed_candle(completed)

    # =====================================================
    # Historical Candle
    # =====================================================

    def process_candle(

        self,

        candle: Candle,

    ):

        return self._process_completed_candle(candle)

    # =====================================================
    # Common Candle Processing
    # =====================================================

    def _process_completed_candle(

        self,

        candle: Candle,

    ):

        # Store 1m candle

        self.timeframe_manager.add(

            "1m",

            candle,

        )

        # Aggregate higher timeframes

        completed = self.timeframe_aggregator.update(

            candle

        )

        # Store aggregated candles

        for tf, tf_candle in completed.items():

            self.timeframe_manager.add(

                tf,

                tf_candle,

            )

        return {

            "1m": candle,

            **completed,

        }

    # =====================================================
    # History
    # =====================================================

    def history(

        self,

        timeframe,

    ):

        return self.timeframe_manager.history(

            timeframe

        )

    # =====================================================
    # Last Candle
    # =====================================================

    def last(

        self,

        timeframe,

    ):

        return self.timeframe_manager.last(

            timeframe

        )

    # =====================================================
    # Count
    # =====================================================

    def count(

        self,

        timeframe,

    ):

        return self.timeframe_manager.count(

            timeframe

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.tick_engine.reset()

        self.timeframe_manager.reset()

        self.timeframe_aggregator.reset()