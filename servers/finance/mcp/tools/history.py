from fastmcp.tools import tool
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading, Muted
from prefab_ui.components.charts import LineChart, ChartSeries

from utils.ticker import history


@tool(
    annotations={
        "title": "Price History Chart",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def price_history(
    symbols: list[str],
    period: str = "1mo",
    interval: str = "1d",
) -> PrefabApp:
    """
    Generate a price history chart comparing one or more stock symbols.

    When multiple symbols are provided, prices are normalized to percent
    change from the first trading day so differently-priced stocks can be
    compared on the same scale.

    Args:
        symbols:  One or more ticker symbols (e.g. ["AAPL"] or ["AAPL", "MSFT", "GOOGL"])
        period:   Data period — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, ytd, max
        interval: Data interval — 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    symbols = [s.upper() for s in symbols]
    multi = len(symbols) > 1

    # ── fetch & merge data ─────────────────────────────────────────────
    # Build a dict of {date_str: {sym1: val, sym2: val, ...}}
    merged: dict[str, dict] = {}
    baselines: dict[str, float] = {}

    for sym in symbols:
        prices = history(sym, period, interval)
        if not prices:
            continue

        baseline = prices[0]["Close"]
        baselines[sym] = baseline

        for row in prices:
            date = row["Date"]
            entry = merged.setdefault(date, {"date": date})
            if multi:
                entry[sym] = round(
                    ((row["Close"] - baseline) / baseline) * 100, 2
                )
            else:
                entry[sym] = row["Close"]

    chart_data = list(merged.values())

    series = [ChartSeries(dataKey=sym, label=sym) for sym in symbols if sym in baselines]

    # ── build view ─────────────────────────────────────────────────────
    title = (
        f"{symbols[0]} Price History"
        if len(symbols) == 1
        else f"Performance Comparison: {', '.join(symbols)}"
    )

    with Column(gap=4, cssClass="p-6") as view:
        Heading(title)
        if multi:
            Muted("Normalized to % change from first trading day in range")
        LineChart(
            data=chart_data,
            series=series,
            xAxis="date",
            showDots=len(chart_data) <= 40,
            showTooltip=True,
            showLegend=multi,
            showGrid=True,
        )

    return PrefabApp(view=view)
