'''
Date    Open    Close   Volume   Trend   FVG     LiquidityGrabHigh LiquidityGrabLow      Target
'''
import pandas as pd

df = pd.read_csv('../../trading_data.csv')

# df.drop(index=[0, 1], inplace=True)
# df.reset_index(drop=True, inplace=True)

# for column in df.columns[1:]:
#     df[column] = pd.to_numeric(df[column])


# Trend
df['Trend'] = 0
df['MA_5'] = df["Close"].rolling(window=5).mean()

# Upward Trend
df.loc[df['Close'] > df['MA_5'], 'Trend'] = 1

# Downward Trend
df.loc[df['Close'] < df['MA_5'], 'Trend'] = -1


# FVG
df['FVG'] = 0
for i in range(2, len(df)):
    backward = df.loc[i - 2]
    forward = df.loc[i]

    # Upward FVG
    if backward['Low'] > forward['High']:
        df.loc[i, 'FVG'] = 1
    # Downward FVG
    elif backward['High'] < forward['Low']:
        df.loc[i, 'FVG'] = -1


# Liquidity Grab
df['LiquidityGrabHigh'] = 0
df['LiquidityGrabLow'] = 0
lockback = 5

for i in range(lockback, len(df)):
    prev_high = df.loc[i - lockback: i - 1, 'High'].max()
    prev_low = df.loc[i - lockback: i - 1, 'Low'].min()

    curr_high = df.loc[i, 'High']
    curr_low = df.loc[i, 'Low']

    if curr_high > prev_high:
        df.loc[i, 'LiquidityGrabHigh'] = 1

    if curr_low < prev_high:
        df.loc[i, 'LiquidityGrabLow'] = 1


# Target
df["Target"] = df["Close"].shift(-1)

# 1 -> Buy
# 0 -> Sell
# Label
future_window = 20
for i in range(len(df) - future_window):
    future_avg = df.loc[i + 1: i + future_window ,'Close'].mean()
    if df.loc[i, 'Close'] > future_avg:
        df.loc[i, 'Label'] = 0  # Sell
    elif df.loc[i, 'Close'] < future_avg:
        df.loc[i, 'Label'] = 1  # Buy



# Clean Up
# df.drop('High', axis=1, inplace=True)
# df.drop('Low', axis=1, inplace=True)
# df.drop('Volume', axis=1, inplace=True)
df.dropna(inplace=True)

df.to_csv('data.csv')