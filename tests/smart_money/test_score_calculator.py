"""
============================================================

                STACKED ONE

        TEST SCORE CALCULATOR

============================================================
"""

from app.analytics.evidence import Evidence
from app.analytics.evidence_collection import EvidenceCollection
from app.analytics.smart_money.score_calculator import (
    ScoreCalculator,
)


def main():

    evidence = EvidenceCollection()

    #
    # Simulate institutional evidence
    #

    evidence.add(

        Evidence(

            category="Liquidity",

            description="High liquidity",

            weight=25,

            bullish=True,

        )

    )

    evidence.add(

        Evidence(

            category="Absorption",

            description="Absorption",

            weight=20,

            bullish=True,

        )

    )

    evidence.add(

        Evidence(

            category="Large Trades",

            description="Large buy trades",

            weight=15,

            bullish=True,

        )

    )

    evidence.add(

        Evidence(

            category="Pattern",

            description="Institutional accumulation",

            weight=20,

            bullish=True,

        )

    )

    score, confidence = ScoreCalculator.calculate(

        evidence,

    )

    print()

    print("=" * 60)

    print("SCORE CALCULATOR")

    print("=" * 60)

    print(f"Evidence Count : {len(evidence.items)}")

    print(f"Total Weight   : {evidence.total_weight}")

    print(f"Score          : {score}")

    print(f"Confidence     : {confidence:.2f}")

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert score > 0

    assert 0.0 <= confidence <= 1.0

    assert score <= evidence.total_weight

    print("✓ SCORE CALCULATOR PASSED")


if __name__ == "__main__":

    main()