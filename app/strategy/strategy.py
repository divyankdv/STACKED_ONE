"""
============================================================

                    STACKED ONE

                STRATEGY INTERFACE

------------------------------------------------------------

Every trading strategy must implement this interface.

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.pipeline.decision_pipeline import DecisionPipeline
from app.risk.trade_plan import TradePlan


class Strategy(ABC):
    """
    Base interface for all trading strategies.
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def evaluate(
        self,
        pipeline: DecisionPipeline,
    ) -> TradePlan | None:
        """
        Returns a TradePlan if a trade should be taken.

        Returns None if no trade exists.
        """
        ...
