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

class Ttjj(BaseFund):
    """
    天天基金免费行情获取
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

    def get_history_one_page(self, fund_code, start_date, end_date, page=1, per=20):
        '''
            获取基金网页数据
        '''
        url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={}&page={}&sdate={}&edate={}&per={}" \
            .format(fund_code, page, start_date, end_date, per)
        headers = self._get_headers()
        HTML = requests.get(url, headers=headers)
        HTML.encoding = "utf-8"

        return HTML

    def extract_funddata_history(self, fund_code, HTML):
        '''
            通过html获取基金历史数据
        '''
        soup = BeautifulSoup(HTML.text, 'html.parser')
        trs = soup.find_all("tr")
        res = []
        for tr in trs[1:]:
            date = tr.find_all("td")[0].text  # 净值日期
            unit_net = tr.find_all("td")[1].text  # 单位净值
            acc_net = tr.find_all("td")[2].text  # 累计净值
            fund_r = tr.find_all("td")[3].text  # 日增长率
            buy_status = tr.find_all("td")[4].text  # 申购状态
            sell_status = tr.find_all("td")[5].text  # 赎回状态
            res.append([date, unit_net, acc_net, fund_r, buy_status, sell_status])
            # dftemp.columns = ['date', 'totalnet', 'net', 'fqnet', "inc", "rate"]

        # {"date": "2021-12-30", "value": 1.4307, "accumulatedvalue": 1.4307,
        # "changevalue": 0.0119, "changerate": 0.0084}
        # df = pd.DataFrame(res, columns=['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态'])
        dftemp = pd.DataFrame(res, columns=['date', 'value', 'accumulatedvalue', 'changerate', 'rest1', 'rest2'])
        # ttjj的历史数据中，增长率有些不正确，只保留date，value, accumulatedvalue，其余全部计算
        dftemp.drop("rest1", axis=1, inplace=True)
        dftemp.drop("rest2", axis=1, inplace=True)
        dftemp["changerate"] = [x.replace("%", "") if x.strip() != "" else "0.0" for x in dftemp["changerate"]]
        dftemp["accumulatedvalue"] = dftemp["accumulatedvalue"].astype(float)
        dftemp.sort_values(by="date", ignore_index=True, inplace=True)
        # 将前一天的accumulatedvalue作为当天的oldvalue
        templist = list(dftemp["accumulatedvalue"])
        templist.insert(0, 0.0)
        templist.pop()
        dftemp["oldvalue"] = templist
        dftemp["changevalue"] = dftemp["accumulatedvalue"] - dftemp["oldvalue"]
        dftemp["changevalue"] = dftemp["changevalue"].round(4)
        dftemp.drop("oldvalue", axis=1)
        dftemp.columns = ['date', 'net', 'totalnet',  "rate", 'fqnet', "inc"]
        dftemp.sort_values(by="date", ignore_index=True, inplace=True, ascending=False)
        for column in dftemp.columns:
            dftemp[column] = dftemp[column].astype(str)
        return dftemp

    def search_history_data(self, fund_code, start_date="", end_date="") -> pd.DataFrame:
        '''
            获取基金数据主函数（仅支持单基金）, ttjj历史数据需要分页获取
        '''
        # 获取第一页
        html = self.get_history_one_page(fund_code, start_date, end_date)
        # 获取总页数
        pages = int(re.findall(r'pages:(.*),', html.text)[0])
        res_df = pd.DataFrame()
        for page in range(1, pages + 1):
            print("{} search page: {}/{}".format(fund_code, page, pages + 1))
            html = self.get_history_one_page(fund_code, start_date, end_date, page)
            df_ = self.extract_funddata_history(fund_code, html)
            res_df = pd.concat([res_df, df_])
            res_df.reset_index(drop=True, inplace=True)
        res_df["code"] = fund_code
        # 查询到的历史数据保存到数据库表
        savedbresult = self.save_history_to_db(res_df, name="fund_{}".format(fund_code))
        if savedbresult[0] is False:
            print(savedbresult[1])
        print("Found " + fund_code + " history data.")
        return res_df

    def search_normal_data(self, text):
        headers = self._get_headers()
        url = "{}{}{}".format(self.stock_api, text, '.html')
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        bs = BeautifulSoup(response, "html.parser")  # 数据是HTML，要用BeautifulSoup解析器解析
        return bs

    def search_real_data(self, text):
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
