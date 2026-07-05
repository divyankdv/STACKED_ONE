"""
============================================================

                    STACKED ONE

                  REPLAY ENGINE

------------------------------------------------------------

Coordinates historical replay.

Responsibilities

✓ Load replay data
✓ Play
✓ Pause
✓ Resume
✓ Stop
✓ Feed replay sink

============================================================
"""

from __future__ import annotations

from datetime import datetime

from app.replay.replay_clock import ReplayClock
from app.replay.replay_models import (
    ReplaySession,
    ReplaySpeed,
    ReplayState,
)
from app.replay.replay_provider import ReplayProvider
from app.replay.replay_sink import ReplaySink


class ReplayEngine:
    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        provider: ReplayProvider,
        sink: ReplaySink,
    ) -> None:

        self.provider = provider

        self.sink = sink

        self.clock = ReplayClock()

        self.session: ReplaySession | None = None

    # =====================================================
    # Load
    # =====================================================

    def load(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> None:

        self.provider.load(
            symbol,
            start,
            end,
        )

        self.session = ReplaySession(
            symbol=symbol,
            timeframe=timeframe,
            start=start,
            end=end,
            current=start,
            state=ReplayState.LOADED,
        )

    # =====================================================
    # Play
    # =====================================================

    async def play(
        self,
    ) -> None:

        if self.session is None:
            raise RuntimeError("Replay session has not been loaded.")

        self.session.state = ReplayState.PLAYING

        self.clock.play()

        for tick in self.provider:
            if self.session.state == ReplayState.STOPPED:
                break

            await self.clock.wait(
                tick.timestamp,
            )

            self.session.current = tick.timestamp

            self.sink.consume(
                tick,
            )

        self.session.state = ReplayState.FINISHED

    # =====================================================
    # Pause
    # =====================================================

    def pause(
        self,
    ) -> None:

        if self.session is None:
            return

        self.session.state = ReplayState.PAUSED

        self.clock.pause()

    # =====================================================
    # Resume
    # =====================================================

    def resume(
        self,
    ) -> None:

        if self.session is None:
            return

        self.session.state = ReplayState.PLAYING

        self.clock.play()

    # =====================================================
    # Stop
    # =====================================================

    def stop(
        self,
    ) -> None:

        if self.session is None:
            return

        self.session.state = ReplayState.STOPPED

        self.clock.stop()

        self.provider.reset()

    # =====================================================
    # Speed
    # =====================================================

    def set_speed(
        self,
        speed: ReplaySpeed,
    ) -> None:

        self.clock.set_speed(
            speed,
        )

        if self.session is not None:
            self.session.speed = speed

    # =====================================================
    # Status
    # =====================================================

    @property
    def loaded(
        self,
    ) -> bool:

        return self.session is not None

    @property
    def playing(
        self,
    ) -> bool:

        return self.session is not None and self.session.state == ReplayState.PLAYING

    # =====================================================
    # String
    # =====================================================

    def __str__(
        self,
    ) -> str:

        state = self.session.state.value if self.session else "idle"

        return f"ReplayEngine(state={state})"

    __repr__ = __str__
