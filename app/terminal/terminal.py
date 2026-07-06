"""
============================================================

                    STACKED ONE

                    TERMINAL

------------------------------------------------------------

Main application loop. Ties the main menu to each screen.

============================================================
"""

from __future__ import annotations

from app.terminal.menu import show_main_menu
from app.terminal.screens.analytics import show_analytics
from app.terminal.screens.backtest import show_backtest
from app.terminal.screens.history import show_history
from app.terminal.screens.home import show_startup
from app.terminal.screens.lab import show_strategy_lab
from app.terminal.screens.live import show_live
from app.terminal.screens.performance import show_performance
from app.terminal.screens.portfolio import show_portfolio
from app.terminal.screens.settings import show_settings
from app.terminal.state import TerminalState
from app.terminal.theme import console

ROUTES = {
    "1": show_backtest,
    "2": show_live,
    "3": show_strategy_lab,
    "4": show_performance,
    "5": show_history,
    "6": show_portfolio,
    "7": show_analytics,
    "8": show_settings,
}


class Terminal:

    def __init__(self) -> None:

        self.state = TerminalState()

    def run(self) -> None:

        show_startup(self.state)

        while True:

            choice = show_main_menu()

            if choice == "9":

                console.print("\n[muted]Goodbye.[/muted]\n")

                return

            handler = ROUTES.get(choice)

            if handler is None:

                console.print("[negative]Invalid selection.[/negative]")

                continue

            try:

                handler(self.state)

            except KeyboardInterrupt:

                console.print("\n[muted]Cancelled.[/muted]")

            except Exception as error:  # noqa: BLE001

                console.print(f"\n[danger] ERROR [/danger] {error}\n")
