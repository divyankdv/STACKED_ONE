"""
============================================================

                    STACKED ONE

                SIMULATION CONFIG

------------------------------------------------------------

Configuration for a historical simulation.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SimulationConfig:

    # Market

    symbol: str

    timeframe: str

    start: str

    end: str

    # Strategy

    strategy: str

    # Capital

    initial_capital: float

    risk_per_trade: float

    leverage: float

    # Costs

    commission: float

    slippage: float