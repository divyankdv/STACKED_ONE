"""
============================================================

                    STACKED ONE

                  RISK ENGINE

------------------------------------------------------------

Transforms a Confluence decision into an executable
TradePlan.

Responsibilities

✓ Validate trade
✓ Check account risk
✓ Calculate stop loss
✓ Calculate take profit
✓ Calculate position size
✓ Build TradePlan

============================================================
"""

from __future__ import annotations

from app.risk.position_size import PositionSize
from app.risk.risk_profile import RiskProfile
from app.risk.stop_loss import StopLoss
from app.risk.take_profit import TakeProfit
from app.risk.trade_plan import TradePlan
from app.strategy.signal_side import SignalSide


class RiskEngine:

    """
    Portfolio risk manager.
    """

    # =====================================================

    def __init__(

        self,

        profile: RiskProfile | None = None,

    ):

        self.profile = profile or RiskProfile()

        self.position_size = PositionSize(

            self.profile,

        )

        self.stop_loss = StopLoss()

        self.take_profit = TakeProfit()

    # =====================================================

    def evaluate(

        self,

        composite,

        strategy,

        confluence,

        entry_price: float,

    ) -> TradePlan:

        #
        # Trading Disabled
        #

        if not self.profile.trading_allowed:

            return self._reject(

                confluence,

                entry_price,

                "Trading disabled by Risk Profile",

            )

        #
        # Neutral
        #

        if confluence.side == SignalSide.NEUTRAL:

            return self._reject(

                confluence,

                entry_price,

                "Neutral confluence",

            )

        #
        # Low Confidence
        #

        if not confluence.trade_allowed:

            return self._reject(

                confluence,

                entry_price,

                "Insufficient confluence",

            )

        #
        # Stop
        #

        stop = self.stop_loss.calculate(

            confluence.side,

            entry_price,

        )

        #
        # Target
        #

        target = self.take_profit.calculate(

            confluence.side,

            entry_price,

            stop,

        )

        #
        # Position Size
        #

        size = self.position_size.calculate(

            entry_price,

            stop,

        )

        #
        # Exposure
        #

        exposure = self.position_size.exposure(

            size,

            entry_price,

        )

        #
        # Risk
        #

        risk_amount = self.position_size.monetary_risk(

            size,

            entry_price,

            stop,

        )

        reward_amount = abs(

            target -

            entry_price

        ) * size

        rr = self.take_profit.risk_reward(

            entry_price,

            stop,

            target,

        )

        #
        # Strategy Name
        #

        strategy_name = ""

        if strategy.best_signal is not None:

            strategy_name = strategy.best_signal.strategy

        #
        # Trade Plan
        #

        return TradePlan(

            approved=True,

            reasons=("Approved",),

            side=confluence.side,

            entry_price=entry_price,

            stop_price=stop,

            target_price=target,

            position_size=size,

            exposure=exposure,

            leverage=self.profile.leverage,

            risk_amount=risk_amount,

            reward_amount=reward_amount,

            risk_reward=rr,

            confidence=confluence.confidence,

            agreement=confluence.agreement,

            strategy=strategy_name,

            notes=(

                f"Grade={confluence.grade.value}",

            ),

        )

    # =====================================================

    def _reject(

        self,

        confluence,

        entry_price,

        reason,

    ) -> TradePlan:

        return TradePlan(

            approved=False,

            reasons=(reason,),

            side=confluence.side,

            entry_price=entry_price,

            stop_price=entry_price,

            target_price=entry_price,

            position_size=0.0,

            exposure=0.0,

            leverage=self.profile.leverage,

            risk_amount=0.0,

            reward_amount=0.0,

            risk_reward=0.0,

            confidence=confluence.confidence,

            agreement=confluence.agreement,

            strategy="",

            notes=(reason,),

        )

    # =====================================================

    def reset(self):

        self.profile.reset_session()

    # =====================================================

    def __str__(self):

        return (

            "RiskEngine("

            f"risk={self.profile.risk_per_trade:.2%}"

            ")"

        )

    __repr__ = __str__