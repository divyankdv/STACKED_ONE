"""
============================================================

                    STACKED ONE

             Quant Intelligence Platform

                  Powered by SQOS®

         STACKED Quant Operating System

------------------------------------------------------------

Official Application Entry Point

Startup Sequence

    ✓ Load Settings
    ✓ Initialize Application
    ✓ Connect Delta REST
    ✓ Discover Product
    ✓ Load Historical Data
    ✓ Warm Market Pipeline
    ✓ Ready for Live Market

============================================================
"""

from app.config.settings import settings
from app.core.application import Application
from app.exchange.clients.delta_rest_client import DeltaRestClient
from app.exchange.history_loader import HistoryLoader


# ==========================================================
# Banner
# ==========================================================

def print_banner():

    print()

    print("=" * 70)
    print()
    print("                 STACKED ONE")
    print()
    print("          Quant Intelligence Platform")
    print()
    print("             Powered by SQOS®")
    print()
    print("      STACKED Quant Operating System")
    print()
    print("=" * 70)
    print()


# ==========================================================
# Main
# ==========================================================

def main():

    print_banner()

    print("Initializing Platform...")
    print()

    # ------------------------------------------------------
    # Application
    # ------------------------------------------------------

    app = Application()

    print("✓ Application Initialized")

    # ------------------------------------------------------
    # Delta REST
    # ------------------------------------------------------

    app = Application()

    client = app.delta_rest_client

    print("Connecting to Delta Exchange...")

    try:

        product = client.get_product(settings.symbol)

    except Exception as e:

        print()

        print("❌ Unable to connect to Delta Exchange")

        print(e)

        client.close()

        return

    if product is None:

        print()

        print(f"❌ Product '{settings.symbol}' not found.")

        client.close()

        return

    print("✓ Delta REST Connected")
    print(f"✓ Product Loaded : {product.symbol}")
    print(f"✓ Product ID     : {product.id}")
    print(f"✓ Tick Size      : {product.tick_size}")

    # ------------------------------------------------------
    # History Loader
    # ------------------------------------------------------

    loader = HistoryLoader(

        client,

        app.market_pipeline,

    )

    loaded = loader.load(

        hours=24,

        resolution="1m",

    )

    print(f"✓ History Loaded : {loaded} candles")

    loader.summary()

    print("✓ Market Pipeline Warmed")

    # ------------------------------------------------------
    # Ready
    # ------------------------------------------------------

    print()

    print("=" * 70)
    print("🚀 STACKED ONE IS READY")
    print("=" * 70)

    print()

    print("Current Instrument")

    print(f"  Symbol      : {product.symbol}")
    print(f"  Product ID  : {product.id}")
    print(f"  Tick Size   : {product.tick_size}")
    print(f"  Contract    : {product.contract_type}")
    print(f"  Leverage    : {product.default_leverage}x")

    print()

    print("Status")

    print("  REST        : Connected")
    print("  History     : Loaded")
    print("  Pipeline    : Warm")
    print("  WebSocket   : Pending")

    print()

    print("Next Stage")

    print("  Live Delta WebSocket")

    print()

    client.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    main()