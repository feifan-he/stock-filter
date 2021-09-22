import shutil
import urllib
import webbrowser
from urllib.parse import urlencode

from jinja2 import Template
import os
from finance import *
from urllib.request import urlretrieve



def __generate_index(output_path, tickers):
    with open('res/charts.html.jinja2') as f:
        template = Template(f.read())

    with open(os.path.join(output_path, 'index.html'), 'w') as f:
        f.write(template.render(tickers=tickers, path=output_path, charts_dir='charts'))
        f.close()

    output_res_path = os.path.join(output_path, 'res')
    os.makedirs(output_res_path, exist_ok=True)
    shutil.copytree('res', output_res_path, dirs_exist_ok=True)

    webbrowser.get("chrome").open("file://" + os.path.join(output_path, 'index.html'))

def generate_charts(tickers, output_path, remove_if_path_exists=True, ta='0', period='dw', chart_type='c', size='l'):
    '''
    Generate offline charts given price history for stocks.
    '''
    if remove_if_path_exists:
        for f in ['charts', 'res']:
            if os.path.exists(os.path.join(output_path, f)):
                shutil.rmtree(os.path.join(output_path, f))

        idx = os.path.join(output_path, 'index.html')
        if os.path.exists(idx):
            os.remove(idx)
    os.makedirs(os.path.join(output_path, 'charts'), exist_ok=True)

    url = 'https://finviz.com/chart.ashx?' + urlencode(dict(ty=chart_type, ta=ta, s=size)) + '&p=%s&t=%s'

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    os.makedirs(output_path, exist_ok=True)
    jobs = []
    tickers = [t.upper() for t in tickers]
    for ticker in tickers:
        for p in period:
            file_name = os.path.join(output_path, 'charts', f'{ticker}_{p}.jpg')
            cur_url = url %(p, ticker)
            jobs.append((cur_url, file_name))

    print('Download Charts:')
    process_jobs(jobs, urlretrieve)
    __generate_index(output_path, tickers)


if __name__ == '__main__':
    tickers = 'ZS,VUZI,VIPS,VERI,VCEL,UPWK,TXG,TWTR,TWLO,TUP,TTD,TSLA,STAA,SQ,SPT,SONO,SNAP,SE,SBSW,SAIL,ROKU,RDFN,RCM,RCII,QFIN,PTON,PRTS,PRPL,PINS,PDD,OMI,OLN,OCUL,NTRA,NOVA,NK,NIU,NET,MXL,MWK,MRNA,MDB,MAXR,LTHM,LSCC,LPRO,LOGI,IIVI,IIPR,ICLK,HZNP,HUBS,HOME,GNRC,GNMK,FVRR,FTCH,FIVN,FCX,FATE,EVH,ETSY,ENPH,DNLI,DKNG,DE,CVNA,CVET,CRWD,CROX,CRNC,CREE,CHWY,CELH,CDNA,CDMO,CALX,BRKS,BILL,BILI,AXON,ATEC,APPS,ALGN,AGCO,ACRS'
    tickers = tickers.split(',')[:10]
    generate_charts(tickers, '/Users/daveli/OneDrive/Swing/2021_02_01', period='dw')

