# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup
import time
import urllib
import ast
import pandas as pd
import os
from basefund import BaseFund
import requests


class Ths(BaseFund):
    """
    同花顺免费行情获取
    本class继承自basequotation.BaseQuotation，在本clss中，stock codes均表示基金代码，因此无需增加prefix
    """
    max_num = 800
    @property
    def stock_api(self) -> str:
        return f"https://fund.10jqka.com.cn/"

    def _get_headers(self) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'Referer': 'https://fund.10jqka.com.cn/',
    }

    def search_history_data(self, fund_code, startdate="", enddate="") -> pd.DataFrame:
        # 历史数据 https://fund.10jqka.com.cn/dockercache/fund/historynet/013811
        headers = self._get_headers()
        url = "{}/dockercache/fund/historynet/{}".format(self.stock_api, str(fund_code))
        req = requests.get(url=url, headers=headers)
        bs = BeautifulSoup(req.text, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        # 提取匹配结果
        stemp = re.findall('\{"data":(.*?),"error":\{"id":0,"msg":"is access"}}', bs.text)[0]
        # eval比re.findall快很多， ast eval大数据容易递归错误
        # res_df = pd.DataFrame(ast.literal_eval(stemp))
        res_df = pd.DataFrame(eval(stemp))
        # re.findall
        # {"date":"2023-04-14","net":"0.9282","totalnet":"0.9282","fqnet":"0.9282","inc":"0.0248","rate":"2.75"}
        # resultlist = re.findall('{"date":"(.*?)","net":"(.*?)","totalnet":"(.*?)","fqnet":"(.*?)","inc":"(.*?)","rate":"(.*?)"}', stemp)
        # res_df = pd.DataFrame(resultlist, columns=["date", "net", "totalnet", "fqnet", "inc", "rate"])
        res_df["code"] = fund_code
        # 查询到的历史数据保存到数据库表
        savedbresult = self.save_history_to_db(res_df,  name="fund_{}".format(fund_code))
        if savedbresult[0] is False:
            print(savedbresult[1])
        print("Found " + fund_code + " history data.")
        return res_df

    def search_normal_data(self, text):
        # 历史数据 https://fund.10jqka.com.cn/001628/
        headers = self._get_headers()
        url = "{}/{}/".format(self.stock_api, str(text))
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        bs = BeautifulSoup(response, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        return bs

    def search_real_data(self, text):
        # fund_id 和查询实时数据的 vm_fd_JSZ430之间有对应关系，需要找到
        headers = self._get_headers()
        #    https://fund.10jqka.com.cn/data/client/myfund/001628
        url = "{}/data/client/myfund/{}".format(self.stock_api, str(text))
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        bs = BeautifulSoup(response, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        # 转化为字典方式
        bsdata = ast.literal_eval(bs.text)['data'][0]
        name = bsdata['name']
        previousdate = bsdata['enddate']
        totalnet = bsdata['totalnet']
        hqcode = bsdata['hqcode']
        currentrealcode = "".join(["vm_fd_", hqcode])
        # 再查询实时数据 <- 根据currentrealcode
        # https://gz-fund.10jqka.com.cn/?module=api&controller=index&action=chart&info=vm_fd_JSZ430&start=0930&_-168128674648
        # result:
        # vm_fd_JSZ430=
        # '2023-04-11;
        # 0930-1130,1300-1500|2023-04-12~1.9290~
        # 0930,1.93470,1.9290,0.000;0931,1.93138,1.9290,0.000;0932,1.93649,1.9290,0.000;
        # 0933,1.93736,1.9290,0.000;0934,1.94150,1.9290,0.000;0935,1.94475,1.9290,0.000;
        # ......
        # 1458,2.02659,1.9290,0.000;1459,2.02659,1.9290,0.000;1500,2.02645,1.9290,0.000'
        url = "{}?module=api&controller=index&action=chart&info={}&start=0930&_-{}".format(
            "https://gz-fund.10jqka.com.cn/", currentrealcode, int(time.time() * 1000))
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        bs = BeautifulSoup(response, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        # 从text 切割出最后一组（当前实时）数据并转换：list ，['1500', '2.02645', '1.9290', '0.000'] [时刻，估值，前日净值，？？？]
        # 不存在实时估值时，list: ['0930-1130', '1300-1500|2024-04-11~']
        resultlist = bs.text[bs.text.rfind(";") + 1:-2].split(",")
        currentdate = bs.text[bs.text.find("|") + 1: bs.text.find("~")]
        templ = list(resultlist[0])
        templ.insert(-2, ":")
        currenttime = "".join(templ)
        if len(resultlist) == 4:
            # 模仿天天基金的格式生成
            resultdict = {
                "fundcode": text,       # 基金代号
                "name": name,           # 基金名称
                "jzrq": previousdate,   # 累计净值（历史）日期，上一个结算日
                "dwjz": totalnet,       # 历史累计净值
                "gsz": resultlist[1],   # 实时估值
                "gszzl": "{:.2f}".format(100 * ((float(resultlist[1]) - float(resultlist[2]))/float(resultlist[2]))),    # 实时涨跌估算
                "gztime": "{} {}".format(currentdate, currenttime)                 # 实时估值时间
            }
        else:
            # 模仿天天基金的格式生成
            resultdict = {
                "fundcode": text,     # 基金代号
                "name": name,         # 基金名称
                "jzrq": previousdate, # 累计净值（历史）日期，上一个结算日
                "dwjz": totalnet,     # 历史累计净值
                "gsz":  "-",          # 实时估值
                "gszzl": "-",         # 实时涨跌估算
                "gztime": "{} {}".format(currentdate, currenttime)                 # 实时估值时间
            }

        return resultdict

