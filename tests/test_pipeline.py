import os
import sys

# ------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ------------------------------------------------------

from datetime import datetime, timedelta

from app.data.tick_engine import TickEngine
from app.models.tick import Tick


def main():

    print("=" * 60)
    print("STACKED QUANT AI V6")
    print("PIPELINE TEST")
    print("=" * 60)

    engine = TickEngine()

    base = datetime.now().replace(
        second=0,
        microsecond=0,
    )

    ticks = [

        Tick(
            timestamp=base,
            price=100,
            volume=1,
            side="buy",
        ),

        Tick(
            timestamp=base + timedelta(seconds=10),
            price=102,
            volume=2,
            side="buy",
        ),

        Tick(
            timestamp=base + timedelta(seconds=20),
            price=99,
            volume=1,
            side="sell",
        ),

        Tick(
            timestamp=base + timedelta(minutes=1),
            price=101,
            volume=3,
            side="buy",
        ),

    ]

    completed = None

    for tick in ticks:

        completed = engine.update(tick)

    print()

    if completed:

        print("✅ Candle Closed")

        print()

        print(completed)

    else:

        print("❌ No completed candle")

    print("=" * 60)


if __name__ == "__main__":

    main()