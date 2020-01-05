import requests
import random
import json
import re
import threading
import numpy as np
import pandas as pd
import os

class StockSpider(object):
    def __init__(self):
        self.uapools = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
        ]
        self.url = 'http://81.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240011147346140871761_1578147666536' \
                   '&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t' \
                   ':13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18' \
                   ',f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1578147666547' # 爬取个股列表的URL
        self.ua = random.choice(self.uapools)
        # self.sem = threading.Semaphore(100)
        self.stock_dict = dict() # 存储个股列表

    # 获取个股列表
    def getStockList(self):
        self.hosts = "push2.eastmoney.com"
        self.headers = {
            'HOST': self.hosts,
            'User-Agent': self.ua
        }
        self.data_dict = dict()
        response = requests.get(self.url,headers = self.headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            html = re.search(r'.*\((.*)\)',response.text).group(1)
            data_list = json.loads(html)['data']['diff']
            for data in data_list:
                self.data_dict[data['f12']] = data['f14']
        return self.data_dict


    # 获取个股历史数据
    def getStockData(self,stime,etime):
        self.stock_dict = self.getStockList()
        print("数据开始下载...")
        for stock_code,stock_name in self.stock_dict.items():
            # 0:沪市 1:深市
            stock_code = ("0" if stock_code.startswith('6') else "1") + stock_code
            url = 'http://quotes.money.163.com/service/chddata.html?code={0}&start={1}&end={2}' \
                  '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;' \
                  'TCAP;MCAP'.format(stock_code,stime,etime)
            response = requests.get(url)
            print(response.text)
            print("正在下载[{0}]...".format(stock_code+'_'+stock_name))
            self.downLoadData(stock_code + '_' + stock_name, response.text)
        print("数据下载完成...")
        self.mergeData()

    @staticmethod
    def downLoadData(filename,data):
        filepath = 'data/'+ filename +'.csv'
        with open(filepath, 'w+', encoding='utf-8') as f:
            for row in data:
              f.write(row)

    @staticmethod
    def mergeData():
        dir = 'data/'
        filename_list = []
        dfs = []
        for root,_,files in os.walk(dir):
            for file in files:
                filepath = os.path.join(root,file)
                filename_list.append(filepath)
                dfs.append(pd.read_csv(filepath))
        df = pd.concat(dfs,ignore_index=True)
        df.to_csv('result.csv',encoding='utf-8')
        print("数据合并成功...")

if __name__ == '__main__':
    stock = StockSpider()
    stock.getStockData('20191101','20191231')