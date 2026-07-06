"""
============================================================

                    STACKED ONE

                CSV DATA SOURCE

------------------------------------------------------------

Production-grade CSV market data source.

Features
--------
✓ Lazy iteration
✓ Reset support
✓ Progress tracking
✓ Configurable column mapping
✓ ISO timestamp support
✓ Custom timestamp format
✓ Graceful optional fields
✓ Validation

============================================================
"""

from __future__ import annotations

import csv
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from app.simulator.market_data_source import MarketDataSource
from app.simulator.market_event import MarketEvent


class CSVDataSource(MarketDataSource):
    """
    CSV implementation of MarketDataSource.

    Example CSV

    trade_id,exchange,timestamp,price,volume,is_buyer_maker,bid,ask,bid_size,ask_size,sequence
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        csv_file: str | Path,
        symbol: str = "BTCUSD",
        *,
        timestamp_column: str = "timestamp",
        price_column: str = "price",
        quantity_column: str = "volume",
        trade_id_column: str = "trade_id",
        exchange_column: str = "exchange",
        aggressor_column: str = "is_buyer_maker",
        bid_column: str = "bid",
        ask_column: str = "ask",
        bid_size_column: str = "bid_size",
        ask_size_column: str = "ask_size",
        sequence_column: str = "sequence",
        timestamp_format: str | None = None,
    ):

        self.csv_file = Path(csv_file)

        if not self.csv_file.exists():
            raise FileNotFoundError(self.csv_file)

        self.symbol = symbol

        self.timestamp_column = timestamp_column
        self.price_column = price_column
        self.quantity_column = quantity_column

        self.trade_id_column = trade_id_column
        self.exchange_column = exchange_column
        self.aggressor_column = aggressor_column

        self.bid_column = bid_column
        self.ask_column = ask_column

        self.bid_size_column = bid_size_column
        self.ask_size_column = ask_size_column

        self.sequence_column = sequence_column

        self.timestamp_format = timestamp_format

        self._rows: list[dict[str, str]] = []

        self._index = 0

        self._load()

    # =====================================================
    # Load
    # =====================================================

    def _load(self) -> None:

        self._rows.clear()

        with self.csv_file.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as f:
            reader = csv.DictReader(f)

            required = {
                self.timestamp_column,
                self.price_column,
                self.quantity_column,
            }

            missing = required.difference(reader.fieldnames or [])

            if missing:
                raise ValueError(f"CSV missing required columns: {sorted(missing)}")

            for row in reader:
                self._rows.append(row)

    # =====================================================
    # Iterator
    # =====================================================

    def __iter__(self) -> Iterator[MarketEvent]:

        self._index = 0

        while self._index < len(self._rows):
            row = self._rows[self._index]

            self._index += 1

            yield self._row_to_event(row)

    # =====================================================
    # Row Conversion
    # =====================================================

    def _row_to_event(
        self,
        row: dict[str, str],
    ) -> MarketEvent:

        timestamp = self._parse_timestamp(row[self.timestamp_column])

        price = self._float(row.get(self.price_column))

        quantity = self._float(row.get(self.quantity_column))

        bid = self._float(
            row.get(self.bid_column),
            default=price,
        )

        ask = self._float(
            row.get(self.ask_column),
            default=price,
        )

        bid_size = self._float(
            row.get(self.bid_size_column),
            default=0.0,
        )

        ask_size = self._float(
            row.get(self.ask_size_column),
            default=0.0,
        )

        sequence = self._int(
            row.get(self.sequence_column),
            default=0,
        )

        aggressor = self._parse_bool(row.get(self.aggressor_column))

        return MarketEvent(
            trade_id=row.get(
                self.trade_id_column,
                "",
            ),
            exchange=row.get(
                self.exchange_column,
                "UNKNOWN",
            ),
            symbol=self.symbol,
            timestamp=timestamp,
            price=price,
            quantity=quantity,
            is_buyer_maker=aggressor,
            bid=bid,
            ask=ask,
            bid_size=bid_size,
            ask_size=ask_size,
            sequence=sequence,
        )

    # =====================================================
    # Parsing Helpers
    # =====================================================

    def _parse_timestamp(
        self,
        value: str,
    ) -> datetime:

        if self.timestamp_format:
            return datetime.strptime(
                value,
                self.timestamp_format,
            )

        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    @staticmethod
    def _float(
        value,
        default: float = 0.0,
    ) -> float:

        if value in (None, ""):
            return default

        return float(value)

    @staticmethod
    def _int(
        value,
        default: int = 0,
    ) -> int:

        if value in (None, ""):
            return default

        return int(value)

    @staticmethod
    def _parse_bool(
        value,
    ) -> bool | None:

        if value is None:
            return None

        value = value.strip().lower()

        if value in ("true", "1", "yes"):
            return True

        if value in ("false", "0", "no"):
            return False

        return None

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:

        self._index = 0

    # =====================================================
    # Properties
    # =====================================================

    @property
    def finished(self) -> bool:

        return self._index >= len(self._rows)

    @property
    def event_count(self) -> int:

        return len(self._rows)

    @property
    def current_index(self) -> int:

        return self._index

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def file_name(self) -> str:

        return self.csv_file.name

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return f"CSVDataSource(file='{self.file_name}', events={self.event_count})"

    __repr__ = __str__
