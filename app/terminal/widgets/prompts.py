"""
============================================================

                    STACKED ONE

                    PROMPTS

------------------------------------------------------------

Reusable keyboard input helpers shared by every screen.

============================================================
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from app.terminal.theme import console


class CancelledError(Exception):
    """
    Raised when the user backs out of a wizard step.

    Typing 'b' or 'back' at any prompt raises this so the
    caller can return to the previous screen/menu.
    """


def _raise_if_back(raw: str) -> None:

    if raw.strip().lower() in ("b", "back", "q", "quit"):
        raise CancelledError


def choose(
    title: str,
    options: Sequence[str],
    default: int = 1,
) -> str:
    """
    Displays a numbered list and returns the chosen option text.
    """

    console.print(f"\n[heading]{title}[/heading]")

    for index, option in enumerate(options, start=1):

        marker = "[accent]>[/accent]" if index == default else " "

        console.print(f" {marker} [value]{index}[/value]  {option}")

    while True:

        raw = console.input(
            f"\n[label]Select 1-{len(options)} (Enter = {default}, 'b' = back):[/label] ",
        )

        _raise_if_back(raw)

        raw = raw.strip()

        if raw == "":
            return options[default - 1]

        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]

        console.print("[negative]Invalid selection.[/negative]")


def prompt_text(
    label: str,
    default: str | None = None,
) -> str:

    suffix = f" (Enter = {default})" if default is not None else ""

    while True:

        raw = console.input(f"[label]{label}{suffix}:[/label] ")

        _raise_if_back(raw)

        raw = raw.strip()

        if raw == "" and default is not None:
            return default

        if raw != "":
            return raw

        console.print("[negative]A value is required.[/negative]")


def prompt_float(
    label: str,
    default: float | None = None,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:

    suffix = f" (Enter = {default})" if default is not None else ""

    while True:

        raw = console.input(f"[label]{label}{suffix}:[/label] ")

        _raise_if_back(raw)

        raw = raw.strip()

        if raw == "" and default is not None:
            return default

        try:

            value = float(raw)

        except ValueError:

            console.print("[negative]Enter a number.[/negative]")

            continue

        if minimum is not None and value < minimum:

            console.print(f"[negative]Must be >= {minimum}.[/negative]")

            continue

        if maximum is not None and value > maximum:

            console.print(f"[negative]Must be <= {maximum}.[/negative]")

            continue

        return value


def prompt_date(
    label: str,
    default: datetime | None = None,
    minimum: datetime | None = None,
    maximum: datetime | None = None,
) -> datetime:

    suffix = f" (Enter = {default.date()})" if default is not None else ""

    while True:

        raw = console.input(
            f"[label]{label} - YYYY-MM-DD{suffix}:[/label] ",
        )

        _raise_if_back(raw)

        raw = raw.strip()

        if raw == "" and default is not None:
            return default

        try:

            value = datetime.strptime(raw, "%Y-%m-%d")

        except ValueError:

            console.print("[negative]Use format YYYY-MM-DD.[/negative]")

            continue

        if minimum is not None and value < minimum:

            console.print(f"[negative]Must be on/after {minimum.date()}.[/negative]")

            continue

        if maximum is not None and value > maximum:

            console.print(f"[negative]Must be on/before {maximum.date()}.[/negative]")

            continue

        return value


def confirm(
    label: str,
    default: bool = True,
) -> bool:

    hint = "Y/n" if default else "y/N"

    while True:

        raw = console.input(f"[label]{label} ({hint}):[/label] ")

        _raise_if_back(raw)

        raw = raw.strip().lower()

        if raw == "":
            return default

        if raw in ("y", "yes"):
            return True

        if raw in ("n", "no"):
            return False

        console.print("[negative]Enter y or n.[/negative]")


def pause(message: str = "Press Enter to continue...") -> None:

    console.input(f"\n[muted]{message}[/muted]")
