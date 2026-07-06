from dataclasses import dataclass


@dataclass(slots=True)
class StrategyProfile:
    name: str

    reliability: float = 1.0

    win_rate: float = 0.50

    average_rr: float = 1.0

    total_trades: int = 0

    enabled: bool = True
