import asyncio

from app.pipeline.market_pipeline import MarketPipeline

from app.exchange.managers.message_router import MessageRouter

from app.exchange.clients.delta_websocket_client import DeltaWebSocketClient

from app.exchange.protocol.delta_channels import DeltaChannel
from app.exchange.protocol.delta_subscription import DeltaSubscription


pipeline = MarketPipeline()

router = MessageRouter()


async def main():

    client = DeltaWebSocketClient()

    await client.connect()

    await client.subscribe([

        DeltaSubscription(

            channel=DeltaChannel.TRADES,

            symbols=["BTCUSD"]

        )

    ])

    print("=" * 70)
    print("LIVE PIPELINE")
    print("=" * 70)

    async for message in client.listen():

        events = router.route(message)

        if not events:

            continue

        for trade in events:

            tick = trade.to_tick()

            completed = pipeline.process_tick(

                tick

            )

            if completed:

                candle = completed["1m"]

                print()

                print("=" * 60)

                print("1 Minute Candle Closed")

                print(candle)

                print("=" * 60)

    await client.disconnect()


asyncio.run(main())