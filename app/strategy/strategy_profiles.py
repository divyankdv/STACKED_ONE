from app.strategy.strategy_profile import StrategyProfile

STRATEGY_PROFILES = {
    "Accumulation": StrategyProfile(
        name="Accumulation",
        reliability=1.00,
    ),
    "Distribution": StrategyProfile(
        name="Distribution",
        reliability=1.00,
    ),
    "Breakout": StrategyProfile(
        name="Breakout",
        reliability=0.90,
    ),
    "Reversal": StrategyProfile(
        name="Reversal",
        reliability=0.80,
    ),
}
