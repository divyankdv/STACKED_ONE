"""
============================================================

                    STACKED ONE

              CONFIDENCE BUILDER

------------------------------------------------------------

Utility class for building strategy confidence and
collecting supporting and opposing evidence.

============================================================
"""

from __future__ import annotations


class ConfidenceBuilder:
    """
    Helper used by trading strategies.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self._positive = 0.0

        self._negative = 0.0

        self._positive_reasons: list[str] = []

        self._negative_reasons: list[str] = []

    # =====================================================
    # Positive Evidence
    # =====================================================

    def add(

        self,

        condition: bool,

        weight: float,

        reason: str,

    ) -> bool:

        if condition:

            self._positive += weight

            self._positive_reasons.append(reason)

        return condition

    # =====================================================
    # Negative Evidence
    # =====================================================

    def add_negative(

        self,

        condition: bool,

        penalty: float,

        reason: str,

    ) -> bool:

        if condition:

            self._negative += penalty

            self._negative_reasons.append(reason)

        return condition

    # =====================================================
    # Force Add
    # =====================================================

    def add_weight(

        self,

        weight: float,

        reason: str,

    ):

        self._positive += weight

        self._positive_reasons.append(reason)

    # =====================================================
    # Properties
    # =====================================================

    @property
    def positive(self) -> float:

        return self._positive

    @property
    def negative(self) -> float:

        return self._negative

    @property
    def confidence(self) -> float:
        """
        Final confidence after subtracting penalties.
        """

        value = self._positive - self._negative

        if value < 0:

            value = 0.0

        if value > 1.0:

            value = 1.0

        return value

    @property
    def score(self) -> float:

        return self.confidence * 100.0

    @property
    def reasons(self) -> tuple[str, ...]:

        return tuple(self._positive_reasons)

    @property
    def warnings(self) -> tuple[str, ...]:

        return tuple(self._negative_reasons)

    @property
    def all_messages(self) -> tuple[str, ...]:

        return tuple(

            self._positive_reasons

            +

            self._negative_reasons

        )

    @property
    def empty(self) -> bool:

        return (

            len(self._positive_reasons)

            +

            len(self._negative_reasons)

        ) == 0

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "ConfidenceBuilder("

            f"confidence={self.confidence:.2f}, "

            f"positive={self.positive:.2f}, "

            f"negative={self.negative:.2f}"

            ")"

        )

    __repr__ = __str__