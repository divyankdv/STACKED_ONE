"""
============================================================

                    STACKED ONE

                    SETTINGS

============================================================
"""

from __future__ import annotations

from app.terminal import engine_bridge
from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.theme import console
from app.terminal.widgets.prompts import (
    CancelledError,
    choose,
    prompt_float,
    prompt_text,
)


def show_settings(state: TerminalState) -> None:

    while True:

        header("SETTINGS")

        settings = state.settings

        console.print(f"  [value]1[/value]  Initial Capital     : [value]{settings.initial_capital:,.2f}[/value]")
        console.print(f"  [value]2[/value]  Risk Per Trade      : [value]{settings.risk_per_trade:.2f}%[/value]")
        console.print(f"  [value]3[/value]  Leverage            : [value]{settings.leverage:.2f}x[/value]")
        console.print(f"  [value]4[/value]  Default Symbol      : [value]{settings.default_symbol}[/value]")
        console.print(f"  [value]5[/value]  Default Timeframe   : [value]{settings.default_timeframe}[/value]")

        footer("1-5 = edit, b = back")

        raw = console.input("[label]Select:[/label] ").strip().lower()

        if raw in ("b", "back", "q"):
            return

        try:

            if raw == "1":

                settings.initial_capital = prompt_float(
                    "New initial capital",
                    default=settings.initial_capital,
                    minimum=1.0,
                )

            elif raw == "2":

                settings.risk_per_trade = prompt_float(
                    "New risk per trade (%)",
                    default=settings.risk_per_trade,
                    minimum=0.01,
                    maximum=100.0,
                )

            elif raw == "3":

                settings.leverage = prompt_float(
                    "New leverage",
                    default=settings.leverage,
                    minimum=1.0,
                    maximum=125.0,
                )

            elif raw == "4":

                settings.default_symbol = prompt_text(
                    "New default symbol",
                    default=settings.default_symbol,
                ).upper()

            elif raw == "5":

                available = engine_bridge.timeframes()

                settings.default_timeframe = choose(
                    "Default timeframe",
                    available,
                    default=(
                        available.index(settings.default_timeframe) + 1
                        if settings.default_timeframe in available
                        else 1
                    ),
                )

            else:

                console.print("[negative]Invalid selection.[/negative]")

                continue

        except CancelledError:

            continue

        settings.save()

        console.print("[positive]Saved.[/positive]")
