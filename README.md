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
- On a paid Investor's Business Daily account, filter stocks with with the following criterias
  - RS Rating: 86－99
  - Spon Rating: A,B,C
  - Price: 12.00－1000000000.00
  - Vol. (1000s): 500－1000000000
  - Vol- 50 Day Avg. (1000s): 500－1000000000
  - Last Qtr Sales % Chg.: 5－1000000000
- Download the results as excel, and copy all the tickers to screener.txt
- Run the stock filter: **python3 screener.py**
- The screener.py will filter stocks continue to matching all criteria from the Mark Minervini's VCP check list
- 2 links will be generated similar to:
  - [https://finviz.com/screener.ashx?v=211&t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA](https://finviz.com/screener.ashx?v=211&t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA)
  - [http://feifanhe.com/charts/?t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA](http://feifanhe.com/charts/?t=BNTX,CELH,LPI,OLN,SBLK,BCRX,ATKR,CROX,RVLV,XEC,INMD,THC,SBNY,SNAP,WLL,TRGP,LTHM,MRNA)
