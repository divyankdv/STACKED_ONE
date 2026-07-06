"""
============================================================

                    STACKED ONE

                SCREEN BASE

------------------------------------------------------------

Shared chrome (clear/header/footer) used by every screen.

============================================================
"""

from __future__ import annotations

import os

from app.terminal.theme import console, rule


def clear() -> None:

    os.system("cls" if os.name == "nt" else "clear")


def header(title: str, subtitle: str = "") -> None:

    clear()

    rule(f"STACKED ONE TERMINAL  │  {title}")

    if subtitle:
        console.print(f"[muted]{subtitle}[/muted]\n")


def footer(hint: str = "Enter = continue, b = back") -> None:

    console.print()

    rule()

    console.print(f"[muted]{hint}[/muted]")
