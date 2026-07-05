"""
============================================================

                    STACKED ONE

                WEBSOCKET MANAGER

------------------------------------------------------------

Responsibilities

✓ Connect
✓ Subscribe
✓ Listen
✓ Route Messages
✓ Feed Market Pipeline
✓ Reconnect

Never parses exchange JSON.

============================================================
"""

from __future__ import annotations

import asyncio

from app.config.settings import settings
from app.exchange.clients.delta_websocket_client import DeltaWebSocketClient
from app.exchange.managers.message_router import MessageRouter
from app.exchange.protocol.connection_state import ConnectionState
from app.exchange.protocol.delta_channels import DeltaChannel
from app.exchange.protocol.delta_subscription import DeltaSubscription
from app.logger import logger
from app.pipeline.market_pipeline import MarketPipeline


class WebSocketManager:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        client: DeltaWebSocketClient,

        router: MessageRouter,

        pipeline: MarketPipeline,

    ):

        self.client = client

        self.router = router

        self.pipeline = pipeline

        self.running = False

        self.state = ConnectionState.DISCONNECTED

    # =====================================================
    # Set Connection State
    # =====================================================

    def set_state(

        self,

        state: ConnectionState,

    ):

        if self.state == state:

            return

        self.state = state

        logger.info(

            f"Connection State -> "

            f"{state.value.upper()}"

        )

    # =====================================================
    # Start
    # =====================================================

    async def start(self):

        self.running = True

        self.set_state(

            ConnectionState.CONNECTING

        )

        await self.client.connect()
        self.set_state(

            ConnectionState.CONNECTED

        )

        await self.subscribe()

        asyncio.create_task(

            self.run()

        )

    # =====================================================
    # Connect
    # =====================================================

    async def connect(self):

        await self.client.connect()

        self.set_state(ConnectionState.CONNECTED)

        logger.info(

            "Connected to Delta WebSocket."

        )

    # =====================================================
    # Subscribe
    # =====================================================

    async def subscribe(self):

        subscriptions = [

            DeltaSubscription(

                channel=DeltaChannel.TRADES,

                symbols=[

                    settings.symbol

                ],

            ),

        ]

        await self.client.subscribe(

            subscriptions

        )

        logger.info(

            f"Subscribed to {settings.symbol}"

        )

            # =====================================================
            # Main Event Loop
            # =====================================================

async def run(self):

    while self.running:

        try:

            async for message in self.client.listen():

                #
                # Route incoming message
                #

                events = self.router.route(message)

                if not events:
                    continue

                #
                # Process routed events
                #

                for event in events:

                    tick = event.to_tick()

                    completed = self.pipeline.process_tick(
                        tick
                    )

                    if completed:

                        candle = completed.get("1m")

                        if candle is None:
                            continue

                        logger.info(

                            f"1m Candle Closed | "
                            f"O:{candle.open} "
                            f"H:{candle.high} "
                            f"L:{candle.low} "
                            f"C:{candle.close} "
                            f"V:{candle.volume}"

                        )

        except asyncio.CancelledError:

            logger.info(

                "WebSocket Manager Cancelled."

            )

            break

        except Exception as e:

            logger.exception(e)

            self.set_state(ConnectionState.DISCONNECTED)

            await self.reconnect()

    # =====================================================
    # Reconnect
    # =====================================================

    async def reconnect(self):

        self.set_state(

            ConnectionState.RECONNECTING

        )

        await self.client.connect()

        self.set_state(

            ConnectionState.CONNECTED

        )

        await self.subscribe()

    # =====================================================
    # Stop
    # =====================================================

    async def stop(self):

        logger.info(

            "Stopping WebSocket Manager..."

        )

        self.set_state(

            ConnectionState.STOPPING

        )

        self.running = False

        await self.client.disconnect()

        self.set_state(

            ConnectionState.STOPPED

        )

        logger.info(

            "WebSocket Manager Stopped."

        )
    

    # =====================================================
    # Status
    # =====================================================

    @property
    def status(self):

        return {

            "running": self.running,

            "connected": self.connected,

            "symbol": settings.symbol,

        }

    # =====================================================
    # Is Running
    # =====================================================

    @property
    def is_running(self):

        return self.running

    # =====================================================
    # Context Manager
    # =====================================================

    async def __aenter__(self):

        await self.start()

        return self

    async def __aexit__(

        self,

        exc_type,

        exc,

        tb,

    ):

        await self.stop()

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self):

        return (

            "WebSocketManager("

            f"running={self.running}, "

            f"connected={self.connected}, "

            f"symbol='{settings.symbol}')"

        )