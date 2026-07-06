"""
============================================================

                    STACKED ONE

                    TERMINAL

------------------------------------------------------------

Official entry point.

    python main.py

============================================================
"""

from __future__ import annotations

import sys


def _ensure_utf8_console() -> None:
    """
    Windows consoles/redirected streams often default to a
    legacy codepage (cp1252) that cannot encode the box-
    drawing characters rich uses for tables and rules. Force
    UTF-8 so the terminal never crashes on startup.
    """

    for stream in (sys.stdout, sys.stderr):

        reconfigure = getattr(stream, "reconfigure", None)

        if reconfigure is not None:

            reconfigure(encoding="utf-8", errors="replace")


_ensure_utf8_console()

from app.terminal.terminal import Terminal  # noqa: E402


def main() -> None:

    Terminal().run()


if __name__ == "__main__":

    main()
