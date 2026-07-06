"""
============================================================

                    STACKED ONE

              HISTORICAL SIMULATION RUNNER

------------------------------------------------------------

Standalone entry point for running the Simulator.

The DI container does not wire the simulator package yet,
so every dependency is constructed by hand here.

============================================================
"""

from __future__ import annotations

import csv
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from app.analytics.analytics_manager import AnalyticsManager
from app.execution.execution_engine import ExecutionEngine
from app.execution.paper_broker import PaperBroker
from app.performance.performance_manager import PerformanceManager
from app.pipeline.decision_pipeline import DecisionPipeline
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position_manager import PositionManager
from app.replay.csv_tick_provider import CSVTickProvider
from app.replay.replay_engine import ReplayEngine
from app.simulator.simulation_config import SimulationConfig
from app.simulator.simulator import Simulator

SYMBOL = "BTCUSD"

TIMEFRAME = "1m"

START = datetime(2026, 1, 1, 0, 0, 0)


# ==========================================================
# Synthetic Tick Tape
# ==========================================================


def _generate_ticks(path: Path) -> datetime:
    """
    Writes a synthetic tick tape that exercises both the
    entry and exit execution paths.

    Phase 1 - a sell-heavy consolidation at a single price,
    giving the analytics engines enough evidence (absorption,
    iceberg, a large trade, negative CVD) to produce an
    approved BUY trade plan.

    Phase 2 - a sustained uptrend so the opened long position
    reaches its take-profit target.
    """

    rows: list[tuple[datetime, float, float, str]] = []

    timestamp = START

    price = 100.0

    #
    # Phase 1 - Consolidation
    #

    for i in range(100):

        if i == 99:

            #
            # Final consolidation tick lands exactly on the
            # next minute boundary, closing the candle while
            # still trading at the consolidation price - this
            # is the tick the analytics engines see last, so
            # it must stay at the consolidation price for the
            # iceberg/absorption evidence to still be active.
            #

            timestamp = START + timedelta(minutes=1)

        if i == 0:

            #
            # Single oversized sell print - trips the
            # large-trade engine on the same side as the
            # rest of the tape, so strategy votes don't tie.
            #

            side = "sell"

            volume = 120.0

        elif i % 5 == 0:

            side = "buy"

            volume = 6.0

        else:

            side = "sell"

            volume = 8.0

        rows.append((timestamp, price, volume, side))

        if i < 99:

            timestamp += timedelta(seconds=0.3)

    #
    # Phase 2 - Uptrend
    #

    for minute in range(1, 240):

        for i in range(20):

            price += 0.05

            side = "buy" if i % 2 == 0 else "sell"

            rows.append((timestamp, price, 3.0, side))

            timestamp += timedelta(seconds=2)

        timestamp = START + timedelta(minutes=minute + 1)

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["timestamp", "price", "volume", "side"])

        for ts, px, volume, side in rows:

            writer.writerow(
                [ts.isoformat(), f"{px:.4f}", volume, side]
            )

    return timestamp


# ==========================================================
# Main
# ==========================================================


def main() -> None:

    with tempfile.TemporaryDirectory() as tmp_dir:

        csv_path = Path(tmp_dir) / "ticks.csv"

        end = _generate_ticks(csv_path)

        provider = CSVTickProvider(str(csv_path))

        replay = ReplayEngine(provider)

        replay.load(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            start=START,
            end=end,
        )

        simulator = Simulator(
            replay=replay,
            analytics=AnalyticsManager(),
            market=MarketPipeline(),
            decision=DecisionPipeline(),
            execution=ExecutionEngine(broker=PaperBroker()),
            positions=PositionManager(),
            performance=PerformanceManager(),
        )

        config = SimulationConfig(
            symbol=SYMBOL,
            timeframe=TIMEFRAME,
            start=START.isoformat(),
            end=end.isoformat(),
            strategy="All",
            initial_capital=100000.0,
            risk_per_trade=0.01,
            leverage=1.0,
            commission=0.0,
            slippage=0.0,
        )

        result = simulator.run(config)

    print("Simulation complete")
    print(f"  Total trades   : {result.total_trades}")
    print(f"  Winning trades : {result.winning_trades}")
    print(f"  Losing trades  : {result.losing_trades}")
    print(f"  Net profit     : {result.net_profit:.2f}")
    print(f"  Win rate       : {result.win_rate:.2%}")
    print(f"  Profit factor  : {result.profit_factor:.2f}")
    print(f"  Max drawdown   : {result.max_drawdown:.2f}")
    print(f"  Ending equity  : {result.ending_equity:.2f}")
    print(f"  Trade IDs      : {result.trades}")


if __name__ == "__main__":

    main()
