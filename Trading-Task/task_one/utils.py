import yfinance as yf
import numpy as np
import pandas as pd

def download_trading_data(trinker="EURUSD=X", period="1mo", interval="15m"):    
    data = yf.download(trinker, period, interval)
    data.to_csv("trading_data.csv")

offline_data = pd.read_csv('trading_data.csv')
print(offline_data.count())