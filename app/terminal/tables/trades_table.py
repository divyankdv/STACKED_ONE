"""
============================================================

                    STACKED ONE

                TRADES TABLE

============================================================
"""

from __future__ import annotations

from rich.table import Table

from app.terminal.state import ClosedTradeRecord
from app.terminal.theme import console, pnl_style


def render_trades(trades: list[ClosedTradeRecord]) -> None:

    if not trades:

        console.print("[muted]No completed trades in the current session.[/muted]")

        return

    table = Table(
        title=f"Trade History  ({len(trades)} trades)",
        border_style="accent",
        header_style="heading",
    )

    table.add_column("#", justify="right")
    table.add_column("Symbol")
    table.add_column("Side")
    table.add_column("Strategy")
    table.add_column("Entry", justify="right")
    table.add_column("Exit", justify="right")
    table.add_column("Qty", justify="right")
    table.add_column("PnL", justify="right")
    table.add_column("Reason")
    table.add_column("Closed At")

    for index, trade in enumerate(trades, start=1):

        style = pnl_style(trade.pnl)

        table.add_row(
            str(index),
            trade.symbol,
            trade.side,
            trade.strategy or "-",
            f"{trade.entry_price:,.2f}",
            f"{trade.exit_price:,.2f}",
            f"{trade.quantity:.4f}",
            f"[{style}]{trade.pnl:,.2f}[/{style}]",
            trade.reason or "-",
            trade.closed_at.replace("T", " ")[:19] if trade.closed_at else "-",
        )

    console.print(table)
