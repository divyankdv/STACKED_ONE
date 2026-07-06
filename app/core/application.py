"""
============================================================

                    STACKED ONE

            APPLICATION CONTAINER

------------------------------------------------------------

Creates every shared service exactly once.

============================================================
"""

# Exchange Clients
from app.exchange.clients.delta_rest_client import DeltaRestClient
from app.exchange.clients.delta_websocket_client import DeltaWebSocketClient
from app.exchange.engines.orderbook_engine import OrderBookEngine

# Exchange Engines
from app.exchange.engines.trade_engine import TradeEngine

# Exchange Managers
from app.exchange.managers.message_router import MessageRouter
from app.exchange.managers.websocket_manager import WebSocketManager
from app.exchange.market_data import market_data
from app.execution.execution_engine import ExecutionEngine
from app.performance.performance_manager import PerformanceManager
from app.pipeline.decision_pipeline import DecisionPipeline

# Data
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position_manager import PositionManager


class Application:
    def __init__(self):

        # ==================================================
        # Shared Market Data
        # ==================================================

        self.market_data = market_data

        # ==================================================
        # Exchange Clients
        # ==================================================

        self.delta_rest_client = DeltaRestClient()

        self.delta_websocket_client = DeltaWebSocketClient()

        # ==================================================
        # Exchange Managers
        # ==================================================

        self.message_router = MessageRouter()

        # ==================================================
        # Data Pipeline
        # ==================================================

        self.market_pipeline = MarketPipeline()

        # ==================================================
        # Decision Pipeline
        # ==================================================

        self.decision_pipeline = DecisionPipeline()

        # ==================================================
        # Execution
        # ==================================================

        self.execution_engine = ExecutionEngine()

        # ==================================================
        # Portfolio
        # ==================================================

        self.position_manager = PositionManager()

        # ==================================================
        # Performance
        # ==================================================

        self.performance_manager = PerformanceManager()

        # ==================================================
        # Exchange Engines
        # ==================================================

        self.trade_engine = TradeEngine()

        self.orderbook_engine = OrderBookEngine()

        # ==================================================
        # WebSocket Manager
        # ==================================================

        self.websocket_manager = WebSocketManager(

            client=self.delta_websocket_client,

            router=self.message_router,

            pipeline=self.market_pipeline,

        )

    # ==================================================
    # Reset
    # ==================================================

    async def shutdown(self):

        if self.websocket_manager.is_running:
            await self.websocket_manager.stop()

        self.delta_rest_client.close()
