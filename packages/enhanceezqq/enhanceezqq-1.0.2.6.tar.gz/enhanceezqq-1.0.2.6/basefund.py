# -*- coding: utf-8 -*-

import multiprocessing.pool

import pandas as pd
from easyquotation import basequotation
from df_excel_define import dftrans_simple_decrypt
from sqlalchemy import create_engine
import sqlite3 as sl


DATABASE_TYPE_SQLITE = 'sqlite'
DATABASE_TYPE_MYSQL = 'mysql'


class BaseFund(basequotation.BaseQuotation):
    """
    同花顺免费行情获取
    本class继承自basequotation.BaseQuotation，在本class中，stock codes均表示基金代码，因此无需增加prefix
    """
    def __init__(self, ip='', port: int = 8000, database='', user='', password='', select_limit=10000,
                 databasetype="mysql"):
        self.ip = ip.strip()
        self.port = port
        self.database = database.strip()
        self.user = user.strip()
        self.password = password
        self.select_limit = select_limit
        self.databasetype = databasetype
        super().__init__()

    def save_history_to_db(self, df, name="") -> list:
        """
        将基金历史数据保存到数据库
        :param df:          pd.DataFrame 历史数据df
        :param name:        数据库表名
        :return:            结果Dataframe
        """
        # 如果没有设置相关数据库信息，保存直接返回成功。
        if "" in [self.ip.strip(), self.database.strip(), name, self.databasetype.strip()]:
            return [True, ""]
        if self.databasetype == DATABASE_TYPE_SQLITE:
            mycon = sl.connect(self.database)
        else:
            # engine = sql.create_engine('mysql+mysqlconnector://user:password@localhost:port/database?auth_plugin=mysql_native_password')
            # mycon = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
            mycon = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
                self.user, dftrans_simple_decrypt(self.password), self.ip, self.port, self.database)
        print("save history to db:{}/{}".format(self.database, name))
        # 先删除旧表格
        deleltestr = "DROP TABLE IF EXISTS {};".format(name)
        try:
            if self.databasetype == DATABASE_TYPE_SQLITE:
                mycon.execute(deleltestr)
                df.to_sql(name=name, con=mycon)
            else:
                engine = create_engine(mycon, echo=False,
                                       connect_args={'auth_plugin': 'mysql_native_password', 'charset': 'utf8'})
                engine.execute(deleltestr)
                df.to_sql(name=name, con=engine, schema=None, if_exists='fail',
                          index=False, index_label=None, chunksize=None, dtype=None, method=None)
        except Exception as err:
            return [False, "历史数据写数据到数据库失败:{}！".format(err)]
        return [True, ""]

    def load_history_from_db(self, name="") -> list or str:
        if self.databasetype == DATABASE_TYPE_SQLITE:
            mycon = sl.connect(self.database)
        else:
            # engine = sql.create_engine('mysql+mysqlconnector://user:password@localhost:port/database?auth_plugin=mysql_native_password')
            # mycon = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?charset=utf8".format(
            mycon = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?auth_plugin=mysql_native_password".format(
                self.user, dftrans_simple_decrypt(self.password), self.ip, self.port, self.database)
        print("load history from db:{}/{}".format(self.database, name))
        try:
            # engine = create_engine(mycon, echo=False,
            #                        connect_args={'auth_plugin': 'mysql_native_password', 'charset': 'utf8'})
            sqlstr = "SELECT * from fund_{} limit {};".format(name, self.select_limit)
            df = pd.read_sql_query(sqlstr, mycon)
        except Exception as err:
            print("历史数据读取失败:{}！".format(err))
            return pd.DataFrame([])
        return df

    def funds_history_save(self, fund_list) -> list[pd.DataFrame]:
        return self._fetch_history_data(fund_list)

    def funds_history_load(self, fund_list) -> list[pd.DataFrame]:
        return self._load_history_data(fund_list)

    def search_history_data(self, fund_code, startdate="", enddate="") -> pd.DataFrame:
        pass

    def search_normal_data(self, text):
        pass

    def search_real_data(self, text):
        pass

    def get_stocks_by_range(self, params):
        return self.search_real_data(params)

    def gen_stock_list(self, stock_codes):
        return stock_codes

    def _fetch_history_data(self, fund_list) -> list:
        """获取股票信息"""
        pool = multiprocessing.pool.ThreadPool(len(fund_list))
        try:
            res = pool.map(self.search_history_data, fund_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def _load_history_data(self, fund_list):
        """获取股票信息"""
        pool = multiprocessing.pool.ThreadPool(len(fund_list))
        try:
            res = pool.map(self.load_history_from_db, fund_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def _gen_stock_prefix(self, stock_codes):
        return stock_codes

    def format_response_data(self, fundresultlist, prefix=False):
        # {"fundcode":"016020",
        #  "name":"招商中证电池主题ETF联接C",
        #  "jzrq":"2023-04-11",
        #  "dwjz":"0.7207",
        #  "gsz":"0.7080",
        #  "gszzl":"-1.77",
        #  "gztime":"2023-04-12 11:30"}
        return {x['fundcode']: x for x in fundresultlist}
