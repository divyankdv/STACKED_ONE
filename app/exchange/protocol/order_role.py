"""
============================================================

                    STACKED ONE

                   ORDER ROLE

------------------------------------------------------------

Represents liquidity role in a trade.

============================================================
"""

from enum import StrEnum


class OrderRole(StrEnum):

    MAKER = "maker"

    TAKER = "taker"

    @property
    def is_maker(self) -> bool:

        return self == OrderRole.MAKER

    @property
    def is_taker(self) -> bool:

        return self == OrderRole.TAKER