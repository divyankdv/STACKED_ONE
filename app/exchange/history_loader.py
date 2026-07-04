"""
============================================================

                STACKED QUANT AI V6

                HISTORY LOADER

------------------------------------------------------------

Downloads historical candles from Delta Exchange and
warms up the market pipeline.

Responsibilities
----------------
✓ Download history
✓ Feed MarketPipeline
✓ Warm all higher timeframes

Does NOT
---------
✗ Calculate indicators
✗ Make trading decisions
✗ Connect WebSocket

============================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta, UTC

from app.config.settings import settings
from app.logger import logger


class HistoryLoader:

    def __init__(

        self,

        rest_client,

        market_pipeline,

    ):

        self.client = rest_client

        self.pipeline = market_pipeline

    # =====================================================
    # Load History
    # =====================================================

    def load(

        self,

        hours: int = 24,

        resolution: str = "1m",

    ) -> int:

        """
        Download historical candles and feed
        them into the Market Pipeline.

        Returns
        -------
        int
            Number of candles loaded.
        """

        logger.info("Loading historical candles...")

        end = datetime.now(UTC)

        start = end - timedelta(hours=hours)

        candles = self.client.get_history(

            symbol=settings.symbol,

            resolution=resolution,

            start=start,

            end=end,

        )

        loaded = 0

        for candle in candles:

            self.pipeline.process_candle(candle)

            loaded += 1

        logger.info(

            f"History Loaded : {loaded} candles"

        )

        return loaded

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        print()

        print("=" * 60)

        print("History Summary")

        print("=" * 60)

        for tf in settings.timeframes:

            print(

                f"{tf:5} : "

                f"{self.pipeline.timeframe_manager.count(tf)}"

            )

        print()