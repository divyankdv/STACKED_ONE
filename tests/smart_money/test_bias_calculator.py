"""
============================================================

                STACKED ONE

         TEST BIAS CALCULATOR

============================================================
"""

from app.analytics.evidence import Evidence
from app.analytics.evidence_collection import EvidenceCollection
from app.analytics.smart_money.bias_calculator import (
    BiasCalculator,
)
from app.analytics.smart_money_bias import (
    SmartMoneyBias,
)
from app.config.settings import settings

# =====================================================
# Helper
# =====================================================

def make_evidence(

    bullish_weight: float,

    bearish_weight: float,

) -> EvidenceCollection:

    evidence = EvidenceCollection()

    if bullish_weight > 0:

        evidence.add(

            Evidence(

                category="Bullish",

                description="Bullish evidence",

                weight=bullish_weight,

                bullish=True,

            )

        )

    if bearish_weight > 0:

        evidence.add(

            Evidence(

                category="Bearish",

                description="Bearish evidence",

                weight=bearish_weight,

                bullish=False,

            )

        )

    return evidence


# =====================================================
# LONG
# =====================================================

def test_long():

    score = settings.smart_money_bias_threshold + 10

    evidence = make_evidence(

        bullish_weight=80,

        bearish_weight=20,

    )

    bias = BiasCalculator.calculate(

        evidence,

        score,

    )

    print("LONG TEST :", bias)

    assert bias == SmartMoneyBias.LONG


# =====================================================
# SHORT
# =====================================================

def test_short():

    score = settings.smart_money_bias_threshold + 10

    evidence = make_evidence(

        bullish_weight=20,

        bearish_weight=80,

    )

    bias = BiasCalculator.calculate(

        evidence,

        score,

    )

    print("SHORT TEST:", bias)

    assert bias == SmartMoneyBias.SHORT


# =====================================================
# NEUTRAL (Below Threshold)
# =====================================================

def test_neutral_threshold():

    score = settings.smart_money_bias_threshold - 1

    evidence = make_evidence(

        bullish_weight=100,

        bearish_weight=0,

    )

    bias = BiasCalculator.calculate(

        evidence,

        score,

    )

    print("THRESHOLD TEST:", bias)

    assert bias == SmartMoneyBias.NEUTRAL


# =====================================================
# NEUTRAL (Equal Conviction)
# =====================================================

def test_neutral_equal():

    score = settings.smart_money_bias_threshold + 10

    evidence = make_evidence(

        bullish_weight=50,

        bearish_weight=50,

    )

    bias = BiasCalculator.calculate(

        evidence,

        score,

    )

    print("EQUAL TEST:", bias)

    assert bias == SmartMoneyBias.NEUTRAL


# =====================================================
# Main
# =====================================================

def main():

    print()

    print("=" * 60)

    print("BIAS CALCULATOR")

    print("=" * 60)

    test_long()

    test_short()

    test_neutral_threshold()

    test_neutral_equal()

    print("=" * 60)

    print()

    print("✓ BIAS CALCULATOR PASSED")


if __name__ == "__main__":

    main()