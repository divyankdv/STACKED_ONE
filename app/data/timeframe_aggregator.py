"""
============================================================

                STACKED QUANT AI V6

            TIMEFRAME AGGREGATOR

------------------------------------------------------------

Aggregates completed 1-minute candles into higher
timeframes using TradingView-style bucket alignment.

Responsibilities
----------------
✓ Build 5m candles
✓ Build 15m candles
✓ Build 1h candles
✓ Build 4h candles
✓ Build Daily candles

Does NOT
---------
✗ Build 1m candles
✗ Store history
✗ Calculate indicators

============================================================
"""

from datetime import datetime

from app.models.candle import Candle


class TimeframeAggregator:

    def __init__(self):

        self.timeframes = {

            "5m": 5,

            "15m": 15,

            "1h": 60,

            "4h": 240,

            "1d": 1440,

        }

        self.buffers: dict[str, list[Candle]] = {

            tf: []

            for tf in self.timeframes

        }

        self.bucket_start: dict[str, datetime | None] = {

            tf: None

            for tf in self.timeframes

        }

    # =====================================================
    # TradingView Bucket
    # =====================================================

    def get_bucket_start(

        self,

        dt: datetime,

        minutes: int,

    ) -> datetime:

        # Daily

        if minutes == 1440:

            return dt.replace(

                hour=0,

                minute=0,

                second=0,

                microsecond=0,

            )

        # Hourly+

        if minutes >= 60:

            hours = minutes // 60

            hour = (dt.hour // hours) * hours

            return dt.replace(

                hour=hour,

                minute=0,

                second=0,

                microsecond=0,

            )

        # Minute

        bucket = (

            dt.minute // minutes

        ) * minutes

        return dt.replace(

            minute=bucket,

            second=0,

            microsecond=0,

        )

    # =====================================================
    # Update
    # =====================================================

    def update(

        self,

        candle: Candle,

    ) -> dict[str, Candle]:

        completed = {}

        for tf, minutes in self.timeframes.items():

            bucket = self.get_bucket_start(

                candle.time,

                minutes,

            )

            # ------------------------------------------
            # First Candle
            # ------------------------------------------

            if self.bucket_start[tf] is None:

                self.bucket_start[tf] = bucket

            # ------------------------------------------
            # Bucket Closed
            # ------------------------------------------

            elif bucket != self.bucket_start[tf]:

                aggregated = self.build(

                    self.buffers[tf]

                )

                if aggregated is not None:

                    completed[tf] = aggregated

                self.buffers[tf].clear()

                self.bucket_start[tf] = bucket

            # ------------------------------------------
            # Add Candle
            # ------------------------------------------

            self.buffers[tf].append(candle)

        return completed

    # =====================================================
    # Aggregate Candles
    # =====================================================

    def build(

        self,

        candles: list[Candle],

    ) -> Candle | None:

        if not candles:

            return None

        assert len(candles) > 0

        first = candles[0]

        last = candles[-1]

        return Candle(

            time=first.time,

            open=first.open,

            high=max(

                c.high

                for c in candles

            ),

            low=min(

                c.low

                for c in candles

            ),

            close=last.close,

            volume=sum(

                c.volume

                for c in candles

            ),

            buy_volume=sum(

                c.buy_volume

                for c in candles

            ),

            sell_volume=sum(

                c.sell_volume

                for c in candles

            ),

            delta=sum(

                c.delta

                for c in candles

            ),

            trades=sum(

                c.trades

                for c in candles

            ),

        )

    # =====================================================
    # Buffer Count
    # =====================================================

    def count(

        self,

        timeframe: str,

    ) -> int:

        return len(

            self.buffers.get(

                timeframe,

                [],

            )

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        for tf in self.timeframes:

            self.buffers[tf].clear()

            self.bucket_start[tf] = None