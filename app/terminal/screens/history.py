"""
============================================================

                    STACKED ONE

                TRADE HISTORY

============================================================
"""

from __future__ import annotations

from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.tables.trades_table import render_trades
from app.terminal.theme import console
from app.terminal.widgets.prompts import pause


def show_history(state: TerminalState) -> None:

    header(
        "TRADE HISTORY",
        f"Session: {state.session.mode or 'none'} "
        f"{state.session.symbol or ''} {state.session.timeframe or ''}".strip(),
    )

    if not state.session.has_data:

        console.print("[muted]No data yet. Run a Historical Backtest or start Live Paper Trading first.[/muted]")

    else:

        render_trades(state.session.trades)

    footer()

    pause()
