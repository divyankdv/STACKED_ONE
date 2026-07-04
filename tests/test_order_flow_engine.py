"""
============================================================

        TEST ORDER FLOW ENGINE

============================================================
"""

from app.analytics.order_flow_engine import OrderFlowEngine
from app.exchange.protocol.trade_message import TradeMessage


def make_trade(

    side: str,

    price: float,

    size: float,

):

    if side == "buy":

        buyer = "taker"
        seller = "maker"

    else:

        buyer = "maker"
        seller = "taker"

    return TradeMessage.from_delta(

        {

            "symbol": "BTCUSD",

            "product_id": 27,

            "price": price,

            "size": size,

            "buyer_role": buyer,

            "seller_role": seller,

            "timestamp": 1782918453777950,

        }

    )


def main():

    engine = OrderFlowEngine()

    engine.update_trade(

        make_trade(

            "buy",

            100,

            10,

        )

    )

    engine.update_trade(

        make_trade(

            "sell",

            101,

            5,

        )

    )

    engine.update_trade(

        make_trade(

            "buy",

            102,

            20,

        )

    )

    engine.update_trade(

        make_trade(

            "buy",

            103,

            15,

        )

    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    assert snapshot.buy_volume == 45

    assert snapshot.sell_volume == 5

    assert snapshot.delta == 40

    assert snapshot.cvd == 40

    assert snapshot.trade_count == 4

    assert snapshot.buy_trades == 3

    assert snapshot.sell_trades == 1

    assert snapshot.largest_trade == 20

    print("✓ ALL TESTS PASSED")


if __name__ == "__main__":

    main()