from app.exchange.protocol.trade_message import TradeMessage


sample = {

    "type": "all_trades",

    "symbol": "BTCUSD",

    "product_id": 27,

    "price": "59919.0",

    "size": 15,

    "timestamp": 1782918453777950,

    "buyer_role": "taker",

    "seller_role": "maker",

}


trade = TradeMessage.from_delta(sample)

print("=" * 60)

print(trade)

print()

tick = trade.to_tick()

print(tick)

print("=" * 60)