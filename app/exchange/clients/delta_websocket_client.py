"""
============================================================

                    STACKED ONE

            DELTA WEBSOCKET CLIENT

------------------------------------------------------------

Responsibilities

✓ Connect
✓ Disconnect
✓ Send JSON
✓ Receive JSON

No business logic belongs here.

============================================================
"""

from __future__ import annotations

import asyncio
import json

import websockets
from websockets import WebSocketClientProtocol

from app.config.settings import settings
from app.exchange.protocol.delta_subscription import DeltaSubscription
from app.logger import logger


class DeltaWebSocketClient:

    """
    Low-level WebSocket client for Delta Exchange.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.url = settings.ws_url

        self.websocket: WebSocketClientProtocol | None = None

        self.connected = False

    # =====================================================
    # Connect
    # =====================================================

    async def connect(self):

        if self.connected:

            return

        logger.info(f"Connecting to {self.url}")

        self.websocket = await websockets.connect(

            self.url,

            ping_interval=settings.ping_interval,

            ping_timeout=settings.ping_timeout,

        )

        self.connected = True

        logger.info("Delta WebSocket Connected")

    # =====================================================
    # Disconnect
    # =====================================================

    async def disconnect(self):

        if self.websocket is None:

            return

        await self.websocket.close()

        self.websocket = None

        self.connected = False

        logger.info("Delta WebSocket Closed")

    # =====================================================
    # Send JSON
    # =====================================================

    async def send(

        self,

        payload: dict,

    ):

        if not self.connected:

            raise RuntimeError(

                "WebSocket is not connected."

            )

        await self.websocket.send(

            json.dumps(payload)

        )

    # =====================================================
    # Receive JSON
    # =====================================================

    async def receive(self):

        if not self.connected:

            raise RuntimeError(

                "WebSocket is not connected."

            )

        message = await self.websocket.recv()

        return json.loads(message)
    
    # =====================================================
    # Subscribe
    # =====================================================

    async def subscribe(

        self,

        subscriptions: list[DeltaSubscription],

    ):

        payload = {

            "type": "subscribe",

            "payload": {

                "channels": [

                    subscription.to_dict()

                    for subscription in subscriptions

                ]

            }

        }

        logger.info(

            "Subscribe Request"

        )

        logger.debug(payload)

        await self.send(payload)

    # =====================================================
    # Unsubscribe
    # =====================================================

    async def unsubscribe(

        self,

        subscriptions: list[DeltaSubscription],

    ):

        payload = {

            "type": "unsubscribe",

            "payload": {

                "channels": [

                    subscription.to_dict()

                    for subscription in subscriptions

                ]

            }

        }

        logger.info(

            "Unsubscribe Request"

        )

        logger.debug(payload)

        await self.send(payload)

    # =====================================================
    # Listen
    # =====================================================

    async def listen(self):

        """
        Infinite receive loop.

        Yields one decoded JSON message
        at a time.
        """

        while self.connected:

            try:

                message = await self.receive()

                yield message

            except websockets.ConnectionClosed as e:

                logger.warning(

                    f"WebSocket Closed | "
                    f"Code={e.code} "
                    f"Reason={e.reason}"

                )

                self.connected = False

                break

            except Exception:

                logger.exception(

                    "Unexpected error in listen()"

                )

                self.connected = False

                break

    # =====================================================
    # Reconnect
    # =====================================================

    async def reconnect(self):

        """
        Automatic reconnect.
        """

        logger.info(

            "Attempting reconnect..."

        )

        await self.disconnect()

        await asyncio.sleep(

            settings.reconnect_delay

        )

        await self.connect()

    # =====================================================
    # Connection Status
    # =====================================================

    @property
    def is_connected(self):

        return self.connected

    # =====================================================
    # Async Context Manager
    # =====================================================

    async def __aenter__(self):

        await self.connect()

        return self

    async def __aexit__(

        self,

        exc_type,

        exc,

        tb,

    ):

        await self.disconnect()

    # =====================================================
    # Ping
    # =====================================================

    async def ping(self):

        if not self.connected:

            return

        await self.websocket.ping()

    # =====================================================
    # Connection Info
    # =====================================================

    def __str__(self):

        return (

            f"DeltaWebSocketClient("
            f"connected={self.connected})"

        )

    __repr__ = __str__