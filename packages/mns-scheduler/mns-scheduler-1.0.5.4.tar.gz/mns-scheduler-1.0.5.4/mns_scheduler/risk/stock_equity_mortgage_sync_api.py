import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)

# 股权质押 https://data.eastmoney.com/gpzy/pledgeRatio.aspx

import requests


def get_equity_mortgage():
    url = (
        'https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123018114616341595302_1715993497168&sortColumns=PLEDGE_RATIO&sortTypes=-1'
        '&pageSize=50000'
        '&pageNumber=1'
        '&reportName=RPT_CSDC_LIST&columns=ALL&quoteColumns=&source=WEB'
        '&client=WEB'
        '&filter=(TRADE_DATE%3D%272024-05-17%27)')

    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url, headers=headers)
    data_json = r.json()
    print(data_json)


if __name__ == '__main__':
    get_equity_mortgage()
