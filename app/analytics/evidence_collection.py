"""
============================================================

                    STACKED ONE

              EVIDENCE COLLECTION

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.analytics.evidence import Evidence


@dataclass(slots=True)
class EvidenceCollection:

    items: list[Evidence] = field(default_factory=list)

    # =====================================================
    # Add
    # =====================================================

    def add(

        self,

        evidence: Evidence,

    ):

        self.items.append(

            evidence

        )

    # =====================================================
    # Total Weight
    # =====================================================

    @property
    def total_weight(self) -> float:

        return sum(

            item.weight

            for item in self.items

        )

    # =====================================================
    # Bullish Weight
    # =====================================================

    @property
    def bullish_weight(self) -> float:

        return sum(

            item.weight

            for item in self.items

            if item.bullish

        )

    # =====================================================
    # Bearish Weight
    # =====================================================

    @property
    def bearish_weight(self) -> float:

        return sum(

            item.weight

            for item in self.items

            if not item.bullish

        )

    # =====================================================
    # Tuple
    # =====================================================

    def to_tuple(self):

        return tuple(

            self.items

        )