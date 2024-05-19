# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

import pandas as pd
from basefund import BaseFund
import akshare as ak
from bs4 import BeautifulSoup
import time
import urllib
import re
import ast

class Akpack(BaseFund):
    """
    同花顺免费行情获取
    本class继承自basequotation.BaseQuotation，在本clss中，stock codes均表示基金代码，因此无需增加prefix
    """
    max_num = 800
    @property
    def stock_api(self) -> str:
        return f"http://fundgz.1234567.com.cn/"

    def _get_headers(self) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
    }

    def search_history_data(self, fund_code, startdate="", enddate="") -> pd.DataFrame:
        res_df = ak.fund_open_fund_info_em(fund=fund_code)
        # re.findall
        # {"date":"2023-04-14","net":"0.9282","totalnet":"0.9282","fqnet":"0.9282","inc":"0.0248","rate":"2.75"}
        # resultlist = re.findall('{"date":"(.*?)","net":"(.*?)","totalnet":"(.*?)","fqnet":"(.*?)","inc":"(.*?)","rate":"(.*?)"}', stemp)
        # res_df = pd.DataFrame(resultlist, columns=["date", "net", "totalnet", "fqnet", "inc", "rate"])
        res_df.columns = ["date", "totalnet", "rate"]
        res_df['net'] = res_df['totalnet']
        res_df['fqnet'] = res_df['totalnet']
        res_df["code"] = fund_code
        res_df.sort_values(by=['date'], inplace=True, ignore_index=True, ascending=False)
        savedbresult = self.save_history_to_db(res_df,  name="fund_{}".format(fund_code))
        if savedbresult[0] is False:
            print(savedbresult[1])
        # # akshare查询历史数据的方式改变！直接获取到json格式文件
        print("Found " + fund_code + " history data.")
        return res_df

    def search_normal_data(self, text):
        # 历史数据 https://fund.10jqka.com.cn/001628/
        return pd.DataFrame([])

    def search_real_data(self, text):
        # 借用ttjj的real，实际akpack只能按大类整体获取实时数据，而且使用的时ttjj的数据
        headers = self._get_headers()
        url = "{}js/{}.js?rt={}".format(self.stock_api, text, int(time.time() * 1000))
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        bs = BeautifulSoup(response, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        tempstr = re.findall("jsonpgz\((.*?)\);", bs.text)
        return ast.literal_eval(tempstr[0]) if '' not in tempstr else {
            "fundcode": text,
            "name": "-",
            "jzrq": "-",
            "dwjz": "-",          # 历史累计净值
            "gsz":  "-",          # 实时估值
            "gszzl": "-",         # 实时涨跌估算
            "gztime": "-"
        }

