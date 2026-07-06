"""
============================================================

                    STACKED ONE

                STRATEGY PERFORMANCE

============================================================
"""

from __future__ import annotations

from collections import defaultdict

from rich.table import Table

from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.theme import console, pnl_style
from app.terminal.widgets.prompts import pause


def _sharpe_by_strategy(state: TerminalState) -> dict[str, float]:

    by_strategy: dict[str, list[float]] = defaultdict(list)

    for trade in state.session.trades:

        by_strategy[trade.strategy].append(trade.pnl)

    result: dict[str, float] = {}

    for strategy, pnls in by_strategy.items():

        if len(pnls) < 2:

            result[strategy] = 0.0

            continue

        mean_pnl = sum(pnls) / len(pnls)

        variance = sum((p - mean_pnl) ** 2 for p in pnls) / len(pnls)

        stdev = variance ** 0.5

        result[strategy] = mean_pnl / stdev if stdev > 0 else 0.0

    return result


def show_performance(state: TerminalState) -> None:

    header(
        "STRATEGY PERFORMANCE",
        "Ranked by reliability, then net profit, then win rate.",
    )

    session = state.session

    if not session.has_data or session.simulator is None:

        console.print("[muted]No data yet. Run a Historical Backtest or start Live Paper Trading first.[/muted]")

        footer()

        pause()

        return

    profiles = session.simulator.performance.ranked_profiles()

    if not profiles:

        console.print("[muted]No trades were recorded in the last run.[/muted]")

        footer()

        pause()

        return

    sharpe_by_strategy = _sharpe_by_strategy(state)

    table = Table(
        border_style="accent",
        header_style="heading",
    )

    table.add_column("Strategy")
    table.add_column("Profit Factor", justify="right")
    table.add_column("Win Rate", justify="right")
    table.add_column("Net Profit", justify="right")
    table.add_column("Expectancy", justify="right")
    table.add_column("Sharpe", justify="right")
    table.add_column("Max Drawdown", justify="right")
    table.add_column("Trades", justify="right")

    for profile in profiles:

        expectancy = profile.net_profit / profile.total_trades if profile.total_trades else 0.0

        sharpe = sharpe_by_strategy.get(profile.name, 0.0)

        table.add_row(
            profile.name,
            f"{profile.profit_factor:.2f}",
            f"{profile.win_rate:.2%}",
            f"[{pnl_style(profile.net_profit)}]{profile.net_profit:,.2f}[/{pnl_style(profile.net_profit)}]",
            f"[{pnl_style(expectancy)}]{expectancy:,.2f}[/{pnl_style(expectancy)}]",
            f"{sharpe:.2f}",
            f"{profile.max_drawdown:,.2f}",
            str(profile.total_trades),
        )

    console.print(table)

    console.print(
        "\n[muted]Profit Factor / Win Rate / Net Profit / Max Drawdown / Trades come from the engine's "
        "PerformanceManager. Expectancy and Sharpe are computed here from the session trade log.[/muted]",
    )

    footer()

    pause()
