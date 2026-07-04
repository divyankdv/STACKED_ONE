"""
============================================================

                    STACKED ONE

                STRATEGY PROFILE

------------------------------------------------------------

Tracks long-term performance statistics for one strategy.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StrategyProfile:

    #
    # Identity
    #

    name: str

    #
    # Reliability Weight
    #

    reliability: float = 1.0

    #
    # Performance
    #

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.50

    #
    # Risk Metrics
    #

    average_rr: float = 1.0

    profit_factor: float = 1.0

    max_drawdown: float = 0.0

    #
    # Money
    #

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    #
    # Status
    #

    enabled: bool = True

    # =====================================================
    # Update
    # =====================================================

    def record_trade(

        self,

        pnl: float,

        rr: float,

    ) -> None:

        self.total_trades += 1

        if pnl >= 0:

            self.winning_trades += 1

            self.gross_profit += pnl

        else:

            self.losing_trades += 1

            self.gross_loss += abs(pnl)

        self.net_profit = (

            self.gross_profit

            -

            self.gross_loss

        )

        self.win_rate = (

            self.winning_trades

            /

            self.total_trades

        )

        #
        # Running Average RR
        #

        previous = self.total_trades - 1

        self.average_rr = (

            (

                self.average_rr

                *

                previous

            )

            +

            rr

        ) / self.total_trades

        #
        # Profit Factor
        #

        if self.gross_loss > 0:

            self.profit_factor = (

                self.gross_profit

                /

                self.gross_loss

            )

        #
        # Reliability
        #

        self._update_reliability()

    # =====================================================
    # Reliability
    # =====================================================

    def _update_reliability(self):

        """
        Simple reliability model.

        Can later be replaced by Bayesian updating.
        """

        if self.total_trades < 20:

            self.reliability = 1.0

            return

        score = (

            0.5 * self.win_rate

            +

            0.3 * min(

                self.profit_factor,

                3.0,

            ) / 3.0

            +

            0.2 * min(

                self.average_rr,

                3.0,

            ) / 3.0

        )

        self.reliability = max(

            0.25,

            min(

                score,

                1.5,

            ),

        )

    # =====================================================

    def __str__(self):

        return (

            "StrategyProfile("

            f"{self.name}, "

            f"win_rate={self.win_rate:.2f}, "

            f"reliability={self.reliability:.2f}"

            ")"

        )

    __repr__ = __str__