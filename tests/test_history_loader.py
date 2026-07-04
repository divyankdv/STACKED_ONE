import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.exchange.clients.delta_rest_client import DeltaRestClient
from app.exchange.history_loader import HistoryLoader
from app.pipeline.market_pipeline import MarketPipeline


def main():

    print()
    print("=" * 60)
    print("STACKED QUANT AI V6")
    print("HISTORY LOADER TEST")
    print("=" * 60)

    client = DeltaRestClient()

    pipeline = MarketPipeline()

    loader = HistoryLoader(

        client,

        pipeline,

    )

    loaded = loader.load(

        hours=24,

        resolution="1m",

    )

    print()

    print(f"Loaded : {loaded}")

    print()

    loader.summary()

    client.close()


if __name__ == "__main__":

    main()