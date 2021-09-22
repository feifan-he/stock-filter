import multiprocessing
import threading
from datetime import datetime
from queue import Queue

import itertools
import pandas as pd
import requests
import time

o, c, h, l = 'open', 'close', 'high', 'low'

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'})
_RED = '\033[91m%s\033[0m'
def main():
    pairs = fx('EURUSD GBPUSD AUDUSD')

    sd = get_stock_data(pairs, drop=False, interval='1d', range='1d')

    for key, df in sd.items():
        sd[key] = round(last_df(df)[c], 5)

    print(sd)


# interval: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# range: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# period1=int(start.timestamp())
def get_stock_data(tickers, progress=True, **kwargs):
    '''
    Retrieve price history using the Yahoo api
    :param tickers(list(str)): list of tickers
    :param progress(bool): show progress bar?
    :param kwargs: request parameters for the yahoo api
        interval: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        range: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    :return ({str: response})): ticker and the corresponding price data
    '''
    visited = set()
    if type(tickers) == str:
        tickers = tickers.split(' ')
    tickers = [ticker for ticker in tickers if ticker not in visited and not visited.add(ticker)]

    return dict(process_jobs(tickers, get_ticker, progress=progress, **kwargs))


def process_jobs(jobs, callback, progress=True, failed_callback=lambda job, **kwargs: None, **kwargs):
    '''
    Using consumer/producer logic, process jobs in parallel
    :param jobs(list(str)): what are the params for the jobs
    :param callback(func(params...)): how to process the job given the params
    :param progress(bool): show progress bar for the job execution?
    :param failed_callback(func(str)): if job failed, what to do
    :param kwargs: any keyword argument to pass in for each job?
    :return:
    '''
    res = []
    failed = []
    q = Queue()

    cnt = itertools.count()
    next(cnt)

    def consumer():
        nonlocal failed
        while True:
            pos, job = q.get()
            try:
                if type(job) == tuple:
                    execute = (job, callback(*job, **kwargs))
                else:
                    execute = (job, callback(job, **kwargs))
                res.append((pos, execute))
            except Exception as ex:
                failed.append(f'{job}\n{"-" * 50}\n\n{ex}')
                failed_callback(job, **kwargs)

            if progress:
                progress_bar(next(cnt), len(failed), len(jobs))

            time.sleep(.001)
            q.task_done()

    # produce
    for pos_job_pair in enumerate(jobs):
        q.put(pos_job_pair)

    # consume
    thread_count = multiprocessing.cpu_count() * 2
    for _ in range(thread_count):
        threading.Thread(target=consumer, daemon=True).start()
    q.join()

    if progress:
        print(_RED % '\n%s\n' % f'\n{"="*50}\n\n'.join(failed))

    res.sort(key=lambda pos_job_pair: pos_job_pair[0])
    return [r[1] for r in res]


def get_ticker(ticker, drop=True, **kwargs):
    """
    Given a stock symbol retrieve the historical prices using the Yahoo api
    :param ticker: stock symbol
    :param drop: drop the last incomplete candlestick if incomplete
    :param kwargs: request parameters
    :return:
    """
    data = session.get(url=f"https://query1.finance.yahoo.com//v8/finance/chart/{ticker}", params=kwargs).json()
    result = data['chart']['result'][0]

    candles = result['indicators']['quote'][0]
    candles['time'] = list(map(lambda ts: datetime.fromtimestamp(ts), result['timestamp']))
    attrs = ['time', 'open', 'close', 'high', 'low', 'volume']
    df = pd.DataFrame({attr: candles[attr] for attr in attrs}).set_index('time')

    if len(df.index) and drop:
        last = df.index[-1]
        interval = kwargs.get('interval', '')
        if interval == '1h' and not (last.minute == last.second == 0) or \
                interval == '1d' and not (last.hour == last.minute == last.second == 0) or \
                interval.endswith('m') and not (last.minute % int(interval[:-1]) == 0):
            df = df[:-1]

    return df.dropna()


def progress_bar(processed_cnt, error_cnt, total, bar_length=30):
    """
    Update the following status bar on standard output

    example standard output:
    [************* 100% ***********] 0/3/3

    processed_cnt: how many success
    error_cnt: how many failed
    total: what is the total
    bar_length: how many characters is the length of the progress bar
    """
    percent = float(processed_cnt) * 100 / total
    total_bars = int(percent / 100 * bar_length)
    progress = list(f'{"*" * total_bars}{" " * (bar_length - total_bars)}')
    status = f' {round(percent)}% '
    mid = int(bar_length / 2) + 4
    for i in range(1, len(status) + 1):
        progress[mid - i] = status[- i]
    progress = ''.join(progress)
    print(f'\r[{progress}] {_RED % error_cnt}/{processed_cnt}/{total}', end='')


def last_df(df):
    return df.iloc[[-1]].to_dict('records')[0]


def pretty_sd(sd):
    return '\n' + f'\n\n{"=" * 80}\n\n'.join(map(lambda kv: f'{kv[0]}\n{"-" * 9}\n\n{kv[1]}', sd.items()))


def fx(pairs):
    return (pairs + ' ').replace(' ', '=X ').strip().split(' ')


if __name__ == '__main__':
    main()
