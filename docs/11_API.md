# STACKED QUANT AI V6

# API SPECIFICATION

Version: 1.0

---

# WebSocketManager

## Purpose

Maintain a live websocket connection to Delta Exchange.

It is the ONLY component allowed to communicate with the exchange websocket.

It never performs trading logic.

It never calculates indicators.

It never stores historical candles.

Its only responsibility is transporting exchange data into the system.

---

## Responsibilities

✓ Connect

✓ Authenticate (if required)

✓ Subscribe

✓ Receive Messages

✓ Detect Disconnect

✓ Reconnect

✓ Forward Data

---

## Public Methods

connect()

Creates websocket connection.

---

disconnect()

Gracefully closes websocket.

---

subscribe()

Subscribes to exchange channels.

---

on_message()

Receives websocket messages.

---

on_error()

Handles websocket errors.

---

on_close()

Handles websocket disconnection.

---

reconnect()

Reconnects automatically.

---

send()

Send websocket message.

---

## Output

Trade Messages

↓

TradeEngine

OrderBook Messages

↓

OrderBookEngine

---

## Never

Never calculate indicators.

Never create candles.

Never make decisions.

Never execute trades.

---

END