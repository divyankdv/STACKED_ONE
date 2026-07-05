"""
============================================================

                    STACKED ONE

                  REPLAY CLOCK

------------------------------------------------------------

Controls replay timing.

Responsibilities

✓ Realtime replay
✓ Variable replay speed
✓ Pause
✓ Resume
✓ Stop

============================================================
"""

from __future__ import annotations

import asyncio
from datetime import datetime

from app.replay.replay_models import (
    ReplaySpeed,
    ReplayState,
)


class ReplayClock:
    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
    ) -> None:

        self.speed = ReplaySpeed.REALTIME

        self.state = ReplayState.IDLE

        self._previous_timestamp: datetime | None = None

    # =====================================================
    # Speed
    # =====================================================

    def set_speed(
        self,
        speed: ReplaySpeed,
    ) -> None:

        self.speed = speed

    # =====================================================
    # State
    # =====================================================

    def play(
        self,
    ) -> None:

        self.state = ReplayState.PLAYING

    def pause(
        self,
    ) -> None:

        self.state = ReplayState.PAUSED

    def stop(
        self,
    ) -> None:

        self.state = ReplayState.STOPPED

        self._previous_timestamp = None

    # =====================================================
    # Wait
    # =====================================================

    async def wait(
        self,
        timestamp: datetime,
    ) -> None:

        #
        # MAX = no waiting
        #

        if self.speed == ReplaySpeed.MAX:
            self._previous_timestamp = timestamp

            return

        #
        # First tick
        #

        if self._previous_timestamp is None:
            self._previous_timestamp = timestamp

            return

        #
        # Pause
        #

        while self.state == ReplayState.PAUSED:
            await asyncio.sleep(
                0.1,
            )

        #
        # Stop
        #

        if self.state == ReplayState.STOPPED:
            return

        #
        # Calculate delay
        #

        delay = (timestamp - self._previous_timestamp).total_seconds()

        self._previous_timestamp = timestamp

        if delay <= 0:
            return

        multiplier = self.speed.value

        await asyncio.sleep(
            delay / multiplier,
        )
