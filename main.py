import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

plt.style.use("dark_background")

# decide moving averages (average for a certain period of time)
ma_1 = 30 # 30-day moving average
ma_2 = 100 # 100-day moving average


# These moving averages are used to determine golden/death crosses
ma_50 = 50
ma_200 = 200

#define timeframe
start = dt.datetime.now() - dt.timedelta(days=365*5) #from past 3 years
end = dt.datetime.now() # current time

# get price for a specific stock in this timeframe
data = web.DataReader('TSLA', 'yahoo', start, end) #get the Facebook data from the yahoo index
data[f'SMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
data[f'SMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

data[f'SMA_{ma_50}'] = data['Adj Close'].rolling(window=ma_50).mean()
data[f'SMA_{ma_200}'] = data['Adj Close'].rolling(window=ma_200).mean()

#when the 2 averages meet, we want to place a buy/sell signal
buy_signals = []
sell_signals = []

gold_signals = []
death_signals = []

trigger = 0
triggerGD = 0

for x in range(len(data)):
    if(data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1):
        buy_signals.append(data['Adj Close'].iloc[x])
        sell_signals.append(float('nan'))
        trigger = 1
    elif(data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1):
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[x])
        trigger = -1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

    if(data[f'SMA_{ma_50}'].iloc[x] > data[f'SMA_{ma_200}'].iloc[x] and triggerGD != 1):
        gold_signals.append(data['Adj Close'].iloc[x])
        death_signals.append(float('nan'))
        triggerGD = 1
    elif(data[f'SMA_{ma_50}'].iloc[x] < data[f'SMA_{ma_200}'].iloc[x] and triggerGD != -1):
        gold_signals.append(float('nan'))
        death_signals.append(data['Adj Close'].iloc[x])
        triggerGD = -1
    else:
        gold_signals.append(float('nan'))
        death_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

data['Golden Crosses'] = gold_signals
data['Death Crosses'] = death_signals

print(data)

# draw the info

plt.plot(data['Adj Close'], label="Share Price", alpha=0.5)
plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="lightgreen", linestyle="--")
plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="green", linestyle="--")
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="green", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="red", lw=3)

plt.plot(data[f'SMA_{ma_50}'], label=f"SMA_{ma_50}", color="orange", linestyle="--", alpha=0.25)
plt.plot(data[f'SMA_{ma_200}'], label=f"SMA_{ma_200}", color="pink", linestyle="--", alpha=0.25)
plt.scatter(data.index, data['Golden Crosses'], label="Golden Cross", marker="X", color="gold", lw=1)
plt.scatter(data.index, data['Death Crosses'], label="Death Cross", marker="X", color="red", lw=1)

plt.legend(loc="upper left")
plt.show()
