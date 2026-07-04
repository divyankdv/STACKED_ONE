"""
============================================================

                    STACKED ONE

              CONTAINER BUILDER

------------------------------------------------------------

Builds and wires all application services.

============================================================
"""

from __future__ import annotations

from app.application.dependency_container import DependencyContainer

from app.core.events.event_bus import EventBus

from app.pipeline.market_pipeline import MarketPipeline
from app.pipeline.decision_pipeline import DecisionPipeline

from app.execution.execution_engine import ExecutionEngine
from app.execution.paper_broker import PaperBroker

from app.risk.risk_engine import RiskEngine

from app.config.settings import settings


class ContainerBuilder:

    """
    Builds the dependency container.
    """

    def build(self) -> DependencyContainer:

        container = DependencyContainer()

        #
        # Core
        #

        event_bus = EventBus()

        broker = PaperBroker()

        risk = RiskEngine()

        execution = ExecutionEngine(

            broker=broker,

        )

        market_pipeline = MarketPipeline()

        decision_pipeline = DecisionPipeline()

        #
        # Register
        #

        container.register(

            "settings",

            settings,

        )

        container.register(

            "event_bus",

            event_bus,

        )

        container.register(

            "broker",

            broker,

        )

        container.register(

            "risk",

            risk,

        )

        container.register(

            "execution",

            execution,

        )

        container.register(

            "market_pipeline",

            market_pipeline,

        )

        container.register(

            "decision_pipeline",

            decision_pipeline,

        )

        return container