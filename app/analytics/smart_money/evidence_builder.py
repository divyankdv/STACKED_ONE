"""
============================================================

                    STACKED ONE

          SMART MONEY EVIDENCE BUILDER

------------------------------------------------------------

Collects all base evidence for Smart Money.

Does NOT:

✓ Score
✓ Determine bias
✓ Apply synergy

============================================================
"""

from __future__ import annotations

from app.analytics.evidence import Evidence
from app.analytics.evidence_collection import EvidenceCollection
from app.config.settings import settings


class EvidenceBuilder:

    @staticmethod
    def build(context) -> EvidenceCollection:

        analytics = context.analytics
        liquidity = context.liquidity
        exhaustion = context.exhaustion

        evidence = EvidenceCollection()

        # =====================================================
        # Liquidity
        # =====================================================

        if liquidity.state == "HIGH":

            evidence.add(

                Evidence(

                    category="Liquidity",

                    description="High liquidity",

                    weight=settings.smart_money_liquidity_weight,

                    bullish=True,

                )

            )

        # =====================================================
        # Absorption
        # =====================================================

        if analytics.absorption.active:

            bullish = (

                analytics.absorption.bullish_score

                >=

                analytics.absorption.bearish_score

            )

            evidence.add(

                Evidence(

                    category="Absorption",

                    description="Absorption detected",

                    weight=settings.smart_money_absorption_weight,

                    bullish=bullish,

                )

            )

        # =====================================================
        # Iceberg
        # =====================================================

        if analytics.iceberg.active:

            bullish = (

                analytics.iceberg.side.lower()

                ==

                "buy"

            )

            evidence.add(

                Evidence(

                    category="Iceberg",

                    description="Iceberg detected",

                    weight=settings.smart_money_iceberg_weight,

                    bullish=bullish,

                )

            )

        # =====================================================
        # Large Trades
        # =====================================================

        if analytics.large_trades.buy_large_trades > 0:

            evidence.add(

                Evidence(

                    category="Large Trades",

                    description="Large buy trades",

                    weight=settings.smart_money_large_trade_weight,

                    bullish=True,

                )

            )

        if analytics.large_trades.sell_large_trades > 0:

            evidence.add(

                Evidence(

                    category="Large Trades",

                    description="Large sell trades",

                    weight=settings.smart_money_large_trade_weight,

                    bullish=False,

                )

            )

        # =====================================================
        # Exhaustion
        # =====================================================

        if exhaustion.seller_exhausted:

            evidence.add(

                Evidence(

                    category="Exhaustion",

                    description="Seller exhaustion",

                    weight=settings.smart_money_exhaustion_weight,

                    bullish=True,

                )

            )

        if exhaustion.buyer_exhausted:

            evidence.add(

                Evidence(

                    category="Exhaustion",

                    description="Buyer exhaustion",

                    weight=settings.smart_money_exhaustion_weight,

                    bullish=False,

                )

            )

        # =====================================================
        # CVD
        # =====================================================

        if analytics.cvd.current > 0:

            evidence.add(

                Evidence(

                    category="CVD",

                    description="Positive cumulative delta",

                    weight=settings.smart_money_cvd_weight,

                    bullish=True,

                )

            )

        elif analytics.cvd.current < 0:

            evidence.add(

                Evidence(

                    category="CVD",

                    description="Negative cumulative delta",

                    weight=settings.smart_money_cvd_weight,

                    bullish=False,

                )

            )

        return evidence