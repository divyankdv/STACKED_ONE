"""
============================================================

                STACKED QUANT AI V6

                SETTINGS

------------------------------------------------------------

Single source of truth for all configuration.

Nothing in the application should hardcode values.

Always use:

from app.config.settings import settings

Example

settings.symbol
settings.ws_url
settings.ema_fast

============================================================
"""

import os

from dotenv import load_dotenv

from dataclasses import dataclass, field
from typing import List

load_dotenv()


@dataclass(frozen=True)
class Settings:

    # ======================================================
    # EXCHANGE
    # ======================================================

    exchange: str = "DELTA"

    symbol: str = "BTCUSD"

    # ======================================================
    # DELTA API
    # ======================================================

    rest_url: str = os.getenv(
    "DELTA_BASE_URL",
    "https://api.india.delta.exchange",
)

    ws_url: str = "wss://socket.india.delta.exchange"

    product_id: int | None = None

    # ======================================================
    # WEBSOCKET
    # ======================================================

    ping_interval: int = 20

    ping_timeout: int = 10

    reconnect_delay: int = 5

    max_reconnect_delay: int = 60

    auto_reconnect: bool = True

    # =====================================================
    # Analytics Configuration
    # =====================================================

    # Large Trade Engine
    large_trade_threshold: float = 100.0

    # Absorption Engine
    absorption_window_size: int = 50
    absorption_volume_threshold: float = 100.0
    absorption_price_tolerance: float = 2.0

    # Iceberg Engine
    iceberg_window_size: int = 50
    iceberg_volume_threshold: float = 500.0
    iceberg_trade_threshold: int = 5

    # ======================================================
    # CHANNELS
    # ======================================================

    trade_channel: str = "all_trades"

    orderbook_channel: str = "l2_orderbook"

    # ======================================================
    # HISTORY
    # ======================================================

    history_candles: int = 1000

    max_candles: int = 5000

    # ======================================================
    # TIMEFRAMES
    # ======================================================

    timeframes: List[str] = field(default_factory=lambda: [

        "1m",

        "5m",

        "15m",

        "1h",

        "4h",

        "1d"

    ])

    # ======================================================
    # EMA
    # ======================================================

    ema_fast: int = 9

    ema_medium: int = 21

    ema_trend: int = 50

    ema_long: int = 200

    # ======================================================
    # RSI
    # ======================================================

    rsi_period: int = 14

    # ======================================================
    # ATR
    # ======================================================

    atr_period: int = 14

    # ======================================================
    # MACD
    # ======================================================

    macd_fast: int = 12

    macd_slow: int = 26

    macd_signal: int = 9

    # ======================================================
    # VWAP
    # ======================================================

    vwap_enabled: bool = True

    # ======================================================
    # RISK
    # ======================================================

    default_risk: float = 1.0

    max_risk: float = 2.0

    rr_ratio: float = 3.0

    # ======================================================
    # DASHBOARD
    # ======================================================

    refresh_rate: int = 1

    show_reasons: bool = True

    # ======================================================
    # DEBUG
    # ======================================================

    debug: bool = True

    # =====================================================
    # Exhaustion Engine
    # =====================================================

    exhaustion_buy_aggression: float = 70.0

    exhaustion_sell_aggression: float = 70.0

    exhaustion_cvd_threshold: float = 0.0

    exhaustion_liquidity_threshold: float = 80.0

    # =====================================================
    # Smart Money Engine
    # =====================================================

    smart_money_liquidity_weight: float = 25.0

    smart_money_absorption_weight: float = 20.0

    smart_money_iceberg_weight: float = 20.0

    smart_money_large_trade_weight: float = 15.0

    smart_money_exhaustion_weight: float = 10.0

    smart_money_cvd_weight: float = 5.0

    smart_money_bias_threshold: float = 70.0

    # =====================================================
    # Smart Money Pattern Library
    # =====================================================

    smart_money_pattern_bonus_weight: float = 20.0

    smart_money_hidden_accumulation_weight: float = 10.0

    smart_money_hidden_distribution_weight: float = 10.0

    # =====================================================
    # Smart Money Synergy
    # =====================================================

    smart_money_synergy_enabled: bool = True

    smart_money_synergy_weight: float = 20.0

    smart_money_max_score: float = 100.0

        # =====================================================
    # Regime Engine
    # =====================================================

    regime_trend_threshold: float = 70.0

    regime_range_threshold: float = 40.0

    regime_unknown_threshold: float = 20.0

    # =====================================================
    # Strategy Engine
    # =====================================================

    strategy_signal_threshold: float = 0.70

    strategy_min_confidence: float = 0.50

    # =====================================================
    # Accumulation Strategy
    # =====================================================

    accumulation_liquidity_weight: float = 0.25

    accumulation_smart_money_weight: float = 0.35

    accumulation_regime_weight: float = 0.25

    accumulation_cvd_weight: float = 0.15

    # =====================================================
    # Distribution Strategy
    # =====================================================

    distribution_liquidity_weight: float = 0.25

    distribution_smart_money_weight: float = 0.35

    distribution_regime_weight: float = 0.25

    distribution_cvd_weight: float = 0.15

    # =====================================================
    # Breakout Strategy
    # =====================================================

    breakout_liquidity_weight: float = 0.30

    breakout_iceberg_weight: float = 0.30

    breakout_large_trade_weight: float = 0.20

    breakout_cvd_weight: float = 0.20

    # =====================================================
    # Reversal Strategy
    # =====================================================

    reversal_exhaustion_weight: float = 0.40

    reversal_absorption_weight: float = 0.30

    reversal_regime_weight: float = 0.20

    reversal_cvd_weight: float = 0.10


# ==========================================================
# Global Settings Object
# ==========================================================

settings = Settings()