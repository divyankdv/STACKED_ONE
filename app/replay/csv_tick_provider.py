"""
============================================================

                    STACKED ONE

                CSV TICK PROVIDER

------------------------------------------------------------

Loads historical tick data from CSV.

CSV Format

timestamp,price,volume,side

Example

2026-01-01T09:15:00,3512.5,0.42,buy

============================================================
"""

from __future__ import annotations

import csv
from datetime import datetime

from app.models.tick import Tick
from app.replay.replay_provider import ReplayProvider


class CSVTickProvider(ReplayProvider):
    """
    ReplayProvider backed by a CSV file.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        csv_path: str,
    ) -> None:

        self.csv_path = csv_path

        self._ticks: list[Tick] = []

        self._index = 0

    # =====================================================
    # Load
    # =====================================================

    def load(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
    ) -> None:

        #
        # Symbol is ignored because each CSV
        # represents one instrument.
        #

        self._ticks.clear()

        self._index = 0

        with open(
            self.csv_path,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                timestamp = datetime.fromisoformat(
                    row["timestamp"],
                )

                if timestamp < start:
                    continue

                if timestamp > end:
                    break

                self._ticks.append(
                    Tick(
                        timestamp=timestamp,
                        price=float(row["price"]),
                        volume=float(row["volume"]),
                        side=row["side"].lower(),
                    )
                )

    # =====================================================
    # Iterator
    # =====================================================

    def __iter__(self):

        self._index = 0

        return self

    def __next__(self):

        if self._index >= len(self._ticks):
            raise StopIteration

        tick = self._ticks[self._index]

        self._index += 1

        return tick

    # =====================================================
    # Length
    # =====================================================

    def __len__(self):

        return len(self._ticks)

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self._index = 0

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def empty(self):

        return len(self._ticks) == 0

    @property
    def count(self):

        return len(self._ticks)

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return f"CSVTickProvider(ticks={len(self)})"

    __repr__ = __str__
