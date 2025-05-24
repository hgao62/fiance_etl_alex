import pandas as pd
import numpy as np
import extract_data as ed

def normalize_stock_data(stock_history:pd.DataFrame)->pd.DataFrame:
    """Normalize the data in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to be normalized

    Returns:
        pd.DataFrame: Normalized DataFrame
    """
    # Normalize the data
    stock_history[['Open', 'High', 'Low', 'Close']] = stock_history[['Open','High','Low','Close']].round(2)
    stock_history = stock_history.rename(columns={'Date': 'Trade_Date'})
    
    return stock_history

def add_stock_returns(stock_history:pd.DataFrame)->pd.DataFrame:
    """This function adds two columns to stock_history data frame
        a. "daily_return": this is caluclated using the "close" price column, google "how to calcualte daily return pandas"
        b. "cummulative_return": this is caculated using the "daily_return" caculated from step above(see stackoverflow below)
        https://stackoverflow.com/questions/35365545/calculating-cumulative-returns-with-pandas-dataframe

    Args:
        df (pd.DataFrame): DataFrame to add stock returns to

    Returns:
        pd.DataFrame: DataFrame with stock returns
    """
    # Calculate daily return
    stock_history['daily_return'] = stock_history['Close'].pct_change(by='Date')
    
    # Calculate cumulative return
    stock_history['cumulative_return'] = (1 + stock_history['daily_return']).cumprod() - 1
    
    return stock_history

def standardize_price_to_usd(stock_history:pd.DataFrame)->pd.DataFrame:
    """Standardize the price to USD using the exchange rate.

    Args:
        stock_history (pd.DataFrame): DataFrame with stock history
        fx_rates (pd.DataFrame): DataFrame with exchange rates

    Returns:
        pd.DataFrame: DataFrame with standardized prices
    """
    cur = ed.get_stock_currency_code(stock_history['Stock'][0])
    # Get currency code for the stock
    stock_history['currency_code'] = cur

    if cur == 'USD':
        stock_history['usd_close'] = stock_history['Close']
    else:
        # Get exchange rate for the stock
        fx_rates = ed.get_exchange_rate(cur, 'USD', 'ytd', '1d')
        stock_history['usd_close'] = stock_history['Close'] * fx_rates['Close']

    
    return stock_history

def calculate_moving_average(stock_history:pd.DataFrame, window:int = 5 )->pd.DataFrame:
    """Calculate the moving average for 5 days window.

    Args:
        stock_history (pd.DataFrame): DataFrame with stock history
        window (int): Window size for moving average

    Returns:
        pd.DataFrame: DataFrame with moving average
    """
    stock_history['moving_average'] = stock_history['Close'].rolling(window=window).mean()
    
    return stock_history

def get_top_bottom_days(stock_history:pd.DataFrame, top:int = 5, bottom:int = 5)->pd.DataFrame:
    """Get the top and bottom days for the stock.

    Args:
        stock_history (pd.DataFrame): DataFrame with stock history
        top (int): Number of top days to get
        bottom (int): Number of bottom days to get

    Returns:
        pd.DataFrame: DataFrame with top and bottom days
    """
    # Get top and bottom days
    top_days = stock_history.nlargest(top, 'Close')
    bottom_days = stock_history.nsmallest(bottom, 'Close')
    
    return pd.concat([top_days, bottom_days])

def group_by_sector(stock_history:pd.DataFrame)->pd.DataFrame:
    """Group the stock history by sector.

    Args:
        stock_history (pd.DataFrame): DataFrame with stock history
        sector (str): Sector to group by

    Returns:
        pd.DataFrame: DataFrame with grouped stock history
    """
    # Group by sector
    grouped = stock_history.groupby('sector').agg(
        avg_close=('Close', 'mean'),
        avg_volume=('Volume', 'mean'),
    ).reset_index()
    
    return grouped


