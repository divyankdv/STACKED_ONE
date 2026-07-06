"""
============================================================

                    STACKED ONE

                DATA SOURCES

------------------------------------------------------------

Locates or generates the tick datasets the terminal replays.

Bundled sample datasets are generated once and cached under
data/samples/ so a freshly cloned repository can run a
backtest immediately, with no external data file required.

============================================================
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "samples"

SAMPLE_DAYS = 2

SAMPLE_SEED = 42


@dataclass(frozen=True)
class Dataset:
    symbol: str
    path: Path
    start: datetime
    end: datetime
    tick_count: int
    is_sample: bool


# ==========================================================
# Sample Generation
# ==========================================================


def _base_price(symbol: str) -> float:

    upper = symbol.upper()

    if "BTC" in upper:
        return 50_000.0

    if "ETH" in upper:
        return 3_000.0

    return 100.0


def _generate_sample(symbol: str, path: Path) -> None:

    rng = random.Random(SAMPLE_SEED)

    start = datetime(2026, 1, 1)

    end = start + timedelta(days=SAMPLE_DAYS)

    price = _base_price(symbol)

    timestamp = start

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(["timestamp", "price", "volume", "side"])

        while timestamp < end:

            drift = rng.gauss(0.0, 1.0) * (price * 0.0006)

            price = max(price + drift, 1.0)

            side = "buy" if rng.random() > 0.5 else "sell"

            volume = round(rng.uniform(0.01, 3.0), 4)

            writer.writerow(
                [
                    timestamp.isoformat(),
                    f"{price:.2f}",
                    volume,
                    side,
                ]
            )

            timestamp += timedelta(
                seconds=rng.uniform(1.0, 6.0),
            )


# ==========================================================
# Dataset Access
# ==========================================================


def sample_symbols() -> tuple[str, ...]:

    return ("BTCUSD", "ETHUSD")


def ensure_sample_dataset(symbol: str) -> Dataset:

    path = DATA_DIR / f"{symbol.upper()}_sample.csv"

    if not path.exists():

        _generate_sample(symbol, path)

    return describe_dataset(path, symbol=symbol, is_sample=True)


def describe_dataset(
    path: Path,
    symbol: str,
    is_sample: bool = False,
) -> Dataset:

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    if not rows:
        raise ValueError(f"Dataset '{path}' contains no rows.")

    start = datetime.fromisoformat(rows[0]["timestamp"])

    end = datetime.fromisoformat(rows[-1]["timestamp"])

    return Dataset(
        symbol=symbol,
        path=path,
        start=start,
        end=end,
        tick_count=len(rows),
        is_sample=is_sample,
    )


def custom_dataset(path_str: str, symbol: str) -> Dataset:

    path = Path(path_str).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")

    return describe_dataset(path, symbol=symbol, is_sample=False)
