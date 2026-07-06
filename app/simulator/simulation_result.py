"""
============================================================

                    STACKED ONE

               SIMULATION RESULT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SimulationResult:
    #
    # Metadata
    #

    strategy: str = ""

    symbol: str = ""

    timeframe: str = ""

    #
    # Trades
    #

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    breakeven_trades: int = 0

    #
    # Performance
    #

    net_profit: float = 0.0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    win_rate: float = 0.0

    profit_factor: float = 0.0

    expectancy: float = 0.0

    sharpe_ratio: float = 0.0

    max_drawdown: float = 0.0

    ending_equity: float = 0.0

    #
    # Curves
    #

    equity_curve: list[float] = field(default_factory=list)

    #
    # Trade IDs
    #

    trades: list[str] = field(default_factory=list)
