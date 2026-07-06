"""
============================================================

                    STACKED ONE

                TERMINAL THEME

------------------------------------------------------------

Shared rich Console, color palette and branding for every
screen in the terminal package.

============================================================
"""

from __future__ import annotations

from rich.console import Console
from rich.theme import Theme

# ==========================================================
# Palette
# ==========================================================

STACKED_THEME = Theme(
    {
        "brand": "bold bright_cyan",
        "accent": "bright_cyan",
        "muted": "grey62",
        "positive": "bold bright_green",
        "negative": "bold bright_red",
        "neutral": "bright_yellow",
        "heading": "bold white",
        "label": "grey74",
        "value": "bold white",
        "grade.a": "bold bright_green",
        "grade.b": "bold green",
        "grade.c": "bold bright_yellow",
        "grade.d": "bold dark_orange",
        "grade.f": "bold bright_red",
        "danger": "bold white on red",
        "ok": "bold black on bright_green",
    }
)

console = Console(theme=STACKED_THEME, highlight=False)

# ==========================================================
# Branding
# ==========================================================

BANNER = r"""
[brand] ____ _____ _    ____ _  _____ ____    ___  _   _ _____ [/brand]
[brand]/ ___|_   _/ \  / ___| |/ / ____|  _ \  / _ \| \ | | ____|[/brand]
[brand]\___ \ | |/ _ \| |   | ' /|  _| | | | || | | |  \| |  _|  [/brand]
[brand] ___) || / ___ \ |___| . \| |___| |_| || |_| | |\  | |___ [/brand]
[brand]|____/ |_/_/   \_\____|_|\_\_____|____/  \___/|_| \_|_____|[/brand]
"""

TAGLINE = "Institutional-Grade Quantitative Trading Terminal"


def print_banner() -> None:

    console.print(BANNER)

    console.print(
        f"[muted]{TAGLINE:^62}[/muted]\n",
    )


def rule(title: str = "") -> None:

    console.rule(
        f"[heading]{title}[/heading]" if title else "",
        style="accent",
    )


def grade_style(grade: str) -> str:

    mapping = {
        "A+": "grade.a",
        "A": "grade.a",
        "B": "grade.b",
        "C": "grade.c",
        "D": "grade.d",
        "F": "grade.f",
    }

    return mapping.get(grade, "muted")


def pnl_style(value: float) -> str:

    if value > 0:
        return "positive"

    if value < 0:
        return "negative"

    return "muted"
