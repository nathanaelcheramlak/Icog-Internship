import yfinance as yf
import pandas as pd

def download_trading_data(tickers="EURUSD=X", period="1mo", interval="5m"):   
    data = yf.download(tickers=tickers, period=period, interval=interval)
    
    # Remove the ticker row
    if len(data) > 1:  
        data.columns = [col[0] for col in data.columns.values]
        data.reset_index(drop=False, inplace=True)

    # Convert only numeric-compatible columns (excluding Date column)
    numeric_cols = data.select_dtypes(include=['number']).columns
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric)

    data.dropna()
    data.to_csv("../trading_data.csv", index=False)

    print('Data downloaded and exported successfully.')

download_trading_data()