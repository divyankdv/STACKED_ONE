from app.exchange.managers.message_router import MessageRouter

router = MessageRouter()

message = {

    "type": "all_trades",

    "symbol": "BTCUSD",

    "product_id": 27,

    "price": "60000",

    "size": 5,

    "timestamp": 1782918453777950,

    "buyer_role": "taker",

    "seller_role": "maker",

}

events = router.route(message)

print("=" * 60)

print(f"Events: {len(events)}")

for event in events:
    print(event)

print("=" * 60)