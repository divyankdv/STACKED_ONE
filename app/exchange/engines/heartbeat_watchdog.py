"""
============================================================

                STACKED ONE

            HEARTBEAT WATCHDOG

------------------------------------------------------------

Monitors incoming market data.

Reconnects if feed becomes stale.

============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class HeartbeatWatchdog:

    def __init__(

        self,

        timeout_seconds: int = 20,

    ):

        self.timeout = timedelta(

            seconds=timeout_seconds

        )

        self.last_message = datetime.now(UTC)

    # =====================================================
    # Feed
    # =====================================================

    def beat(self):

        self.last_message = datetime.now(UTC)

    # =====================================================
    # Health
    # =====================================================

    @property
    def healthy(self):

        return (

            datetime.now(UTC)

            - self.last_message

        ) < self.timeout