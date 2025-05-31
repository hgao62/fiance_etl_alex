import pytest
import os
from transform_data import add_stock_returns, normalize_stock_data, calculate_moving_average
import pandas as pd

def test_add_stock_returns_valid():
    # Create a sample DataFrame with stock prices
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'Open': [100, 102, 101, 105, 107],
        'High': [101, 103, 102, 106, 108],
        'Low': [99, 101, 100, 104, 106],
        'Close': [100, 102, 101, 105, 107]
    }
    df = pd.DataFrame(data)

    # Apply the function
    result = add_stock_returns(df)

    # Check if daily_return and cumulative_return are calculated correctly
    assert 'daily_return' in result.columns
    assert 'cumulative_return' in result.columns
    assert result['daily_return'].iloc[0] is None  # First row should be NaN
    assert result['cumulative_return'].iloc[0] == -1.0  # First row cumulative return should be -1.0


def test_normalize_stock_data_valid():
    # Create a sample DataFrame with stock prices
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'Open': [100, 102, 101, 105, 107],
        'High': [101, 103, 102, 106, 108],
        'Low': [99, 101, 100, 104, 106],
        'Close': [100, 102, 101, 105, 107]
    }
    df = pd.DataFrame(data)

    # Apply the function
    result = normalize_stock_data(df)

    # Check if the columns are renamed correctly and data is normalized
    assert 'Trade_Date' in result.columns
    assert all(result[['Open', 'High', 'Low', 'Close']].applymap(lambda x: isinstance(x, (int, float))))  # Check if values are numeric


def test_calculate_moving_average_valid():
    # Create a sample DataFrame with stock prices
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=5, freq='D'),
        'Open': [100, 102, 101, 105, 107],
        'High': [101, 103, 102, 106, 108],
        'Low': [99, 101, 100, 104, 106],
        'Close': [100, 102, 101, 105, 107]
    }
    df = pd.DataFrame(data)

    # Apply the function
    result = calculate_moving_average(df)

    # Check if the moving average is calculated correctly
    assert 'MA_5' in result.columns
    assert result['MA_5'].iloc[0] is None  # First row should be NaN
    assert result['MA_5'].iloc[4] == (100 + 102 + 101 + 105 + 107) / 5  # Last row should be the average of all values