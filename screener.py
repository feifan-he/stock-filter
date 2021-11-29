from pandas.tseries.offsets import BDay
import numpy as np
import re
from finance import *


"""
RS Rating: 86－99
Spon Rating: A,B,C
Price: 12.00－1000000000.00
Vol. (1000s): 500－1000000000
Vol- 50 Day Avg. (1000s): 500－1000000000
Last Qtr Sales % Chg.: 5－1000000000
"""

avg200_pos_period = 20 * 6
filters = [
    "price > avg(150) > avg(200)",
    "avg(50) > avg(150)",
    "price > year_high * 0.7",
    "price > year_low * 3",
    "avg200_rising",
]

save = False
replace = True
create_charts = True
start = datetime.now() - BDay(200 + int(avg200_pos_period) + 40)
end = datetime.now()
pd.options.mode.chained_assignment = None
bdays_year = 261

stocks = open('./screener.txt').read().strip().split('\n')

print('Download Tickers:')
stock_charts = get_stock_data(stocks, period1=int(start.timestamp()), period2=int(end.timestamp()), interval='1d')

filteredCount = 0
filteredTickers = []

stock_charts = dict(sorted(stock_charts.items(), key=lambda ticker_df: stocks.index(ticker_df[0])))
for ticker, df in stock_charts.items():
    criteria = {}
    df.fillna(method='ffill', inplace=True)

    df['avg200'] = df.close.rolling(200).mean()
    avg200_look_back = df.avg200[len(df) - avg200_pos_period:]
    avg200_rising = ((avg200_look_back - avg200_look_back.shift(1))[1:] >= 0).all()

    year_high = np.max(df.high[max(len(df) - bdays_year, 0):])
    year_low = np.min(df.low[max(len(df) - bdays_year, 0):])
    price = df.close[len(df) - 1]
    volume = df.volume[len(df) - 1]
    avg = lambda length: np.mean(df.close[len(df) - length:])

    def check_criteria(exp):
        exp_key = re.sub(r"[^*]([a-zA-Z][\w\d]+)", lambda regex: f"[{regex.group()}:{eval(regex.group())}]", exp)
        criteria[exp_key] = eval(exp)

    for f in filters: check_criteria(f)

    if all(criteria.values()):
        filteredCount += 1
        filteredTickers.append(ticker)

filteredTickersStr = ",".join(filteredTickers)


print(f'''total: {len(stock_charts)}
filtered: {filteredCount}
url: http://feifanhe.com/charts/?t={filteredTickersStr}
finviz url: https://finviz.com/screener.ashx?v=211&t={filteredTickersStr}
tickers: {filteredTickersStr}''')

