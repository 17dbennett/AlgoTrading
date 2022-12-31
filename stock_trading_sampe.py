
import yfinance as yahooFinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('default') 
 
def plot_stock_info(ticker= ''):
    GetStockInformation = yahooFinance.Ticker(ticker)
    
    # Valid options are 1d, 5d, 1mo, 3mo, 6mo, 1y,
    # 2y, 5y, 10y and ytd.
    df = pd.DataFrame(GetStockInformation.history(period="6mo"))

    df['rolling_close'] = df['Close'].rolling(30).mean()
    df['EWMA30'] = df['Close'].ewm(span=30).mean()

    df[['Close', 'rolling_close', 'EWMA30']].plot(label=ticker, figsize=(16, 8))
    plt.title(ticker)
    #plt.show()
    data = df[['Close', 'rolling_close', 'EWMA30']]

    return data


tickers =['DIS', 'TSLA', 'VIGAX', 'META', 'GPRO', 'AAPL', 'AMZN', 'FNMFN', 'CXMSF', 'PTTAX', 'GLD']
for t in tickers:
    buy = True
    sell = False
    decision = []
    profit = []
    data = plot_stock_info(t)
    for i in enumerate(data['Close']): 
        if i[1] > data['rolling_close'][i[0]] and sell:
            decision.append('Sell') 
            profit.append(i[1] - data['rolling_close'][i[0]])
            buy = True
            sell = False
        elif i[1] < data['rolling_close'][i[0]] and buy:
            decision.append('buy') 
            profit.append(0)
            sell = True
            buy = False
        else:
            profit.append(0)
            if buy:
                decision.append('waiting for right timing to buy') 
            elif sell:
                decision.append('holding till opprotunity to sell')

    data['decision'] = decision
    data['profit'] = profit


    print( t,'you made $',round(sum(data['profit']),2))
