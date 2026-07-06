"""
============================================================

                    STACKED ONE

                RESULTS TABLE

============================================================
"""

from __future__ import annotations

from rich.table import Table

from app.terminal import engine_bridge
from app.terminal.theme import console, pnl_style

SPARK_CHARS = "▁▂▃▄▅▆▇█"


def sparkline(values: list[float], width: int = 40) -> str:

    if not values:
        return ""

    if len(values) > width:

        step = len(values) / width

        sampled = [values[int(i * step)] for i in range(width)]

    else:

        sampled = values

    low = min(sampled)

    high = max(sampled)

    span = high - low

    if span == 0:
        return SPARK_CHARS[0] * len(sampled)

    chars = []

    for value in sampled:

        position = (value - low) / span

        index = min(int(position * (len(SPARK_CHARS) - 1)), len(SPARK_CHARS) - 1)

        chars.append(SPARK_CHARS[index])

    return "".join(chars)


def render_results(result: engine_bridge.SimulationResult) -> None:

    table = Table(
        title=f"Backtest Results  -  {result.strategy or 'All Strategies'}  ({result.symbol} / {result.timeframe})",
        border_style="accent",
        header_style="heading",
        show_header=False,
    )

    table.add_column("Metric", style="label")
    table.add_column("Value", style="value", justify="right")

    def add(label: str, value: str, style: str | None = None) -> None:

        table.add_row(label, f"[{style}]{value}[/{style}]" if style else value)

    add("Total Trades", str(result.total_trades))
    add("Winning Trades", str(result.winning_trades))
    add("Losing Trades", str(result.losing_trades))
    add("Breakeven Trades", str(result.breakeven_trades))
    add("Win Rate", f"{result.win_rate:.2%}")
    add("Net Profit", f"{result.net_profit:,.2f}", pnl_style(result.net_profit))
    add("Gross Profit", f"{result.gross_profit:,.2f}", "positive")
    add("Gross Loss", f"-{result.gross_loss:,.2f}" if result.gross_loss else "0.00", "negative")
    add("Profit Factor", f"{result.profit_factor:.2f}")
    add("Sharpe Ratio", f"{result.sharpe_ratio:.2f}")
    add("Expectancy", f"{result.expectancy:,.2f}", pnl_style(result.expectancy))
    add("Max Drawdown", f"{result.max_drawdown:,.2f}", "negative" if result.max_drawdown else None)
    add("Ending Equity", f"{result.ending_equity:,.2f}")

    console.print(table)

    console.print("\n[heading]Equity Curve Summary[/heading]")

    curve = result.equity_curve

    if len(curve) > 1:

        console.print(f"  [accent]{sparkline(curve)}[/accent]")

        console.print(
            f"  [label]Start:[/label] {curve[0]:,.2f}   "
            f"[label]Min:[/label] {min(curve):,.2f}   "
            f"[label]Max:[/label] {max(curve):,.2f}   "
            f"[label]End:[/label] {curve[-1]:,.2f}   "
            f"[label]Points:[/label] {len(curve)}",
        )

    else:

        console.print("  [muted]No trades were closed during this run.[/muted]")
