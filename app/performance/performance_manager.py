"""
============================================================

                    STACKED ONE

              PERFORMANCE MANAGER

------------------------------------------------------------

Maintains performance profiles for every strategy.

Profiles are automatically created on first use.

============================================================
"""

from __future__ import annotations

from app.performance.strategy_profile import StrategyProfile


class PerformanceManager:
    """
    Manages StrategyProfile objects.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self._profiles: dict[str, StrategyProfile] = {}

    # =====================================================
    # Get Profile
    # =====================================================

    def profile(

        self,

        strategy_name: str,

    ) -> StrategyProfile:

        """
        Returns the profile for a strategy.

        Creates one automatically if necessary.
        """

        if strategy_name not in self._profiles:

            self._profiles[strategy_name] = StrategyProfile(

                name=strategy_name,

            )

        return self._profiles[strategy_name]

    # =====================================================
    # Record Trade
    # =====================================================

    def record_trade(

        self,

        strategy_name: str,

        pnl: float,

        rr: float,

    ) -> None:

        profile = self.profile(

            strategy_name,

        )

        profile.record_trade(

            pnl=pnl,

            rr=rr,

        )

    # =====================================================
    # Lookup
    # =====================================================

    def has_profile(

        self,

        strategy_name: str,

    ) -> bool:

        return strategy_name in self._profiles

    # =====================================================
    # All Profiles
    # =====================================================

    @property
    def profiles(self) -> tuple[StrategyProfile, ...]:

        return tuple(

            self._profiles.values()

        )

    # =====================================================
    # Ranking
    # =====================================================

    def ranked_profiles(

        self,

    ) -> tuple[StrategyProfile, ...]:

        return tuple(

            sorted(

                self._profiles.values(),

                key=lambda profile: (

                    profile.reliability,

                    profile.net_profit,

                    profile.win_rate,

                ),

                reverse=True,

            )

        )

    # =====================================================
    # Best Strategy
    # =====================================================

    @property
    def best_strategy(

        self,

    ) -> StrategyProfile | None:

        ranked = self.ranked_profiles()

        if not ranked:

            return None

        return ranked[0]

    # =====================================================
    # Worst Strategy
    # =====================================================

    @property
    def worst_strategy(

        self,

    ) -> StrategyProfile | None:

        ranked = self.ranked_profiles()

        if not ranked:

            return None

        return ranked[-1]

    # =====================================================
    # Reset
    # =====================================================

    def reset(

        self,

    ) -> None:

        self._profiles.clear()

    # =====================================================
    # Count
    # =====================================================

    def __len__(

        self,

    ) -> int:

        return len(

            self._profiles,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(

        self,

    ):

        return (

            "PerformanceManager("

            f"profiles={len(self)}"

            ")"

        )

    __repr__ = __str__