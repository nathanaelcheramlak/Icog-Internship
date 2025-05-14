import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('../labeled_data.csv', parse_dates=['Datetime'])
data.set_index('Datetime', inplace=True)

# Plot the closing price 
plt.plot(data.index, data['Close'], label='Price', color='blue', alpha=0.7)

# Add buy/sell signals
buy_signals = data[data['Label'] == 1]
sell_signals = data[data['Label'] == -1]

plt.scatter(buy_signals.index, buy_signals['Close'], 
            color='green', label='Buy Signal', alpha=0.7, s=20)
plt.scatter(sell_signals.index, sell_signals['Close'], 
            color='red', label='Sell Signal', alpha=0.7, s=20)

# Formatting
plt.title('Trading Signals on Price Data')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)

plt.show()