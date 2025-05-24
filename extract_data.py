import yfinance as yf
import pandas as pd


def get_stock_history(stock: str, period: str, interval: str) -> pd.DataFrame:
    """Pull stock history given a stock input.

    Args:
        stock (str): text
        period (str): valid periods - 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval (str): Valid intervals - 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    Returns:
        pd.DataFrame: DataFrame
    """
    yf_data = yf.Ticker(stock)
    hist = yf_data.history(period=period, interval=interval)
    hist.reset_index(inplace=True)
    hist = hist[['Date','Open','High','Low','Close','Volume','Dividends']]  # remove last column
    hist["Stock"] = stock  # Add a new column with the stock variable

    return hist

def get_exchange_rate(
    from_currency: str, to_currency: str, period: str, interval: str
) -> pd.DataFrame:
    """Download fx rate from yfinance.

    Args:
        base (str): base currency
        quote (str): quote currency
        period (str): valid periods - 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        interval (str): Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    Returns:
        pd.DataFrame: DataFrame
    """
    fx_rate_ticker = f"{from_currency}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval)
    fx_rates.columns = [
        col[0] for col in fx_rates.columns
    ]  # Keep only the first level of the MultiIndex
    fx_rates["Ticker"] = fx_rate_ticker
    fx_rates.reset_index(inplace=True)
    fx_rates["From Currency"] = from_currency
    fx_rates["To Currency"] = to_currency
    fx_rates = fx_rates[
        [
            "Date",
            "Ticker",
            "From Currency",
            "To Currency",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]
    ]
    fx_rates["Adj Close"] = fx_rates["Close"]  # add 'Adj Close'
    fx_rates = fx_rates.drop(columns=["Volume"])  # drop 'Close' column

    return fx_rates


def get_stock_currency_code(stock: str) -> str:
    """Get the currency code for a given stock.

    Args:
        stock (str): stock ticker

    Returns:
        str: currency code
    """
    dat = yf.Ticker(stock)
    cur = dat.fast_info["currency"]
    return cur


def get_news(stock: str) -> pd.DataFrame:
    """Get news for a given stock.

    Args:
        stock (str): stock ticker

    Returns:
        pd.DataFrame: DataFrame with news
    """
    dat = yf.Ticker(stock)
    news = dat.news
    news_df = pd.DataFrame(news)
    content_df = pd.json_normalize(news_df["content"])
    content_df["stock"] = stock
    content_df = content_df.rename(
        columns={
            "stock": "stock",
            "id": "uuid",
            "title": "title",
            "provider.displayName": "publisher",
            "previewUrl": "link",
            "contentType": "type",
        }
    )
    content_df = content_df[["stock", "uuid", "title", "publisher", "link", "type"]]
    return content_df

get_stock_history('META','ytd','1d')