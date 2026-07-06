"""
============================================================

                    STACKED ONE

                HISTORICAL BACKTEST

============================================================
"""

from __future__ import annotations

from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from app.terminal import data_sources, engine_bridge
from app.terminal.screens.base import footer, header
from app.terminal.state import ClosedTradeRecord, TerminalState
from app.terminal.tables.results_table import render_results
from app.terminal.theme import console
from app.terminal.widgets.prompts import (
    CancelledError,
    choose,
    confirm,
    pause,
    prompt_date,
    prompt_float,
    prompt_text,
)


def show_backtest(state: TerminalState) -> None:

    header(
        "HISTORICAL BACKTEST",
        "Configure and run a replay against tick data. Type 'b' at any step to cancel.",
    )

    try:

        dataset = _choose_dataset(state)

        timeframe = choose(
            "Choose Timeframe",
            engine_bridge.timeframes(),
            default=(
                list(engine_bridge.timeframes()).index(state.settings.default_timeframe) + 1
                if state.settings.default_timeframe in engine_bridge.timeframes()
                else 1
            ),
        )

        start, end = _choose_date_range(dataset)

        strategy = _choose_strategy(state)

        capital = prompt_float(
            "Choose Initial Capital",
            default=state.settings.initial_capital,
            minimum=1.0,
        )

        risk = prompt_float(
            "Choose Risk % Per Trade",
            default=state.settings.risk_per_trade,
            minimum=0.01,
            maximum=100.0,
        )

    except CancelledError:

        return

    console.print("\n[heading]Confirm Backtest[/heading]")
    console.print(f"  [label]Symbol      :[/label] {dataset.symbol}")
    console.print(f"  [label]Data Source :[/label] {'Sample Data' if dataset.is_sample else dataset.path}")
    console.print(f"  [label]Timeframe   :[/label] {timeframe}")
    console.print(f"  [label]Date Range  :[/label] {start.date()} -> {end.date()}")
    console.print(f"  [label]Strategy    :[/label] {strategy}")
    console.print(f"  [label]Capital     :[/label] {capital:,.2f}")
    console.print(f"  [label]Risk        :[/label] {risk:.2f}%\n")

    if not confirm("Run this backtest?", default=True):
        return

    _run_backtest(
        state,
        dataset=dataset,
        timeframe=timeframe,
        start=start,
        end=end,
        strategy=strategy,
        capital=capital,
        risk=risk,
    )

    footer("Enter = return to main menu")

    pause()


# ==========================================================
# Wizard Steps
# ==========================================================


def _choose_dataset(state: TerminalState):

    samples = data_sources.sample_symbols()

    options = [f"{symbol} (bundled sample data)" for symbol in samples] + ["Custom CSV file..."]

    default_index = 1

    if state.settings.default_symbol in samples:
        default_index = samples.index(state.settings.default_symbol) + 1

    choice = choose("Choose Symbol", options, default=default_index)

    if choice == "Custom CSV file...":

        path = prompt_text("CSV file path (timestamp,price,volume,side)")

        symbol = prompt_text("Symbol label", default=state.settings.default_symbol).upper()

        return data_sources.custom_dataset(path, symbol)

    symbol = choice.split(" ")[0]

    with console.status(f"[accent]Preparing {symbol} sample data...[/accent]"):

        dataset = data_sources.ensure_sample_dataset(symbol)

    return dataset


def _choose_date_range(dataset):

    console.print(
        f"\n[muted]Available data: {dataset.start.date()} -> {dataset.end.date()} "
        f"({dataset.tick_count:,} ticks)[/muted]",
    )

    start = prompt_date(
        "Start Date",
        default=dataset.start,
        minimum=dataset.start,
        maximum=dataset.end,
    )

    end = prompt_date(
        "End Date",
        default=dataset.end,
        minimum=start,
        maximum=dataset.end,
    )

    return start, end


def _choose_strategy(state: TerminalState) -> str:

    names = engine_bridge.strategy_display_names()

    options = [engine_bridge.ALL_STRATEGIES, *names]

    default_index = 1

    if state.settings.default_strategy in options:
        default_index = options.index(state.settings.default_strategy) + 1

    return choose("Choose Strategy", options, default=default_index)


# ==========================================================
# Run
# ==========================================================


def _run_backtest(
    state: TerminalState,
    dataset,
    timeframe: str,
    start,
    end,
    strategy: str,
    capital: float,
    risk: float,
) -> None:

    simulator = engine_bridge.build_simulator(str(dataset.path))

    engine_bridge.load_replay(
        simulator,
        symbol=dataset.symbol,
        timeframe=timeframe,
        start=start,
        end=end,
    )

    config = engine_bridge.SimulationConfig(
        symbol=dataset.symbol,
        timeframe=timeframe,
        start=start.isoformat(),
        end=end.isoformat(),
        strategy=strategy,
        initial_capital=capital,
        risk_per_trade=risk,
        leverage=state.settings.leverage,
        commission=0.0,
        slippage=0.0,
    )

    session = state.new_session(
        mode="backtest",
        symbol=dataset.symbol,
        timeframe=timeframe,
        strategy_label=strategy,
    )

    session.simulator = simulator

    console.print()

    progress = Progress(
        TextColumn("[accent]Replaying[/accent]"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    with progress:

        task = progress.add_task("backtest", total=100)

        with engine_bridge.strategy_scope(strategy):

            for step in simulator.iter_run(config):

                progress.update(task, completed=step.progress * 100)

                if step.tick is not None:

                    session.last_price = step.tick.price

                if step.decision is not None:

                    session.last_snapshot = step.decision.analytics

                    session.last_grade = step.decision.confluence.grade.value

                    session.last_confidence = step.decision.confluence.confidence

                if step.closed_trade is not None and step.closed_trade.closed_position is not None:

                    session.trades.append(
                        ClosedTradeRecord.from_step(step, fallback_symbol=dataset.symbol),
                    )

                if step.result is not None:

                    session.result = step.result

    console.print()

    if session.result is not None:

        render_results(session.result)
