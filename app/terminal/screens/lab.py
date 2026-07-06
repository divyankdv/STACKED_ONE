"""
============================================================

                    STACKED ONE

                STRATEGY LABORATORY

============================================================
"""

from __future__ import annotations

from rich.table import Table

from app.terminal import engine_bridge
from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.theme import console
from app.terminal.widgets.prompts import pause


def _render(state: TerminalState) -> list[type[engine_bridge.BaseStrategy]]:

    classes = list(engine_bridge.strategy_classes())

    table = Table(
        title="Registered Strategies",
        border_style="accent",
        header_style="heading",
    )

    table.add_column("#", justify="right")
    table.add_column("Strategy")
    table.add_column("Category")
    table.add_column("Version")
    table.add_column("Status", justify="center")

    for index, cls in enumerate(classes, start=1):

        meta = cls.metadata

        status = "[positive]ENABLED[/positive]" if meta.enabled else "[negative]DISABLED[/negative]"

        table.add_row(
            str(index),
            meta.name,
            meta.category,
            meta.version,
            status,
        )

    console.print(table)

    console.print(
        f"\n[label]Default backtest strategy:[/label] "
        f"[value]{state.settings.default_strategy}[/value]",
    )

    return classes


def show_strategy_lab(state: TerminalState) -> None:

    while True:

        header(
            "STRATEGY LABORATORY",
            "Enable, disable, or set a default strategy for backtesting.",
        )

        classes = _render(state)

        footer("# = toggle enabled, 'd' = set default strategy, b = back")

        raw = console.input("[label]Select:[/label] ").strip().lower()

        if raw in ("b", "back", "q"):
            return

        if raw == "d":

            _set_default_strategy(state, classes)

            continue

        if raw.isdigit() and 1 <= int(raw) <= len(classes):

            cls = classes[int(raw) - 1]

            state.set_strategy_enabled(
                cls.metadata.name,
                not cls.metadata.enabled,
            )

            continue

        console.print("[negative]Invalid selection.[/negative]")

        pause()


def _set_default_strategy(
    state: TerminalState,
    classes: list[type[engine_bridge.BaseStrategy]],
) -> None:

    console.print(f"\n[value]0[/value]  {engine_bridge.ALL_STRATEGIES}")

    for index, cls in enumerate(classes, start=1):

        console.print(f"[value]{index}[/value]  {cls.metadata.name}")

    raw = console.input("\n[label]Select default strategy:[/label] ").strip()

    if raw == "0" or raw == "":

        state.settings.default_strategy = engine_bridge.ALL_STRATEGIES

    elif raw.isdigit() and 1 <= int(raw) <= len(classes):

        state.settings.default_strategy = classes[int(raw) - 1].metadata.name

    else:

        console.print("[negative]Invalid selection.[/negative]")

        pause()

        return

    state.settings.save()

    console.print("[positive]Default strategy updated.[/positive]")
