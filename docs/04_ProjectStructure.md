# STACKED QUANT AI V6

# PROJECT STRUCTURE

Version: 1.0

Status: LOCKED

---

# Root

STACKED_QUANT_AI_V6/

├── app/
├── docs/
├── tests/
├── venv/
├── run.py
├── requirements.txt
├── README.md
└── .gitignore

---

# app/

Contains all source code.

---

## config/

Purpose

Application configuration.

Files

settings.py

Future

symbols.py

constants.py

---

## core/

Purpose

Application bootstrap.

Dependency injection.

Files

application.py

base_engine.py

---

## exchange/

Purpose

Everything related to Delta Exchange.

Files

market_data.py

trade_engine.py

orderbook_engine.py

websocket_manager.py

history_loader.py

---

## data/

Purpose

Market data processing.

Files

tick_engine.py

timeframe_manager.py

timeframe_aggregator.py

---

## models/

Purpose

Business objects.

Files

tick.py

candle.py

indicator_set.py

context.py

signal.py

position.py

trade.py

orderbook.py

---

## indicators/

Purpose

Indicator calculations.

Files

ema.py

rsi.py

atr.py

vwap.py

macd.py

momentum.py

volume.py

---

## modules/

Purpose

Institutional market analysis.

Files

trend_module.py

market_structure.py

smart_money.py

liquidity.py

displacement.py

order_blocks.py

breaker_blocks.py

mitigation.py

premium_discount.py

fvg.py

inducement.py

---

## engine/

Purpose

Decision pipeline.

Files

indicator_engine.py

context_engine.py

decision_engine.py

confidence_engine.py

risk_engine.py

position_engine.py

---

## execution/

Purpose

Trade execution.

Files

execution_engine.py

trade_manager.py

---

## dashboard/

Purpose

Display information only.

Files

dashboard.py

---

## logger/

Purpose

Central logging.

Files

logger.py

---

## services/

Purpose

External services.

Future

telegram.py

discord.py

database.py

---

## strategy/

Purpose

Strategy configuration.

Files

strategy.py

---

## utils/

Purpose

Shared helper functions.

Files

time_utils.py

math_utils.py

validation.py

---

# Project Rules

Every file must have one responsibility.

Every folder has one purpose.

Business logic must never exist inside the WebSocket.

Market analysis belongs inside modules.

Trading decisions belong inside DecisionEngine.

Execution belongs only inside ExecutionEngine.

---

END OF DOCUMENT