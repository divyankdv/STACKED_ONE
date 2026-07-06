"""
============================================================

                    STACKED ONE

                MARKET ANALYTICS

============================================================
"""

from __future__ import annotations

from rich.columns import Columns
from rich.panel import Panel

from app.terminal.screens.base import footer, header
from app.terminal.state import TerminalState
from app.terminal.theme import console, grade_style
from app.terminal.widgets.prompts import pause


def show_analytics(state: TerminalState) -> None:

    header(
        "MARKET ANALYTICS",
        f"{state.session.symbol or ''} {state.session.timeframe or ''}".strip(),
    )

    session = state.session

    if not session.has_data or session.last_snapshot is None:

        console.print("[muted]No data yet. Run a Historical Backtest or start Live Paper Trading first.[/muted]")

        footer()

        pause()

        return

    snapshot = session.last_snapshot

    order_flow = snapshot.order_flow
    cvd = snapshot.cvd
    absorption = snapshot.absorption
    iceberg = snapshot.iceberg
    large_trades = snapshot.large_trades

    panels = [
        Panel(
            f"Buy Volume   : {order_flow.buy_volume:,.2f}\n"
            f"Sell Volume  : {order_flow.sell_volume:,.2f}\n"
            f"Delta        : {order_flow.delta:,.2f}\n"
            f"Buy Aggr.    : {order_flow.buy_aggression:.1f}%\n"
            f"Sell Aggr.   : {order_flow.sell_aggression:.1f}%\n"
            f"VWAP         : {order_flow.vwap:,.2f}\n"
            f"Trades       : {order_flow.trade_count}",
            title="Order Flow",
            border_style="accent",
        ),
        Panel(
            f"Current      : {cvd.current:,.2f}\n"
            f"Highest      : {cvd.highest:,.2f}\n"
            f"Lowest       : {cvd.lowest:,.2f}\n"
            f"Trades       : {cvd.trade_count}",
            title="CVD",
            border_style="accent",
        ),
        Panel(
            f"Active       : {'YES' if absorption.active else 'no'}\n"
            f"Bullish Score: {absorption.bullish_score:.2f}\n"
            f"Bearish Score: {absorption.bearish_score:.2f}\n"
            f"Absorbed Vol : {absorption.absorbed_volume:,.2f}\n"
            f"Last Price   : {absorption.last_price:,.2f}",
            title="Absorption",
            border_style="accent",
        ),
        Panel(
            f"Active       : {'YES' if iceberg.active else 'no'}\n"
            f"Side         : {iceberg.side}\n"
            f"Price        : {iceberg.price:,.2f}\n"
            f"Absorbed Vol : {iceberg.absorbed_volume:,.2f}\n"
            f"Trade Count  : {iceberg.trade_count}\n"
            f"Confidence   : {iceberg.confidence:.2f}",
            title="Icebergs",
            border_style="accent",
        ),
        Panel(
            f"Total        : {large_trades.total_large_trades}\n"
            f"Buy Side     : {large_trades.buy_large_trades}\n"
            f"Sell Side    : {large_trades.sell_large_trades}\n"
            f"Largest      : {large_trades.largest_trade:,.2f}\n"
            f"Avg Size     : {large_trades.average_large_trade:,.2f}",
            title="Large Trades",
            border_style="accent",
        ),
    ]

    console.print(Columns(panels, equal=True, expand=True))

    if session.last_price is not None:

        console.print(f"\n[label]Last Price:[/label] [value]{session.last_price:,.2f}[/value]")

    if session.last_grade is not None:

        style = grade_style(session.last_grade)

        console.print(
            f"[label]Last Confluence Grade:[/label] [{style}]{session.last_grade}[/{style}]  "
            f"[label]Confidence:[/label] {session.last_confidence:.2f}",
        )

    footer()

    pause()
