"""
============================================================

                    STACKED ONE

                LIVE PAPER TRADING

------------------------------------------------------------

"Live" here means the bundled/chosen tick tape replayed
through the exact same engine pipeline used for backtests,
paced to feel live and rendered as a continuously refreshing
dashboard. No network connection is required.

============================================================
"""

from __future__ import annotations

import time

from rich.live import Live
from rich.table import Table

from app.terminal import data_sources, engine_bridge
from app.terminal.screens.base import footer, header
from app.terminal.state import ClosedTradeRecord, TerminalState
from app.terminal.theme import console, grade_style, pnl_style
from app.terminal.widgets.prompts import (
    CancelledError,
    choose,
    confirm,
    pause,
    prompt_float,
)

try:

    import msvcrt

    def _stop_requested() -> bool:

        if msvcrt.kbhit():

            msvcrt.getch()

            return True

        return False

except ImportError:  # pragma: no cover - non-Windows fallback

    def _stop_requested() -> bool:

        return False


def show_live(state: TerminalState) -> None:

    header(
        "LIVE PAPER TRADING",
        "Simulated live feed - replays tick data through the real engine, paced to feel live.",
    )

    try:

        samples = data_sources.sample_symbols()

        symbol_choice = choose(
            "Choose Symbol",
            [f"{s} (bundled sample data)" for s in samples],
            default=1,
        )

        symbol = symbol_choice.split(" ")[0]

        with console.status(f"[accent]Preparing {symbol} sample data...[/accent]"):

            dataset = data_sources.ensure_sample_dataset(symbol)

        timeframe = choose(
            "Choose Timeframe",
            engine_bridge.timeframes(),
            default=1,
        )

        strategy = choose(
            "Choose Strategy",
            [engine_bridge.ALL_STRATEGIES, *engine_bridge.strategy_display_names()],
            default=1,
        )

        capital = prompt_float(
            "Initial Capital",
            default=state.settings.initial_capital,
            minimum=1.0,
        )

        speed = choose(
            "Playback Speed",
            ["Demo Speed (recommended)", "Instant (no pacing)"],
            default=1,
        )

    except CancelledError:

        return

    if not confirm("Start live paper trading session?", default=True):
        return

    console.print("\n[muted]Press any key to stop early.[/muted]\n")

    time.sleep(0.5)

    _run_live(
        state,
        dataset=dataset,
        timeframe=timeframe,
        strategy=strategy,
        capital=capital,
        instant=speed.startswith("Instant"),
    )

    footer("Enter = return to main menu")

    pause()


def _run_live(
    state: TerminalState,
    dataset,
    timeframe: str,
    strategy: str,
    capital: float,
    instant: bool,
) -> None:

    simulator = engine_bridge.build_simulator(str(dataset.path))

    engine_bridge.load_replay(
        simulator,
        symbol=dataset.symbol,
        timeframe=timeframe,
        start=dataset.start,
        end=dataset.end,
    )

    config = engine_bridge.SimulationConfig(
        symbol=dataset.symbol,
        timeframe=timeframe,
        start=dataset.start.isoformat(),
        end=dataset.end.isoformat(),
        strategy=strategy,
        initial_capital=capital,
        risk_per_trade=state.settings.risk_per_trade,
        leverage=state.settings.leverage,
        commission=0.0,
        slippage=0.0,
    )

    session = state.new_session(
        mode="live",
        symbol=dataset.symbol,
        timeframe=timeframe,
        strategy_label=strategy,
    )

    session.simulator = simulator
    session.running = True

    trend_state = {"previous_price": None}

    previous_timestamp = None

    with Live(console=console, refresh_per_second=8, screen=False) as live:

        with engine_bridge.strategy_scope(strategy):

            for step in simulator.iter_run(config):

                if step.tick is not None:

                    session.last_price = step.tick.price

                if step.decision is not None:

                    session.last_snapshot = step.decision.analytics

                    session.last_grade = step.decision.confluence.grade.value

                    session.last_confidence = step.decision.confluence.confidence

                if step.closed_trade is not None and step.closed_trade.closed_position is not None:

                    session.trades.append(ClosedTradeRecord.from_step(step, fallback_symbol=dataset.symbol))

                if step.result is not None:

                    session.result = step.result

                    break

                live.update(_render_dashboard(session, trend_state))

                if not instant and step.tick is not None:

                    delay = 0.05

                    if previous_timestamp is not None:

                        raw = (step.tick.timestamp - previous_timestamp).total_seconds()

                        delay = min(max(raw / 300.0, 0.01), 0.25)

                    previous_timestamp = step.tick.timestamp

                    time.sleep(delay)

                if _stop_requested():

                    break

    session.running = False

    console.print("\n[positive]Live session ended.[/positive]")

    if session.result is not None:

        console.print(f"[label]Final Equity:[/label] {session.result.ending_equity:,.2f}")


def _render_dashboard(session, trend_state) -> Table:

    price = session.last_price

    previous = trend_state["previous_price"]

    if price is not None and previous is not None:

        if price > previous:
            trend = "[positive]UP[/positive]"
        elif price < previous:
            trend = "[negative]DOWN[/negative]"
        else:
            trend = "[muted]FLAT[/muted]"

    else:

        trend = "[muted]-[/muted]"

    if price is not None:
        trend_state["previous_price"] = price

    table = Table(border_style="accent", header_style="heading", title="STACKED ONE  -  Live Dashboard")

    table.add_column("Field", style="label")
    table.add_column("Value", style="value")

    table.add_row("Current Price", f"{price:,.2f}" if price is not None else "-")
    table.add_row("Trend", trend)

    snapshot = session.last_snapshot

    if snapshot is not None:

        table.add_row("CVD", f"{snapshot.cvd.current:,.2f}")
        table.add_row("Absorption", "ACTIVE" if snapshot.absorption.active else "none")
        table.add_row("Icebergs", "ACTIVE" if snapshot.iceberg.active else "none")
        table.add_row("Large Trades", str(snapshot.large_trades.total_large_trades))

    if session.last_grade is not None:

        style = grade_style(session.last_grade)

        table.add_row("Confluence Grade", f"[{style}]{session.last_grade}[/{style}]")

    position = session.simulator.positions.current_position if session.simulator else None

    if position is not None:

        table.add_row("Current Position", f"{position.side.value} {position.quantity:.4f} {position.symbol}")
        table.add_row("Entry", f"{position.average_price:,.2f}")
        table.add_row("Stop", f"{position.stop_price:,.2f}")
        table.add_row("Target", f"{position.target_price:,.2f}")

        if price is not None:

            position.mark_to_market(price)

        pnl = position.unrealized_pnl

        style = pnl_style(pnl)

        table.add_row("Live PnL", f"[{style}]{pnl:,.2f}[/{style}]")

    else:

        table.add_row("Current Position", "[muted]none[/muted]")
        table.add_row("Entry", "-")
        table.add_row("Stop", "-")
        table.add_row("Target", "-")
        table.add_row("Live PnL", "-")

    return table
