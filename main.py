import extract_data
import transform_data

if __name__ == '__main__':
    hist = extract_data.get_stock_history('META','ytd','1d')
    fx_rates = extract_data.get_exchange_rate('GBP','USD','ytd','1d')
    cur = extract_data.get_stock_currency_code('META')
    news = extract_data.get_news('TSLA')
    df_normalized = transform_data.normalize_stock_data(hist)

    