"""
============================================================

                    STACKED ONE

                    PORTFOLIO

============================================================
"""

from __future__ import annotations

from rich.table import Table

from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.theme import console, pnl_style
from app.terminal.widgets.prompts import pause


def show_portfolio(state: TerminalState) -> None:

    header("PORTFOLIO")

    session = state.session

    if not session.has_data or session.simulator is None:

        console.print("[muted]No data yet. Run a Historical Backtest or start Live Paper Trading first.[/muted]")

        footer()

        pause()

        return

    positions = session.simulator.positions

    balance = state.settings.initial_capital

    #
    # PositionManager only tracks currently-open positions -
    # once a trade closes it's popped out entirely, so its
    # total_realized_pnl reads back to 0 the moment nothing
    # is open. The session trade log is the durable record.
    #

    realized_pnl = sum(trade.pnl for trade in session.trades)

    if session.result is not None:

        equity = session.result.ending_equity

    else:

        equity = balance + realized_pnl + positions.total_unrealized_pnl - positions.total_cost

    console.print(f"[label]Balance (Starting Capital):[/label] [value]{balance:,.2f}[/value]")

    equity_style = pnl_style(equity - balance)

    console.print(f"[label]Equity:[/label] [{equity_style}]{equity:,.2f}[/{equity_style}]")

    console.print(f"[label]Realized PnL:[/label] [{pnl_style(realized_pnl)}]{realized_pnl:,.2f}[/{pnl_style(realized_pnl)}]")

    console.print(f"[label]Unrealized PnL:[/label] [{pnl_style(positions.total_unrealized_pnl)}]{positions.total_unrealized_pnl:,.2f}[/{pnl_style(positions.total_unrealized_pnl)}]")

    console.print(f"[label]Total Costs:[/label] {positions.total_cost:,.2f}")

    risk = sum(
        abs(position.average_price - position.stop_price) * position.quantity
        for position in positions.positions
    )

    console.print(f"[label]Current Risk (open positions):[/label] {risk:,.2f}\n")

    console.print("[heading]Open Positions[/heading]")

    if positions.position_count == 0:

        console.print("[muted]None.[/muted]\n")

    else:

        table = Table(border_style="accent", header_style="heading")

        table.add_column("Symbol")
        table.add_column("Side")
        table.add_column("Qty", justify="right")
        table.add_column("Avg Price", justify="right")
        table.add_column("Stop", justify="right")
        table.add_column("Target", justify="right")
        table.add_column("Unrealized PnL", justify="right")

        for position in positions.positions:

            style = pnl_style(position.unrealized_pnl)

            table.add_row(
                position.symbol,
                position.side.value,
                f"{position.quantity:.4f}",
                f"{position.average_price:,.2f}",
                f"{position.stop_price:,.2f}",
                f"{position.target_price:,.2f}",
                f"[{style}]{position.unrealized_pnl:,.2f}[/{style}]",
            )

        console.print(table)

        console.print()

    console.print("[heading]Closed Positions[/heading]  [muted](this session)[/muted]")

    console.print(f"  {len(session.trades)} closed trade(s). See Trade History for detail.\n")

    footer()

    pause()
