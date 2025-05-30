from extract_data import get_stock_history, get_news, get_stock_currency_code
from transform_data import add_stock_returns, normalize_stock_data, standardize_price_to_usd,calculate_moving_average
import load_data
import pandas as pd

def run_pipeline(
    tickers: list[str],
    period: str = "1mo",
    interval: str = "1d",)->None:
    for ticker in tickers:
        '''Run the ETL pipeline for a list of stock tickers.
        Args:
        tickers (list[str]): List of stock tickers to process.
        period (str): Period for stock history (default: "1mo"). 
        interval (str): Interval for stock history (default: "1d")
        Returns:
        '''
        # Extract stock history
        stock_history = get_stock_history(ticker, period, interval)
        news = get_news(ticker)
        
        # Transform stock history
        stock_history = add_stock_returns(stock_history)
        stock_history = standardize_price_to_usd(stock_history)
        stock_history = normalize_stock_data(stock_history)
        stock_history = calculate_moving_average(stock_history, window=5)

        # Load to database
        load_data.save_df_to_db(stock_history, table_name="stock_history")
        load_data.save_df_to_db(news, table_name="news")


if __name__ == '__main__':
    tickers = ['AAPL', 'SHOP.TO', 'MSFT', 'AMZN', 'TSLA']
    run_pipeline(tickers)



    