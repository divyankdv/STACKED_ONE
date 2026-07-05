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
from typing import Any

from app.config.settings import settings
from app.exchange.clients.delta_websocket_client import DeltaWebSocketClient
from app.exchange.managers.message_router import MessageRouter
from app.exchange.protocol.connection_state import ConnectionState
from app.exchange.protocol.delta_channels import DeltaChannel
from app.exchange.protocol.delta_subscription import DeltaSubscription
from app.logger import logger
from app.pipeline.market_pipeline import MarketPipeline


class WebSocketManager:
    """
    High-level manager for the Delta WebSocket client.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(
        self,
        client: DeltaWebSocketClient,
        router: MessageRouter,
        pipeline: MarketPipeline,
        decision_pipeline: DecisionPipeline,
    ) -> None:

        self.client = client
        self.router = router
        self.pipeline = pipeline
        self.decision_pipeline = decision_pipeline

        self.running = False
        self.state = ConnectionState.DISCONNECTED

    # =====================================================
    # Connection State
    # =====================================================

    def set_state(
        self,
        state: ConnectionState,
    ) -> None:

        if self.state == state:
            return

        self.state = state

        logger.info(
            f"Connection State -> {state.value.upper()}"
        )

    # =====================================================
    # Start
    # =====================================================

    async def start(self) -> None:

        self.running = True

        self.set_state(
            ConnectionState.CONNECTING,
        )

        await self.client.connect()

        self.set_state(
            ConnectionState.CONNECTED,
        )

        await self.subscribe()

        asyncio.create_task(
            self.run(),
        )

    # =====================================================
    # Connect
    # =====================================================

    async def connect(self) -> None:

        await self.client.connect()

        self.set_state(
            ConnectionState.CONNECTED,
        )

        logger.info(
            "Connected to Delta WebSocket."
        )

    # =====================================================
    # Subscribe
    # =====================================================

    async def subscribe(self) -> None:

        subscriptions = [
            DeltaSubscription(
                channel=DeltaChannel.TRADES,
                symbols=[
                    settings.symbol,
                ],
            ),
        ]

        await self.client.subscribe(
            subscriptions,
        )

        logger.info(
            f"Subscribed to {settings.symbol}"
        )

    # =====================================================
    # Main Event Loop
    # =====================================================

    async def run(self) -> None:

        while self.running:

            try:

                async for message in self.client.listen():

                    events = self.router.route(
                        message,
                    )

                    if not events:
                        continue

                    for event in events:

                        tick = event.to_tick()

                        completed = self.pipeline.process_tick(
                            tick,
                        )

                        if not completed:
                            continue

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

            except Exception as exc:

                logger.exception(exc)

                self.set_state(
                    ConnectionState.DISCONNECTED,
                )

                await self.reconnect()

    # =====================================================
    # Reconnect
    # =====================================================

    async def reconnect(self) -> None:

        self.set_state(
            ConnectionState.RECONNECTING,
        )

        await self.client.disconnect()

        await asyncio.sleep(
            settings.reconnect_delay,
        )

        await self.client.connect()

        self.set_state(
            ConnectionState.CONNECTED,
        )

        await self.subscribe()

    # =====================================================
    # Stop
    # =====================================================

    async def stop(self) -> None:

        logger.info(
            "Stopping WebSocket Manager..."
        )

        self.running = False

        self.set_state(
            ConnectionState.STOPPING,
        )

        await self.client.disconnect()

        self.set_state(
            ConnectionState.STOPPED,
        )

        logger.info(
            "WebSocket Manager Stopped."
        )

    # =====================================================
    # Status
    # =====================================================

    @property
    def status(self) -> dict[str, Any]:

        return {
            "running": self.running,
            "connected": self.client.is_connected,
            "state": self.state.value,
            "symbol": settings.symbol,
        }

    # =====================================================
    # Running
    # =====================================================

    @property
    def is_running(self) -> bool:

        return self.running

    # =====================================================
    # Context Manager
    # =====================================================

    async def __aenter__(self) -> WebSocketManager:

        await self.start()

        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        await self.stop()

    # =====================================================
    # String
    # =====================================================

    def __str__(self) -> str:

        return (
            "WebSocketManager("
            f"running={self.running}, "
            f"connected={self.client.is_connected}, "
            f"symbol='{settings.symbol}')"
        )

    __repr__ = __str__