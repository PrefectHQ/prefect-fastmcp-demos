from yfinance import Ticker
from yfinance.scrapers.quote import Quote

def ticker(symbol) -> Ticker:
    return Ticker(symbol)

def current_price(symbol) -> Quote:
    info = ticker(symbol).get_info()
    return info['regularMarketPrice']

def history(symbol, period='1mo', interval='1d'):
    data = ticker(symbol).history(period=period, interval=interval)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].astype(str)
    return data.to_dict(orient='records')
