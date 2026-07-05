"""
============================================================

                STACKED QUANT AI V6

                PRODUCT TEST

------------------------------------------------------------

Tests:

✓ REST Connectivity
✓ Product Download
✓ Product Cache
✓ Product Lookup
✓ Product ID

Also prints the complete product JSON so that we
can inspect the Delta API schema.

============================================================
"""

import os
import sys
from pprint import pprint

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================================
# Imports
# ==========================================================

from app.config.settings import settings
from app.exchange.clients.delta_rest_client import DeltaRestClient

# ==========================================================
# Main
# ==========================================================

def main():

    client = DeltaRestClient()

    print()
    print("=" * 70)
    print("STACKED QUANT AI V6")
    print("DELTA PRODUCT TEST")
    print("=" * 70)

    # ------------------------------------------------------
    # Health Check
    # ------------------------------------------------------

    connected = client.health_check()

    print(f"\nREST Connected : {connected}")

    if not connected:

        print("\n❌ Unable to connect to Delta REST")

        return

    # ------------------------------------------------------
    # Products
    # ------------------------------------------------------

    products = client.get_products()

    print(f"\nTotal Products : {len(products)}")

    # ------------------------------------------------------
    # Lookup
    # ------------------------------------------------------

    product = client.get_product(settings.symbol)

    if product is None:

        print(f"\n❌ Product '{settings.symbol}' not found")

        return

    print("\n✅ Product Found")

    print("\nProduct ID :", client.get_product_id(settings.symbol))

    print("\n")

    print("=" * 70)
    print("COMPLETE PRODUCT JSON")
    print("=" * 70)

    pprint(product)

    print("\n")

    client.close()


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    main()