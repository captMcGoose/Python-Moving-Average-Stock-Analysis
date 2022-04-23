import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

plt.style.use("dark_background")


print("Welcome to the Stock Viewer!")
print("Please select a fast SMA (Recommended 30): ")
ma_1 = int(input())
print("Please select a slow SMA (Recommended 100): ")
ma_2 = int(input())

# These moving averages are used to determine golden/death crosses
ma_50 = 50
ma_200 = 200

print("Please select the time frame (in months): ")
inputMonths = int(input())

#define timeframe
start = dt.datetime.now() - dt.timedelta(days=inputMonths*31) #from past 3 years
end = dt.datetime.now() # current time


print("Please select how many stocks you wish to view(max 9): ")
MAX = int(input())
print("Number of rows: ")
RMAX = int(input())
print("Number of columns: ")
CMAX = int(input())
if(RMAX*CMAX != MAX):
    print("ERROR: INVALID NUMBER OF ROWS/COLUMNS")
    exit()
fig, axs = plt.subplots(RMAX, CMAX)

print("Select an index provider (recommended: yahoo): ")
PROVIDER = str(input())

for i in range(RMAX):
    for j in range(CMAX):
        # get price for a specific stock in this timeframe
        print("Select a stock symbol:")
        symbol = str(input())
        data = web.DataReader(symbol, PROVIDER, start, end) #get the Facebook data from the yahoo index
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



        axs[i][j].plot(data['Adj Close'], label="Share Price", alpha=0.5)
        axs[i][j].plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="lightgreen", linestyle="--")
        axs[i][j].plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="green", linestyle="--")
        axs[i][j].scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="green", lw=3)
        axs[i][j].scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="red", lw=3)

        axs[i][j].plot(data[f'SMA_{ma_50}'], label=f"SMA_{ma_50}", color="orange", linestyle="--", alpha=0.25)
        axs[i][j].plot(data[f'SMA_{ma_200}'], label=f"SMA_{ma_200}", color="pink", linestyle="--", alpha=0.25)
        axs[i][j].scatter(data.index, data['Golden Crosses'], label="Golden Cross", marker="X", color="gold", lw=1)
        axs[i][j].scatter(data.index, data['Death Crosses'], label="Death Cross", marker="X", color="red", lw=1)
        axs[i][j].set_title(symbol)

axs[0][0].legend(loc="upper left")
plt.show()
