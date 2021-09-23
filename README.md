# Stock Filter


### Filter Based on Mark Minervini's Pivot Volatility Contraction PatternCancel changes
- 200 day moving average has consistent upward slope for at least half a year
- Price greater than 150 day average price
- 150 day average price greater than 200 day average price
- 50 day average price greater than 150 day average price
- Price is within 30% from the one year high
- Price is at least 3 times the one year low

Referrence -> http://thetraderdiaries.blogspot.com/2016/03/three-trading-lessons-from-trade-like.html
![](https://4.bp.blogspot.com/-Sbd60ef_S4Y/VtbaITrI-YI/AAAAAAAABqc/V31wAawRnyU/s1600/IMG_0077.PNG)


### Usage

#### Requirements
- Python3
- pip3

#### Instructions
- Install libraries: **pip3 install -r requirements.txt**
- Change the output_path at the top of the screener.py script, this will be the location where the candle stick charts will be generated for offline use
- On a paid Investor's Business Daily account, filter stocks with 85+ IBD rating
- Download the results as excel, and copy all the tickers to screener.txt
- Run the stock filter: **python3 screener.py**
- The screener.py will generate a list of stocks with the filters
- A folder containing index.html will be generated for the filtered stocks at the output_path specified ealier
- Also a link is generated similar to [https://finviz.com/screener.ashx?v=211&t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA](https://finviz.com/screener.ashx?v=211&t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA)
