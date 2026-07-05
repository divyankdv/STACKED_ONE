"""
============================================================

                    STACKED ONE

         Delta Exchange REST Client

------------------------------------------------------------

Responsibilities

✓ Maintain HTTP Session
✓ Generic GET Requests
✓ Download Products
✓ Cache Products
✓ Product Lookup
✓ Product ID Lookup
✓ Historical Candles

============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast

import requests

from app.config.settings import settings
from app.logger import logger
from app.models.candle import Candle
from app.models.product import Product


class DeltaRestClient:

    """
    Delta Exchange REST API Client
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.base_url = settings.rest_url.rstrip("/")

        self.timeout = 15

        self.session = requests.Session()

        self.session.headers.update({

            "Accept": "application/json",

            "User-Agent": "STACKED ONE / SQOS"

        })

        self._products: list[dict[str, Any]] | None = None

    # =====================================================
    # Generic GET
    # =====================================================

    def get(

        self,

        endpoint: str,

        params: dict | None = None,

    ) -> dict[str, Any]:

        url = f"{self.base_url}{endpoint}"

        logger.info(f"GET {url}")

        try:

            response = self.session.get(

                url,

                params=params,

                timeout=self.timeout,

            )

            response.raise_for_status()

            return cast(dict[str, Any], response.json())

        except requests.Timeout:

            logger.error("REST request timed out.")

            raise

        except requests.ConnectionError:

            logger.error("Unable to connect to Delta.")

            raise

        except requests.HTTPError as e:

            logger.error(f"HTTP Error : {e}")

            raise

        except Exception as e:

            logger.exception(e)

            raise

    # =====================================================
    # Products
    # =====================================================

    def get_products(self) -> list[dict[str, Any]]:

        """
        Download every exchange product.

        Uses memory cache.
        """

        if self._products is not None:

            return self._products

        data = self.get(

            "/v2/products"

        )

        self._products = cast(
            list[dict[str, Any]],
            data.get(
                "result",
                [],
            ),
        )

        logger.info(

            f"Loaded {len(self._products)} products"

        )

        return self._products

    # =====================================================
    # Single Product
    # =====================================================

    def get_product(

        self,

        symbol: str,

    ) -> Product | None:

        symbol = symbol.upper()

        for item in self.get_products():

            if item.get(

                "symbol",

                ""

            ).upper() == symbol:

                product = Product.from_delta(

                    item

                )

                logger.info(

                    f"Loaded Product {product.symbol}"

                )

            return product

        logger.warning(

            f"{symbol} not found."

        )

        return None

    # =====================================================
    # Product ID
    # =====================================================

    def get_product_id(

        self,

        symbol: str,

    ) -> int | None:

        product = self.get_product(

            symbol

        )

        if product is None:

            return None

        return product.id
        # =====================================================
    # Historical Candles
    # =====================================================

    def get_history(

        self,

        symbol: str,

        resolution: str,

        start: datetime,

        end: datetime,

    ) -> list[Candle]:

        """
        Download historical candles.

        Parameters
        ----------
        symbol
            Example: BTCUSD

        resolution
            1m, 5m, 15m, 1h, 4h, 1d

        start
            UTC datetime

        end
            UTC datetime

        Returns
        -------
        list[Candle]
        """

        params = {

            "symbol": symbol,

            "resolution": resolution,

            "start": int(start.timestamp()),

            "end": int(end.timestamp()),

        }

        logger.info(

            f"Downloading {resolution} history for {symbol}"

        )

        data = self.get(

            "/v2/history/candles",

            params=params,

        )

        rows = data.get(

            "result",

            [],

        )

        candles = []

        # -------------------------------------------------
        # Delta returns newest -> oldest.
        # Convert to oldest -> newest.
        # -------------------------------------------------

        for row in reversed(rows):

            candle = Candle(

                time=datetime.fromtimestamp(

                    row["time"],

                    tz=UTC,

                ),

                open=float(

                    row["open"]

                ),

                high=float(

                    row["high"]

                ),

                low=float(

                    row["low"]

                ),

                close=float(

                    row["close"]

                ),

                volume=float(

                    row["volume"]

                ),

                buy_volume=0.0,

                sell_volume=0.0,

                delta=0.0,

                trades=0,

            )

            candles.append(

                candle

            )

        logger.info(

            f"Downloaded {len(candles)} candles."

        )

        return candles

    # =====================================================
    # Product Cache Status
    # =====================================================

    @property

    def products_loaded(

        self,

    ) -> bool:

        return self._products is not None

    # =====================================================
    # Clear Product Cache
    # =====================================================

    def clear_cache(

        self,

    ):

        self._products = None

        logger.info(

            "Product cache cleared."

        )

    # =====================================================
    # Close Session
    # =====================================================

    def close(

        self,

    ):

        self.session.close()

        logger.info(

            "Delta REST Session Closed."

        )