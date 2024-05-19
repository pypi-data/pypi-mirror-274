# -*- coding: utf-8 -*-

from psgspecialelements import errprintwithname


def dftestfunction(ip: str, port: int = 8000, database: str = '',
                   user: str = '', password: str = '', sqlstr: str = ''):
    print("this is dftestfunction：ip:{}, port:{}, database:{}, user:{}, passowrd:{}, sqlstr:{}".format(
        ip, port, database, user, password, sqlstr))
    return [True, ""]


def dftestfunction1(specialdflist: list, tableindex: list, ip: str, port: int = 8000, database: str = '',
                    user: str = '', password: str = '', sqlstr: str = ''):
    print("this is dftestfunction1：ip:{}, port:{}, database:{}, user:{}, passowrd:{}, sqlstr:{}".format(
        ip, port, database, user, password, sqlstr))
    return


def dftestfunction2(specialdflist: list, tableindex: list, ip: str, port: int = 8000, database: str = '',
                   user: str = '', password: str = '', sqlstr: str = ''):
    print("this is dftestfunction1：ip:{}, port:{}, database:{}, user:{}, passowrd:{}, sqlstr:{}".format(
        ip, port, database, user, password, sqlstr))
    return [True, ""]


def dftestfunctionwithdf(specialdflist: list, tableindex: list, ip: str, port: int, database: str,
                         user: str, password: str = '', sqlstr: str = ''):
    """

    :param specialdflist:
    :param tableindex:
    :param ip:
    :param port:
    :param database:
    :param user:
    :param password:
    :param sqlstr:
    :return:
    """
    print("this is dftestfunctionwithdf：ip:{}, port:{}, database:{}, user:{}, passowrd:{}, sqlstr:{}".format(
        ip, port, database, user, password, sqlstr))
    return errprintwithname("出错输出测试：sql：{}导入数据到表格{}错误:{}！".format(sqlstr, tableindex, "错误代码测试"))


def dftestcolumnplus(specialdflist: list, tableindex: list,
                     opcolumn: list, resultcolname:str, plusflag: bool = True) -> list:
    """
    底层测试函数，对指定表的指定列按标记做+1或者*2输出到指定列
    :param specialdflist:           list: SepcialDf 当前系统处理的所有df列表
    :param tableindex:              list: 相对于specialdflist 列表函数要操作的specialdflist中的元素的下标列表[l,[m, n.....]], 元素从0到多个 
    :param opcolumn:                list: 操作的列[[], []]
    :param resultcolname:           str: 输出的列名
    :param plusflag:                bool: 是否使用+1， True：是， False：否， *2
    :return:                        list: [bool True:成功，False:失败, errstr]
    """
    # 获取当前指定的specialdf实例
    specialdf = specialdflist[tableindex[0]]
    # 获取当前操作的dataframe
    df = specialdf.dfdata
    # 获取操作列名称
    opcolname = opcolumn[1]
    try:
        df[resultcolname] = df[opcolname] + 1 if plusflag else df[opcolname] * 2
        # 更新specialdf和df相关的列信息
        specialdf.headings = df.columns.tolist()
        specialdf.colnamelist = specialdf.headings
        specialdf.colnameusedlist = [""] + specialdf.headings
        specialdf.colnamefilterlist = [""] + specialdf.headings
    except Exception as err:
        return errprintwithname("对指定列{}执行{}操作失败：{}".format(opcolumn, "+1" if plusflag else "*2", err))

    return [True, ""]
