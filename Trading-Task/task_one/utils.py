import yfinance as yf

def download_trading_data(tickers="EURUSD=X", period="1mo", interval="5m"):   
    data = yf.download(tickers=tickers, period=period, interval=interval)
    data.to_csv("trading_data.csv")

    print('Data Saved.')

download_trading_data()