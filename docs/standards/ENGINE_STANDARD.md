# STACKED ONE - ENGINE STANDARD

## Purpose

Every analytics engine must follow the same interface.

This guarantees consistency across the entire platform.

---

# Required Methods

Every engine MUST implement:

```python
update_trade(trade)

reset()

snapshot()
```

---

# Constructor

The constructor should initialize internal state only.

No network calls.

No file access.

No database access.

---

# update_trade()

Receives ONE TradeMessage.

Updates internal state.

Must be deterministic.

---

# reset()

Returns the engine to a clean state.

Must clear all rolling windows.

Must not recreate the object.

---

# snapshot()

Returns an immutable dataclass.

Never returns dictionaries.

Never returns mutable objects.

---

# Snapshot Rules

Snapshots must:

- use @dataclass(frozen=True)
- contain only data
- contain no business logic
- contain no calculations

---

# Engine Rules

An engine must never:

- connect to WebSockets
- access REST APIs
- read files
- write files
- access databases
- update UI

An engine only performs calculations.

---

# Performance

Target processing time:

< 100 microseconds per trade.

---

# Testing

Every engine must have:

tests/test_<engine>.py

before integration.

---

# Documentation

Every engine must have:

Purpose

Inputs

Outputs

Algorithm

Complexity

Future Improvements