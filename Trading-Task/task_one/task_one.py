import pandas as pd
import json

# Close > Open - Increasing (Green)
# Open > Close - Decreasing (Red)

def is_green(open, close):
    return close > open

def is_red(open, close):
    return open > close


def detect_liquidity_grab(df, lookback=20):
    liquidity_signals = []

    for i in range(lookback, len(df)):
        recent_high = df['High'][i - lookback: i].max()
        recent_low = df['Low'][i - lookback: i].min()
        open, close, low, high = df.iloc[i][['Open', 'Close', 'Low', 'High']]

        # Above High
        if high > recent_high and is_red(open, close):
            liquidity_signals.append((df['Datetime'][i], 'SELL'))
        
        # Below Low
        if low < recent_low and is_green(open, close):
            liquidity_signals.append((df['Datetime'][i], 'BUY'))
        
    return liquidity_signals


def candlestick_patterns(df):
    candle_signals = []
    
    for i in range(1, len(df)):
        prev = df.iloc[i-1]
        curr = df.iloc[i]
        
        o1, c1 = prev['Open'], prev['Close']
        o2, c2 = curr['Open'], curr['Close']
        h2, l2 = curr['High'], curr['Low']
        
        # Calculate candle components
        body = abs(c2 - o2)
        total_range = h2 - l2
        lower_wick = min(o2, c2) - l2
        upper_wick = h2 - max(o2, c2)
        
        # Hammer (only valid in downtrend)
        if (body < total_range * 0.3 and 
            lower_wick > 2 * body and 
            upper_wick < body and
            c1 < o1):  # Previous candle was red (downtrend)
            candle_signals.append((df['Datetime'][i], 'BUY - Hammer'))
            
        # Shooting Star (only valid in uptrend)
        if (body < total_range * 0.3 and
            upper_wick > 2 * body and
            lower_wick < body and
            c1 > o1):  # Previous candle was green (uptrend)
            candle_signals.append((df['Datetime'][i], 'SELL - Shooting Star'))
        
        # Bullish Engulfing
        if is_red(o1, c1) and is_green(o2, c2) and (o2 < c1) and (c2 > o1):
            candle_signals.append((df['Datetime'][i], 'BUY - Bullish Engulfing'))
            
        # Bearish Engulfing
        if (is_green(o1, c1) and is_red(o2, c2) and (o2 > c1) and (c2 < o1)):
            candle_signals.append((df['Datetime'][i], 'SELL - Bearish Engulfing'))
            
    return candle_signals

def detect_fvg(df, min_gap=0.001):
    fvg_signals = []

    for i in range(2, len(df)):
        high1 = df.iloc[i - 2]['High']
        low3 = df.iloc[i]['Low']
        low1 = df.iloc[i - 2]['Low']
        high3 = df.iloc[i]['High']
        date = df['Datetime'][i]

        # Bullish FVG
        if low3 - high1 >= min_gap:
            fvg_signals.append((date, 'BULLISH FVG', high1, low3, round(low3 - high1, 2)))

        # Bearish FVG
        elif low1 - high3 >= min_gap:
            fvg_signals.append((date, 'BEARISH FVG', high3, low1, round(low1 - high3, 2)))

    return fvg_signals


def combine(liquidity, candle, fvg):
    from collections import defaultdict

    combined = defaultdict(list)

    for date, signal in liquidity:
        date = str(date)
        combined[date].append(f"Liquidity: {signal}")

    for date, signal in candle:
        date = str(date)
        combined[date].append(f"Candlestick: {signal}")

    for date, signal, *_ in fvg:
        date = str(date)
        combined[date].append(f"FVG: {signal}")

    return dict(combined)


df = pd.read_csv('../trading_data.csv')

liquidity = detect_liquidity_grab(df, 10)
candle = candlestick_patterns(df)
fvg = detect_fvg(df, 0.01)

signals = combine(liquidity, candle, fvg)

# Labels the data and saves it
def save_dataframe(df, signals):
    new_df = df.copy(deep=True)
    new_df['Label'] = 0
    for row in df.itertuples():
        index = row.Index
        date = row.Datetime
        if date in signals and new_df.loc[index, 'Label'] == 0:
            sell_count = sum(1 for strategy in signals[date] if 'SELL' in strategy)
            buy_count = sum(1 for strategy in signals[date] if 'BUY' in strategy)

            if sell_count > buy_count:
                new_df.loc[index, 'Label'] = -1
            if sell_count < buy_count:
                new_df.loc[index, 'Label'] = 1

    new_df = new_df[new_df['Label'] != 0]
    new_df.to_csv("../labeled_data.csv", index=False)

def save_signals(df, signals):
    with open('signals.json', 'w') as f:
        json.dump(signals, f, indent=2)

save_dataframe(df, signals)
save_signals(df, signals)

