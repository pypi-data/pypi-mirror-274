# -*- coding: utf-8 -*-
from psgspecialelements import *

"""
################################################################################################
# 定义所有和股票金融相关的计算
################################################################################################

"""


def dfstockcolumnsma(specialdflist: list, tableindex: list, inputcolumns: list,
                     resultcolname="", rollingcount=3) -> list:
    """
    对df的指定列计算简单移动平均
    :param specialdflist:           list: SepcialDf 当前系统处理的所有df列表
    :param tableindex:              list: 相对于specialdflist 列表函数要操作的specialdflist中的元素的下标列表[l,[m, n.....]], 元素从0到多个
    :param inputcolumns:            list: 用于计算的列序号、列名列表 [[num1, num2, ....],[name1,name2,....]],第一列有效
    :param resultcolname:           str:  生成的列列名
    :param rollingcount:            int: 移动均线的移动数
    :return:                        [bool True:成功，False:失败, errstr]
    """
    specialdf = specialdflist[tableindex[0]]
    df = specialdf.dfdata
    try:
        if resultcolname in [None, ""]:
            resultcolname = "SMA_{}".format(rollingcount)
        df[resultcolname] = df[df.columns[inputcolumns[0][0]]].rolling(rollingcount).mean()
        specialdf.headings = list(df)
        specialdf.colnamelist = specialdf.headings
        specialdf.colnameusedlist = [""] + specialdf.headings
        specialdf.colnamefilterlist = [""] + specialdf.headings
        # 刷新列类型
        specialdf.refreshcolumntype(columnnamelist=[resultcolname])
    except Exception as err:
        return errprintwithname("列:{} rolling：{} 生成移动均线列:{} 错误:{}".format(
            inputcolumns, rollingcount, resultcolname, err))

    return [True, ""]


def stockWMA(close, n):
    weights = np.array(range(1, n+1))
    sum_weights = np.sum(weights)

    res = close.rolling(window=n).apply(lambda x: np.sum(weights*x) / sum_weights, raw=False)
    return res


# 与上一个函数等价
def stockWMA1(close, n):
    return close.rolling(n).apply(lambda x: x[::-1].cumsum().sum() * 2 / n / (n + 1))


def dfstockcolumnwma(specialdflist: list, tableindex: list, inputcolumns: list,
                     resultcolname="", rollingcount=3) -> list:
    """
    对df的指定列计算加权移动平均
    :param specialdflist:           list: SepcialDf 当前系统处理的所有df列表
    :param tableindex:              list: 相对于specialdflist 列表函数要操作的specialdflist中的元素的下标列表[l,[m, n.....]], 元素从0到多个
    :param inputcolumns:            list: 用于计算的列序号、列名列表 [[num1, num2, ....],[name1,name2,....]],第一列有效
    :param resultcolname:           str:  生成的列列名
    :param rollingcount:            int:  移动均线的移动数
    :return:                        [bool True:成功，False:失败, errstr]
    """
    specialdf = specialdflist[tableindex[0]]
    df = specialdf.dfdata
    try:
        if resultcolname in [None, ""]:
            resultcolname = "WMA_{}".format(rollingcount)
        df[resultcolname] = stockWMA(df[df.columns[inputcolumns[0][0]]], rollingcount)
        specialdf.headings = list(df)
        specialdf.colnamelist = specialdf.headings
        specialdf.colnameusedlist = [""] + specialdf.headings
        specialdf.colnamefilterlist = [""] + specialdf.headings
        # 刷新列类型
        specialdf.refreshcolumntype(columnnamelist=[resultcolname])
    except Exception as err:
        return errprintwithname("列:{} rolling：{} 生成加权移动均线列:{} 错误:{}".format(
            inputcolumns, rollingcount, resultcolname, err))

    return [True, ""]


def dfstockcolumnema(specialdflist: list, tableindex: list, inputcolumns: list,
                     resultcolname="", rollingcount=3, min_periods=3) -> list:
    """
    对df的指定列计算指数移动平均
    :param specialdflist:           list: SepcialDf 当前系统处理的所有df列表
    :param tableindex:              list: 相对于specialdflist 列表函数要操作的specialdflist中的元素的下标列表[l,[m, n.....]], 元素从0到多个
    :param inputcolumns:            list: 用于计算的列序号、列名列表 [[num1, num2, ....],[name1,name2,....]],第一列有效
    :param resultcolname:           str:  生成的列列名
    :param rollingcount:            int:  移动均线的移动数
    :param min_periods:             int:  最小周期
    :return:                        [bool True:成功，False:失败, errstr]
    """

    specialdf = specialdflist[tableindex[0]]
    df = specialdf.dfdata
    try:
        if resultcolname in [None, ""]:
            resultcolname = "EMA_{}".format(rollingcount)
        # ema: com or span or halflife or alpha, 四个参数要填写一个
        df[resultcolname] = df[df.columns[inputcolumns[0][0]]].ewm(span=rollingcount, min_periods=min_periods).mean()
        specialdf.headings = list(df)
        specialdf.colnamelist = specialdf.headings
        specialdf.colnameusedlist = [""] + specialdf.headings
        specialdf.colnamefilterlist = [""] + specialdf.headings
        # 刷新列类型
        specialdf.refreshcolumntype(columnnamelist=[resultcolname])
    except Exception as err:
        return errprintwithname("列:{} rolling：{} 生成指数移动均线列:{} 错误:{}".format(
            inputcolumns, rollingcount, resultcolname, err))

    return [True, ""]


def dfstockcolumnmacd(specialdflist: list, tableindex: list, inputcolumns: list, resultcolname="") -> list:
    """
    对df的指定列计算指数移动平均
    :param specialdflist:           list: SepcialDf 当前系统处理的所有df列表
    :param tableindex:              list: 相对于specialdflist 列表函数要操作的specialdflist中的元素的下标列表[l,[m, n.....]], 元素从0到多个
    :param inputcolumns:            list: 用于计算的列序号、列名列表 [[num1, num2, ....],[name1,name2,....]],第一列有效
    :param resultcolname:           str:  生成的列列名
    :return:                        [bool True:成功，False:失败, errstr]
    """

    specialdf = specialdflist[tableindex[0]]
    df = specialdf.dfdata
    try:
        if resultcolname in [None, ""]:
            resultcolname = "MACD"
        # MACD指标用法：
        #
        # MACD金叉: DIFF # 由下向上突破 , DEA，为买入信号。
        # MACD死叉: DIFF # 由上向下突破,  DEA，为卖出信号。
        #  （1）计算移动平均值：EMA
        SMA_FAST = df[df.columns[inputcolumns[0][0]]].rolling(12).mean()
        SMA_SLOW = df[df.columns[inputcolumns[0][0]]].rolling(26).mean()
        # （2）计算离差值：DIF
        DIF = SMA_FAST - SMA_SLOW
        # （3）计算：DEA
        DEA = DIF.rolling(9).mean()
        # （4）计算柱状图MACD
        df[resultcolname] = (DIF - DEA) * 2

        specialdf.headings = list(df)
        specialdf.colnamelist = specialdf.headings
        specialdf.colnameusedlist = [""] + specialdf.headings
        specialdf.colnamefilterlist = [""] + specialdf.headings
        # 刷新列类型
        specialdf.refreshcolumntype(columnnamelist=[resultcolname])
    except Exception as err:
        return errprintwithname("列:{} 生成MACD列:{} 错误:{}".format(inputcolumns, resultcolname, err))

    return [True, ""]