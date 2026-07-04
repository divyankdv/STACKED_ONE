"""
============================================================

                    STACKED ONE

                 ORDER RESULT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.execution.order import Order


@dataclass(slots=True)
class OrderResult:

    """
    Result returned by a Broker.
    """

    success: bool

    message: str

    order: Order | None = None

    def __bool__(self):

        return self.success

    def __str__(self):

        return (

            "OrderResult("

            f"{self.success}, "

            f"{self.message}"

            ")"

        )

    __repr__ = __str__