"""
============================================================

                    STACKED ONE

                TERMINAL STATE

------------------------------------------------------------

Persisted terminal settings (JSON) plus in-session objects
that outlive a single screen.

Every backtest/live run calls Simulator.reset() internally,
which wipes its PositionManager / PerformanceManager /
AnalyticsManager clean. So "session" here always means
"since the last run started" - not a cross-run accumulation.

============================================================
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from app.terminal import engine_bridge

SETTINGS_PATH = Path(__file__).resolve().parents[2] / "data" / "terminal_settings.json"


# ==========================================================
# Persisted Settings
# ==========================================================


@dataclass
class TerminalSettings:

    initial_capital: float = 100_000.0

    risk_per_trade: float = 1.0

    leverage: float = 1.0

    default_symbol: str = "BTCUSD"

    default_timeframe: str = "1m"

    default_strategy: str = "All Strategies"

    disabled_strategies: list[str] = field(default_factory=list)

    # =====================================================

    @classmethod
    def load(cls) -> TerminalSettings:

        if SETTINGS_PATH.exists():

            try:

                data = json.loads(
                    SETTINGS_PATH.read_text(encoding="utf-8"),
                )

                known = {f: data[f] for f in cls.__dataclass_fields__ if f in data}

                return cls(**known)

            except (json.JSONDecodeError, TypeError, ValueError):

                pass

        return cls()

    # =====================================================

    def save(self) -> None:

        SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)

        SETTINGS_PATH.write_text(
            json.dumps(asdict(self), indent=2),
            encoding="utf-8",
        )


# ==========================================================
# Closed Trade Record (terminal-side trade blotter)
# ==========================================================


@dataclass(slots=True)
class ClosedTradeRecord:

    symbol: str

    side: str

    strategy: str

    entry_price: float

    exit_price: float

    quantity: float

    pnl: float

    reason: str

    opened_at: str

    closed_at: str

    # =====================================================

    @classmethod
    def from_step(
        cls,
        step: engine_bridge.SimulationStep,
        fallback_symbol: str = "",
    ) -> ClosedTradeRecord:
        """
        Builds a blotter row from a SimulationStep whose
        closed_trade is set. The engine doesn't retain closed
        positions itself (PositionManager only tracks open
        ones), so the terminal captures the detail at the
        moment iter_run() yields it.

        fallback_symbol covers a pre-existing gap upstream:
        RiskEngine builds TradePlan without a symbol, so
        Position.symbol ends up "" for every trade. The
        terminal already knows which symbol it configured
        the run for, so it fills the display gap without
        touching RiskEngine.
        """

        assert step.closed_trade is not None

        position = step.closed_trade.closed_position

        assert position is not None

        last_execution = position.executions[-1] if position.executions else None

        return cls(
            symbol=position.symbol or fallback_symbol,
            side=position.side.value,
            strategy=step.entry_plan.strategy if step.entry_plan else "",
            entry_price=position.average_price,
            exit_price=last_execution.executed_price if last_execution else position.average_price,
            quantity=position.max_quantity,
            pnl=step.closed_trade.realized_pnl,
            reason=step.exit_decision.reason.value if step.exit_decision else "",
            opened_at=position.opened_at.isoformat() if position.opened_at else "",
            closed_at=position.closed_at.isoformat() if position.closed_at else "",
        )


# ==========================================================
# Session (reflects the most recent run)
# ==========================================================


@dataclass
class SessionResults:

    mode: str | None = None

    symbol: str | None = None

    timeframe: str | None = None

    strategy_label: str | None = None

    result: engine_bridge.SimulationResult | None = None

    simulator: engine_bridge.Simulator | None = None

    trades: list[ClosedTradeRecord] = field(default_factory=list)

    last_price: float | None = None

    last_snapshot: engine_bridge.AnalyticsSnapshot | None = None

    last_grade: str | None = None

    last_confidence: float | None = None

    running: bool = False

    # =====================================================

    @property
    def has_data(self) -> bool:

        return self.simulator is not None

    @property
    def open_positions(self) -> tuple[engine_bridge.Position, ...]:

        if self.simulator is None:
            return ()

        return self.simulator.positions.positions


# ==========================================================
# Terminal State
# ==========================================================


class TerminalState:

    def __init__(self) -> None:

        self.settings = TerminalSettings.load()

        self.session = SessionResults()

        self._apply_disabled_strategies()

    # =====================================================
    # Strategy Enable / Disable
    # =====================================================

    def _apply_disabled_strategies(self) -> None:

        disabled = set(self.settings.disabled_strategies)

        for cls in engine_bridge.strategy_classes():

            engine_bridge.set_strategy_enabled(
                cls,
                cls.metadata.name not in disabled,
            )

    def set_strategy_enabled(self, name: str, enabled: bool) -> None:

        classes = engine_bridge.strategy_classes_by_name()

        cls = classes.get(name)

        if cls is None:
            return

        engine_bridge.set_strategy_enabled(cls, enabled)

        disabled = set(self.settings.disabled_strategies)

        if enabled:
            disabled.discard(name)
        else:
            disabled.add(name)

        self.settings.disabled_strategies = sorted(disabled)

        self.settings.save()

    # =====================================================
    # Session
    # =====================================================

    def new_session(self, mode: str, symbol: str, timeframe: str, strategy_label: str) -> SessionResults:

        self.session = SessionResults(
            mode=mode,
            symbol=symbol,
            timeframe=timeframe,
            strategy_label=strategy_label,
        )

        return self.session
