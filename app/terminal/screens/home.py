"""
============================================================

                    STACKED ONE

                STARTUP SCREEN

============================================================
"""

from __future__ import annotations

import time

from app.terminal.screens.base import clear
from app.terminal.state import TerminalState
from app.terminal.theme import console, print_banner


def show_startup(state: TerminalState) -> None:

    clear()

    print_banner()

    console.print(
        f"[label]Default Symbol   :[/label] [value]{state.settings.default_symbol}[/value]",
    )

    console.print(
        f"[label]Default Timeframe:[/label] [value]{state.settings.default_timeframe}[/value]",
    )

    console.print(
        f"[label]Initial Capital  :[/label] [value]{state.settings.initial_capital:,.2f}[/value]",
    )

    console.print(
        f"[label]Risk Per Trade   :[/label] [value]{state.settings.risk_per_trade:.2f}%[/value]\n",
    )

    with console.status(
        "[accent]Initializing engines...[/accent]",
        spinner="dots",
    ):

        time.sleep(0.6)

    console.print("[positive]Ready.[/positive]\n")
