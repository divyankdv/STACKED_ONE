"""
============================================================

                    STACKED ONE

            POSITION UPDATE RESULT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.portfolio.position import Position


@dataclass(slots=True)
class PositionUpdateResult:
    """
    Result returned by PositionManager after processing
    an ExecutionReport.
    """

    previous_position: Position | None = None

    current_position: Position | None = None

    closed_position: Position | None = None

    opened_new_position: bool = False

    closed_existing_position: bool = False

    position_flipped: bool = False

    realized_pnl: float = 0.0