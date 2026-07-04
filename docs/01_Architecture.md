# STACKED QUANT AI V6

Version: 1.0

Status: ACTIVE DEVELOPMENT

---

# Vision

STACKED QUANT AI V6 is an institutional-grade quantitative trading platform designed for:

- Live Trading
- Paper Trading
- Backtesting
- Replay
- Smart Money Concepts
- Order Flow
- AI Decision Making

The architecture follows an event-driven design.

---

# Core Principles

1. One Responsibility per Class
2. One Direction of Data Flow
3. No Duplicate Logic
4. No Duplicate Data Ownership
5. Event Driven
6. Multi-Timeframe
7. Fully Modular
8. Production Ready

---

# Project Structure

STACKED_QUANT_AI_V6/

app/

config/

core/

data/

engine/

exchange/

execution/

indicators/

logger/

models/

modules/

services/

strategy/

utils/

docs/

tests/

---

# High Level Pipeline

Exchange

↓

WebSocket Manager

↓

Trade Engine

↓

Tick Engine

↓

Timeframe Aggregator

↓

Timeframe Manager

↓

Indicator Engine

↓

Context Engine

↓

Decision Engine

↓

Risk Engine

↓

Execution Engine

↓

Dashboard

---

# Current Status

Module 1

Infrastructure

IN PROGRESS