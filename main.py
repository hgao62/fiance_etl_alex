import extract_data
import transform_data

if __name__ == '__main__':
    hist = extract_data.get_stock_history('SHOP.TO','ytd','1d')
    fx_rates = extract_data.get_exchange_rate('CAD','USD','ytd','1d')
    # cur = extract_data.get_stock_currency_code('SHOP.TO')
    news = extract_data.get_news('TSLA')
    df_normalized = transform_data.normalize_stock_data(hist)
    df_added_returns = transform_data.add_stock_returns(df_normalized)
    df_added_us_price = transform_data.standardize_price_to_usd(df_added_returns)
    df_added_moving_avg = transform_data.calculate_moving_average(df_added_us_price, 5)

    