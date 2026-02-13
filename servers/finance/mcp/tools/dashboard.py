"""
Company Snapshot Card — FastMCP + Prefab + yfinance demo

A single MCP tool that returns a rich dashboard showing key financial
metrics for any publicly traded company.

Usage:
    uv run company_snapshot.py          # starts the MCP server
    prefab serve company_snapshot.py    # preview in browser
"""

from __future__ import annotations

import yfinance as yf
from fastmcp.tools import tool
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Badge,
    Card,
    CardContent,
    CardHeader,
    CardDescription,
    CardTitle,
    Column,
    Dashboard,
    DashboardItem,
    Metric,
    Muted,
    Row,
    Separator,
    Text,
)
from prefab_ui.components.charts import AreaChart, ChartSeries


# ── helpers ────────────────────────────────────────────────────────────


def _fmt_large_number(n: float | None) -> str:
    """Format large numbers into human-readable strings (e.g. 3.45T)."""
    if n is None:
        return "N/A"
    abs_n = abs(n)
    if abs_n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:,.2f}T"
    if abs_n >= 1_000_000_000:
        return f"${n / 1_000_000_000:,.2f}B"
    if abs_n >= 1_000_000:
        return f"${n / 1_000_000:,.2f}M"
    return f"${n:,.2f}"


def _fmt_number(n: float | None, prefix: str = "", suffix: str = "") -> str:
    if n is None:
        return "N/A"
    return f"{prefix}{n:,.2f}{suffix}"


def _pct_change(current: float | None, previous: float | None) -> str | None:
    """Return a formatted percent-change string, or None."""
    if current is None or previous is None or previous == 0:
        return None
    delta = ((current - previous) / abs(previous)) * 100
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f}%"


# ── tool ───────────────────────────────────────────────────────────────


@tool(
    annotations={
        "title": "Company Snapshot",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def company_snapshot(ticker: str = "AAPL") -> PrefabApp:
    """
    Show a rich snapshot dashboard for a publicly traded company.

    Displays key financial metrics (market cap, P/E, EPS, dividend yield,
    52-week range) alongside a 3-month price chart.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, MSFT, GOOGL)
    """

    stock = yf.Ticker(ticker.upper())
    info = stock.info

    # ── pull data ──────────────────────────────────────────────────────
    name = info.get("shortName", ticker.upper())
    sector = info.get("sector", "Unknown")
    industry = info.get("industry", "")
    currency = info.get("currency", "USD")

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    previous_close = info.get("regularMarketPreviousClose")
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")
    fifty_two_wk_high = info.get("fiftyTwoWeekHigh")
    fifty_two_wk_low = info.get("fiftyTwoWeekLow")
    volume = info.get("regularMarketVolume")
    avg_volume = info.get("averageDailyVolume10Day")
    beta = info.get("beta")

    day_change = _pct_change(current_price, previous_close)

    # 3-month price history for the chart
    hist = stock.history(period="3mo")
    chart_data = [
        {"date": d.strftime("%b %d"), "price": round(row["Close"], 2)}
        for d, row in hist.iterrows()
    ]

    # ── build the view ─────────────────────────────────────────────────
    with Dashboard(columns=12, rowHeight=120, gap=4, cssClass="p-6") as view:
        # ── Row 1: header card spanning full width ─────────────────────
        with DashboardItem(col=1, row=1, colSpan=12, rowSpan=1):
            with Card(cssClass="h-full"):
                with CardHeader():
                    with Row(align="center", cssClass="justify-between"):
                        with Column(gap=1):
                            CardTitle(f"{name}  ({ticker.upper()})")
                            CardDescription(f"{sector}  ·  {industry}")
                        with Row(gap=2, align="center"):
                            Badge(sector, variant="default")
                            Badge(
                                f"{currency}",
                                variant="outline",
                            )

        # ── Row 2: key metrics (4 Metric cards) ───────────────────────
        with DashboardItem(col=1, row=2, colSpan=3, rowSpan=1):
            with Card(cssClass="h-full"):
                with CardContent():
                    Metric(
                        label="Price",
                        value=_fmt_number(current_price, prefix="$"),
                        delta=day_change,
                    )

        with DashboardItem(col=4, row=2, colSpan=3, rowSpan=1):
            with Card(cssClass="h-full"):
                with CardContent():
                    Metric(
                        label="Market Cap",
                        value=_fmt_large_number(market_cap),
                    )

        with DashboardItem(col=7, row=2, colSpan=3, rowSpan=1):
            with Card(cssClass="h-full"):
                with CardContent():
                    Metric(
                        label="P/E (TTM)",
                        value=_fmt_number(pe_ratio) if pe_ratio else "N/A",
                        delta=(
                            f"Fwd: {forward_pe:.2f}" if forward_pe else None
                        ),
                    )

        with DashboardItem(col=10, row=2, colSpan=3, rowSpan=1):
            with Card(cssClass="h-full"):
                with CardContent():
                    Metric(
                        label="EPS (TTM)",
                        value=_fmt_number(eps, prefix="$"),
                    )

        # ── Row 3: chart (8 cols) + details panel (4 cols) ────────────
        with DashboardItem(col=1, row=3, colSpan=8, rowSpan=2):
            with Card(cssClass="h-full"):
                with CardHeader():
                    CardTitle("3-Month Price History")
                with CardContent():
                    AreaChart(
                        data=chart_data,
                        series=[
                            ChartSeries(dataKey="price", label="Close"),
                        ],
                        xAxis="date",
                        height=200,
                        showTooltip=True,
                        showGrid=True,
                    )

        with DashboardItem(col=9, row=3, colSpan=4, rowSpan=2):
            with Card(cssClass="h-full"):
                with CardHeader():
                    CardTitle("Details")
                with CardContent():
                    with Column(gap=3):
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("52-Wk High")
                            Text(_fmt_number(fifty_two_wk_high, prefix="$"))
                        Separator()
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("52-Wk Low")
                            Text(_fmt_number(fifty_two_wk_low, prefix="$"))
                        Separator()
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("Dividend Yield")
                            Text(
                                _fmt_number(
                                    (dividend_yield or 0) * 100, suffix="%"
                                )
                                if dividend_yield
                                else "N/A"
                            )
                        Separator()
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("Volume")
                            Text(f"{volume:,}" if volume else "N/A")
                        Separator()
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("Avg Volume (10d)")
                            Text(f"{avg_volume:,}" if avg_volume else "N/A")
                        Separator()
                        with Row(
                            align="center", cssClass="justify-between"
                        ):
                            Muted("Beta")
                            Text(
                                f"{beta:.2f}" if beta else "N/A"
                            )

    return PrefabApp(
        title=f"{ticker.upper()} Snapshot",
        view=view,
    )
