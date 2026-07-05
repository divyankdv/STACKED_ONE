"""
============================================================

                    STACKED ONE

                 REPLAY MODELS

------------------------------------------------------------

Core replay models used throughout the replay engine.

Contains

✓ ReplayState
✓ ReplaySpeed
✓ ReplaySession
✓ ReplayStatistics

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# ============================================================
# Replay State
# ============================================================


class ReplayState(Enum):
    IDLE = "idle"

    LOADED = "loaded"

    PLAYING = "playing"

    PAUSED = "paused"

    STOPPED = "stopped"

    FINISHED = "finished"


# ============================================================
# Replay Speed
# ============================================================


class ReplaySpeed(Enum):
    REALTIME = 1

    X2 = 2

    X5 = 5

    X10 = 10

    X20 = 20

    X50 = 50

    X100 = 100

    MAX = 0


# ============================================================
# Replay Session
# ============================================================


@dataclass(slots=True)
class ReplaySession:
    symbol: str

    timeframe: str

    start: datetime

    end: datetime

    current: datetime

    state: ReplayState = ReplayState.IDLE

    speed: ReplaySpeed = ReplaySpeed.REALTIME

    @property
    def duration_seconds(self) -> float:

        return (self.end - self.start).total_seconds()

    @property
    def elapsed_seconds(self) -> float:

        return (self.current - self.start).total_seconds()

    @property
    def remaining_seconds(self) -> float:

        return max(
            0.0,
            (self.end - self.current).total_seconds(),
        )

    @property
    def progress(self) -> float:

        duration = self.duration_seconds

        if duration <= 0:
            return 1.0

        return min(
            self.elapsed_seconds / duration,
            1.0,
        )

    @property
    def finished(self) -> bool:

        return self.current >= self.end


# ============================================================
# Replay Statistics
# ============================================================


@dataclass(slots=True)
class ReplayStatistics:
    processed_ticks: int = 0

    processed_candles: int = 0

    elapsed_wall_time: float = 0.0

    elapsed_market_time: float = 0.0

    replay_speed: float = 1.0

    remaining_seconds: float = 0.0

    @property
    def wall_time(self) -> timedelta:

        return timedelta(
            seconds=self.elapsed_wall_time,
        )

    @property
    def market_time(self) -> timedelta:

        return timedelta(
            seconds=self.elapsed_market_time,
        )

    @property
    def eta(self) -> timedelta:

        return timedelta(
            seconds=self.remaining_seconds,
        )

    def reset(self) -> None:

        self.processed_ticks = 0

        self.processed_candles = 0

        self.elapsed_wall_time = 0.0

        self.elapsed_market_time = 0.0

        self.replay_speed = 1.0

        self.remaining_seconds = 0.0
