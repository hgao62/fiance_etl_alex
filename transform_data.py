import pandas as pd
import numpy as np

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