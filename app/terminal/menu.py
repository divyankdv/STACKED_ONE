"""
============================================================

                    STACKED ONE

                    MAIN MENU

============================================================
"""

from __future__ import annotations

from app.terminal.screens.base import header
from app.terminal.theme import console

MENU_ITEMS: tuple[tuple[str, str], ...] = (
    ("1", "Historical Backtest"),
    ("2", "Live Paper Trading"),
    ("3", "Strategy Laboratory"),
    ("4", "Strategy Performance"),
    ("5", "Trade History"),
    ("6", "Portfolio"),
    ("7", "Market Analytics"),
    ("8", "Settings"),
    ("9", "Exit"),
)


def show_main_menu() -> str:

    header("MAIN MENU")

    for key, label in MENU_ITEMS:

        console.print(f"  [value]{key}[/value]   {label}")

    console.print()

    choice = console.input("[label]Select an option (1-9):[/label] ").strip()

    return choice
