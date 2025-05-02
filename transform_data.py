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
    df_normalized = stock_history['Open','High','Low','Close'].round(2)
    df_normalized = df_normalized.rename(columns={'Date': 'Trade_Date'})
    
    return df_normalized