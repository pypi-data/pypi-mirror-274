# -*- coding: utf-8 -*-

"""
###############################################################################################################
# 封装 easyquotation 模块作为获取网络股票数据的工具
#   -f 优先级最高， -s -c结合获取股票信息
#   * -s -datasource 数据来源（sina，jsl， qq, tencent, boc, timekline, dayline, hkquote)
#     datasourcelist = [
#         'sina',             # sina： A股，sh， sz 000001
#         'jsl',              # 集思录
#         'qq',               # 腾讯： A股
#         'tencent',          # 同上
#         'boc',              # 中银 外汇牌价，目前只支持usa
#         'timekline',        # A股 当天K线
#         'daykline',         # 港股 1500天日K 00001
#         'hkquote',          # 港股 00001
#         'ttjj',             # 天天基金, 实时基金估值，如果his -y  则为获取基金历史数据
#         'ths',              # 同花顺基金, 实时基金估值， 如果his -y 则为获取基金历史数据
#         'akpack',           # akshare 实时基金估值，如果his -y 则为获取基金历史数据
#         'funddb',           # 数据库基金历史数据
#         'stockdb'           # 数据库股票历史数据
#
#     ]
#   * -c -code stockcode1 stockcode2 ...... 股票代码列表, 可以多个
#   * -p --prefix
#   * -f -commandfile 使用指定json文件输入命令参数
#   * -u -updatelist 根据网络数据更新本地stockcode缓冲清单
#   * -g -getlist （realtime/nonrealtime) 获取stockcode清单，realtime(直接使用网络数据), nonrealtime（使用本地缓冲数据）
#   * -o -outputfile (结果输出文件，json？ excel？)
#   :return:
# Version：1.0
###############################################################################################################
"""
import argparse
import sys
import warnings
import json
import pandas as pd
import easyquotation as ezqtt
import ast
import re
import requests
from df_excel_define import is_mem_virtual_file_name, save_object_to_virtual_file

# 本程序调试时使用

# 外部调用是使用
import os
import datasource_ttjj as ttjj
import datasource_ths as ths
import datasource_akpack as akpack
STOCK_RESEARCH_CONFIG = "config/enhanceezqq/enhanceezqq_config.json"


class myBoc:
    """中行美元最新汇率"""

    url = "http://www.boc.cn/sourcedb/whpj/"

    def get_exchange_rate(self, currency="usa"):
        rep = requests.get(self.url)
        data = re.findall(r"<td *>(.*?)</td>", rep.text)

        if currency == "usa":
            return {"现汇买入：{}, 现钞买入：{}, 现钞卖出：{} 现钞卖出：{}，中行折算价：{}， 时间：{}".format(
                data[-13], data[-12], data[-11], data[-10], data[-9], data[-8])}
        return {}


def enhanceezqq_main(*args, **kwargs):
    """
    -f 优先级最高， -s -c结合获取股票信息
    * -s -datasource 数据来源（sina，jsl， qq, tencent, boc, timekline, dayline, hkquote)
    * -c -code stockcode1 stockcode2 ...... 股票代码列表, 可以多个
    * -p --prefix
    * -f -commandfile 使用指定json文件输入命令参数
    * -u -updatelist 根据网络数据更新本地stockcode缓冲清单
    * -his y 获取基金的历数据
    * -g -getlist （realtime/nonrealtime) 获取stockcode清单，realtime(直接使用网络数据), nonrealtime（使用本地缓冲数据）
    * -o -outputfile (结果输出文件，json？ excel？)
    :return:
    """
    # 获取命令参数
    # print(sys.path)
    # 默认输入文件名list
    warnings.filterwarnings('ignore')

    # 当函数被内部其他函数调用，而不是从外部直接option运行时，将argc、kwargs转化为argv
    if len(sys.argv) == 1:
        argvstr = []
        for key, value in kwargs.items():
            # 对于每个kwargs， 将key加上“-”， value按空格split为单个串，并且丢弃空串
            argvstr.append("-{}".format(key))
            argvstr += [x for x in value.split(" ") if x]
        # 现有的sys.argv[0]、argc（转换为字符串）、转换后的kwargs合并为完整的sys.argv供argparse模块使用
        sys.argv = [sys.argv[0]] + [str(x) for x in args] + argvstr
        print("内部调用, 将argc:{}, kwargs:{} 转化为argv".format(args, kwargs))


    # 数据源
    datasourcedefault = 'sina'
    # 可用数据源
    datasourcelist = [
        'sina',             # sina： A股，sh， sz 000001
        'jsl',              # 集思录
        'qq',               # 腾讯： A股
        'tencent',          # 同上
        'boc',              # 中银 外汇牌价，目前只支持usa
        'timekline',        # A股 当天K线
        'daykline',         # 港股 1500天日K 00001
        'hkquote',          # 港股 00001
        'ttjj',             # 天天基金, 实时基金估值，如果his -y  则为获取基金历史数据
        'ths',              # 同花顺基金, 实时基金估值， 如果his -y 则为获取基金历史数据
        'akpack',           # akshare 实时基金估值，如果his -y 则为获取基金历史数据
        'funddb',           # 数据库基金历史数据
        'stockdb'           # 数据库股票历史数据

    ]

    JSL_ETFINDEX = 'etfindex'
    JSL_FUNDA = 'funda'
    JSL_FUNDB = 'fundb'
    JSL_FUNDM = 'fundm'
    JSL_FUNDARB = 'fundarb'
    JSL_QDII = 'qdii'
    JSL_CB = 'cb'
    jsltypedefault = JSL_ETFINDEX
    jsltypelist = {
        JSL_FUNDA,            # 分级a
        JSL_FUNDM,            # 母基金
        JSL_FUNDB,            # 分级b
        JSL_FUNDARB,          # 分级套利
        JSL_ETFINDEX,         # 指数
        JSL_QDII,             # qdii
        JSL_CB                # 可转债
    }
    jslparamdefault = "nan"

    jslparambase = {
        JSL_FUNDA: [None, 0, 0, False, False],
        JSL_FUNDB: [None, 0, 0, False],
        JSL_FUNDM: [],
        JSL_FUNDARB: ["", "", 100, 100, 'price'],
        JSL_QDII: [0],
        JSL_ETFINDEX: ["", 0, None, None],
        JSL_CB: [0, None]
    }

    # 股票代码
    stockcodesdefault = ['000001']
    # 是否添加股票代码前缀
    prefixflag = 'y'
    # 是否根据网络数据更新本地股票代码信息
    updatecodesflag = 'n'
    # 是否更新历史数据的本地缓存
    historyflag = 'n'
    # 是否从网络股票代码信息
    getcodesflag = 'n'
    getcodechoice = ['real', 'local']
    # 输出结果配置文件
    resultconfigfile = 'nan'
    # 默认输出文件名
    resultfile = 'd:/temp/equotation_result.xlsx'
    # 是否输出过程log到屏幕
    printlogflag = 'y'

    try:
        with open(STOCK_RESEARCH_CONFIG, "r", encoding="utf-8") as fp:
            configdic = json.load(fp)
            databaseinfo = configdic["database"]
            fp.close()
    except Exception as err:
        print("读取配置文件：{}失败：{}".format(STOCK_RESEARCH_CONFIG, err))
        exit(-1)

    # 设置各个参数
    parser = argparse.ArgumentParser(description='easyquotation投资交易信息')
    # 获取股票信息来源
    parser.add_argument('-s', '-datasource', type=str,  default=datasourcedefault, choices=datasourcelist,
                        help='股票信息来源：{}, 默认值：{}'.format(datasourcelist, datasourcedefault))

    # 需要获取数据的标的代码
    parser.add_argument('-c', '-code', nargs="+", type=str,  default=stockcodesdefault,
                        help='需要获取数据的标的代码列表：[代码1，[代码2,......]], all表示所有, 默认值：{}'.format(
                            stockcodesdefault))
    # 是否增加代码前缀
    parser.add_argument('-p', '-prefixflag', type=str, choices=("y", "n", "Y", "N"), default=prefixflag,
                        help='是否增加代码前缀, 默认值：{}'.format(prefixflag))

    # 是否打印log到屏幕
    parser.add_argument('-l', '-printlog', type=str, choices=("y", "n", "Y", "N"), default=prefixflag,
                        help='是否打印log到屏幕, 默认值：{}'.format(printlogflag))

    # 是否更新股票本地代码信息
    parser.add_argument('-u', '-updateflag', type=str, choices=("y", "n", "Y", "N"), default=updatecodesflag,
                        help='是否根据网络数据更新股票代码信息的本地缓冲, 默认值：{}'.format(updatecodesflag))

    # 是否更新基金或者股票的历史数据本地缓存
    parser.add_argument('-his', '-history', type=str, choices=("y", "n", "Y", "N"), default=historyflag,
                        help='是否根据网络数据更新股票数据的本地缓冲, 默认值：{}'.format(historyflag))

    # 获取股票全部股票代码
    parser.add_argument('-g', '-getcodes', type=str, choices=getcodechoice, default=getcodesflag,
                        help='获取网络股票代码/本地缓冲信息, 默认值：{}'.format(getcodesflag))

    # 数据源为jsl时的子参数
    parser.add_argument('-j', '-jsltype', type=str,  default=jsltypedefault, choices=jsltypelist,
                        help='jsl子项选择：{}, 默认值：{}'.format(jsltypelist, jsltypedefault))

    # jsl子参数对应的param
    parser.add_argument('-t', '-jslparam', nargs="+", type=str,  default=jslparamdefault,
                        help='jsl子参数对应的param的列表：[param1，[param2,......]], nan表示使用默认值, 默认值：{}'.format(
                            jslparamdefault))

    # 输出结果配置文件
    parser.add_argument('-f', '-outconfig', type=str, default=resultconfigfile,
                        help='输出结果配置json文件，默认值：{}'.format(resultconfigfile))

    # 输出结果文件
    parser.add_argument('-o', '-output', type=str, default=resultfile,
                        help='输出结果Excel文件，默认值：{}'.format(resultfile))

    args, argv = parser.parse_known_args()
    if argv:
        print("命令错误，未知option：{}".format(argv))
        return 206
    args = parser.parse_args()
    mydatasource = args.s.lower()
    mystockcodes = args.c
    myprefixflag = True if args.p.lower() == 'y' else False
    myupdateflag = args.u.lower()
    myhistoryflag = args.his.lower()
    mygetcodesflag = args.g.lower()
    myresultconfig = args.f if args.f != resultconfigfile else None
    myresultfile = args.o
    myjsltype = args.j.lower()
    myjslparam = args.t
    myprintlogflag = True if args.l.lower() == 'y' else False

    if myprintlogflag:
        print("result sys.argv:{}".format(sys.argv))
        print("默认输入参数：{}".format(sys.argv[1:]))
        print("数据源：{}，标的代码：{}，前缀：{}， 是否更新：{}，获取股票代码方式：{}，jsl: {}, jslparam: {}, 输出文件：{}".format(
            mydatasource, mystockcodes, myprefixflag, myupdateflag, mygetcodesflag, myjsltype, myjslparam, myresultfile))
    # 列名与数据对其显示
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 更新选项优于-s -c
    if myupdateflag == 'y':
        # 首先从网络更新本地缓冲，然后返回缓冲后的股票列表
        ezqtt.update_stock_codes()
        resultcontent = ezqtt.get_stock_codes(realtime=False)
        resultdf = pd.DataFrame(resultcontent)
    # 获取stock/fund code本地list选项优先级其次
    elif mygetcodesflag == 'real':
        resultcontent = ezqtt.get_stock_codes(realtime=True)
        resultdf = pd.DataFrame(resultcontent)
    elif mygetcodesflag == 'local':
        resultcontent = ezqtt.get_stock_codes(realtime=False)
        resultdf = pd.DataFrame(resultcontent)
    else:
        if mydatasource == 'boc':
            datasource = myBoc()
        elif mydatasource == "ttjj":
            # {
            #     "ip_address": "192.168.31.237",
            #     "port": 3306,
            #     "database_name": "stk_research",
            #     "user_name": "admin",
            #     "password": "30028b684f025758ced1447add1eec57"
            #     "select_limit": 10000
            # }
            datasource = ttjj.Ttjj(ip=databaseinfo["ip_address"],
                                   port=databaseinfo["port"],
                                   database=databaseinfo["database_name"],
                                   databasetype=databaseinfo["database_type"],
                                   user=databaseinfo["user_name"],
                                   password=databaseinfo["password"],
                                   select_limit=databaseinfo['select_limit'])
        elif mydatasource == 'ths':
            datasource = ths.Ths(ip=databaseinfo["ip_address"],
                                 port=databaseinfo["port"],
                                 database=databaseinfo["database_name"],
                                 databasetype=databaseinfo["database_type"],
                                 user=databaseinfo["user_name"],
                                 password=databaseinfo["password"],
                                 select_limit=databaseinfo['select_limit'])
        elif mydatasource == 'akpack':
            datasource = akpack.Akpack(ip=databaseinfo["ip_address"],
                                       port=databaseinfo["port"],
                                       database=databaseinfo["database_name"],
                                       databasetype=databaseinfo["database_type"],
                                       user=databaseinfo["user_name"],
                                       password=databaseinfo["password"],
                                       select_limit=databaseinfo['select_limit'])
        elif mydatasource == "funddb":
            datasource = ths.Ths(ip=databaseinfo["ip_address"],
                                 port=databaseinfo["port"],
                                 database=databaseinfo["database_name"],
                                 databasetype=databaseinfo["database_type"],
                                 user=databaseinfo["user_name"],
                                 password=databaseinfo["password"],
                                 select_limit=databaseinfo['select_limit'])
        else:
            datasource = ezqtt.use(mydatasource)
        # 判断是否更新历史数据，优先级最高
        if myhistoryflag == 'y' and mydatasource in ['ths', 'ttjj', 'akpack']:
            resultdf = datasource.funds_history_save(mystockcodes)
        elif mydatasource in ["funddb"]:
            # 读取数据库历史数据
            resultdf = datasource.funds_history_load(mystockcodes)
        # boc 外汇牌价
        elif mydatasource == 'boc':           # 中银外汇牌价
            resultcontent = datasource.get_exchange_rate(mystockcodes[0])
            resultdf = pd.DataFrame(resultcontent)
        elif mydatasource == 'jsl':         # 集思录低风险投资
            # 根据类型确定需要使用的操作函数以及对应的参数类型
            # JSL_FUNDA: [None, 0, 0, False, False],
            # JSL_FUNDB: [None, 0, 0, False],
            # JSL_FUNDM: [],
            # JSL_FUNDARB: ["", "", 100, 100, 'price'],
            # JSL_QDII: [0],
            # JSL_ETFINDEX: ["", 0, None, None],
            # JSL_CB: [0, None]
            jslfunctiondict = {
                JSL_FUNDA: datasource.funda,
                JSL_FUNDB: datasource.fundb,
                JSL_FUNDM: datasource.fundm,
                JSL_FUNDARB: datasource.fundarb,
                JSL_ETFINDEX: datasource.etfindex,
                JSL_QDII: datasource.qdii,
                JSL_CB: datasource.cb
            }
            # 获取当前jsl下的默认输入参数，并用[:]完整复制，也可以用list()
            currentjslparam = jslparambase.get(myjsltype, jslparambase[JSL_ETFINDEX])[:]
            # 将输入的jsl子参数param顺序按type替换默认参数，如果为nna，直接使用base
            if 'nan' not in myjslparam:
                for index, param in enumerate(myjslparam):
                    # 输入参数根据实际的参数个数截短
                    if index >= len(currentjslparam):
                        break
                    # base类型为str时，直接用输入值替换，否则需要eval转换为实际类型
                    currentjslparam[index] = param \
                        if isinstance(currentjslparam[index], str) else ast.literal_eval(param)
            jslfunction = jslfunctiondict.get(myjsltype, jslfunctiondict[JSL_ETFINDEX])
            # 根据参数执行相应的jsl命令
            try:
                resultcontent = jslfunction(*currentjslparam)
            except Exception as err:
                print("jsl: {} 使用参数 param :{} 错误：{}".format(myjsltype, currentjslparam, err))
                print("jsl 方式下参数的基本格式如下：\n{}".format(jslparambase))
                return -1
            resultdf = pd.DataFrame(resultcontent.values())
        else:
            # datasource.stocks 与 datasource.real 相同， 获取实时数据
            if 'all' in mystockcodes:
                resultcontent = datasource.all_market
            else:
                resultcontent = datasource.stocks(mystockcodes, prefix=myprefixflag)
            resultdf = pd.DataFrame(resultcontent.values())

    # 当输出是多个df的list时，将输出文件带上序号（第一个不带），
    # 第二个从2开始输出多个输出数据文件，否则用原定义的文件；同时记录所有输出文件名，以便-j使用
    resultfilenameslist = []
    if not isinstance(resultdf, list):
        resultdf = [resultdf]
    for num, df in enumerate(resultdf):
        if myprintlogflag:
            print("处理输出结果{}：\n{}".format(num, df))
        if num == 0:
            # 第一个文件使用原始定义的文件名
            currentoutputfile = myresultfile
        else:
            # 第二个文件开始加上数字序号1-n
            insertposition = myresultfile.rfind(".")
            currentoutputfile = "".join([myresultfile[0: insertposition], str(num), myresultfile[insertposition:]])
        resultfilenameslist.append(currentoutputfile)
        try:
            if is_mem_virtual_file_name(currentoutputfile):
                save_object_to_virtual_file(currentoutputfile, df)
            else:
                df.to_excel(currentoutputfile, index=False)
        except Exception as err:
            print("输出到文件{}失败：{}".format(currentoutputfile, err))
            return -1
        if myprintlogflag:
            print("{}处理完成！".format(currentoutputfile))

    # 判断是否产生输出配置文件
    if myresultconfig is not None:
        # 形成输出字典
        tempdict = {"resultfiles": resultfilenameslist}
        try:
            if is_mem_virtual_file_name(myresultconfig):
                save_object_to_virtual_file(myresultconfig, tempdict)
            else:
                with open(myresultconfig, "w", encoding="utf-8") as fp:
                    json.dump(tempdict, fp, ensure_ascii=False, sort_keys=False, indent=4)
                    fp.close()
        except Exception as err:
            print("生成结果配置文件{}失败：{}".format(myresultconfig, err))
            return -1
        if myprintlogflag:
            print("结果配置文件{}处理完成！".format(myresultconfig))

    return 0


if __name__ == "__main__":
    sys.exit(enhanceezqq_main())
