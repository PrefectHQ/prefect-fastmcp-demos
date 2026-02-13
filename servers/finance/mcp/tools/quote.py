from fastmcp.tools import tool

from utils.ticker import current_price


@tool(
    annotations={
        "title": "Stock Price Quote",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def quote(symbol: str) -> str:
    """
    Get the current stock price for a given ticker symbol.
    """
    
    price = current_price(symbol)
    return f"Current price for {symbol}: ${price}"
