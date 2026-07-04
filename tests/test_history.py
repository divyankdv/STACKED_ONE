import os
import sys

from datetime import datetime, timedelta

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config.settings import settings
from app.exchange.clients.delta_rest_client import DeltaRestClient


def main():

    client = DeltaRestClient()

    print("=" * 60)
    print("HISTORY TEST")
    print("=" * 60)

    candles = client.get_history(

        symbol=settings.symbol,

        resolution="1m",

        start=datetime.utcnow() - timedelta(hours=6),

        end=datetime.utcnow(),

    )

    print()

    print(f"Candles Downloaded : {len(candles)}")

    if candles:

        print()

        print("First Candle")

        print(candles[0])

        print()

        print("Last Candle")

        print(candles[-1])

    client.close()


if __name__ == "__main__":

    main()