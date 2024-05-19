# -*- coding: utf-8 -*-

"""
####################################################################################################################
# DFTrans V2.0.2
# 使用dataframe作为底层， 进行数据文件处理
# 提供一种简单实用的数据批量处理工具，使用户可以方便地通过所见即所得的图形化界面，记录对于多个不同数据源（excel、csv、txt、数据库表等）
# 的各种操作（行处理、列处理、表内处理、表间处理等），并自动形成相应的操作记录，在此基础上，可以对操作记录进行单步、多步、回退、全部执行
# 等调试验证，验证通过的操作命令记录文件可在非图形方式下全速后台执行，对多个数据源的数据自动进行批量处理，并输出多个处理结果文件或者数据库表。
#####################################################################################################################
"""
import pandas as pd
from openpyxl import load_workbook
import copy
import argparse
import os
from pathlib import Path
import sys
import warnings
import json
import jsonlines
import PySimpleGUI as Sg
import ctypes
from psgspecialelements import *
from hash_password import dftrans_simple_encrypt
from df_excel_define import *
from datetime import datetime
import re
import inspect
import importlib
from inspect import Parameter
from inspect import getmembers, isfunction
import collections
from IPy import IP
import ast

USER_FUNCTION_MODULE = "df_excel_define_user"


# 命令分类
COMMAND_ROW_PROCESS = '行处理'
COMMAND_COLUMN_PROCESS = '列处理'
COMMAND_TWO_DF_PROCESS = '双表处理'
COMMAND_MULTI_DF_PROCESS = '多表处理'
COMMAND_SINGLE_DF_PROCESS = '单表处理'
COMMAND_NEW_TABLE_IMPORT = '表格导入'
COMMAND_OTHER = '扩展功能'
COMMAND_TYPE_LIST = [
    COMMAND_ROW_PROCESS,
    COMMAND_COLUMN_PROCESS,
    COMMAND_TWO_DF_PROCESS,
    COMMAND_MULTI_DF_PROCESS,
    COMMAND_SINGLE_DF_PROCESS,
    COMMAND_NEW_TABLE_IMPORT,
    COMMAND_OTHER
]
# 命令说明文件中，字段key
COMMAND_TYPE = "command_type"  # 命令分类
COMMAND_ENGLISH_NAME = "english_name"  # 命令英文名
COMMAND_SHOW_FLAG = "show_flag"  # 命令是否显示
COMMAND_NEW_TABLE_FLAG = "new_table"  # 命令是否产生新表
COMMAND_MULTI_DF_FLAG = "used_table_number"  # 命令涉及的表格数
COMMAND_FUNCTION_NAME = "function_name"  # 命令有用到的函数名
COMMAND_FUNCTION_PARAM = "function_param"  # 命令用到的函数的argv列表
COMMAND_FORMAT = "command_format"  # 转化命令为处理函数时使用的格式串，之后调用eval执行
COMMAND_SEND_PROCCESSING_EVENT = 'percentage_bar'  # 命令是否使用进度条窗口显示进度信息
COMMAND_USER_INPUT_PARAM = "user_operate"  # 是否记录用户参数输入值
COMMAND_USED_INPUT_FORMAT = "record_format"  # 采用记录方式时，用来拼接命令的格式串
FUNCTION_ARG_TYPE = "type"  # 参数类型
FUCNTION_ARG_VALIDVALUE = "validvalue"  # 参数合法值
FUNCTION_ARG_DEFAULTVALUE = "defaultvalue"  # 参数默认值
FUNCTION_ARG_SENTENCE = "sentence"  # 参数语法说明
FUNCTION_ARG_COMMENT = "comment"  # 参数配置字段说明
FUNCTION_ARG_LONG_COMMENT = "long_comment"  # 参数配置字段说明，信息较多，

# 是否产生新表
NOT_GENERATE_NEW_TABLE = "否"
GENERATE_NEW_TABLE = "是"
GENERATE_NEW_TABLE_FLAG_LIST = [
    NOT_GENERATE_NEW_TABLE,
    GENERATE_NEW_TABLE
]

RECORD_USER_PARAM_YES = "是"
RECORD_USER_PARAM_NO = "否"

RECORD_USER_PARAM_LIST = [
    RECORD_USER_PARAM_YES,
    RECORD_USER_PARAM_NO
]

SEND_PROCESSING_EVENT_YES = '是'
SEND_PROCESSING_EVENT_NO = '否'

SEND_PROCESSING_EVENT_LIST = [
    SEND_PROCESSING_EVENT_YES,
    SEND_PROCESSING_EVENT_NO
]

# 命令是否显示
NOT_SHOW_COMMAND_FLAG = "否"
SHOW_COMMAND_FLAG = "是"
SHOW_COMMAND_FLAG_LIST = [
    NOT_SHOW_COMMAND_FLAG,
    SHOW_COMMAND_FLAG
]

# 命令表格中list，每个字段的偏移量
CURRENT_COMMAND = 0
CURRENT_OPERATE_DFS = 1
CURRENT_COMMAND_PARAMS = 1
CURRENT_MULTI_TABLE_RESULT = 3
CURRENT_COLUMN_ROW_INFO = 3

# 在命令行中区分单表、两表、多表命令
SINGLE_DF = "单表"
TWO_DF = "双表"
MULTI_DF = "多表"

OPERATE_DFS_NUMBER_FLAG_LIST = [
    SINGLE_DF,
    TWO_DF,
    MULTI_DF
]

# 函数说明中的常量定义
FUNCTION_PARAM_TYPE = 0
FUNCITON_PARAM_VALID_VALUE = 1
FUNCTION_PARAM_DEFAULT_VALUE = 2
FUNCTION_PARAM_SENTENCE = 3

# 调试环境中运行模式，单步、运行到光标、全部运行
STEP_RUN = 0
TO_CURRENT_RUN = 1
ALL_RUN = 2

# 命令是否已经运行标记
COMMAND_EXECUTED_FLAG = 0


fileprocconfig = 'config/DFTrans/DFTrans_config.json'
useroperatedir = 'filetrans'
userconfigfile = 'user_operate_record.json'

DFTRANS_SYSTEM_DATA_FILES = [fileprocconfig, LOCAL_SYSTEM_ICON, LOCAL_SYSTEM_IMAGE]

global usecolumnnameforprocess, originfunctiondict, commanddict, commandcomment
global commandalias, showversioninfo, ramfilesuffix
global localusecolumnnameforprocess, localoriginfunctiondict, localcommanddict
global commandcombolist, commandtabledictlist, commandtablekey, commandmenulist
global currentdfnamelist, currentdfcolumnlist, commandmenudict, datatablebuttonmenuevent, datatablerightclickevent
global specialdflist, specialdflistcopy, usermodule
global mycommandlistfile, myinputfiles, commandfilecomment
global totalprocesslist
global mainwindow, editwindow
global debugflag


def getsystemresolution():
    # http://www.manongjc.com/detail/32-pmcdxhxcuaptfos.html
    user32 = ctypes.windll.user32
    # # 单显示器屏幕宽度和高度:
    # screen_size0 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # # 对于多显示器设置,您可以检索虚拟显示器的组合宽度和高度:
    # screen_size1 = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1),
            user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)]


def commandfunctionchoose2config(functionname: str, commandtype: str, newtableflag: str,
                                 usedtablenumber: str, argvparam: list,
                                 initialflag: bool = True) -> list:
    """
    根据命令行配置中的相关选项生成 命令转换结构串和命令记录结构串
    :param functionname:                                str: 函数名称
    :param commandtype:                                 str: 命令分类类别
    :param newtableflag:                                str: 命令是否产生新表标记
    :param usedtablenumber:                             str: 命令使用的表格数类型标记
    :param argvparam:                                   str: 命令涉及的argv的list
    :param initialflag:                                 bool: True 初始化是调用，False：页面配置编辑调用
    :return:                                            [None, None, None, None] |
                                                        [命令转换结构串, 命令记录结构串, 命令转换演示示例， 命令记录演示示例]
    """
    errresult = [None, None, None, None]
    global originfunctiondict, localoriginfunctiondict
    # 函数名为空时，无法处理
    if functionname.strip() == "":
        return errresult

    # 根据函数名获取函数配置信息
    if initialflag:  # 初始化调用
        functionconfig = originfunctiondict.get(functionname, False)
    else:
        functionconfig = localoriginfunctiondict.get(functionname, False)

    # 函数无配置，无法处理
    if functionconfig is False:
        return errresult

    # 函数配置不正确，无法处理
    argcitems, argcconfig, argvconfig = map(functionconfig.get, ["argcitems", "argc", "argv"], [None, None, None])
    if None in [argcitems, argcconfig, argvconfig]:
        return errresult

    try:
        # 获取argc 参数类型str
        argcstructurestr = [
            "".join(["'{", str(item + 5), "}'"])
            if paramtypetransmap[argcconfig.get(argc, None)[FUNCTION_ARG_TYPE]][PARAM_TYPE_VALID] in [str, check_ip]
            else "".join(["{", str(item + 5), "}"])
            for item, argc in enumerate(argcitems)]

        # 根据各个选项拼接命令结构串
        # SPECIALFUNCTION = ["dfswapposition", "dfdroptables"] # 2023/1/12 全部函数简化为{1}，{3}, 无论是否使用输入参数 nouse
        commandstructurestr = "".join([
            # 1、函数名称+df相关参数
            "{0}({1}, {3}",  # 2023/1/12 全部函数简化为{1}，{3}, 无论是否使用输入参数

            # 1.5、当argc，argv有一个有值就需要","
            ", " if len(argcstructurestr) > 0 or len(argvparam) > 0 else "",
            # 2.argcparam，字符串型需要加'{x}', 否则{x}
            ", ".join(argcstructurestr),
            # 3、避免argc为空 , argc不为空并且argv有值才需要","
            ", " if len(argcstructurestr) > 0 and len(argvparam) > 0 else "",
            # 4、argvparam + )
            "**dict({{}}, **{4}))" if len(argvparam) > 0 else ")",
        ])
        # 根据各个选项拼接命令记录结构串
        # "采用记录方式时，用来拼接命令的格式串,
        #  {0} currentsubtab[1], {1}selectedrow, {2}selectedcolumn,
        #  {3} currentrowcontent, {4}currentcolumnname, {5}len(specialdflist), {6}specialdflist"
        # "[{0}], {{}}, [{5}], '192.168.1.1', 8000, '', '', '', ''"
        # argv对应的子语句
        # 获取当前命令使用的argv的默认值并组成字典
        tempargvdefaultdict = dict(
            zip(argvparam, [argvconfig.get(x, None)[FUNCTION_ARG_DEFAULTVALUE] for x in argvparam]))
        # argc对应的子语句
        # 获取argc的自定义类型
        argctypelist = [argcconfig.get(argc, None)[FUNCTION_ARG_TYPE] for argc in argcitems]
        # 获取当前命令使用的argc的默认值并组成list
        argcdefaultlist = [argcconfig.get(x, None)[FUNCTION_ARG_DEFAULTVALUE] for x in argcitems]
        # {1}selectedrow, {2}selectedcolumn, {3}currentrowcontent, {4}currentcolumnname, {6}specialdflist"
        argcdefaultupdatedict = {
            "rows": {1},
            "columns": {2},
            "rowvaluelist": {3},
            "columnname": {4},
            "newtable": [{5}]  # newtable 直接使用 [{5}], 抛弃现有默认值
        }
        # 对于list中, 第一次出现的columns类别或者rows类别等进行替换
        specialstr = "xyz1234****5677999**frankgong_gyj"
        for i, defaultvalue in enumerate(argctypelist):
            tempnew = argcdefaultupdatedict.get(defaultvalue, specialstr)  # 确定是否有需要替代（有特殊的返回值）
            if tempnew != specialstr:
                argcdefaultlist[i] = tempnew  # 如果找到，说明需要替换
                argcdefaultupdatedict.pop(defaultvalue)  # 每个替换值只用一次

        recordstructurestr = "".join([
            "[{0}], ",  # 操作的表号
            "".join(["{", "{}".format(tempargvdefaultdict), "}"]),  # 变参argv内容
            ", " if len(argcdefaultlist) > 0 else "",
            str(argcdefaultlist)[1: -1],  # 将默认值list转化为串，去掉[, ]
        ])
    except Exception as err:
        print("函数:{}, 新表标记:{}，表数:{}, 变参:{}串接格式失败：{}".format(
            functionname, newtableflag, usedtablenumber, argvparam, err))
        return errresult
    # 命令结构演示代码
    # {0}：函数名 {1}:dfprefix， {2}:当前处理df列表, {3}：当前处理df下标列表  {4}:字典参数字典：删除行的序号列表 {5}..其他位置参数
    # 'functionname', 'specialdflist', '[specialdflist[0], specialdflist[1], ...]', [0, 1, ...], {"a": x1, "b": x2...},...
    commandtdemostr = commandstructurestr.format(
        functionname,
        "specialdflist",
        "specialdflist[0]"
        if usedtablenumber == SINGLE_DF else "[specialdflist[0], specialdflist[1]]"
        if usedtablenumber == TWO_DF else "[specialdflist[0], specialdflist[1]...]",  # 该参数保留实际已经无效
        "[0]" if usedtablenumber == SINGLE_DF else "[0, 1]"
        if usedtablenumber == TWO_DF else "[0, 1, 2...]",
        str(dict([(x, argvconfig[x].get(FUNCTION_ARG_DEFAULTVALUE, None)) for x, y in argvconfig.items()])),  # {4} 字典参数
        *argcitems  # {5}..... 位置参数列表
    )
    # 记录结构演示
    # {0} currentsubtab[1], {1}selectedrow, {2}selectedcolumn,
    # {3}currentrowcontent, {4}currentcolumnname, {5}len(specialdflist) , {6}specialdflist"
    recordstructuredemo = recordstructurestr.format(
        "0",  # currentsubtab[1]
        "[0,1,2...]",  # selectedrow
        "[[0,1,...],['列名1','列名2',...]]",  # selected columns
        "['列1值','列2值',...]",  # currentrowcontent
        "新列名",  # currentcolumnname
        "4",  # len(specialdflist)
        "specialdflist"  # specialdflist
    )

    return [commandstructurestr, recordstructurestr, commandtdemostr, recordstructuredemo]


def loadcommandfile(initialflag: bool = False):
    """
    将命令文件导入到界面
    :param initialflag       bool，True, 初始化调用，mycommandlistfile已经有初始值，False：打开界面用户选择命令文件
    :return:
    """
    global mycommandlistfile
    global commandtabledictlist
    global commanddict

    # 不是系统初始化，首先指定命令文件
    if initialflag is False:
        filetemp = Sg.popup_get_file(
            '选择命令文件',
            icon=LOCAL_SYSTEM_ICON,
            file_types=(("Jsonl命令文件", "*.jsonl"),),
            initial_folder='./data/301_df_file_trans/',
            default_path='',
            no_window=True,
            keep_on_top=True,
            modal=True)
        if filetemp:
            mycommandlistfile = filetemp
        else:
            return

    global totalprocesslist, commandfilecomment
    totalprocesslist = []
    commandfilecomment = {}
    if mycommandlistfile != "":
        try:
            with jsonlines.open(mycommandlistfile) as fp:
                for i, item in enumerate(fp):
                    if i == 0:
                        # 对于第一行，首先检查是否注释
                        tempcomment = item.get("comment", None)
                        commandfilecomment = tempcomment if tempcomment not in [None, ""] else {}
                    # 检查是否命令
                    tempcommand = item.get("command", None)
                    if tempcommand is not None:
                        # 获取命令注释
                        templinecomment = item.get("linecomment", "")
                        totalprocesslist.append([tempcommand, templinecomment])
                fp.close()
        except Exception as err:
            print("读取命令文件：{}失败：{}".format(mycommandlistfile, err))
            sys.exit(-1)

    # 形成字典方式的list
    commandtabledictlist = [
        dict(commandfinished='否',  # 已执行标记
             commandstring=command2sentence(item[0]),  # 命令行对应的解释语句
             commandparam=str(item[0]),
             linecomment=item[1])  # 命令语句
        for item in totalprocesslist]

    # 非初始化，刷新数据
    if initialflag is False:
        mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_WHOLEVALUE,
                                           currentwindow=mainwindow, headings=list(columninfodic),
                                           infodict=commandtabledictlist)

        # 重置命令执行状态，不修改上次运行产生的数据,命令列表已经全部设置为’否‘，只需要重置所有命令的颜色
        for item in range(mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_MAXROWNUMBER)):
            # 修改已执行的命令的颜色
            # mainwindow[commandtablekey].update(row_colors=((item, 'black', 'white'), (item, 'white')))
            defaultcolor = (INPUT_TEXT_COLOR, INPUT_TEXT_BACKGROUND_COLOR) \
                if CELL_EDITABLE else (TEXT_COLOR, TEXT_BACKGROUND_COLOR)
            mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                                               currentwindow=mainwindow,
                                               rownumber=item, color=defaultcolor)

        Sg.popup_ok("命令文件{}导入完成！".format(mycommandlistfile),
                    keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)


def savecommandfile() -> bool:
    """
    保存当前的command到file
    :return:                    bool True:成功，False:失败
    """
    global mycommandlistfile
    filetemp = Sg.popup_get_file('选择输出文件',
                                 save_as=True,
                                 file_types=(("Jsonl命令文件", "*.jsonl"),),
                                 initial_folder=os.path.dirname(mycommandlistfile),
                                 default_path='',
                                 keep_on_top=True,
                                 modal=True,
                                 no_window=True)
    if filetemp:
        tempdic = {}
        mycommandlistfile = filetemp
        # 获取命令行的字典list
        resultdictlist = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
        # 逐个字典获取需要的命令行串并转换成list，加入list二维数组
        # 将list二维数组组成字典list写入批量写入jsonl
        try:
            with jsonlines.open(mycommandlistfile, 'w') as fp:
                # 首先写入注释表头
                fp.write({"comment": commandfilecomment})
                # 从返回的字典list中逐个抽取命令行组成命令行字典list，成批写jsonl
                fp.write_all(
                    {
                        "command": ast.literal_eval("{}".format(itemsdict[columninfodic['命令语句']])),
                        "linecomment": itemsdict[columninfodic['命令备注']]
                    } for itemsdict in resultdictlist)
        except Exception as err:
            Sg.popup_error("写命令文件：{} 失败:{}！".format(mycommandlistfile, err),
                           modal=True, keep_on_top=True, )
            return False

        Sg.popup_ok("命令文件{}导出完成！".format(mycommandlistfile),
                    keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
        return True


def transfilecommenttostr(commentdict: dict) -> str:
    """
    将注释字典转换成字符串
    :param commentdict:
    :return:
    """
    tempstr = ""
    for key, values in commentdict.items():
        tempstr = "\n".join([
            tempstr,
            "----------------------------" + "表{}".format(key) + "----------------------------",
            "行数：{}，列数：{}".format(values.get("行数", None), values.get("列数", None)),
            "列名：\n{}".format("".join([("[{:=02d}]{}".format(x, y).ljust(16) + ("\n" if (x + 1) % 5 == 0 else '\t'))
                                      for x, y in enumerate(values.get("列名", []))])),
        ])
    return tempstr


def generatecommandfilecomment():
    """
    根据当前specialdflist生成命令文件头，并确认是否替换当前文件头
    :return:
    """
    print("generate command comment")
    global specialdflist, commandfilecomment
    tempfilecomment = {}
    for item in range(len(specialdflist)):
        tempdict = {}
        tempdict['行数'], tempdict['列数'] = specialdflist[item].dfdata.shape[0], specialdflist[item].dfdata.shape[1]
        tempdict['列名'] = list(specialdflist[item].dfdata)
        tempfilecomment['[{}]'.format(item)] = tempdict
    tempstr = transfilecommenttostr(tempfilecomment)
    currentstr = transfilecommenttostr(commandfilecomment)
    diffstr = ""
    # 先判断哪个字典更长
    if len(tempfilecomment.keys()) > len(commandfilecomment.keys()):
        firstcomment, secondcomment, switchflag = tempfilecomment, commandfilecomment, False
    else:
        firstcomment, secondcomment, switchflag = commandfilecomment, tempfilecomment, True
    # 逐项比较
    for keys, values in firstcomment.items():
        # 先比较表格本身
        comparevalues = secondcomment.get(keys, None)
        if comparevalues is None:
            diffstr += "表{}格式不一致\n".format(keys)
        else:
            # 再比较表格内的行、列、列名信息
            diffstr += "----------------表{}------------------\n".format(keys)
            for subkeys, subvalues in values.items():
                subcomparevalues = comparevalues.get(subkeys, None)
                if subcomparevalues is None:
                    diffstr += "[{}]格式不一致\n现值：\n{}\n原值：\n{}\n".format(
                        subkeys,
                        None if switchflag else subvalues,
                        subvalues if switchflag else None)
                elif subcomparevalues != subvalues:
                    diffstr += "[{}]格式不一致\n现值：\n{}\n原值：\n{}\n".format(
                        subkeys,
                        subcomparevalues if switchflag else subvalues,
                        subvalues if switchflag else subcomparevalues)

    layout = [[
        Sg.Col([[Sg.Text("原有注释")],
                [Sg.Multiline(
                    default_text=currentstr, size=(100, 20), font='黑体 10',
                    expand_x=True, expand_y=True, write_only=True, auto_size_text=True,
                    autoscroll=True, auto_refresh=True, k='temp1',
                    reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                    visible=True, disabled=True, metadata=False)]]),
        Sg.Col([[Sg.Text("新有注释")],
                [Sg.Multiline(
                    default_text=tempstr, size=(100, 20), font='黑体 10',
                    expand_x=True, expand_y=True, write_only=True, auto_size_text=True,
                    autoscroll=True, auto_refresh=True, k='temp2',
                    reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                    visible=True, disabled=True, metadata=False)]])],
        [
            Sg.Col([[Sg.Text("新旧注释差异")],
                    [
                        Sg.Multiline(
                            default_text=diffstr, font='黑体 10', size=(205, 20),
                            expand_x=True, expand_y=True, write_only=True, auto_size_text=True,
                            autoscroll=True, auto_refresh=True, k='temp3',
                            reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                            visible=True, disabled=True, metadata=False)]])
        ],
        [
            Sg.Col([[Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')]], justification='r')
        ]
    ]
    commentwindow = Sg.Window('文件注释', layout, icon=LOCAL_SYSTEM_ICON,
                              font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=True)

    while True:
        event, values = commentwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        # 确定文件
        elif event == '_ok_':
            # 修改注释
            commandfilecomment = tempfilecomment
            break

        else:
            continue

    # 点击close或者关闭，不修改任何值，返回 None
    commentwindow.close()
    print(commandfilecomment)
    return


FUNCTION_NAME_LIST = "_funtion_name_list_"
FUNCTION_NAME_FRAME = '_function_name_frame_'
USE_COLUMNNAME_IN_FUNCTION = '_use_columnname_in_function_'
SHOW_VERSION_INFO = '_show_version_info_'
RAM_FILE_DIRECTORY = '_ram_file_directory_'
FUNCTION_NAME_EDIT = "".join(["编辑函数名", Sg.MENU_KEY_SEPARATOR, FUNCTION_NAME_LIST])
FUNCTION_NAME_ADD = "".join(["增加函数名", Sg.MENU_KEY_SEPARATOR, FUNCTION_NAME_LIST])
FUNCTION_NAME_DELETE = "".join(["删除函数名", Sg.MENU_KEY_SEPARATOR, FUNCTION_NAME_LIST])
FUNCTION_NAME_MOVE = "".join(["移动函数名", Sg.MENU_KEY_SEPARATOR, FUNCTION_NAME_LIST])
FUNCTION_ARGC_CONFIG_FRAME = '_function_argc_config_frame_'
FUNCTION_ARGV_CONFIG_FRAME = '_function_argv_config_frame_'
FUNCTION_ARGC_CONFIG_TABLE = '_function_argc_config_table_'
FUNCTION_ARGV_CONFIG_TABLE = '_function_argv_config_table_'
COMMAND_CONFIG_FRAME = '_command_config_frame_'
COMMAND_CONFIG_TABLE = '_command_config_table_'

VALID_DF_FUNCTION_PARAMS = ["specialdflist", "tableindex"]  # df 处理内部前两个参数的必须格式


def paramtypevalidcheckandtrans(paramvalue: str, paramtype: str) -> list:
    """
    根据系统定义的参数类型，检查字符串给四的paramvalue 转换格式后是否合法
    :param paramvalue:          str： 字符串形式的param
    :param paramtype:           str:  给当前param定义的type
    :return:                    list： [True,转化的值] 合法 , [False, errstr] 非法
    """
    if paramvalue is None:  # 如果是value是空None，适应各种type，直接返回成功
        return [True, paramvalue]

    # 获取类型对应的配置
    currenttypeconfig = paramtypetransmap.get(paramtype, None)
    if currenttypeconfig is None:  # 如果没有类型配置就转换，直接返回成功
        return [True, paramvalue]

    if not currenttypeconfig[PARAM_TYPE_TRANS_FLAG]:  # 属于不需要类型检查的类型，直接返回成功
        return [True, paramvalue]

    try:
        # 转换之后，检查转换结果是否合法
        if paramtype == 'ipaddress':  # ipaddress对应的是检查函数， 其他检查类型
            if currenttypeconfig[PARAM_TYPE_VALID](paramvalue) is False:
                errstr = "{}不是IP地址格式".format(paramvalue)
                if debugflag:
                    print(errstr)
                return [False, errstr]
            else:
                return [True, paramvalue]
        elif paramtype == "password":  # password是str，但是为了进行加解密，FLAG设置为True
            return [True, paramvalue]
        else:
            # 进行转换
            # 检查默认值的合法性
            if isinstance(ast.literal_eval(paramvalue), (currenttypeconfig[PARAM_TYPE_VALID], type(None))) is False:
                errstr = "{}类型{}错误：{}".format(paramvalue, currenttypeconfig[PARAM_TYPE_VALID], type(paramvalue))
                if debugflag:
                    print(errstr)
                return [False, errstr]
            else:
                return [True, ast.literal_eval(paramvalue)]
    except Exception as err:
        errstr = "{}类型转换失败：{}".format(paramvalue, str(err))
        if debugflag:
            print(errstr)
        return [False, errstr]

    return [True, ast.literal_eval(paramvalue)]


def functionparamitemeditgui(
        paramconfigitem: list, method: int = None,
        current_row: int = None, index_col_value: list = None) -> list:
    """
    编辑或者增加表格行，增加行需要判断是否已经存在关键词相同的记录
    :param paramconfigitem:         list, 表格行的一维列表， 位置参数, 不同表格这一参数都必须放在第一个
    :param method:                  EDIT_METHOD or ADD_METHOD
    :param current_row:             当前编辑的行号，用于判断是否重复
    :param index_col_value:         索引列的当前列值，用于判断是否重复值
    :return :                       [a, b, c,......] or None
    """
    # "rows": {
    #     "type": "rows",
    #     "validvalue": [],
    #     "defaultvalue": [],
    #     "sentence": "按行序号",
    #     "comment": "删除的行序号",
    #     "long_comment": "删除的行序号, 可多行[l, m, n...]"
    # }
    # ('参数名称', 'rows') ('参数类型', 'rows') ('合法值', '[]') ('默认值', '[]') ('命令行描述说明', '按行序号')
    # ('参数说明', '删除的行序号') ('参数详细说明', '删除的行序号, 可多行[l, m, n...]')
    NAME = '_param_name_'
    PARAMTYPE = '_param_type_'
    VALIDVALUE = '_valid_value_'
    DEFAULTVALUE = '_default_value_'
    SENTENCE = '_sentence_'
    COMMENT = '_comment_'
    LONGCOMMENT = '_long_comment_'

    # 表格的编辑页面
    paramconfiglayinfo = [
        [
            [Sg.Text("参数名称".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[0], k=NAME, size=(50, 1), font=DEF_FT_L)],
            [Sg.Text("参数类型".ljust(2), font=DEF_FT_L)],
            [Sg.InputCombo(list(paramtypetransmap), k=PARAMTYPE, pad=(5, 5),
                           default_value=paramconfigitem[1], enable_events=False,
                           font=DEF_FT_L, size=(49, 1), readonly=True)],
            [Sg.Text("合法值".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[2], k=VALIDVALUE, size=(50, 1), font=DEF_FT_L)],
            [Sg.Text("默认值".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[3], k=DEFAULTVALUE, size=(50, 1), font=DEF_FT_L)],
            [Sg.Text("命令行描述说明".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[4], k=SENTENCE, size=(50, 1), font=DEF_FT_L)],
            [Sg.Text("参数说明".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[5], k=COMMENT, size=(50, 1), font=DEF_FT_L)],
            [Sg.Text("参数详细说明".ljust(2), font=DEF_FT_L)],
            [Sg.Input(paramconfigitem[6], k=LONGCOMMENT, size=(50, 1), font=DEF_FT_L)],
        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('函数参数配置', paramconfiglayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    resultitem = None

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            resultitem = None
            break

        elif event == '_ok_':
            currentname = values[NAME]
            if currentname.strip() == "":
                Sg.popup_error("参数名称不能为空！", modal=True, keep_on_top=True, )
                continue
            # 检查是否重名
            if currentname in index_col_value:
                cmdindex = index_col_value.index(currentname)
                # 如果是编辑方式而且是当前编辑行，说明没有重复
                if not (method == EDIT_METHOD and cmdindex == current_row):
                    # 新增内容和原有内容重复
                    Sg.popup_error("{}和第{}条记录同名！".format(currentname, cmdindex),
                                   keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
                    continue

            # 检查合法值的正确性
            currentvalidvalue = values[VALIDVALUE]
            try:
                if not isinstance(ast.literal_eval(currentvalidvalue), (list, type(None))):
                    errstr = "合法值:{}格式不合规!".format(currentvalidvalue)
                    if debugflag:
                        print(errstr)
                    Sg.popup_error(errstr, modal=True, keep_on_top=True)
                    continue
            except Exception as err:
                errstr = "合法值:{}格式转换错误：{}!".format(currentvalidvalue, err)
                if debugflag:
                    print(errstr)
                Sg.popup_error(errstr, modal=True, keep_on_top=True)
                continue

            # 进一步确认参数类型、默认值、合法值的关联是否正确（isinstance 判断）
            currentdefaultvalue = values[DEFAULTVALUE]
            currenttype = values[PARAMTYPE]
            # 先把要判读的各个valid值全部转换为字符串
            checkvaluelist = [str(x) for x in ast.literal_eval(currentvalidvalue)] + [currentdefaultvalue]
            # ('参数名称', 'rows') ('参数类型', 'rows') ('合法值', '[]') ('默认值', '[]') ('命令行描述说明', '按行序号')
            # ('参数说明', '删除的行序号') ('参数详细说明', '删除的行序号, 可多行[l, m, n...]')
            if len(checkvaluelist) > 0:
                resultlist = [x[0] for x in list(map(
                    paramtypevalidcheckandtrans, checkvaluelist,
                    [currenttype for _ in range(len(checkvaluelist))]))]
                if False in resultlist:
                    errstr = "合法值或默认值{}中有类型不匹配类型:{} --> {}".format(
                        checkvaluelist, currenttype, paramtypetransmap.get(currenttype, None))
                    if debugflag:
                        print(errstr)
                    Sg.popup_error(errstr, modal=True, keep_on_top=True)
                    continue

            resultitem = [
                currentname,
                values[PARAMTYPE],
                currentvalidvalue,
                currentdefaultvalue,
                values[SENTENCE],
                values[COMMENT],
                values[LONGCOMMENT]
            ]
            print(resultitem)
            break

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return resultitem


def commandconfigitemeditgui(
        commandconfigitem: list, method: int = None,
        current_row: int = None, index_col_value: list = None) -> list:
    """
    编辑或者增加表格行，增加行需要判断是否已经存在关键词相同的记录
    :param commandconfigitem:       list, 表格行的一维列表， 位置参数, 不同表格这一参数都必须放在第一个
    :param method:                  EDIT_METHOD or ADD_METHOD
    :param current_row:             当前编辑的行号，用于判断是否重复
    :param index_col_value:         索引列的当前列值，用于判断是否重复值
    :return :                       [a, b, c,......] or None
    """
    global localoriginfunctiondict
    # "command_type": "单表处理", "english_name": "table Nan fill value", "new_table": "否",
    # "used_table_number": "单表", "function_name": "dffillna", "function_param": ["fillvalue"], "percentage_bar”："否"
    # "user_operate": "是",
    # "command_format": "{0}({1}{3}, **dict({{}}, **{4}))",
    # "record_format": "[{0}], {{'fillvalue': None}}"
    # COMMAND_TYPE_LIST,  # 命令类型
    # GENERATE_NEW_TABLE_FLAG_LIST,  # 是否新表
    # OPERATE_DFS_NUMBER_FLAG_LIST,  # 命令涉及的表数目
    # COMMAND_SEND_PROCCESSING_EVENT # 命令进度信息
    # COMMAND_USER_INPUT_PARAM       # 是否记录用户输入的param
    # SHOW_COMMAND_FLAG_LIST         # 菜单是否显示使用该命令
    NAME = '_command_name_'  # 0
    ENGLISTNAME = '_english_name_'  # 2
    COMMANDTYPE = '_command_type_'  # 1
    CREATENEWTABLE = '_create_new_table_'  # 3
    OPERATETABLENUMBER = '_operate_table_number_'  # 4
    USEDFUNCTION = '_used_function_'  # 5
    USEDARGV = '_used_argv_'  # 6
    SENDPROCESSEVENT = '_send_event_'  # 7
    USERINPUTRECORD = '_user_input_record'  # 8
    COMMANDSTRUCTURE = '_command_structure_'  # 9
    RECORDSTRUCTURE = '_record_structure_'  # 10
    COMMANDSHOW = '_command_show_flag_'  # 11
    COMMANDSTRUCTUREDEMO = '_command_structure_demo_'
    RECORDSTRUCTUREDEMO = '_record_structure_demo_'

    if method == ADD_METHOD and current_row is None:  # 空值新增模式
        currentargvs = []
        currentdefaultargvs = None
    else:
        currentargvs = list(localoriginfunctiondict[commandconfigitem[5]]['argv'])
        currentdefaultargvs = ast.literal_eval(commandconfigitem[6])
    # 表格的编辑页面
    # ('名称', '行合并')('类型', '行处理')('英文名', 'rows combine')('新表', '否')
    # ('表数', '单表')('调用函数名', 'dfrowcombine')('字典参数',"['seperate', 'nanreplace']")
    # ('命令格式串', "{0}({1}{3}, {5}, {6}, '{7}', **dict({{}}, **{4}))"),('进度条','否‘)
    # ('用户记录','是‘）('记录方式', '')('记录方式格式串', "[{0}], {{}}
    # ('菜单显示','是')
    initstructure, initrecord, initstructuredemo, initrecorddemo = commandfunctionchoose2config(
        commandconfigitem[5],  # name
        commandconfigitem[1],  # type
        commandconfigitem[3],  # newtableflag
        commandconfigitem[4],  # used table number
        currentdefaultargvs,  # currentargvs
        initialflag=False)
    if initrecorddemo is not None:
        initrecorddemo = "".join(['["{}", '.format(commandconfigitem[0]), initrecorddemo, "]"])
    commandconfiglayinfo = [
        [
            [Sg.Text("命令名称".ljust(2), font=DEF_FT_L)],
            [Sg.Input(commandconfigitem[0], k=NAME, size=(60, 1), font=DEF_FT_L)],
            [Sg.Text("英文名称".ljust(2), font=DEF_FT_L, visible=False)],
            [Sg.Input(commandconfigitem[2], k=ENGLISTNAME, size=(60, 1), font=DEF_FT_L, visible=False)],
        ],
        [Sg.HSeparator()],
        [
            [
                Sg.Col([
                    [Sg.Text("命令类型".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(COMMAND_TYPE_LIST, k=COMMANDTYPE, pad=(5, 5),
                                   default_value=commandconfigitem[1], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)],
                    [Sg.Text("是否产生新表".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(GENERATE_NEW_TABLE_FLAG_LIST, k=CREATENEWTABLE, pad=(5, 5),
                                   default_value=commandconfigitem[3], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)],
                    [Sg.Text("涉及源表数".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(OPERATE_DFS_NUMBER_FLAG_LIST, k=OPERATETABLENUMBER, pad=(5, 5),
                                   default_value=commandconfigitem[4], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)],
                    [Sg.Text("发送进度数据".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(SEND_PROCESSING_EVENT_LIST, k=SENDPROCESSEVENT, pad=(5, 5),
                                   default_value=commandconfigitem[7], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)],
                    [Sg.Text("记录用户输入".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(RECORD_USER_PARAM_LIST, k=USERINPUTRECORD, pad=(5, 5),
                                   default_value=commandconfigitem[8], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)],
                    [Sg.Text("菜单显示".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(SHOW_COMMAND_FLAG_LIST, k=COMMANDSHOW, pad=(5, 5),
                                   default_value=commandconfigitem[11], enable_events=True,
                                   font=DEF_FT_L, size=(15, 1), readonly=True)]]),
                Sg.Col([
                    [Sg.Text("调用函数".ljust(2), font=DEF_FT_L)],
                    [Sg.InputCombo(list(localoriginfunctiondict), k=USEDFUNCTION, pad=(5, 5),
                                   default_value=commandconfigitem[5],
                                   font=DEF_FT_L, size=(37, 1), readonly=True, enable_events=True)],
                    [Sg.Text("涉及字典参数".ljust(2), font=DEF_FT_L)],
                    [Sg.Listbox(currentargvs, k=USEDARGV, pad=(5, 5),
                                highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                highlight_text_color='white',
                                default_values=currentdefaultargvs,
                                # text_color=INPUT_TEXT_COLOR,
                                select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                enable_events=True,
                                font=DEF_FT_L, size=(37, 15))]])
            ]
        ],
        [Sg.HSeparator()],
        [
            [Sg.Text("命令格式串".ljust(2), font=DEF_FT_L)],
            [Sg.Input(
                initstructure,  # commandconfigitem[8],
                k=COMMANDSTRUCTURE, size=(60, 1), font=DEF_FT_L, readonly=True)],
        ],
        [
            [Sg.Text("命令记录格式串".ljust(2), font=DEF_FT_L)],
            [Sg.Input(
                initrecord,  # commandconfigitem[9],
                k=RECORDSTRUCTURE, size=(60, 1), font=DEF_FT_L, readonly=True)],
        ],
        [Sg.HSeparator()],
        [
            [Sg.Text("调用函数演示".ljust(2), font=DEF_FT_L, visible=True)],
            [Sg.Input(
                initstructuredemo,
                k=COMMANDSTRUCTUREDEMO, size=(60, 1), font=DEF_FT_L, readonly=True, visible=True)],
        ],
        [
            [Sg.Text("命令记录演示".ljust(2), font=DEF_FT_L, visible=True)],
            [Sg.Input(
                initrecorddemo,
                k=RECORDSTRUCTUREDEMO, size=(60, 1), font=DEF_FT_L, readonly=True, visible=True)],
        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('命令语句配置', commandconfiglayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    resultitem = None

    def refreshcommandstructure():
        # functionname: str: 函数名称
        # commandtype: str: 命令分类类别
        # newtableflag: str: 命令是否产生新表标记
        # usedtablenumber: str: 命令使用的表格数类型标记
        # argvparam: str: 命令涉及的argv的list
        tempresult = commandfunctionchoose2config(
            values[USEDFUNCTION],
            values[COMMANDTYPE],
            values[CREATENEWTABLE],
            values[OPERATETABLENUMBER],
            datawindow[USEDARGV].get(),
            initialflag=False
        )
        if tempresult != [None, None, None, None]:
            datawindow[COMMANDSTRUCTURE].update(value=tempresult[0])
            datawindow[RECORDSTRUCTURE].update(value=tempresult[1])
            datawindow[COMMANDSTRUCTUREDEMO].update(value=tempresult[2])
            datawindow[RECORDSTRUCTUREDEMO].update(value='["{}", {}]'.format(values[NAME], tempresult[3]))
        return

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            resultitem = None
            break

        elif event in [NAME, ENGLISTNAME, COMMANDTYPE, CREATENEWTABLE, OPERATETABLENUMBER, USEDARGV]:
            # 任何变化都重组结构串
            refreshcommandstructure()
            continue

        elif event == USEDFUNCTION:
            # 如果函数名称变化，更新USEDARGVlist
            currentargvs = list(localoriginfunctiondict[values[USEDFUNCTION]]['argv'])
            datawindow[USEDARGV].update(values=currentargvs)
            # 刷新结构串
            refreshcommandstructure()
            continue

        elif event == '_ok_':
            currentname = values[NAME]
            currentenglishname = values[ENGLISTNAME]
            if currentname.strip() == "":
                Sg.popup_error("命令名称不能为空！", modal=True, keep_on_top=True, )
                continue
            # 检查是否重名
            if currentname in index_col_value:
                cmdindex = index_col_value.index(currentname)
                # 如果是编辑方式而且是当前编辑行，说明没有重复
                if not (method == EDIT_METHOD and cmdindex == current_row):
                    # 新增内容和原有内容重复
                    Sg.popup_error("{}和第{}条记录同名！".format(currentname, cmdindex),
                                   keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
                    continue
            # ('名称', '行合并')('类型', '行处理')('英文名', 'rows combine')('新表', '否')
            # ('表数', '单表')('调用函数名', 'dfrowcombine')('字典参数',"['seperate', 'nanreplace']")
            # ('用户参数', '否')
            # ('命令格式串', "{0}({1}{3}, {5}, {6}, '{7}', **dict({{}}, **{4}))")
            # ('记录方式格式串', "[{0}], {{}}
            # ('菜单显示','是')
            resultitem = [
                currentname,
                values[COMMANDTYPE],
                currentenglishname,
                values[CREATENEWTABLE],
                values[OPERATETABLENUMBER],
                values[USEDFUNCTION],
                str(values[USEDARGV]),
                values[SENDPROCESSEVENT],
                values[USERINPUTRECORD],
                values[COMMANDSTRUCTURE],
                values[RECORDSTRUCTURE],
                values[COMMANDSHOW]
            ]
            print(resultitem)
            break

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return resultitem


def editsystemconfig():
    """
    编辑系统的配置文件（底层函数、命令配置信息）
    :return:
    """
    global usecolumnnameforprocess, originfunctiondict, commanddict
    global commandcomment, commandalias, showversioninfo, ramfilesuffix

    print("edit system configuration:\nusecolumnname: {}\nshowversioninfo: {}\n" +
          "ramfilesuffix: {}\nfuntion:\n{}\ncommand:\n{}".format(
              usecolumnnameforprocess, showversioninfo, ramfilesuffix, originfunctiondict, commanddict))

    # 1、基本配置信息
    layoutbasicconfig = [
        Sg.Frame("系统基本配置",
                 [[
                     Sg.Checkbox("直接使用列名", default=usecolumnnameforprocess, k=USE_COLUMNNAME_IN_FUNCTION, 
                                 size=(12, 1), enable_events=True, font=DEF_FT_L),
                     Sg.Checkbox("显示版本信息", default=showversioninfo, k=SHOW_VERSION_INFO,
                                 size=(12, 1), enable_events=True, font=DEF_FT_L),
                     # 该部分暂时不使用配置文件，直接定义全局变量， 保留
                     Sg.Text("内存文件后缀", visible=False),
                     Sg.Input(ramfilesuffix, k=RAM_FILE_DIRECTORY, font=DEF_FT_L, visible=False,
                              enable_events=True, size=(16, 1))
                 ]], expand_x=True)
    ]

    # 2、函数名、字典参数、位置参数配置表格
    # 函数名称的管理使用右键菜单方式
    functionnameeditmenuevent = [
        FUNCTION_NAME_ADD,
        # FUNCTION_NAME_EDIT,
        FUNCTION_NAME_DELETE,
        FUNCTION_NAME_MOVE]
    functionnameeditmenu = ["", functionnameeditmenuevent]
    currentfuntionnamelist = list(originfunctiondict)
    argcolumndict = {
        "参数名称": "name",
        "参数类型": FUNCTION_ARG_TYPE,
        "合法值": FUCNTION_ARG_VALIDVALUE,
        "默认值": FUNCTION_ARG_DEFAULTVALUE,
        "命令行描述说明": FUNCTION_ARG_SENTENCE,
        "参数说明": FUNCTION_ARG_COMMENT,
        "参数详细说明": FUNCTION_ARG_LONG_COMMENT,
    }
    argcolunmvisiblemap = [True, True, True, True, True, True, True]
    argcolumnwidth = [16, 10, 16, 10, 15, 15, 36]
    argcolvalescale = [
        None,  # 名称
        list(paramtypetransmap),  # 类型
        None,  # 合法值
        None,  # 默认值
        None,  # 命令行描述语句
        None,  # 参数说明语句
        None  # 参数详细说明
    ]
    commandcolumndict = {
        "名称": "name",
        "类型": COMMAND_TYPE,
        "英文名": COMMAND_ENGLISH_NAME,
        "新表": COMMAND_NEW_TABLE_FLAG,
        "表数": COMMAND_MULTI_DF_FLAG,
        "调用函数名": COMMAND_FUNCTION_NAME,
        "字典参数": COMMAND_FUNCTION_PARAM,
        "进度条": COMMAND_SEND_PROCCESSING_EVENT,
        "用户参数": COMMAND_USER_INPUT_PARAM,  # 记录用户输入参数值
        "命令格式串": COMMAND_FORMAT,
        "记录方式格式串": COMMAND_USED_INPUT_FORMAT,
        "显示": COMMAND_SHOW_FLAG
    }

    commandcolunmvisiblemap = [True, True, False, True, True, True, True, True, True, True, True, True]
    commandcolumnwidth = [13, 8, 0, 5, 5, 16, 13, 6, 8, 36, 36, 5]
    commandcolvaluesecale = [
        [],  # 命令名称
        COMMAND_TYPE_LIST,  # 命令类型
        [],  # 英文名称
        GENERATE_NEW_TABLE_FLAG_LIST,  # 是否新表
        OPERATE_DFS_NUMBER_FLAG_LIST,  # 命令涉及的表数目
        list(originfunctiondict),  # 调用函数名
        [],  # 命令涉及的函数argv清单
        SEND_PROCESSING_EVENT_LIST,  # 是否发送进度条信息
        RECORD_USER_PARAM_LIST,  # 是否记录用户输入参数值
        [],  # 命令格式串
        [],  # 操作记录格式串
        SHOW_COMMAND_FLAG_LIST  # 是否菜单显示
    ]
    argtablesize = (980, 156)
    commandtablesize = (1248, 446)
    configwindowsize = (1280, 946)

    layoutargctable = SpecialTable(
        tablekey=FUNCTION_ARGC_CONFIG_TABLE,
        v_slider_resolution=0.1,
        h_slider_resolution=0.1,
        slider_every_row_column=True,
        use_inner_right_click_menu=True,
        display_row_numbers=True,
        # right_click_menu=None,
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        text_color=TEXT_COLOR,
        text_background_color=TEXT_BACKGROUND_COLOR,
        input_text_color=INPUT_TEXT_COLOR,
        input_text_background_color=INPUT_TEXT_BACKGROUND_COLOR,
        cell_editable=CELL_EDITABLE,
        filter_visible=False,
        edit_button_visible=False,
        move_row_button_visible=False,
        v_slider_show=True,
        h_slider_show=False,
        dfshowdata=pd.DataFrame([], columns=list(argcolumndict.values())),
        tabledatadictlist=None,
        headings=list(argcolumndict),
        itemeditfunc=functionparamitemeditgui,  # 编辑记录行时的钩子函数
        itemeditfuncargsdic={},  # 编辑函数的参数列表
        indexcol=0,  # 记录不可以重复，用name做索引列
        font=('黑体', 10),
        pad=(0, 0),
        border_width=1,
        size=argtablesize,
        cell_justification='l',
        max_rows=6,
        max_columns=len(argcolunmvisiblemap),
        visible_column_map=argcolunmvisiblemap,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        col_widths=argcolumnwidth,
        col_value_scale=argcolvalescale,
        relief=Sg.RELIEF_SUNKEN,
        datachangeeventtrigger=True,  # 数据改变是触发事件给主窗口
        disable_slider_number_display=True,
    ).layout

    layoutargvtable = SpecialTable(
        tablekey=FUNCTION_ARGV_CONFIG_TABLE,
        v_slider_resolution=0.1,
        h_slider_resolution=0.1,
        use_inner_right_click_menu=True,
        display_row_numbers=True,
        # right_click_menu=None,
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        slider_every_row_column=True,
        text_color=TEXT_COLOR,
        text_background_color=TEXT_BACKGROUND_COLOR,
        input_text_color=INPUT_TEXT_COLOR,
        input_text_background_color=INPUT_TEXT_BACKGROUND_COLOR,
        cell_editable=CELL_EDITABLE,
        filter_visible=False,
        edit_button_visible=False,
        move_row_button_visible=False,
        v_slider_show=True,
        h_slider_show=False,
        dfshowdata=pd.DataFrame([], columns=list(argcolumndict.values())),
        tabledatadictlist=None,
        headings=list(argcolumndict),
        itemeditfunc=functionparamitemeditgui,  # 编辑记录行时的钩子函数
        itemeditfuncargsdic={},  # 编辑函数的参数列表
        indexcol=0,  # 记录不可以重复，用name做索引列
        font=('黑体', 10),
        pad=(0, 0),
        border_width=1,
        size=argtablesize,
        cell_justification='l',
        max_rows=6,
        max_columns=len(argcolunmvisiblemap),
        visible_column_map=argcolunmvisiblemap,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        col_widths=argcolumnwidth,
        col_value_scale=argcolvalescale,
        vertical_scroll_only=True,
        relief=Sg.RELIEF_SUNKEN,
        datachangeeventtrigger=True,  # 数据改变是触发事件给主窗口
        disable_slider_number_display=True,
    ).layout
    layoutfunction = [
        Sg.Frame("基础函数配置", [
            [
                Sg.Col([
                    [
                        Sg.Listbox(currentfuntionnamelist,
                                   k=FUNCTION_NAME_LIST,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   text_color=INPUT_TEXT_COLOR,
                                   select_mode=Sg.LISTBOX_SELECT_MODE_BROWSE,
                                   enable_events=True,
                                   tooltip="基础函数名称",
                                   right_click_menu=functionnameeditmenu,
                                   default_values=currentfuntionnamelist[0]
                                   if len(currentfuntionnamelist) > 0 else None,
                                   pad=DEF_PD_L, size=(30, 23))
                    ]
                ], vertical_alignment='top'),
                Sg.Col([
                    [
                        Sg.Frame("位置参数选项", layoutargctable, size=argtablesize,
                                 vertical_alignment='top', k=FUNCTION_ARGC_CONFIG_FRAME, pad=DEF_PD_L),
                    ],
                    [
                        Sg.Frame("字典参数选项", layoutargvtable, size=argtablesize,
                                 vertical_alignment='top', k=FUNCTION_ARGV_CONFIG_FRAME, pad=DEF_PD_L),
                    ],
                ]),
            ],
        ], k=FUNCTION_NAME_FRAME, vertical_alignment='top'),
    ]

    # 3、命令描述表格
    # 命令编辑表
    # 命令初始数据
    commandtabledatadictlist = [
        dict(zip([list(commandcolumndict.values())[0]] + list(value), [key] + [str(y) for y in value.values()]))
        for key, value in commanddict.items()
    ]

    layoutcommandtable = SpecialTable(
        tablekey=COMMAND_CONFIG_TABLE,
        specialdf=None if commandtabledatadictlist != []
        else SpecialDf(dfdata=pd.DataFrame([], columns=list(commandcolumndict.values())),
                       headings=list(commandcolumndict)),
        v_slider_resolution=0.1,
        h_slider_resolution=0.1,
        slider_every_row_column=True,
        use_inner_right_click_menu=True,
        right_click_menu=None,
        display_row_numbers=True,
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        text_color=TEXT_COLOR,
        text_background_color=TEXT_BACKGROUND_COLOR,
        input_text_color=INPUT_TEXT_COLOR,
        input_text_background_color=INPUT_TEXT_BACKGROUND_COLOR,
        cell_editable=CELL_EDITABLE,
        filter_visible=True,
        edit_button_visible=True,
        move_row_button_visible=True,
        v_slider_show=True,
        h_slider_show=False,
        dfshowdata=None,
        tabledatadictlist=commandtabledatadictlist,
        headings=list(commandcolumndict),
        itemeditfunc=commandconfigitemeditgui,  # 编辑记录行时的钩子函数
        itemeditfuncargsdic={},  # 编辑函数的参数列表
        indexcol=0,  # 记录不可以重复，用name做索引列
        font=('黑体', 10),
        pad=(0, 0),
        border_width=1,
        size=commandtablesize,
        cell_justification='l',
        max_rows=18,
        max_columns=len(commandcolunmvisiblemap),
        visible_column_map=commandcolunmvisiblemap,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        col_widths=commandcolumnwidth,
        col_value_scale=commandcolvaluesecale,
        datachangeeventtrigger=True,  # 数据改变是触发事件给主窗口
        relief=Sg.RELIEF_SUNKEN,
        disable_slider_number_display=True,
    ).layout

    layoutcommand = [
        Sg.Col([
            [
                Sg.Frame("命令相关配置", layoutcommandtable,
                         vertical_alignment='top', k=COMMAND_CONFIG_FRAME, pad=DEF_PD_L),
            ],
        ]),
    ]

    # 4、选择按钮
    layouttail = [[Sg.Col([[
        Sg.Frame("",
                 [[Sg.Button(' 保  存 ', k=EDIT_WIN_OK),
                   Sg.Button(' 另存为 ', k=EDIT_WIN_SAVEAS),
                   Sg.Button(' 关  闭 ', k=EDIT_WIN_CANCEL)]],
                 vertical_alignment='top', element_justification='right', expand_x=False)
    ]], justification='right')]]

    layout = [
        layoutbasicconfig,
        layoutfunction,
        layoutcommand,
        layouttail,
    ]

    configwindow = Sg.Window(
        '系统配置',
        layout,
        font=DEF_FT_L,
        icon=LOCAL_SYSTEM_ICON,
        use_ttk_buttons=True,
        size=configwindowsize,
        return_keyboard_events=False,  # 把mouse事件交给内部组建，不由主页面处理
        resizable=True,
        modal=True,
        # keep_on_top=True,
        finalize=True)

    # 初始化mousewheel updown相关的环境
    # argc事件绑定处理
    configwindow[FUNCTION_ARGC_CONFIG_TABLE].update(
        commandtype=SPECIAL_TABLE_SET_BIND,
        currentwindow=configwindow)

    # argv事件绑定处理
    configwindow[FUNCTION_ARGV_CONFIG_TABLE].update(
        commandtype=SPECIAL_TABLE_SET_BIND,
        currentwindow=configwindow)

    # command 表格鼠标事件
    configwindow[COMMAND_CONFIG_TABLE].update(
        commandtype=SPECIAL_TABLE_SET_BIND,
        currentwindow=configwindow)

    # 0、深度复制全局配置
    global localoriginfunctiondict, localcommanddict, localusecolumnnameforprocess
    global localshowversioninfo, localramfilesuffix
    localoriginfunctiondict = copy.deepcopy(originfunctiondict)
    localcommanddict = copy.deepcopy(commanddict)
    localusecolumnnameforprocess = usecolumnnameforprocess
    localshowversioninfo = showversioninfo
    localramfilesuffix = ramfilesuffix

    def configsave():
        # 保存当前的信息到配置文件
        if event == EDIT_WIN_OK:
            print("save to system configuration...")
            # 将各个字典深度复制到全局变量, 配置文件作为输出文件
            if not Sg.popup_ok_cancel("确定覆盖系统原始配置文件：{}？！".format(fileprocconfig),
                                      modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON) == "OK":
                return
            global originfunctiondict, commanddict, usecolumnnameforprocess, showversioninfo, ramfilesuffix
            # 因为是选择复制到系统文件，所以先保存local到system
            originfunctiondict = copy.deepcopy(localoriginfunctiondict)
            commanddict = copy.deepcopy(localcommanddict)
            usecolumnnameforprocess = localusecolumnnameforprocess
            showversioninfo = localshowversioninfo
            ramfilesuffix = localramfilesuffix
            filetemp = fileprocconfig
            # filetemp = "d:/temp/testconfig.json"
        else:
            # 获取输出文件名
            filetemp = Sg.popup_get_file('选择导出文件',
                                         save_as=True,
                                         file_types=(("Json配置文件", "*.json"),),
                                         initial_folder='d:/temp/',
                                         default_path='',
                                         keep_on_top=True,
                                         modal=True,
                                         no_window=True)

        if filetemp:
            # 获取funtiondict、commanddict、获取基本配置、 组成完整字典
            tempdic = {
                "usecolnameforprocess": localusecolumnnameforprocess,
                "showversioninfo": localshowversioninfo,
                "ramfilesuffix": localramfilesuffix,
                "originfunctiondict": localoriginfunctiondict,
                "commanddict": localcommanddict,
                "commandalias": commandalias,
                "commandcomment": commandcomment
            }
            try:
                with open(filetemp, 'w', encoding='utf8') as fp:
                    json.dump(tempdic, fp, ensure_ascii=False, sort_keys=False, indent=4)
                    fp.flush()
                    fp.close()
            except Exception as err:
                Sg.popup_error("保存配置文件：{} 失败：{}".format(filetemp, str(err)),
                               modal=True,
                               keep_on_top=True,
                               icon=LOCAL_SYSTEM_ICON)
                return

            Sg.popup_ok("命令文件{}保存完成！{}".format(filetemp,
                                               "重新启动程序后新配置方能生效！！！" if event == EDIT_WIN_OK else ""),
                        keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
            return

    def functionnamechoosed():
        """
        当函数名的list选择改变时处理
        :return:
        """
        # 获取当前的函数名 并 将对应的argc，argv填入对应的表格
        currentfunction = values[FUNCTION_NAME_LIST]
        if currentfunction[0] != '':
            currentfunctiondict = localoriginfunctiondict.get(currentfunction[0], None)
            if currentfunctiondict is None:
                return

            # 转换argc, argv的dictlist ，所有值先转换为str, 然后分别赋值给相应的表格
            for temparg, temptable in [("argc", FUNCTION_ARGC_CONFIG_TABLE), ("argv", FUNCTION_ARGV_CONFIG_TABLE)]:
                currentarglist = [
                    dict(zip([list(argcolumndict.values())[0]] + list(value), [key] + [str(y) for y in value.values()]))
                    for key, value in currentfunctiondict.get(temparg, None).items()
                ]

                configwindow[temptable].update(
                    commandtype=SPECIAL_TABLE_SET_WHOLEVALUE,
                    currentwindow=configwindow,
                    infodict=currentarglist,
                    headings=list(argcolumndict),
                    dfshowdata=None)

    def configuretupleprocess():
        """
        configwindow 元组事件的处理
        :return:
        """
        # TABLE 被点击后，会连续输出两个事件，一个是元组，格式如下，包含了点击的（行号，列号），行号-1表示点击的是heading
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # 第二个事件是表格本身key事件, 表格点击事件, 因为处理了第一个元组事件，第二个可以忽略
        # 对于表格相关事件，针对调试过程中的已处理命令行，先做好预处理。针对不同命令以及不同位置做相应的执行命令回滚。
        # 兼容Sg.table和Special element方式, # Sg.Table方式，event[0] == (tablekey, tablekey)
        # 处理鼠标wheel, 目前 （tablekey,x, y), "mousewheel", 不再需要兼容Sg.Table
        currenttable = event[0][0] if isinstance(event[0], tuple) else event[0]

        # 对于SpecialTable，如果datachangeeventtrigger=True, 表格数据改变时，会触发 SPECIAL_TABLE_CHANGE_EVENT_TRIGGER
        # argc 和 argv设置了该项
        if event[1] == SPECIAL_TABLE_CHANGE_EVENT_TRIGGER and \
                event[0] in [FUNCTION_ARGC_CONFIG_TABLE, FUNCTION_ARGV_CONFIG_TABLE]:
            tempfunctionlist = values[FUNCTION_NAME_LIST]
            currentfunction = None if tempfunctionlist == [] else tempfunctionlist[0]
            if currentfunction is None:
                if debugflag:
                    print("无法获取当前函数名！")
                Sg.popup_error("无法获取当前函数名!", modal=True, keep_on_top=True)
                return
            currentarg = "argc" if event[0] == FUNCTION_ARGC_CONFIG_TABLE else "argv"
            # 从当前arg table获取值并组成字典，
            resultdictlist = configwindow[currenttable].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
            print(resultdictlist)
            # 将字典list中的每项单独转换，
            # "name",FUNCTION_ARG_TYPE,FUCNTION_ARG_VALIDVALUE,FUNCTION_ARG_DEFAULTVALUE,
            # FUNCTION_ARG_SENTENCE, FUNCTION_ARG_COMMENT, FUNCTION_ARG_LONG_COMMENT
            # type 为str，不用处理，defaultvalue需要根据type单独处理，其他为list调用eval转换
            itemevaltrans = [FUCNTION_ARG_VALIDVALUE]
            tempparamdict = {}
            argitems = []
            for item in resultdictlist:
                # 第一项为参数名，后续项为参数dict
                name = item.pop(list(argcolumndict.values())[0])  # "参数名称"
                argitems.append(name)
                # 字典剩余其他项为param项, 要將返回item字典中的每項从字符串转化为实际类型
                # 转换eval相关项
                try:
                    for option in itemevaltrans:
                        item[option] = ast.literal_eval(item[option])
                except Exception as err:
                    errstr = "参数{}配置项:{}格式不合规：{}".format(name, option, err)
                    if debugflag:
                        print(errstr)
                    Sg.popup_error(errstr, modal=True, keep_on_top=True)
                    return
                # 根据type转换defaultvalue, FUNCTION_ARG_DEFAULTVALUE ,并单独检查合法性
                resultvalue = paramtypevalidcheckandtrans(item[FUNCTION_ARG_DEFAULTVALUE], item[FUNCTION_ARG_TYPE])
                if resultvalue[0] is True:
                    item[FUNCTION_ARG_DEFAULTVALUE] = resultvalue[1]
                else:
                    errstr = "参数{}默认值:{}格式不合规：{}".format(
                        name, item[FUNCTION_ARG_DEFAULTVALUE], item[FUNCTION_ARG_TYPE])
                    if debugflag:
                        print(errstr)
                    Sg.popup_error(errstr, modal=True, keep_on_top=True)
                    return

                # 赋值给functiondict的当前argparam， 必须整个"argc"或"argv"赋值，避免字典残留以前的key
                tempparamdict[name] = item

            global localoriginfunctiondict
            if currentarg == 'argc':
                localoriginfunctiondict[currentfunction]["argcitems"] = argitems
            localoriginfunctiondict[currentfunction][currentarg] = tempparamdict
            print(localoriginfunctiondict[currentfunction])
            return

        elif event[1] == SPECIAL_TABLE_CHANGE_EVENT_TRIGGER and \
                event[0] == COMMAND_CONFIG_TABLE:
            print("command table changed")
            # 处理command相关字典
            # 从command table获取值并组成字典，
            resultdictlist = configwindow[COMMAND_CONFIG_TABLE].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
            print(resultdictlist)
            # 将字典整体复制到localcommand
            # 将字典list中的每项单独转换，
            # 只有function_param 需要转化eval
            # type 为str，不用处理，defaultvalue需要根据type单独处理，其他为list调用eval转换
            itemevaltrans = [COMMAND_FUNCTION_PARAM]
            tempparamdict = {}
            for item in resultdictlist:
                # 第一项为参数名，后续项为参数dict
                name = item.pop(list(commandcolumndict.values())[0])  # "参数名称"
                # 字典剩余其他项为配置项，COMMAND_FUNCTION_PARAM从字符串转化为实际类型
                # 转换eval相关项
                try:
                    for option in itemevaltrans:
                        item[option] = ast.literal_eval(item[option])
                except Exception as err:
                    if debugflag:
                        print("命令：{}配置项:{}格式不合规：{}".format(name, option, err))
                    Sg.popup_error("命令：{}配置项:{}格式不合规：{}".format(name, option, err),
                                   modal=True, keep_on_top=True)
                    return
                # 赋值给commanddict的， 必须赋值，避免字典残留以前的key
                tempparamdict[name] = item
            # 整体赋值
            global localcommanddict
            localcommanddict = tempparamdict
            print(localcommanddict)
            return

        configwindow[currenttable].update(
            commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
            currentevent=event, currentwindow=configwindow, currentvalues=values)

    def getnewfunctionname(currentfunction: str, comparefunctionlist: list) -> str:
        """
        根据输入和函数名和已有函数清单，输出不重复值的新函数名
        :param currentfunction:         现有函数名
        :param comparefunctionlist:     用于判断是否重名的list
        :return:                        str | None
        """
        # 弹出窗口， cancel 返回None
        # OK 获取newname并返回
        namelayout = [
            [
                Sg.Text("输入函数名"),
                Sg.Input(currentfunction, k="_function_name_", pad=(5, 5),
                         font=PARAM_FT, size=(50, 1), expand_x=True, border_width=2)
            ],
            [
                Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
            ]
        ]
        namewindow = Sg.Window('函数名编辑', namelayout, icon=LOCAL_SYSTEM_ICON,
                               font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

        while True:
            event, values = namewindow.read()
            # --- Process buttons --- #
            tempfunctionname = None
            if event in (Sg.WIN_CLOSED, '_close_'):
                break
            # 确定新名字
            elif event == '_ok_':
                # 返回菜单项值
                tempfunctionname = values["_function_name_"]
                if tempfunctionname.strip() == '':
                    tempfunctionname = None
                    Sg.popup_error("函数名不能为空！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                if tempfunctionname in comparefunctionlist:
                    tempfunctionname = None
                    Sg.popup_error("新函数名与已有函数重名！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                break

        # 点击close或者关闭，不修改任何值，返回 None
        namewindow.close()
        return tempfunctionname

    def getmovetolocation(totallist: list):
        """
        从名字列表中获取要移动到个函数名后面
        :param totallist:
        :return:
        """
        # 弹出窗口， cancel 返回None
        # OK 获取newname并返回
        namelayout = [
            [
                Sg.Text("选择目标位置函数名"),
                Sg.Combo(totallist, k="_function_name_", font=PARAM_FT, size=(50, 1), expand_x=True)
            ],
            [
                Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
            ]
        ]
        namewindow = Sg.Window('函数移动位置选择', namelayout, icon=LOCAL_SYSTEM_ICON,
                               font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

        while True:
            event, values = namewindow.read()
            # --- Process buttons --- #
            tempfunctionname = None
            if event in (Sg.WIN_CLOSED, '_close_'):
                break
            # 确定新名字
            elif event == '_ok_':
                # 返回菜单项值
                tempfunctionname = values["_function_name_"]
                if tempfunctionname.strip() == '':
                    Sg.popup_error("函数名不能为空！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                if tempfunctionname not in totallist:
                    Sg.popup_error("所选择目标函数名{}不正取".format(tempfunctionname),
                                   modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                break

        # 点击close或者关闭，不修改任何值，返回 None
        namewindow.close()
        return tempfunctionname

    def queryfunctioninsystem(functionname: str) -> list:
        """
        根据函数名查询系统，获取函数的参数信息并形成配置字典
        :param functionname:    str: 函数名
        :return:                list: [True, dict 函数参数配置自字典]|[False, {}]
        """
        # 先在系统中招该函数，如果找到，由用户确认使用系统参数生成还是使用手工产生的值
        try:
            # 自动获取函数参数
            print(globals()[functionname])
            autogetargs = inspect.signature(globals()[functionname])
            paramdict = dict(autogetargs.parameters)
            # 根据自动获取的参数配置函数的参数说明
            # {"argcitems": [], "argc": {}, "argv": {}}
            # 首先判断函数的前两个参数是否specialdflist， tableindex，如果不是，提示错误并且返回
            paramlist = list(autogetargs.parameters.values())
            if len(paramlist) < len(VALID_DF_FUNCTION_PARAMS):
                return [False, "函数{}的参数个数{}不符合要求格式：{}".format(
                    functionname, len(paramlist), VALID_DF_FUNCTION_PARAMS)]
            if [paramlist[x].name for x in range(len(VALID_DF_FUNCTION_PARAMS))] != VALID_DF_FUNCTION_PARAMS:
                return [False, "函数{}的前{}个参数{}}不符合要求格式：{}".format(
                    functionname, len(VALID_DF_FUNCTION_PARAMS),
                    [paramlist[x].name for x in range(len(VALID_DF_FUNCTION_PARAMS))], VALID_DF_FUNCTION_PARAMS)]
            # 丢弃specialdflist、dfcurrentlist、tableindex后，逐项处理
            for item in VALID_DF_FUNCTION_PARAMS:
                paramdict.pop(item)
            argvstartflag = False
            argcitems, argcdict, argvdict = [], {}, {}
            for value in paramdict.values():
                print("value.name:{},  value.kind:{},  value.default:{}, value.annotation: {}".format(
                    value.name, value.kind, value.default, value.annotation))
                # 根据是否有default值判断是argc还是argv,
                # 当前是非argv状态， 并且 类型是POSITION_ONLY,
                if argvstartflag is False \
                        and (value.kind in [value.POSITIONAL_ONLY, value.VAR_POSITIONAL]
                             or (value.kind == value.POSITIONAL_OR_KEYWORD and value.default == value.empty)):
                    argcitems.append(value.name)
                    argcdict[value.name] = {
                        "type": "str",
                        "validvalue": [],
                        "defaultvalue": [],
                        "sentence": "",
                        "comment": "",
                        "long_comment": ""
                    }
                else:  # 判读为argv
                    argvstartflag = True

                if argvstartflag is True \
                        and (value.kind in [value.KEYWORD_ONLY, value.VAR_KEYWORD]
                             or (value.kind == value.POSITIONAL_OR_KEYWORD and value.default != value.empty)):
                    argvdict[value.name] = {
                        "type": "str",
                        "validvalue": [],
                        "defaultvalue": value.default,
                        "sentence": "",
                        "comment": "",
                        "long_comment": ""
                    }
            return [True, {"argcitems": argcitems, "argc": argcdict, "argv": argvdict}]
        except Exception as err:
            return [False, "获取函数{}参数列表失败：{}".format(functionname, err)]

    def editfunctionname():
        """
        functionname table 邮件编辑菜单事件的处理
        :return:
        """
        global localoriginfunctiondict
        # 获取list中选中的函数名
        tempfunctionlist = values[FUNCTION_NAME_LIST]
        currentfunction = None if tempfunctionlist == [] else tempfunctionlist[0]
        # 由于暂存原有的函数名list以便比较差异
        comparefunctionlist = list(localoriginfunctiondict)

        if event == FUNCTION_NAME_EDIT:  # TODO 目前不提供该功能，后续再考虑是否提供
            # 先将当前函数名从currentfunctionlist中清理掉，以方便后续比对是否重名
            if currentfunction in comparefunctionlist:
                comparefunctionlist.remove(currentfunction)
            else:  # 当前函数名不合法，提示后返回
                errstr = "要修改的函数名：{} 不存在".format(currentfunction)
                if debugflag:
                    print(errstr)
                Sg.popup_error(errstr, modal=True, keep_on_top=True)
                return
            # 弹出窗口让用户填写新的函数名
            newname = getnewfunctionname(currentfunction, comparefunctionlist)
            if newname is None or newname == currentfunction:  # 无需修改
                return
            try:
                # 自动获取函数参数以确认函数是否在系统中存在
                autogetargs = inspect.signature(ast.literal_eval(newname))
                for key, value in autogetargs.parameters.items():
                    print("key:{}, value:{}".format(key, value))
            except Exception as err:
                errstr = "函数{}在系统中不存在：{}, 是否继续修改？".format(newname, err)
                # 弹出函数名不存在但是修改确认消息
                if not Sg.popup_ok_cancel(errstr, modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON) == "OK":
                    return
            # TODO 10 ，是只修改函数名还是对比修改的函数名和当前列表原函数配置的对应关系让用户确定？
            #  将localoriginfunctiondict中的该项函数key修改为新值  字典中的key而不改变顺序
            localoriginfunctiondict = dict(
                [(newname if key == currentfunction else key, value)
                 for key, value in localoriginfunctiondict.items()])
            # 刷新functionnamelist
            configwindow[FUNCTION_NAME_LIST].update(values=list(localoriginfunctiondict))

        if event == FUNCTION_NAME_ADD:
            # 弹出窗口让用户填写新的函数名
            newname = getnewfunctionname(currentfunction if currentfunction is not None else "", comparefunctionlist)
            if newname is None:  # 无需修改
                return
            # 在系统中差该函数，如果找到，则添加，否则退出
            result = queryfunctioninsystem(newname)
            if result[0] is False:
                if debugflag:
                    print(result[1])
                Sg.popup_error(result[1], modal=True, keep_on_top=True)
                return
            else:
                localoriginfunctiondict[newname] = result[1]

            # 刷新functionnamelist
            configwindow[FUNCTION_NAME_LIST].update(values=list(localoriginfunctiondict))
            Sg.popup_quick_message("添加函数{}完成，请进一步完善各个参数设置！".format(newname),
                                   modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
            return

        if event == FUNCTION_NAME_DELETE:
            # 将key从localfunctionnamedict中删除，
            if currentfunction not in comparefunctionlist:
                # 当前函数名不合法，提示后返回
                errstr = "要删除的函数名：{} 不存在".format(currentfunction)
                if debugflag:
                    print(errstr)
                Sg.popup_error(errstr, modal=True, keep_on_top=True)
                return
            else:
                # 弹出删除确认消息，如果提示返回为OK，
                # 1、反向找到包含该函数的所有命令
                commandlistfordel = [x for x in list(localcommanddict)
                                     if localcommanddict[x][COMMAND_FUNCTION_NAME] == currentfunction]
                # 2、提示是否删除命令和函数
                if not Sg.popup_ok_cancel(
                        "删除函数名：{}的同时需要删除使用该函数的命令{}，确认删除？？？！！！".format(
                            currentfunction, commandlistfordel),
                        modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON) == "OK":
                    return
                # 3、如果确认，首先删除对应的命令，删除成功再删除该函数
                # 3.1、根据列表删除命令
                for tempcommand in commandlistfordel:
                    localcommanddict.pop(tempcommand)
                # 需要用localcommanddict刷新命令显示表格
                configwindow[COMMAND_CONFIG_TABLE].update(
                    commandtype=SPECIAL_TABLE_SET_WHOLEVALUE,
                    currentwindow=configwindow,
                    infodict=[dict(zip([list(commandcolumndict.values())[0]] + list(value),
                                       [key] + [str(y) for y in value.values()]))
                              for key, value in localcommanddict.items()],
                    headings=list(commandcolumndict),
                    dfshowdata=None)

                # 3.2、再删除函数
                localoriginfunctiondict.pop(currentfunction)
                # 刷新functionnamelist
                configwindow[FUNCTION_NAME_LIST].update(values=list(localoriginfunctiondict))
                Sg.popup_quick_message("函数{}删除完成，已同时删除关联命令{}！".format(currentfunction, commandlistfordel),
                                       modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
            return

        if event == FUNCTION_NAME_MOVE:
            if currentfunction not in comparefunctionlist:
                errstr = "要移动的函数名：{} 不存在".format(currentfunction)
                if debugflag:
                    print(errstr)
                Sg.popup_error(errstr, modal=True, keep_on_top=True)
                return

            # 获取需要移动到哪个函数名之后
            afterwho = getmovetolocation(comparefunctionlist)
            # 返回空值或者位置不变
            if afterwho is None or afterwho == currentfunction:
                return
            else:
                myvalue = localoriginfunctiondict[currentfunction]
                #  将localoriginfunctiondict中的该项函数key修改为新值  字典中的key而不改变顺序
                templist = []
                # 逐项处理
                for key, value in localoriginfunctiondict.items():
                    if key == afterwho:  # 发现前缀函数名，加入前缀函数和本函数
                        templist.append((key, value))
                        templist.append((currentfunction, myvalue))
                    elif key == currentfunction:  # 发现本函数跳过
                        continue
                    else:
                        templist.append((key, value))
                localoriginfunctiondict = dict(templist)
                # 刷新functionnamelist
                configwindow[FUNCTION_NAME_LIST].update(values=list(localoriginfunctiondict))
                Sg.popup_quick_message("移动函数{}完成！".format(currentfunction),
                                       modal=True, keep_on_top=True, text_color='white', background_color='dark blue')

    # tirgger FUNCTION_NAME_LIST, 触发初始化相关表格显示
    configwindow.write_event_value(FUNCTION_NAME_LIST,
                                   [currentfuntionnamelist[0]] if len(currentfuntionnamelist) > 0 else None)
    # 选择的参数
    while True:
        event, values = configwindow.read()
        if debugflag:
            print("configwindow event:{}".format(event))
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, EDIT_WIN_CANCEL):
            break

        elif event in [EDIT_WIN_OK, EDIT_WIN_SAVEAS]:
            configsave()
            continue

        elif event == FUNCTION_NAME_LIST:  # 选中某个函数，在argc、argv的table中显示argc、argv
            functionnamechoosed()
            continue

        elif event == SHOW_VERSION_INFO:
            localshowversioninfo = values[SHOW_VERSION_INFO]
            continue
            
        elif event == USE_COLUMNNAME_IN_FUNCTION:
            localusecolumnnameforprocess = values[USE_COLUMNNAME_IN_FUNCTION]
            continue

        elif event == RAM_FILE_DIRECTORY:
            localramfilesuffix = values[RAM_FILE_DIRECTORY]
            
        elif isinstance(event, tuple):
            configuretupleprocess()
            continue

        elif event in functionnameeditmenuevent:
            editfunctionname()
            continue

        else:
            # 判断是否为innerrightmenu事件，如果是就触发该事件, 当窗口中有表格设置了 use_inner_right_click_menu，
            # 需要调用isinnerrightclickmenu 进行回送事件处理
            tempresult = isinnerrightclickmenu(configwindow, event)
            if tempresult is False:
                print("configwindow unknow event:{}".format(event))
            continue

    configwindow.close()
    return


# 导入数据文件窗口key
LOADDATA_NEW_DF_T = '_loaddata_new_df_text_'
LOADDATA_OLD_DF_T = '_loaddata_old_df_text_'
LOADDATA_NEW_DF = '_loaddata_new_df_'
LOADDATA_OLD_DF = '_loaddata_old_df_'
RADIO_NEW_DF = '_R_new_df_'
RADIO_OLD_DF = '_R_old_df_'

# 导出数据窗口key
SAVEDATA_DF = '_savedata_df_'
SAVEDATA_USE_STYLE = '_savedata_use_style_'
SAVEDATA_WITH_INDEX = '_savedata_with_index_'
SAVEDATA_FILENAME = '_savedata_filename_'
SAVEDATA_CHOOSE_OUTPUTFILE = '_savedata_choose_output_file_'
SAVEDATA_USE_MODELFILE = '_savedata_use_modelfile_'
SAVEDATA_MODELFILENAME = '_savedata_modelfilename_'
SAVEDATA_CHOOSE_MODELFILE = '_savedata_choose_modelfile_'
SAVEDATA_STANDARD_MODE_RADIO = '_savedata_standard_mode_radio_'
SAVEDATA_BLOCKCOPY_MODE_RADIO = '_savedata_blockcopy_mode_radio_'
SAVEDATA_STANDARD_MODE_FRAME = '_savedata_standard_mode_frame_'
SAVEDATA_BLOCKCOPY_MODE_FRAME = '_savedata_blockcopy_mode_frame_'
SAVEDATA_HEADLINE = '_savedata_headline_'
SAVEDATA_TAILLINE = '_savedata_tailline_'
SAVE_SUMROW = '_save_sumrow_'
SUMROW_LINE = '_sumrow_line_'
SAVEDATA_SHEETNUMBER = '_savedata_sheetnumber_'
SAVEDATA_MODEL_FRAME = '_savedata_model_frame_'
SAVEDATA_SOURCE_STARTROW = '_savedata_source_startrow_'
SAVEDATA_SOURCE_ENDROW = '_savedata_source_endrow_'
SAVEDATA_SOURCE_STARTCOL = '_savedata_source_startcol_'
SAVEDATA_SOURCE_ENDCOL = '_savedata_source_endcol_'
SAVEDATA_TARGET_STARTROW = '_savedata_target_startrow_'
SAVEDATA_TARGET_STARTCOL = '_savedata_target_startol_'

NA_FILTER_CHECK = "_na_filter_check_"
SHEET_NUMBER = "_sheetnumber_"
COL_FORCE_STRING = '_col_force_string_'
HEADNAME_LINE = "_headnameline_"
TAIL_LINES = "_taillines_"
HEAD_LINES = "_headlines_"
CHOOSE_FILE = '_choose_file_'
FILE_NAME = "_filename_"

DATABASE_TYPE = "_database_type_"
IP_ADDRESS = "_ipaddress_"
IP_PORT = "_ipport_"
DATABASE_NAME = "_database_"
USER_NAME = "_username_"
PASSWORD = "_password_"
SQL_STRING = "_sqlstr_"
REPALCE_METHOD = "_replcae_method_"


def loaddatafromfile(filepath: str, targetdfid: int, headline: int, tailline: int, sheetnumber: int,
                     headnameline: int, na_filter: bool = False, colforcestring=None) -> bool:
    """
    从文件导入数据到df
    :param filepath:                                str： 文件全路径名
    :param targetdfid:                              df：   导出到的df号
    :param headline:                                int: 导出表首丢弃行数
    :param tailline:                                int： 导出表尾丢弃行数
    :param sheetnumber:                                int： 导出的子表号
    :param headnameline:                                int: 丢弃表首后，列名所在行，>=0有效
    :param na_filter:                               bool: 是否检测各种空值并且替换为NaN
    :param colforcestring:                          list 强制作为字符串读取的列名的列表
    :return:                                        bool：True 导入成功 False 导入失败
    """
    if colforcestring is None:
        colforcestring = []
    global myinputfiles, specialdflist, specialdflistcopy, mainwindow, guiflag
    currenttablenubmer = len(specialdflist)
    # 如果指定表号比现有表数大，只在现有表列表的末尾添加
    if targetdfid > currenttablenubmer:
        targetdfid = currenttablenubmer
    result = dfloaddatafromfile(specialdflist, [0], [targetdfid], filepath,  # specialdflist[0], [0], 只是为了兼容调用接口
                                headline=headline, colforcestring=colforcestring,
                                tailline=tailline, sheetnumber=sheetnumber,
                                headnameline=headnameline, na_filter=na_filter)
    if result[0] is False:
        Sg.popup_error("导入文件{}到表[{}]错误: {}".format(filepath, targetdfid, result[1]), modal=True, keep_on_top=True)
        return False
    # 判断是新增还是覆盖原有df
    if targetdfid == currenttablenubmer:
        # 新增df
        specialdflistcopy.append(copy.deepcopy(specialdflist[targetdfid]))
    else:
        # 覆盖旧表
        specialdflistcopy[targetdfid] = copy.deepcopy(specialdflist[targetdfid])
    # 刷新tabdata
    if guiflag:
        # 更新表格数据
        mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH, currentwindow=mainwindow)
        mainwindow.refresh()
        Sg.popup_quick_message("导入文件{}到表{}完成".format(filepath, targetdfid),
                               modal=True, keep_on_top=True, text_color='white', background_color='dark blue')

    return True


def loaddatafromfilebutton():
    """
    读取数据文件到df
    :return:
    """
    global myinputfiles, specialdflist, specialdflistcopy, mainwindow
    """
    弹出输入界面，用户输入数据文件名及表头表尾行后，跳过相关行，读取数据然后刷新展示
    """
    # 表格的编辑页面
    currentdfnumber = len(specialdflist)
    loaddatalayinfo = [
        [
            Sg.Text("数据文件".ljust(2), font=DEF_FT_L),
            Sg.Input("", k=FILE_NAME, size=(50, 1), font=DEF_FT_L),
            Sg.Button('选择文件', k=CHOOSE_FILE, font=DEF_FT_L)
        ],
        [
            Sg.Text("文件子表序号".ljust(10), size=(12, 1), font=DEF_FT_L),
            Sg.Input("0", k=SHEET_NUMBER, size=(3, 1), font=DEF_FT_L),
            Sg.Text("表首跳过行数".ljust(6), size=(12, 1), font=DEF_FT_L),
            Sg.Input("0", k=HEAD_LINES, size=(2, 1), font=DEF_FT_L),
            Sg.Text("表尾丢弃行数".ljust(6), size=(12, 1), font=DEF_FT_L),
            Sg.Input("0", k=TAIL_LINES, size=(2, 1), font=DEF_FT_L),
            Sg.Text("列名所在行".ljust(5), size=(10, 1), font=DEF_FT_L),
            Sg.Input("0", k=HEADNAME_LINE, size=(2, 1), font=DEF_FT_L),
        ],
        [
            Sg.Text("列强制字符串（列名逗号隔开）".ljust(16), size=(25, 1), font=DEF_FT_L),
            Sg.Input("", k=COL_FORCE_STRING, size=(42, 1), font=DEF_FT_L),
        ],
        [
            Sg.Checkbox("空值检测为NaN", default=False, k=NA_FILTER_CHECK,
                        size=(12, 1), enable_events=True, font=DEF_FT_L)
        ],
        [
            # 使用已有表空间并覆盖还是使用新表
            [Sg.HSeparator()],
            [Sg.Radio('加载到新表', "_load_data_radio_", default=True, size=(10, 1),
                      k=RADIO_NEW_DF, enable_events=True),
             Sg.Radio('覆盖已有表', "_load_data_radio_", default=False, size=(10, 1),
                      k=RADIO_OLD_DF, enable_events=True)],
            Sg.Text("当前新表表号".ljust(6), size=(12, 1), font=DEF_FT_L, visible=True,
                    k=LOADDATA_NEW_DF_T),
            Sg.Input(currentdfnumber, k=LOADDATA_NEW_DF, size=(4, 1), font=DEF_FT_L, disabled=True, visible=True),
            Sg.Text("已有表号".ljust(6), size=(12, 1), font=DEF_FT_L, visible=False,
                    k=LOADDATA_OLD_DF_T),
            Sg.InputCombo([x for x in range(currentdfnumber)], k=LOADDATA_OLD_DF, pad=(5, 5),
                          font=DEF_FT_L, size=(12, 1), readonly=True, visible=False)

        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('导入数据文件', loaddatalayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        elif event == RADIO_NEW_DF:
            # 显示新表的内容
            datawindow[LOADDATA_NEW_DF_T].update(visible=True)
            datawindow[LOADDATA_NEW_DF].update(visible=True)
            datawindow[LOADDATA_OLD_DF_T].update(visible=False)
            datawindow[LOADDATA_OLD_DF].update(visible=False)
            continue

        elif event == RADIO_OLD_DF:
            # 显示旧表的内容
            datawindow[LOADDATA_NEW_DF_T].update(visible=False)
            datawindow[LOADDATA_NEW_DF].update(visible=False)
            datawindow[LOADDATA_OLD_DF_T].update(visible=True)
            datawindow[LOADDATA_OLD_DF].update(visible=True)
            continue

        # 选择文件
        elif event == CHOOSE_FILE:
            filetemp = Sg.popup_get_file('选择文件',
                                         icon=LOCAL_SYSTEM_ICON,
                                         file_types=(("表格文件", "*.xlsx"),
                                                     ("csv文件", "*.csv"),
                                                     ("txt文本", "*.txt"),
                                                     ("jsonl文件", "*.jsonl")),
                                         no_window=True)

            if filetemp:
                datawindow[FILE_NAME](filetemp)

        # 确定分析文件
        elif event == '_ok_':
            # 返回菜单项值
            tempfilename = values[FILE_NAME]
            try:
                targetdfid = int(datawindow[LOADDATA_NEW_DF].get()) \
                    if datawindow[RADIO_NEW_DF].get() else int(datawindow[LOADDATA_OLD_DF].get())
            except Exception as err:
                Sg.popup_error("目标表号不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue
            if tempfilename == '':
                Sg.popup_error("文件名不能为空！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue
            # 判断文件是否真实存在或者是否为内存虚拟文件
            if not (Path(tempfilename).is_file() or is_mem_virtual_file_exist(tempfilename)):
                Sg.popup_error("文件{}不存在！".format(tempfilename), modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue
            try:
                headline = int(values[HEAD_LINES])
                tailline = int(values[TAIL_LINES])
                headnameline = int(values[HEADNAME_LINE])
                sheetnumber = int(values[SHEET_NUMBER])
                na_filter = True if values[NA_FILTER_CHECK] else False
                colforcestring = [x.strip() for x in values[COL_FORCE_STRING].strip().split(',')]
            except Exception as err:
                Sg.popup_error("子表号、表首行数或者表尾行数不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            if loaddatafromfile(tempfilename, targetdfid, headline, tailline, sheetnumber,
                                headnameline=headnameline, na_filter=na_filter, colforcestring=colforcestring):
                break
            else:
                continue

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return


def loaddatafromdatabasebysql():
    """
    sql读取数据到df
    :return:
    """
    global specialdflist, specialdflistcopy, mainwindow, manualbuttonoperatedict
    """
    弹出输入界面，用户输入数据文件名及表头表尾行后，跳过相关行，读取数据然后刷新展示
    """
    # 表格的编辑页面
    currentdfnumber = len(specialdflist)
    # 获取界面默认值
    defaultrecordlist = [DATABASE_TYPE, IP_ADDRESS, IP_PORT, DATABASE_NAME, USER_NAME, PASSWORD, SQL_STRING]
    if manualbuttonoperatedict.get(LOAD_SQL, None) is None:
        manualbuttonoperatedict[LOAD_SQL] = {}
    databasetype, ipaddress, ipport, databasename, username, password, sqlstring = map(
        manualbuttonoperatedict[LOAD_SQL].get, defaultrecordlist, ["" for _ in range(len(defaultrecordlist))])
    password = dftrans_simple_decrypt(password)

    Sg.InputCombo([x for x in range(currentdfnumber)], k=LOADDATA_OLD_DF, pad=(5, 5),
                  font=DEF_FT_L, size=(12, 1), readonly=True, visible=False)
    loaddatalayinfo = [
        [
            [Sg.Text("数据库类型".ljust(10), size=(10, 1), font=DEF_FT_L),
             Sg.InputCombo([DATABASE_TYPE_SQLITE, DATABASE_TYPE_MYSQL], default_value=DATABASE_TYPE_SQLITE,
                           k=DATABASE_TYPE, size=(18, 1), font=DEF_FT_L, readonly=True)],
            [Sg.Text("ip地址".ljust(10), size=(10, 1), font=DEF_FT_L),
             Sg.Input(ipaddress, k=IP_ADDRESS, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("端口号".ljust(6), size=(10, 1), font=DEF_FT_L),
             Sg.Input(ipport, k=IP_PORT, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("数据库名".ljust(6), size=(10, 1), font=DEF_FT_L),
             Sg.Input(databasename, k=DATABASE_NAME, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("用户名".ljust(5), size=(10, 1), font=DEF_FT_L),
             Sg.Input(username, k=USER_NAME, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("密码".ljust(5), size=(10, 1), font=DEF_FT_L),
             Sg.Input(password, k=PASSWORD, size=(20, 1), font=DEF_FT_L, password_char='*')],
            [Sg.Text("sql语句".ljust(5), size=(10, 1), font=DEF_FT_L),
             Sg.ML(sqlstring, k=SQL_STRING, size=(50, 6), font=DEF_FT_L, autoscroll=True, horizontal_scroll=True)]
        ],
        [
            # 使用已有表空间并覆盖还是使用新表
            [Sg.HSeparator()],
            [Sg.Radio('加载到新表', "_load_data_radio_", default=True, size=(10, 1),
                      k=RADIO_NEW_DF, enable_events=True),
             Sg.Radio('覆盖已有表', "_load_data_radio_", default=False, size=(10, 1),
                      k=RADIO_OLD_DF, enable_events=True)],
            Sg.Text("当前新表表号".ljust(6), size=(12, 1), font=DEF_FT_L, visible=True,
                    k=LOADDATA_NEW_DF_T),
            Sg.Input(currentdfnumber, k=LOADDATA_NEW_DF, size=(4, 1), font=DEF_FT_L, disabled=True, visible=True),
            Sg.Text("已有表号".ljust(6), size=(12, 1), font=DEF_FT_L, visible=False,
                    k=LOADDATA_OLD_DF_T),
            Sg.InputCombo([x for x in range(currentdfnumber)], k=LOADDATA_OLD_DF, pad=(5, 5),
                          font=DEF_FT_L, size=(12, 1), readonly=True, visible=False)

        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('sql导入数据库数据', loaddatalayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        elif event == RADIO_NEW_DF:
            # 显示新表的内容
            datawindow[LOADDATA_NEW_DF_T].update(visible=True)
            datawindow[LOADDATA_NEW_DF].update(visible=True)
            datawindow[LOADDATA_OLD_DF_T].update(visible=False)
            datawindow[LOADDATA_OLD_DF].update(visible=False)
            continue

        elif event == RADIO_OLD_DF:
            # 显示旧表的内容
            datawindow[LOADDATA_NEW_DF_T].update(visible=False)
            datawindow[LOADDATA_NEW_DF].update(visible=False)
            datawindow[LOADDATA_OLD_DF_T].update(visible=True)
            datawindow[LOADDATA_OLD_DF].update(visible=True)
            continue

        # 确定分析文件
        elif event == '_ok_':
            try:
                targetdfid = int(datawindow[LOADDATA_NEW_DF].get()) \
                    if datawindow[RADIO_NEW_DF].get() else int(datawindow[LOADDATA_OLD_DF].get())
            except Exception as err:
                Sg.popup_error("目标表号不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            try:
                databasetype = values[DATABASE_TYPE]
                database = values[DATABASE_NAME]
                sqlstr = values[SQL_STRING]
                if databasetype != DATABASE_TYPE_SQLITE:
                    ipaddress = values[IP_ADDRESS]
                    if not check_ip(ipaddress):
                        Sg.popup_error("ip地址不正确：{}！".format(ipaddress),
                                       modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                        continue
                    port = int(values[IP_PORT])
                    user = values[USER_NAME]
                    password = dftrans_simple_encrypt(values[PASSWORD])
                else:
                    port = 8000
                    user = ''
                    password = ''
                # 记录当前默认值
                manualbuttonoperatedict[LOAD_SQL] = dict(zip(
                    defaultrecordlist, [databasetype, ipaddress, port, database, user, password, sqlstr]))
            except Exception as err:
                Sg.popup_error("相关参数输入不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            # "mysql+mysqlconnector://datauser:wZq8ne71iVJjNTE5@10.186.146.117:10336/edw?charset=utf8"
            result = dfloaddatafromdbbysql(
                specialdflist, [0], [targetdfid],  # specialdflist[0], [0], 为了适应df封装的标准输入
                databasetype=databasetype,
                ip=ipaddress,
                port=port, database=database, user=user, password=password,
                sqlstr=sqlstr,
            )

            if result[0] is True:
                # 刷新tabdata
                if guiflag:
                    # 更新表格数据
                    mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH, currentwindow=mainwindow)
                    mainwindow.refresh()
                    Sg.popup_quick_message("导入数据到表{}完成".format(targetdfid),
                                           modal=True, keep_on_top=True, text_color='white',
                                           background_color='dark blue')
                break
            else:
                if guiflag:
                    Sg.popup_error("sql导入数据到df序号{}失败：{}！".format(
                        targetdfid, result[1]), modal=True, keep_on_top=True)
                continue

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return


def savedatatodatabasebysql():
    """
    sql数据写入表格
    :return:
    """
    # "mysql+mysqlconnector://datauser:wZq8ne71iVJjNTE5@10.186.146.117:10336/edw?charset=utf8"
    """
    弹出输入界面，将指定数据保存到数据库表中
    """
    # 表格的编辑页面
    currentdfnumber = len(specialdflist)
    # 获取界面默认值
    defaultrecordlist = \
        [DATABASE_TYPE, IP_ADDRESS, IP_PORT, DATABASE_NAME, USER_NAME, PASSWORD, SAVEDATA_FILENAME, REPALCE_METHOD]
    if manualbuttonoperatedict.get(SAVE_SQL, None) is None:
        manualbuttonoperatedict[SAVE_SQL] = {}
    databasetype, ipaddress, ipport, databasename, username, password, outputname, replacemethod = map(
        manualbuttonoperatedict[SAVE_SQL].get, defaultrecordlist, ["" for _ in range(len(defaultrecordlist))])
    if databasetype != DATABASE_TYPE_SQLITE:
        password = dftrans_simple_decrypt(password)

    savedatalayinfo = [
        [
            [Sg.Text("数据库类型".ljust(10), size=(12, 1), font=DEF_FT_L),
             Sg.InputCombo([DATABASE_TYPE_SQLITE, DATABASE_TYPE_MYSQL], default_value=DATABASE_TYPE_SQLITE,
                           k=DATABASE_TYPE, size=(18, 1), font=DEF_FT_L, readonly=True)],
            [Sg.Text("ip地址".ljust(10), size=(12, 1), font=DEF_FT_L),
             Sg.Input(ipaddress, k=IP_ADDRESS, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("端口号".ljust(6), size=(12, 1), font=DEF_FT_L),
             Sg.Input(ipport, k=IP_PORT, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("数据库名".ljust(6), size=(12, 1), font=DEF_FT_L),
             Sg.Input(databasename, k=DATABASE_NAME, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("用户名".ljust(5), size=(12, 1), font=DEF_FT_L),
             Sg.Input(username, k=USER_NAME, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("密码".ljust(5), size=(12, 1), font=DEF_FT_L),
             Sg.Input(password, k=PASSWORD, size=(20, 1), font=DEF_FT_L, password_char='*')],
            [Sg.Text("输出表名".ljust(5), size=(12, 1), font=DEF_FT_L),
             Sg.Input(outputname, k=SAVEDATA_FILENAME, size=(20, 1), font=DEF_FT_L)],
            [Sg.Text("数据替换方式".ljust(5), size=(12, 1), font=DEF_FT_L),
             Sg.Combo(["replace", 'append', 'fail'], default_value=replacemethod,
                      k=REPALCE_METHOD, size=(18, 1), font=DEF_FT_L)],
        ],
        [
            # 使用已有表
            [Sg.HSeparator()],
            Sg.Text("导出数据表".ljust(5), size=(10, 1), font=DEF_FT_L),
            Sg.InputCombo([x for x in range(currentdfnumber)], k=SAVEDATA_DF, pad=(5, 5),
                          font=DEF_FT_L, size=(12, 1), readonly=True)

        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('sql导出到数据库表', savedatalayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        # 确定
        elif event == '_ok_':
            try:
                targetdfid = int(datawindow[SAVEDATA_DF].get())
            except Exception as err:
                Sg.popup_error("源表号不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            try:
                databasetype = values[DATABASE_TYPE]
                ipaddress = values[IP_ADDRESS]
                database = values[DATABASE_NAME]
                name = values[SAVEDATA_FILENAME]
                replacemethod = values[REPALCE_METHOD]
                if databasetype == DATABASE_TYPE_SQLITE:
                    port = 8000
                    user = 'temp'
                    password = ''
                else:
                    if not check_ip(ipaddress):
                        Sg.popup_error("ip地址不正确：{}！".format(ipaddress),
                                       modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                        continue
                    port = int(values[IP_PORT])
                    user = values[USER_NAME]
                    password = dftrans_simple_encrypt(values[PASSWORD])
                # 记录当前默认值
                manualbuttonoperatedict[SAVE_SQL] = dict(zip(
                    defaultrecordlist, [databasetype, ipaddress, port, database, user, password, name, replacemethod]))
            except Exception as err:
                Sg.popup_error("相关参数输入不正确：{}！".format(err),
                               modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            # "mysql+mysqlconnector://datauser:wZq8ne71iVJjNTE5@10.186.146.117:10336/edw?charset=utf8"
            result = dfsavedatatodatabasebysql(specialdflist,
                                               [targetdfid],
                                               databasetype=databasetype,
                                               ip=ipaddress,
                                               port=port,
                                               database=database,
                                               user=user,
                                               password=password,
                                               name=name,
                                               schema=None,
                                               if_exists=replacemethod,
                                               index=False,
                                               index_label=None,
                                               chunksize=None,
                                               dtype=None,
                                               method=None)

            if result[0] is True:
                if guiflag:
                    Sg.popup_quick_message("sql导出数据{}到表{}完成".format(targetdfid, name),
                                           modal=True, keep_on_top=True, text_color='white',
                                           background_color='dark blue')
                break
            else:
                if guiflag:
                    Sg.popup_error("sql导出数据序号{}到表{}失败：{}！".format(
                        targetdfid, name, result[1]), modal=True, keep_on_top=True)
                continue

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return


def savedatatofile(outputfilename, targetdfid, modelfilename='', index: bool = True, styleout: bool = False,
                   sheetnumber: int = 0, headline: int = 0, tailline: int = 0, sumrownumber: int = None) -> bool:
    """
    将df内容保存到文件
    :param outputfilename:                  str：输出文件全路径名
    :param targetdfid:                      int： 导出的df号
    :param modelfilename:                   str：输出模板文件全路径名
    :param index:                           bool: 是否输出行号
    :param styleout:                        bool: 无模板输出时，选择是否带df。style的格式输出
    :param sheetnumber:                     int: 输入模板的子表号
    :param headline:                        int：输出模板表首跳过行数
    :param tailline:                        int: 输出模板表尾跳过行数
    :param sumrownumber:                    int: 输出模板合计行行号
    :return:                                bool： True 导出成功， False 导出失败
    """
    # 判断是否有模板
    global specialdflist, guiflag
    if targetdfid >= len(specialdflist):
        errstr = "导出数据df序号{}不在合法范围[0,{}]！".format(targetdfid, len(specialdflist))
        print(errstr)
        if guiflag:
            Sg.popup_quick_message(errstr,
                                   modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return False

    result = dfsavedatatofile(specialdflist, [targetdfid], outputfilename,
                              modelfilename=modelfilename, index=index,
                              sheetnumber=sheetnumber, headline=headline,
                              tailline=tailline, styleout=styleout, sumrownumber=sumrownumber)

    if result[0] is True:
        errstr = "导出数据df序号{}到文件{}子表{}完成！".format(targetdfid, outputfilename, sheetnumber)
        print(errstr)
        if guiflag:
            Sg.popup_quick_message(errstr,
                                   modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return True
    else:
        errstr = "导出数据df序号{}到文件{}失败：{}！".format(targetdfid, outputfilename, sheetnumber)
        print(errstr)
        if guiflag:
            Sg.popup_error(errstr, modal=True, keep_on_top=True)
        return False


def savedatablocktofile(outputfilename, targetdfid, modelfilename='',
                        sheetnumber: int = 0,
                        sourcestartendrows: list = (0, None),
                        sourcestartendcols: list = (0, None),
                        targetstartrow=None,
                        targetstartcol=None) -> bool:
    """
    将df区块内容复制保存到文件区块
    :param outputfilename:                  str：输出文件全路径名
    :param targetdfid:                      int： 导出的df号
    :param modelfilename:                   str：输出模板文件全路径名
    :param sheetnumber:                     int: 输入模板的子表号
    :param sourcestartendrows:              list: 拷贝开始、结束行号，从0开始 [0, n]
    :param sourcestartendcols:              list: 拷贝开始、结束列号，从0开始 [0, n]
    :param targetstartrow:                  list:  目标起始行list
    :param targetstartcol:                  list: 目标起始列list
    :return:                                bool： True 导出成功， False 导出失败
    """
    # 判断是否有模板
    if targetstartcol is None:
        targetstartcol = [0]
    if targetstartrow is None:
        targetstartrow = [0]
    global specialdflist, guiflag
    if targetdfid >= len(specialdflist):
        errstr = "导出数据df序号{}不在合法范围[0,{}]！".format(targetdfid, len(specialdflist))
        print(errstr)
        if guiflag:
            Sg.popup_quick_message(errstr,
                                   modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return False

    result = dfcopydfblocktomodelexcelfile(
        specialdflist, [targetdfid], outputfilename, modelfilename=modelfilename,
        sheetnumber=sheetnumber, sourcestartendrows=sourcestartendrows, sourcestartendcols=sourcestartendcols,
        targetstartcol=targetstartcol, targetstartrow=targetstartrow)

    if result[0] is True:
        errstr = "导出数据df序号{}到文件{}子表{}完成！".format(targetdfid, outputfilename, sheetnumber)
        print(errstr)
        if guiflag:
            Sg.popup_quick_message(errstr,
                                   modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return True
    else:
        errstr = "导出数据df序号{}到文件{}失败：{}！".format(targetdfid, outputfilename, sheetnumber)
        print(errstr)
        if guiflag:
            Sg.popup_error(errstr, modal=True, keep_on_top=True)
        return False


def savedatatofilebutton():
    """
    将df写入文件按钮
    :return:
    """
    global myinputfiles, specialdflist, specialdflistcopy, mainwindow
    """
    弹出输入界面，用户输入导出文件名、如果有模板文件则模板文件名、表头表尾行，
    """
    # 表格的编辑页面
    currentdfnumber = len(specialdflist)
    loaddatalayinfo = [
        [
            # 使用已有表

            Sg.Text("导出表号".ljust(2), font=DEF_FT_L),
            Sg.InputCombo([x for x in range(currentdfnumber)], k=SAVEDATA_DF, pad=(5, 5),
                          font=DEF_FT_L, size=(12, 1), readonly=True),
            Sg.Checkbox("导出行号", default=True, k=SAVEDATA_WITH_INDEX, visible=True,
                        size=(12, 1), enable_events=False, font=DEF_FT_L),
            Sg.Checkbox("带格式导出", default=False, k=SAVEDATA_USE_STYLE, visible=True,
                        size=(12, 1), enable_events=False, font=DEF_FT_L)

        ],
        [
            Sg.Text("输出文件".ljust(2), font=DEF_FT_L),
            Sg.Input("", k=SAVEDATA_FILENAME, size=(51, 1), font=DEF_FT_L),
            Sg.Button('选择文件', k=SAVEDATA_CHOOSE_OUTPUTFILE, font=DEF_FT_L)
        ],
        [
            [Sg.HSeparator()],
            Sg.Checkbox("使用模板文件", default=False, k=SAVEDATA_USE_MODELFILE,
                        size=(12, 1), enable_events=True, font=DEF_FT_L)
        ],
        [
            Sg.Frame("模板文件配置", [
                [
                    Sg.Text("模板文件".ljust(2), font=DEF_FT_L),
                    Sg.Input("", k=SAVEDATA_MODELFILENAME, size=(50, 1), font=DEF_FT_L),
                    Sg.Button('选择文件', k=SAVEDATA_CHOOSE_MODELFILE, font=DEF_FT_L)
                ],
                [
                    Sg.Text("模板子表号".ljust(6), size=(10, 1), font=DEF_FT_L),
                    Sg.Input("0", k=SAVEDATA_SHEETNUMBER, size=(4, 1), font=DEF_FT_L),
                ],
                [Sg.HSeparator()],
                [
                    Sg.Radio('模板标准输出', "_save_data_radio_", default=True, size=(20, 1),
                             k=SAVEDATA_STANDARD_MODE_RADIO, enable_events=True),
                    Sg.Radio('模板区块拷贝输出', "_save_data_radio_", default=False, size=(20, 1),
                             k=SAVEDATA_BLOCKCOPY_MODE_RADIO, enable_events=True),
                ],
                [
                    Sg.Frame("",
                             [[

                                 Sg.Text("模板表首跳过行数".ljust(6), size=(16, 1), font=DEF_FT_L),
                                 Sg.Input("0", k=SAVEDATA_HEADLINE, size=(4, 1), font=DEF_FT_L),
                                 Sg.Text("模板表尾保留行数".ljust(10), size=(16, 1), font=DEF_FT_L),
                                 Sg.Input("0", k=SAVEDATA_TAILLINE, size=(4, 1), font=DEF_FT_L),
                                 Sg.Checkbox("模板合计行号", default=False, k=SAVE_SUMROW, size=(12, 1),
                                             enable_events=True, font=DEF_FT_L),
                                 Sg.Input("-1", k=SUMROW_LINE, size=(3, 1), font=DEF_FT_L, visible=False)

                             ]], k=SAVEDATA_STANDARD_MODE_FRAME, visible=True, border_width=0),
                    Sg.Frame("",
                             [
                                 [
                                     Sg.Text("源开始行号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("0", k=SAVEDATA_SOURCE_STARTROW, size=(4, 1), font=DEF_FT_L),
                                     Sg.Text("源开始列号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("0", k=SAVEDATA_SOURCE_STARTCOL, size=(4, 1), font=DEF_FT_L),
                                     Sg.Text("目标开始行号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("1", k=SAVEDATA_TARGET_STARTROW, size=(4, 1), font=DEF_FT_L),
                                 ],
                                 [
                                     Sg.Text("源结束行号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("-1", k=SAVEDATA_SOURCE_ENDROW, size=(4, 1), font=DEF_FT_L),
                                     Sg.Text("源结束列号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("-1", k=SAVEDATA_SOURCE_ENDCOL, size=(4, 1), font=DEF_FT_L),
                                     Sg.Text("目标开始列号".ljust(6), size=(12, 1), font=DEF_FT_L),
                                     Sg.Input("0", k=SAVEDATA_TARGET_STARTCOL, size=(4, 1), font=DEF_FT_L),
                                 ]
                             ], k=SAVEDATA_BLOCKCOPY_MODE_FRAME, visible=False, border_width=0)
                ]
            ], k=SAVEDATA_MODEL_FRAME, expand_x=True, visible=False),
        ],
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ]
    ]

    datawindow = Sg.Window('导出数据文件', loaddatalayinfo, icon=LOCAL_SYSTEM_ICON,
                           font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=False)

    while True:
        event, values = datawindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        elif event == SAVEDATA_USE_MODELFILE:
            # 使用模板文件则展示模板选项
            if values[SAVEDATA_USE_MODELFILE]:
                datawindow[SAVEDATA_USE_STYLE].update(visible=False)
                datawindow[SAVEDATA_WITH_INDEX].update(visible=False)
                datawindow[SAVEDATA_MODEL_FRAME].update(visible=True)
            else:
                datawindow[SAVEDATA_WITH_INDEX].update(visible=True)
                datawindow[SAVEDATA_USE_STYLE].update(visible=True)
                datawindow[SAVEDATA_MODEL_FRAME].update(visible=False)
                # 关闭时模板文件名改为“”，
                datawindow[SAVEDATA_MODELFILENAME].update("")
            continue

        elif event == SAVE_SUMROW:
            if values[SAVE_SUMROW]:
                datawindow[SUMROW_LINE].update(visible=True)
            else:
                datawindow[SUMROW_LINE].update(visible=False)

        # 选择文件
        elif event == SAVEDATA_CHOOSE_MODELFILE:
            # 变更模板文件名
            filetemp = Sg.popup_get_file('选择文件',
                                         icon=LOCAL_SYSTEM_ICON,
                                         file_types=(("表格模板文件", "*.xlsx"),),
                                         no_window=True)

            if filetemp:
                datawindow[SAVEDATA_MODELFILENAME](filetemp)

            continue

        # 选择模板输出模式
        elif event == SAVEDATA_STANDARD_MODE_RADIO:
            # 打开标准模式，关闭区块模式
            datawindow[SAVEDATA_BLOCKCOPY_MODE_FRAME].update(visible=False)
            datawindow[SAVEDATA_STANDARD_MODE_FRAME].update(visible=True)
            continue
        # 选择区块拷贝
        elif event == SAVEDATA_BLOCKCOPY_MODE_RADIO:
            # 关闭标准模式，打开区块模式
            datawindow[SAVEDATA_BLOCKCOPY_MODE_FRAME].update(visible=True)
            datawindow[SAVEDATA_STANDARD_MODE_FRAME].update(visible=False)
            continue

        elif event == SAVEDATA_CHOOSE_OUTPUTFILE:
            # 变更输出文件名
            filetemp = Sg.popup_get_file('选择文件',
                                         icon=LOCAL_SYSTEM_ICON,
                                         file_types=(("表格文件", "*.xlsx"),),
                                         no_window=True,
                                         save_as=True)

            if filetemp:
                datawindow[SAVEDATA_FILENAME](filetemp)

            continue

        # 确定分析文件
        elif event == '_ok_':
            # 点击OK，进行导出操作
            modelfilename = ''
            sheetnumber = 0
            headline = 0
            tailline = 0
            try:
                targetdfid = int(datawindow[SAVEDATA_DF].get())
            except Exception as err:
                Sg.popup_error("目标表号不正确！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue
            sumrownumber = None
            modelfilename = None
            outputfilename = values[SAVEDATA_FILENAME]
            styleout = values[SAVEDATA_USE_STYLE]
            index = values[SAVEDATA_WITH_INDEX]
            if outputfilename == '':
                Sg.popup_error("输出文件名不能为空！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                continue

            if values[SAVEDATA_USE_MODELFILE]:
                modelfilename = values[SAVEDATA_MODELFILENAME]
                standardmodelflag = datawindow[SAVEDATA_STANDARD_MODE_RADIO].get()
                if modelfilename == '':
                    Sg.popup_error("模板文件名不能为空！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                try:
                    sheetnumber = int(values[SAVEDATA_SHEETNUMBER])
                    headline = int(values[SAVEDATA_HEADLINE])
                    tailline = int(values[SAVEDATA_TAILLINE])
                    sourcestartendrows = [int(values[SAVEDATA_SOURCE_STARTROW]), int(values[SAVEDATA_SOURCE_ENDROW])]
                    sourcestartendcols = [[int(values[SAVEDATA_SOURCE_STARTCOL]), int(values[SAVEDATA_SOURCE_ENDCOL])],
                                          ["", ""]]
                    targetstartrow = [int(values[SAVEDATA_TARGET_STARTROW])]
                    targetstartcol = [int(values[SAVEDATA_TARGET_STARTCOL])]
                    if values[SAVE_SUMROW]:
                        sumrownumber = int(values[SUMROW_LINE])
                    else:
                        sumrownumber = None
                except Exception as err:
                    if standardmodelflag:
                        Sg.popup_error("子表号、表首行数或者表尾行数等不正确：{}！".format(err),
                                       modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    else:
                        Sg.popup_error("子表号、源数据起止行号、列号或目标坐标不正确：{}！".format(err),
                                       modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                    continue
                if not standardmodelflag:
                    # 如果是模式拷贝方式
                    if savedatablocktofile(
                            outputfilename, targetdfid, sheetnumber=sheetnumber, modelfilename=modelfilename,
                            sourcestartendrows=sourcestartendrows, sourcestartendcols=sourcestartendcols,
                            targetstartrow=targetstartrow, targetstartcol=targetstartcol):
                        break
                    else:
                        continue
            # 非模式拷贝或者无模板模式
            if savedatatofile(
                    outputfilename, targetdfid, sheetnumber=sheetnumber, styleout=styleout, index=index,
                    modelfilename=modelfilename, headline=headline, tailline=tailline, sumrownumber=sumrownumber):
                break
            else:
                continue

    # 点击close或者关闭，不修改任何值，返回 None
    datawindow.close()
    return


def deletedatatable():
    """
    手工删除数据表格
    :return:
    """
    # 从grouptab获取当前表格号
    try:
        currentsubtab = int(mainwindow[GROUP_TAB_KEY].get()[1])
    except:
        Sg.popup_error("无法获取当前表格！", modal=True, keep_on_top=True)
        return
    if not Sg.popup_ok_cancel("确定删除表[{}]？？？！！！".format(currentsubtab),
                              modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON) == "OK":
        return
    # 将数据df从specialdflist、specialdflistcopy弹出
    if currentsubtab in range(len(specialdflist)):
        specialdflist.pop(currentsubtab)

    # 刷新显示页面，刷新当前删除表及以后的表格显示
    print("刷新表格显示数据......")
    starttime = datetime.now()
    mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH, currentwindow=mainwindow)
    endtime = datetime.now()
    # 刷新进度条说明
    mainwindow.refresh()
    print("刷新表格显示数据用时：{}".format(endtime - starttime))


def clearselected(values=None, rowflag: bool = True):
    """
    :param values:          主窗口values
    :param rowflag:         bool True， 复位已选行， False：复位已选列
    清除当前表的已选行
    :return:
    """
    # 从grouptab获取当前表格号
    try:
        currentsubtab = int(mainwindow[GROUP_TAB_KEY].get()[1])
    except:
        Sg.popup_error("无法获取当前表格！", modal=True, keep_on_top=True)
        return

    # 将当前表已选行或者列清空
    if currentsubtab in range(len(specialdflist)):
        if rowflag:
            print("复位选中行")
            specialdflist[currentsubtab].selectedrawrow = set()
        else:
            print("复位选中列")
            specialdflist[currentsubtab].selectedrawcolumn = set()

    # 刷新显示页面，刷新当前删除表及以后的表格显示
    print("刷新表格显示数据......")
    starttime = datetime.now()
    # 仿真当前tab trigger时间
    values[(GROUP_TAB_KEY, GROUP_TAB_KEY)] = (GROUP_TAB_KEY, currentsubtab)
    mainwindow[GROUP_TAB_KEY].update(
        commandtype=SPECIAL_TABLE_GROUP_TRIGGER_TAB, currentwindow=mainwindow,
        currentvalues=values, triggertable=currentsubtab)
    endtime = datetime.now()
    # 刷新进度条说明
    mainwindow.refresh()
    print("刷新表格显示数据用时：{}".format(endtime - starttime))

    return


def plotshowdf():
    # 表格的编辑页面
    currentdfnumber = len(specialdflist)
    if currentdfnumber == 0:
        Sg.popup_error("当前无数据表格！", modal=True, keep_on_top=True)
        return
    try:
        currentsubtab = int(mainwindow[GROUP_TAB_KEY].get()[1])
    except:
        Sg.popup_error("无法获取当前表格！", modal=True, keep_on_top=True)
        return
    dfplotshowdf(specialdflist, [currentsubtab],
                 plottype="", indexcolumn=[[], []],
                 valuecolumns=[[], []],
                 title="",
                 xlabel="",
                 ylabel="",
                 showgrid=True,
                 showlegend=True,
                 showstacked=False,
                 showwidth=DEF_PLOT_WIDTH,
                 showheight=DEF_PLOT_HEIGHT,
                 showdirect=False,
                 savefigurefile=False,
                 figeurefilename=None)
    

def is_ip(address):
    try:
        IP(address)
        return True
    except Exception as e:
        return False


def check_ip(ipaddr):
    # \d表示0~9的任何一个数字
    # {2}表示正好出现两次
    # [0-4]表示0~4的任何一个数字
    # | 的意思是或者
    # 1\d{2}的意思就是100~199之间的任意一个数字
    # 2[0-4]\d的意思是200~249之间的任意一个数字
    # 25[0-5]的意思是250~255之间的任意一个数字
    # [1-9]\d的意思是10~99之间的任意一个数字
    # [1-9])的意思是1~9之间的任意一个数字
    # \.的意思是.点要转义（特殊字符类似，@都要加\\转义）
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipaddr):
        return True
    else:
        return False


def command2sentence(command: list) -> str:
    """
    将命令行参数转换为备注字符串
    :param command:             list： 命令行list
            "['列求差', [0], {}, '差测试列1', '[18, 19]'] 对应代码: dfcolumnsubtract(specialdflist[0], '差测试列1', [18, 19]]"
    :return:                    str：转换后的命令行说明字符串
    """
    # 获取命令名
    if debugflag:
        print("currentcmd:", command)
    commandname = command[CURRENT_COMMAND]
    # 查看是否使用了命令旧名称，如果是，转换为新命令名
    tempname = commandalias.get(commandname, None)
    if tempname is not None:
        commandname = tempname
        # 回填到命令list，以便后续使用
        command[CURRENT_COMMAND] = commandname
    # 从命令字典中获取该命令的配置
    commandconfig = getcommandconfig(commandname)
    # 如果没有该命令，返回None
    if commandconfig is None:
        return ""

    # 获取该命令对应的函数以及函数的参数信息
    functionname = commandconfig[COMMAND_FUNCTION_NAME]
    # 获取函数的整体说明
    functionconfig = originfunctiondict.get(functionname, None)
    if functionconfig is None:
        return ""

    argcstr, argvstr = "", ""
    # 组合argc字符串，逐个获取
    try:
        for item, argcparam in enumerate(functionconfig["argcitems"]):
            # 获取该argc的说明
            argcsentence = functionconfig['argc'][argcparam][FUNCTION_ARG_SENTENCE]
            # 获取该argc的值
            argcvalue = command[CURRENT_COMMAND_PARAMS + 2 + item]
            # 组合
            argcstr += "{0}{1}".format(argcsentence, argcvalue)

        # 组合argv字符串，逐个获取
        for item, argvparam in enumerate(command[CURRENT_COMMAND_PARAMS + 1]):
            # 获取该argv的说明
            argvsentence = functionconfig['argv'][argvparam][FUNCTION_ARG_SENTENCE]
            # 获取该argv的值
            argvvalue = command[CURRENT_COMMAND_PARAMS + 1][argvparam]
            # 组合
            argvstr += "{0}{1}".format(argvsentence, argvvalue)
    except Exception as err:
        print("转换命令{}为说明语句失败：{}".format(command, err))
        return ""

    # 组合整体字符串
    sentencestr = "{0}{1}{2} 执行{3}".format(
        "对表{}".format(command[CURRENT_OPERATE_DFS]) if len(command[CURRENT_OPERATE_DFS]) > 0 else "",
        argcstr,
        argvstr,
        commandname)
    return sentencestr


DATA_TABLE_OPERATE_FRAME = '_data_table_operate_frame_'
LOAD_DATA = '_load_data_'
LOAD_SQL = '_load_sql_'
SAVE_DATA = '_save_data_'
SAVE_SQL = '_save_sql_'
DELETE_DATA = '_delete_data_'
CLEAR_SELECTED_ROW = '_clear_selected_row_'
CLEAR_SELECTED_COL = '_clear_selected_col_'
PLOT_SHOW_DATA = '_plot_show_data_'
START_COMMAND_RECORD = '_start_command_record_'
STOP_COMMAND_RECORD = '_stop_command_record_'
LOAD_COMMAND = '_load_command_'
SAVE_COMMAND = '_save_command_'
GENERATE_COMMAND_FILE_COMMENT = '_generate_command_file_comment_'
EDIT_CONFIG = '_edit_system_config_'

EDIT_WIN_OK = '_edit_win_ok_'
EDIT_WIN_CANCEL = '_edit_win_cancel_'
EDIT_WIN_SAVEAS = '_edit_win_saveas_'

# 命令选择
COMMAND_LIST = '_command_list_'

SIMULATE_EVENT = '_simulate_event_'

# 操作表1相关选择
DF1_CHOOSE = '_df1_choose_'
DF1_COLUMN_CHOOSE = '_df1_column_choose_'
DF1_ROWS_INPUT = '_df1_rows_input_'

# 操作表2相关选择
DF2_CHOOSE = '_df2_choose_'
DF2_COLUMN_CHOOSE = '_df2_column_choose_'
DF2_ROWS_INPUT = '_df2_ROWS_input_'

# 多表操作选择
DF_MULTI_CHOOSE = '_df_multi_choose_'

# 运行参数
ARGC_CONFIG = '_argc_config_'
ARGV_CONFIG = '_argv_config_'

ARGC_CONFIG_VALUE = '_argc_config_value_'
ARGV_CONFIG_VALUE = '_argv_config_value_'

ARGV_CONFIG_COMMENT = '_argv_config_comment_'
ARGC_CONFIG_COMMENT = '_argc_config_comment_'

ARGC_PARAM_EDIT = '_argc_param_edit_'
ARGV_PARAM_EDIT = '_argv_param_edit_'

# 用于editevent驱动开关的其他elements
DF_CHOOSE_RESULT = '_df_choose_result_'
DF_CHOOSE_RESULT_FRAME = '_df_choose_result_frame_'
ARGC_RESULT = '_argc_result_'
ARGC_RESULT_FRAME = '_argc_result_frame_'
ARGV_RESULT = '_argv_result_'
ARGV_RESULT_FRAME = '_argv_result_frame_'
COMMAND_CONFIG_OK = '_command_config_ok_'
COMMAND_GENERATE = '_command_generate_'
COMMAND_STRUCTURE = '_command_structure_'
COMMAND_SENTENCE = '_command_sentence_'
COMMAND_COMMENT = '_command_comment_'

COMMAND_LIST_FRAME = '_command_list_frame_'

#  表格选择
OPERATE_DFS_CHOOES_FRAME = '_operate_df_choose_frame_'
DF_SINGLE_TWO_CHOOSE_FRAME = '_df_single_two_choose_frame_'
# 操作表1相关选择frame
DF1_CHOOSE_FRAME = '_df1_choose_frame_'
DF1_COLUMN_CHOOSE_FRAME = '_df1_column_choose_frame_'
DF1_ROWS_INPUT_FRAME = '_df1_rows_input_frame_'

# 操作表2相关选择frame
DF2_CHOOSE_FRAME = '_df2_choose_frame_'
DF2_COLUMN_CHOOSE_FRAME = '_df2_column_choose_frame_'
DF2_ROWS_INPUT_FRAME = '_df2_ROWS_input_frame_'

# 多表操作选择frame
DF_MULTI_CHOOSE_FRAME = '_df_multi_choose_frame_'

# 运行参数frame
ARGC_CONFIG_FRAME = '_argc_config_frame_'
ARGV_CONFIG_FRAME = '_argv_config_frame_'
ARGC_CONFIG_VALUE_FRAME = '_argc_config_value_frame_'
ARGV_CONFIG_VALUE_FRAME = '_argv_config_value_frame_'

# param编辑窗口key定义
PARAM_EDIT_OK = '_param_edit_ok_'
PARAM_EDIT_CANCEL = '_param_edit_cancel_'
PARAM_EDIT_COMMENT = '_param_edit_comment_'
PARAM_EDIT_RESULT = '_param_edit_result_'
PARAM_EDIT_RESULT_CONFIRM = '_param_edit_result_confirm_'
PARAM_EDIT_COLUMNS_NAME = '_param_edit_columns_name_'
PARAM_EDIT_COLUMNS_INDEX = '_param_edit_columns_index_'
PARAM_EDIT_COLUMNS_FRAME = '_param_edit_column_frame_'
PARAM_EDIT_COLUMNNAMES = '_param_edit_columnnames_'
PARAM_EDIT_COLUMNNAMES_HEADS = '_param_edit_columnames_heads_'
PARAM_EDIT_QUERY_TABLE = '_param_edit_query_table_'
PARAM_SAVE_FILENAME = '_param_save_filename_'
PARAM_READ_FILENAME = '_param_read_filename_'
PARAM_SELECT_ALL = '_select_all_'
PARAM_CLEAR_ALL = '_clear_all_'


def eventnull(currentwindow, event, values):
    print("event:{}".format(event))


def getcommandconfig(commandname, menuflag=False):
    """
    根据commanddict和commandname获取commandname对应的命名配置，
    :param commandname:    命令名称
    :param menuflag:       是否判断菜单显示的配置
    :return:               None or commandname 对应的命令配置
    """
    global commanddict
    # 从命令字典中获取该命令的配置，对于已经用UNSHOW_MENU_FLAG屏蔽的命令，需要多做一次获取尝试
    commandconfig = commanddict.get(commandname, False)
    if commandconfig and menuflag:
        commandconfig = commandconfig if commandconfig[COMMAND_SHOW_FLAG] == SHOW_COMMAND_FLAG else None
    # 如果没有该命令，返回None
    return None if commandconfig in [False, None] else commandconfig


# 选择了某个新命令后进行处理
def commandchoosed(currentwindow, event, values):
    """
    某个命令选中后，初始化命令配置界面中所有的相关配置选项框
    :param currentwindow:                  当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    global debugflag, commanddict, originfunctiondict, useroperatedict
    # 获取当前命令
    currentcommand = values[event]
    currentcommandconfig = getcommandconfig(currentcommand)
    if currentcommandconfig is None:
        return
    if debugflag:
        print("选中命令：{}, {}".format(currentcommand, currentcommandconfig))

    # 获取当前命令的各项关联配置
    # 使用的函数
    functionname = currentcommandconfig[COMMAND_FUNCTION_NAME]
    if functionname.strip() == "":
        return

    # 操作表数
    operatedfsnumber = currentcommandconfig[COMMAND_MULTI_DF_FLAG]
    # LISTBOX_SELECT_MODE_SINGLE LISTBOX_SELECT_MODE_MULTIPLE
    if operatedfsnumber == SINGLE_DF:
        currentwindow[DF_MULTI_CHOOSE].update(select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE)
    else:
        currentwindow[DF_MULTI_CHOOSE].update(select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE)
    # 从function的配置字典获取该function的配置
    # 确定当前命令是否使用用户默认值
    userdefaultflag = currentcommandconfig.get(COMMAND_USER_INPUT_PARAM, None)
    if userdefaultflag == RECORD_USER_PARAM_NO:
        # 不使用用户默认值，保存相关配置，以便文件记录和后续处理
        tempfunctiondict = originfunctiondict
        # useroperatedict[functionname] = copy.deepcopy(originfunctiondict[functionname])
    else:
        tempfunctiondict = useroperatedict
    # 首先判断命令的是否使用用户默认值，
    functioninfodict = tempfunctiondict.get(functionname, None)
    if functioninfodict is None:
        useroperatedict[functionname] = copy.deepcopy(originfunctiondict[functionname])
        functioninfodict = tempfunctiondict.get(functionname, None)

    # 获取argcitems list, 用于确定用到的argc在函数中的赋值顺序
    # 获取argcdict
    # 从functionname获取argvdict
    argcuseditems, argcdict, argvdict = map(functioninfodict.get, ['argcitems', 'argc', 'argv'], [None, None, None])
    if None in (argcuseditems, argcdict, argvdict):
        return

    # 形成argcuseddict
    argcuseddict = dict(zip(argcuseditems, [argcdict[x].get(FUNCTION_ARG_DEFAULTVALUE) for x in argcuseditems]))
    # 获得argv的使用清单
    argvuseditems = list(currentcommandconfig[COMMAND_FUNCTION_PARAM])
    # 形成argvuseddict
    argvuseddict = dict(
        zip([x for x in argvuseditems], [argvdict[x].get(FUNCTION_ARG_DEFAULTVALUE) for x in argvuseditems]))

    # 更新操作表对应的操作表界面内容
    # 更新argc列表及值
    currentwindow[ARGC_CONFIG].update(values=list(str(x) for x in argcuseddict.keys()))
    currentwindow[ARGC_CONFIG_VALUE].update(values=list(str(x) for x in argcuseddict.values()))
    currentwindow[ARGC_CONFIG_COMMENT].update(
        values=[str(argcdict[x].get(FUNCTION_ARG_COMMENT)) for x in argcuseditems])
    # 更新argv列表及值
    currentwindow[ARGV_CONFIG].update(values=list(str(x) for x in argvuseddict.keys()))
    currentwindow[ARGV_CONFIG_VALUE].update(values=list(str(x) for x in argvuseddict.values()))
    currentwindow[ARGV_CONFIG_COMMENT].update(
        values=[str(argvdict[x].get(FUNCTION_ARG_COMMENT)) for x in argvuseditems])
    # 更新操作表选择
    currentwindow[DF_MULTI_CHOOSE].set_value([])
    currentwindow[DF_CHOOSE_RESULT].update(value=str([]))
    commandshowrefresh(currentwindow, event, values)


# 选择了df1 or df2，需要更新df1\df2对应的列信息
def df1_2choosed(currentwindow, event, values):
    """
    选中df1后，初始化命令配置界面中所有的相关配置选项框
    :param currentwindow:           当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    global commanddict
    # 获取当前命令
    # currentcommandconfig = commanddict.get(values[COMMAND_LIST], None)
    currentcommandconfig = getcommandconfig(values[COMMAND_LIST])
    operatedfsnumber = currentcommandconfig[COMMAND_MULTI_DF_FLAG]
    # 获取当前命令的值：指向选择的df
    currentdf = values[event]
    # 更新df1列信息
    if event == DF1_CHOOSE:
        currentwindow[DF1_COLUMN_CHOOSE].update(values=currentdfcolumnlist[currentdf])
        # DF1 需要根据是单表还是双表命令区分使用几个表
        if operatedfsnumber == SINGLE_DF:
            # 单表是只显示表一选择
            currentwindow[DF_CHOOSE_RESULT].update(value=str([values[DF1_CHOOSE]]))
        else:
            # 双表是显示两张表的选择
            currentwindow[DF_CHOOSE_RESULT].update(value=str([values[DF1_CHOOSE], values[DF2_CHOOSE]]))
    elif event == DF2_CHOOSE:
        currentwindow[DF2_COLUMN_CHOOSE].update(values=currentdfcolumnlist[currentdf])
        currentwindow[DF_CHOOSE_RESULT].update(value=str([values[DF1_CHOOSE], values[DF2_CHOOSE]]))

    # 根据df1, df2的情况刷新 DF_CHOOSE_RESULT


# 选择了多表
def dfmultichoosed(currentwindow, event, values):
    """
    选中df multi后，初始化命令配置界面中所有的相关配置选项框
    :param currentwindow:           当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    # 获取当前的选中的表
    currentdf = values[event]
    # 判断选择表数是否和命令需要的额操作表数一致
    # 获取当前命令
    currentcommand = values[COMMAND_LIST]
    # currentcommandconfig = commanddict.get(currentcommand, None)
    currentcommandconfig = getcommandconfig(currentcommand)
    if currentcommandconfig is None:
        return
    # 如果是表格导入命令，不需要选择表格
    if currentcommandconfig[COMMAND_TYPE] == COMMAND_NEW_TABLE_IMPORT:
        currentwindow[DF_MULTI_CHOOSE].set_value([])
        Sg.popup_quick_message("当前命令无需在此选择表格！",
                               modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return
    # 操作表数
    operatedfsnumber = currentcommandconfig[COMMAND_MULTI_DF_FLAG]
    if operatedfsnumber == TWO_DF and len(currentdf) > 2:
        Sg.popup_quick_message("当前命令选择表数目不能大于2！",
                               modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return

    currentwindow[DF_CHOOSE_RESULT].update(value=str(currentdf))
    commandshowrefresh(currentwindow, event, values)


# 选择了arg，需要更新arg对应的输入
def argchoosed(currentwindow, event, values):
    """
    选中某个argc后，初始化命令配置界面中所有的相关配置选项框
    :param currentwindow:                  当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    global debugflag
    # 获取当前命令
    currentagr = currentwindow[event].get_indexes()
    if debugflag:
        print("event {} 选中arg：{}".format(event, currentagr))
    # 如果是argc相关同步argc列表的对应值
    if event in (ARGC_CONFIG, ARGC_CONFIG_VALUE, ARGC_CONFIG_COMMENT):
        currentwindow[ARGC_CONFIG].update(set_to_index=currentagr)
        currentwindow[ARGC_CONFIG_VALUE].update(set_to_index=currentagr)
        currentwindow[ARGC_CONFIG_COMMENT].update(set_to_index=currentagr)
    else:
        # argv相关同步argv列表的对应值
        currentwindow[ARGV_CONFIG].update(set_to_index=currentagr)
        currentwindow[ARGV_CONFIG_VALUE].update(set_to_index=currentagr)
        currentwindow[ARGV_CONFIG_COMMENT].update(set_to_index=currentagr)


# param 编辑窗口
PARAM_WINDOWS_NORMAL_SIZE = (500, 180)
PARAM_WINDOWS_MIDDLE_SIZE = (500, 360)
PARAM_WINDOWS_LONG_SIZE = (500, 660)
PARAM_WINDOWS_WIDE_SIZE = (800, 400)

# 用于记录querylist的左括号位置flag
LEFT_MARK_FLAG = '_left_mark_[_'

# command structure中的param在窗口编辑时做了str()转换，重新拼接时需要反向eval，str不需要
PARAM_TYPE_TRANS_FLAG = "type_trans"
PARAM_TYPE_VALID = "type_valid"
# 参数是否需要进行eval转换，以及参数的类型
paramtypetransmap = {
    'str': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str
    },
    'ipaddress': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: check_ip
    },
    "password": {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: str
    },
    "sqlstr": {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str
    },
    'object': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: object
    },
    'strcombo': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str},
    'columns': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list},
    'targetcolumns': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list},
    'sourcecolumns': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list},
    'columnname': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'rows': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'position': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: int
    },
    'rowvaluelist': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'list': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'bool': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: bool
    },
    'int': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: int
    },
    'intcombo': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: int
    },
    'float': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: int
    },
    'combo': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: list
    },
    'dict': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: dict
    },
    'newtable': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'example': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str
    },
    'querylist': {
        PARAM_TYPE_TRANS_FLAG: True,
        PARAM_TYPE_VALID: list
    },
    'savefile': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str
    },
    'readfile': {
        PARAM_TYPE_TRANS_FLAG: False,
        PARAM_TYPE_VALID: str
    }
}


def argparamedit(currentwindow, event, values):
    """
    选中某个argc后，初始化命令配置界面中所有的相关配置选项框
    :param currentwindow:            当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    global debugflag
    # 获取当前编辑的param，命令，参数类别，具体参数名
    currentcommand = values[COMMAND_LIST]
    # 对于数据导入，不一定要在现有表格中选择
    currentdf = values[DF_CHOOSE_RESULT]
    if (not ast.literal_eval(currentdf)) and commanddict[currentcommand][COMMAND_TYPE] != COMMAND_NEW_TABLE_IMPORT:
        Sg.popup_quick_message("请先选择操作的表格！",
                               modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return

    if event == ARGC_PARAM_EDIT:
        # argc相关
        argparam, argvalue = currentwindow[ARGC_CONFIG].get(), currentwindow[ARGC_CONFIG_VALUE].get()
    else:
        # argv相关
        argparam, argvalue = currentwindow[ARGV_CONFIG].get(), currentwindow[ARGV_CONFIG_VALUE].get()
    if debugflag:
        print("{}选中命令:{}, 表格：{} arg：{}, 值：{}".format(event, currentcommand, currentdf, argparam, argvalue))

    # if argparam == [] or argparam == []:
    if argparam == []:
        Sg.popup_quick_message("请先选择要修改的选项！",
                               modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
        return

    # 调用param编辑窗
    resultdict = argpararmeditgui(currentcommand, currentdf, event, argparam, argvalue)
    if resultdict != {}:
        # 获取当前操作的list
        operatelist = ARGC_CONFIG_VALUE if event == ARGC_PARAM_EDIT else ARGV_CONFIG_VALUE
        # 获取参数名在list中对应的index
        currentvalueindex = currentwindow[operatelist].get_indexes()
        # 获取整个列表清单
        currentvaluelist = currentwindow[operatelist].get_list_values()
        # 对列表清单赋新值， 因为只修改一个参数，所以只需要更新第1个
        currentvaluelist[currentvalueindex[0]] = list(resultdict.values())[0]
        # 列表清单写回list,并复位列表当前选择项
        currentwindow[operatelist].update(values=currentvaluelist, set_to_index=currentvalueindex)
        # 刷新命令显示窗
        commandshowrefresh(currentwindow, event, values)


def argparaminfoget(currentcommand: str, argevent: str, argparam: str) -> list:
    """
    :param currentcommand:                      str 当前命令名
    :param argevent:                            str: 当前的arg类型事件 ARGC_PARAM_EDIT|ARGV_PARAM_EDIT
    :param argparam:                            str: 当前命令对应的事件
    :return:                                    ['type', 'validvalue', 'defaultvalue', 'comment'] or []

    """
    # commandconfig = commanddict.get(currentcommand, None)
    commandconfig = getcommandconfig(currentcommand)
    # 如果没有该命令，返回None
    if commandconfig is None:
        return []

    # 获取该命令对应的函数以及函数的参数信息
    functionname = commandconfig[COMMAND_FUNCTION_NAME]
    # 获取函数的整体说明
    functionconfig = originfunctiondict.get(functionname, None)
    if functionconfig is None:
        return []

    # 获取type、默认值、合法值、comments
    # 确定当期是argc还是argv
    currentargstr = 'argc' if argevent == ARGC_PARAM_EDIT else 'argv'
    # 获取函数参数的整体字典
    functiondict = functionconfig.get(currentargstr, None)
    if functiondict is None:
        return []
    else:
        # 获取当前param的配置字典
        paramdict = functiondict.get(argparam, None)
        if paramdict is None:
            return []

    temp1, temp2, temp3, temp4, temp5 = map(paramdict.get,
                                            ['type', FUCNTION_ARG_VALIDVALUE, FUNCTION_ARG_DEFAULTVALUE,
                                             FUNCTION_ARG_COMMENT, FUNCTION_ARG_LONG_COMMENT])
    # 获取该param的对应条目
    return [temp1, temp2, temp3, temp4, temp5]


def argpararmeditgui(currentcommand: str, currentdf: list, argevent: str, argparam: list, argvalue: list) -> dict:
    """
    编辑当前param的图形界面
    :param currentcommand:                      str 当前命令名
    :param currentdf:                           list： 当前操作的表格列表
    :param argevent:                            str: 当前的arg类型事件
    :param argparam:                            list： 当前param的list， 只有一个元素
    :param argvalue:                            list： 当前param value的list，只有一个元素
    :return:                                    dict： {param: param value}
    """
    # 获取当前param的dict
    global originfunctiondict, commanddict
    # 获取该param的对应条目
    resultlist = argparaminfoget(currentcommand, argevent, argparam[0])
    if not resultlist:
        return {}

    paramtype, paramvalidvalue, paramdefaultvale, paramcomment, paramlongcomment = resultlist
    if debugflag:
        print("当前参数：{}， type:{}, validevalue:{} defaultvalue:{}, comment:{}, longcomment:{}, old value:{}".format(
            argparam[0], paramtype, paramvalidvalue, paramdefaultvale, paramcomment, paramlongcomment, argvalue[0]))

    # 启动对该param的编辑函数
    # 针对不同的param类型，使用不同的界面
    # str， columns， rows， position， list， bool， int，
    paraminfolayout = [[Sg.Text(
        "\n".join([currentcommand, paramlongcomment]),
        k=PARAM_EDIT_COMMENT,
        pad=DEF_PD_L,
        enable_events=False,
        background_color="dark blue",
        text_color='white',
        size=(80, 3),
        border_width=1,
        expand_x=True,
        justification='center')
    ]]

    def debuglayout(layouttype: str = "columns") -> list:
        """
        默认型param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5), font=PARAM_FT,
                         size=(20, 1), expand_x=True, border_width=2)
            ]], justification='center', expand_x=True)
        ]]

    def stringlayout(layouttype: str = "columns") -> list:
        """
        编辑字符串param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2)
            ]], justification='center', expand_x=True)
        ]]

    def ipaddresslayout(layouttype: str = "columns") -> list:
        """
        编辑ipaddress param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2)
            ]], justification='center', expand_x=True)
        ]]

    def passwordlayout(layouttype: str = "columns") -> list:
        """
        编辑ipaddress param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Text("输入密码"),
                Sg.Input(dftrans_simple_decrypt(argvalue[0]), k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2,
                         password_char='*')
            ]], justification='center', expand_x=True)],
            [
                Sg.Col([[
                    Sg.Text("确认密码"),
                    Sg.Input(dftrans_simple_decrypt(argvalue[0]), k=PARAM_EDIT_RESULT_CONFIRM, pad=(5, 5),
                             font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2,
                             password_char='*')
                ]], justification='center', expand_x=True)],
        ]

    def sqlstrlayout(layouttype: str = "columns") -> list:
        """
        编辑sql字符串param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.ML(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                      autoscroll=True, horizontal_scroll=True,
                      font=PARAM_FT, size=(60, 16), expand_x=True, border_width=2)
            ]], justification='center', expand_x=True)
        ]]

    def savefilelayout(layouttype: str = "columns") -> list:
        """
        编辑输出文件名
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(50, 1), expand_x=True, border_width=2),
                Sg.Button('更改', k=PARAM_SAVE_FILENAME)
            ]], justification='center', expand_x=True)
        ]]

    def readfilelayout(layouttype: str = "columns") -> list:
        """
        编辑输入文件名
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(50, 1), expand_x=True, border_width=2),
                Sg.Button('更改', k=PARAM_READ_FILENAME)
            ]], justification='center', expand_x=True)
        ]]

    def stringcombolayout(layouttype: str = "columns") -> list:
        """
        编辑字符串(有几个合法的选择值)param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.InputCombo(paramvalidvalue, k=PARAM_EDIT_RESULT, pad=(5, 5), expand_x=True,
                              font=PARAM_FT, size=(60, 1), default_value=argvalue[0], readonly=False)
            ]], justification='center', expand_x=True)
        ]]

    def columnslayout(layouttype: str = "columns") -> list:
        """
        表格列选择的param的layout
        :return:            list：layout
        """
        # 当前表号
        # 如果是普通通columns或者是双表的第一个表
        if layouttype in ['columns', 'sourcecolumns']:
            currentdfid = ast.literal_eval(currentdf)[0]
        else:
            # 双表的第二张表,如果只有一张表就全部使用第一张表
            currentdfid = ast.literal_eval(currentdf)[1] if len(ast.literal_eval(currentdf)) > 1 else \
            ast.literal_eval(currentdf)[0]
        if currentdfid >= len(currentdfcolumnlist):
            print("目前表格数：{}表格：{}尚未生成！".format(currentdfid, len(currentdfcolumnlist)))
            return debuglayout()
        # 当前表的列名list
        currentcolumnsname = currentdfcolumnlist[currentdfid]
        # 当前选择的列序号list, columnsd格式从[列序号1，列序号2....]变更为[[列序号1，列序号2....],[列名1， 列名2......]]
        # 此处进行判断做前向兼容
        tempindex = ast.literal_eval(argvalue[0])
        if tempindex in [[], None]:
            defaultindex = []
        else:
            defaultindex = tempindex[0] if isinstance(tempindex[0], list) else tempindex
        # 当前表的列序号list
        currentcolumnsindex = [x for x in range(len(currentcolumnsname))]
        # 当前选择的列名list
        # 需要避免选择的列序号不在表格现有列中造成执行错误
        illegallist = []
        for item in defaultindex:
            if item >= len(currentcolumnsname):
                Sg.popup_quick_message("当前选择列{}在表格中尚未生成！".format(item),
                                       modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
                illegallist.append(item)
        for item in illegallist:
            defaultindex.remove(item)
        defaultcolumnname = [currentcolumnsname[x] for x in defaultindex]
        templayout = [[
            Sg.Col([[
                Sg.Frame("列选择", [
                    [Sg.Button('全部选择', k=PARAM_SELECT_ALL),
                     Sg.Button('全部取消', k=PARAM_CLEAR_ALL)],
                    [Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, disabled=True,
                              pad=(5, 5), font=PARAM_FT, size=(32, 1), expand_x=True, border_width=2)],
                    [  # 使用两个并列的list同步显示列索引号和列名，方便选择
                        Sg.Frame("列序号", [[
                            Sg.Listbox(
                                currentcolumnsindex,
                                default_values=defaultindex,
                                k=PARAM_EDIT_COLUMNS_INDEX,
                                highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                highlight_text_color='white',
                                select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                enable_events=True,
                                # no_scrollbar=True,
                                pad=(0, 0), size=(5, 25), expand_x=True, expand_y=True),
                        ]], pad=(0, 0), border_width=0, expand_x=True, expand_y=True),
                        Sg.Frame("列名", [[
                            Sg.Listbox(
                                currentcolumnsname,
                                default_values=defaultcolumnname,
                                k=PARAM_EDIT_COLUMNS_NAME,
                                highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                highlight_text_color='white',
                                select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                enable_events=True,
                                # no_scrollbar=True,
                                pad=(0, 0), size=(25, 25), expand_x=True, expand_y=True),
                        ]], pad=(0, 0), border_width=0, expand_x=True, expand_y=True),
                    ]
                ], k=PARAM_EDIT_COLUMNS_FRAME, visible=True, border_width=1, expand_x=True, expand_y=True)],
            ], justification='center', expand_x=True, expand_y=True)
        ]]
        return templayout

    def columnnamelayout(layouttype: str = "") -> list:
        """
        表格列选择的param的layout
        并列放置 列序号，现有列名，新列名，仅新列名可以编辑
        :return:            list：layout
        """
        # 当前表号
        currentdfid = ast.literal_eval(currentdf)[0]
        # 当前表的列名list
        currentcolumnsname = currentdfcolumnlist[currentdfid]
        # 当前表的列序号list
        currentcolumnsindex = [x for x in range(len(currentcolumnsname))]
        # 当前设置的列名list
        setcolumnsname = ast.literal_eval(argvalue[0])
        # 如果当前没有预设列名，列名全部为空
        if len(setcolumnsname) == 0:
            # setcolumnsname = [x for x in range(len(currentcolumnsname))]
            setcolumnsname = currentcolumnsname

        # 序列旧名称和新名称的二维列表
        tablevalues = [[currentcolumnsname[x], setcolumnsname[x]] for x in currentcolumnsindex]
        # 显示的表格头
        namelayheading = [[
            Sg.T(s,
                 k=(PARAM_EDIT_COLUMNNAMES_HEADS, -1, i - 1),  # headings 加上了序号列，左上角从 （-1， -1）开始
                 justification='center',
                 enable_events=False,
                 font='黑体 10',
                 border_width=1,
                 background_color='dark blue',
                 text_color="white",
                 size=(18, 1),
                 pad=(1, 1)) for i, s in enumerate(['列序号', '现列名', '新列名'])
        ]]
        # 显示表格内容,key用元组（PARAM_EDIT_COLUMNNAMES，行, 列），只有第2列可以编辑，后续事件处理只需要判断key元组的[0],[2]即可
        namelaydata = [
            [Sg.T(r,
                  k=(PARAM_EDIT_COLUMNNAMES, r, -1),
                  size=(18, 1),
                  pad=(1, 1),
                  font='黑体 10',
                  enable_events=False,
                  justification='center',
                  background_color='dark blue',
                  text_color="white")] +
            [Sg.T(
                tablevalues[r][0],
                justification='right',
                # disabled=True,
                background_color='white',
                enable_events=False,
                text_color="black",
                font='黑体 10',
                k=(PARAM_EDIT_COLUMNNAMES, r, 0),
                size=(18, 1), pad=(1, 1))] +
            [Sg.Input(
                tablevalues[r][1],
                justification='right',
                # disabled=True,
                background_color='white',
                enable_events=True,
                text_color="blue",
                font='黑体 10',
                k=(PARAM_EDIT_COLUMNNAMES, r, 1),
                size=(18, 1), pad=(1, 1))] for r in range(len(tablevalues))
        ]

        templayout = [[
            Sg.Col([
                [Sg.Frame("所有新列名", [
                    [Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, disabled=True,
                              pad=(5, 5), font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2)],
                ], k=PARAM_EDIT_COLUMNS_FRAME, visible=True, border_width=1)],
                [Sg.Frame("设置新列名", [[Sg.Col(
                    [[Sg.Frame("", namelayheading + namelaydata, pad=(0, 0), expand_x=True, expand_y=True)]],
                    visible=True,
                    vertical_alignment='top',
                    pad=(0, 0),
                    justification='center',
                    element_justification='center',
                    scrollable=True,
                    vertical_scroll_only=True,
                    expand_x=True, expand_y=True,
                )]], pad=(0, 0), border_width=1, expand_x=True, expand_y=True, size=(430, 450))]
            ], element_justification='center', justification='center', expand_x=True, expand_y=True)
        ]]
        return templayout

    def rowvaluelayout(layouttype: str = "columns") -> list:
        """
        表格行新增、修改时调用的编辑页面
        :return:  list layout
        """
        # 当前表号
        currentdfid = ast.literal_eval(currentdf)[0]
        # 当前表的列名list
        currentcolumnsname = currentdfcolumnlist[currentdfid]
        # 当前表的列序号list
        currentcolumnsindex = [x for x in range(len(currentcolumnsname))]
        # 当前设置的新行值
        currentrowcontent = ast.literal_eval(argvalue[0])
        # 如果当前没有预设列名，列名全部为空
        if currentrowcontent is None:
            currentrowcontent = [None for _ in range(len(currentcolumnsname))]
        else:
            if len(currentrowcontent) == 0:
                currentrowcontent = [None for _ in range(len(currentcolumnsname))]

        tablevalues = [[currentcolumnsname[x], currentrowcontent[x]] for x in currentcolumnsindex]
        # 显示的表格头
        namelayheading = [[
            Sg.T(s,
                 k=(PARAM_EDIT_COLUMNNAMES_HEADS, -1, i - 1),  # headings 加上了序号列，左上角从 （-1， -1）开始
                 justification='center',
                 enable_events=False,
                 font='黑体 10',
                 border_width=1,
                 background_color='dark blue',
                 text_color="white",
                 size=(18, 1),
                 pad=(1, 1)) for i, s in enumerate(['列序号', '列名', '修改值'])
        ]]
        # 显示表格内容,key用元组（PARAM_EDIT_COLUMNNAMES，行, 列），只有第2列可以编辑，后续事件处理只需要判断key元组的[0],[2]即可
        namelaydata = [
            [Sg.T(r,
                  k=(PARAM_EDIT_COLUMNNAMES, r, -1),
                  size=(18, 1),
                  pad=(1, 1),
                  font='黑体 10',
                  enable_events=False,
                  justification='center',
                  background_color='dark blue',
                  text_color="white")] +
            [Sg.T(
                tablevalues[r][0],
                justification='right',
                # disabled=True,
                background_color='white',
                enable_events=False,
                text_color="black",
                font='黑体 10',
                k=(PARAM_EDIT_COLUMNNAMES, r, 0),
                size=(18, 1), pad=(1, 1))] +
            [Sg.Input(
                tablevalues[r][1],
                justification='right',
                # disabled=True,
                background_color='white',
                enable_events=True,
                text_color="blue",
                font='黑体 10',
                k=(PARAM_EDIT_COLUMNNAMES, r, 1),
                size=(18, 1), pad=(1, 1))] for r in range(len(tablevalues))
        ]

        templayout = [[
            Sg.Col([
                [Sg.Frame("行新值", [
                    [Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, disabled=True,
                              pad=(5, 5), font=PARAM_FT, size=(60, 1), expand_x=True, border_width=2)],
                ], k=PARAM_EDIT_COLUMNS_FRAME, visible=True, border_width=1)],
                [Sg.Frame("行新值", [[Sg.Col(
                    [[Sg.Frame("", namelayheading + namelaydata, pad=(0, 0), expand_x=True, expand_y=True)]],
                    visible=True,
                    vertical_alignment='top',
                    pad=(0, 0),
                    justification='center',
                    element_justification='center',
                    scrollable=True,
                    vertical_scroll_only=True,
                    expand_x=True, expand_y=True,
                )]], pad=(0, 0), border_width=1, expand_x=True, expand_y=True, size=(430, 450))]
            ], element_justification='center', justification='center', expand_x=True, expand_y=True)
        ]]
        return templayout

    def rowslayout(layouttype: str = "columns") -> list:
        """
        行序号选择param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                         font=PARAM_FT, size=(20, 1), border_width=2)
            ]], justification='center')
        ]]

    def combolayout(layouttype: str = "columns") -> list:
        """
        多合法值选择的param的layout
        :return:            list：layout
        """
        return [[
            Sg.Col([[
                Sg.InputCombo(paramvalidvalue, k=PARAM_EDIT_RESULT, pad=(5, 5),
                              font=PARAM_FT, size=(20, 1), default_value=argvalue, readonly=True)
            ]], justification='center')
        ]]

    def querylistlayout(layouttype: str = "columns") -> list:
        """
        用于数据条件筛选的参数编辑
        :return:            list：layout
        """
        # 当前表号
        currentdfid = ast.literal_eval(currentdf)[0]
        if currentdfid >= len(currentdfcolumnlist):
            #  表格未生成时，使用普通输入
            print("目前表格数：{}表格：{}尚未生成！".format(currentdfid, len(currentdfcolumnlist)))
            return debuglayout()
        # 当前表的列名list
        currentcolumnsname = currentdfcolumnlist[currentdfid]
        # 当前选择的筛选命令
        currentcommand = ast.literal_eval(argvalue[0])
        # 编辑用的表格相关信息
        parserscaleleft = [" ", "["]
        parserscaleright = [" ", "]"]
        comparemarklist = dfquerycomparemark + list(dfqueryspecialmarkdict)
        columninfodic = {
            '层级(左）': 0,
            '列名称': 1,
            '筛选方式': 2,
            '比较值': 3,
            '比较列': 4,
            '层级(右）': 5,
            '条件组合': 6,
        }
        headings = list(columninfodic)
        # Special'Table标签前缀
        querytablekey = PARAM_EDIT_QUERY_TABLE
        tempfuncargs = {}

        # Special'Table字段的取值范围
        colvaluesecale = [
            parserscaleleft,  # 筛选层级
            [""] + currentcolumnsname,  # 列名称
            [""] + comparemarklist,  # 筛选方式
            None,  # 比较值
            [""] + currentcolumnsname,  # 列名称
            parserscaleright,  # 筛选层级
            [""] + dfqueryconnectmark,  # 多条件组合
        ]
        # Special'Table字段的显示宽度
        column_widths = [8, 16, 16, 16, 16, 8, 8]
        # Special'Table字段的显示map
        visible_column_map = [True, True, True, True, True, True, True]
        column_cell_edit_type_map = [
            SPECIAL_TABLE_CELL_COMBOX,
            SPECIAL_TABLE_CELL_COMBOX,
            SPECIAL_TABLE_CELL_COMBOX,
            SPECIAL_TABLE_CELL_INPUT,
            SPECIAL_TABLE_CELL_COMBOX,
            SPECIAL_TABLE_CELL_COMBOX,
            SPECIAL_TABLE_CELL_COMBOX
        ]
        # 转换数据
        if len(currentcommand) == 0:
            commanddf = pd.DataFrame([['[', "b", "isin", "['未知1']", "", ']', ""]])
        else:
            # 需要递归方式生成数据表，包括[]
            tempresultdictlist = []
            querycommandlist2dflist(currentcommand, resultdictlist=tempresultdictlist)
            commanddf = pd.DataFrame(tempresultdictlist)

        templayout = SpecialTable(
            tablekey=querytablekey,
            headings=headings,
            cell_editable=True,
            v_slider_resolution=0.1,
            h_slider_resolution=0.1,
            display_row_numbers=True,
            slider_every_row_column=True,
            text_color=TEXT_COLOR,
            text_background_color=TEXT_BACKGROUND_COLOR,
            combox_button_arrow_color='blue',
            combox_button_background_color='white',
            input_text_color=INPUT_TEXT_COLOR,
            input_text_background_color=INPUT_TEXT_BACKGROUND_COLOR,
            column_cell_edit_type_map=column_cell_edit_type_map,
            filter_visible=False,
            edit_button_visible=True,
            move_row_button_visible=True,
            v_slider_show=True,
            h_slider_show=False,
            dfshowdata=commanddf,
            tabledatadictlist=None,
            itemeditfunc=None,  # 编辑记录行时的钩子函数
            itemeditfuncargsdic=tempfuncargs,  # 编辑函数的参数列表
            indexcol=None,  # 记录可以重复
            font=('黑体', 10),
            pad=(0, 0),
            border_width=1,
            size=(PARAM_WINDOWS_WIDE_SIZE[0] - 20, PARAM_WINDOWS_WIDE_SIZE[1] - 140),
            cell_justification='c',
            max_rows=10,
            max_columns=len(visible_column_map),
            visible_column_map=visible_column_map,
            select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
            col_widths=column_widths,
            col_value_scale=colvaluesecale,
            vertical_scroll_only=False,
            relief=Sg.RELIEF_SUNKEN,
            disable_slider_number_display=True,
        ).layout

        totallayout = [
            [
                Sg.Col([[
                    Sg.Input(argvalue[0], k=PARAM_EDIT_RESULT, pad=(5, 5),
                             font=PARAM_FT, size=(20, 1), expand_x=True, border_width=2)
                ]], justification='center', expand_x=True)
            ],
            [
                templayout
            ]
        ]
        return totallayout

    def intlayout(layouttype: str = "columns") -> list:
        """
        int 型param的layout
        :return:            list：layout
        """
        return []

    def floatlayout(layouttype: str = "columns") -> list:
        """
        float 型param的layout
        :return:            list：layout
        """
        return []

    def positionlayout(layouttype: str = "columns") -> list:
        """
        生成新表格的序号param的layout
        :return:            list：layout
        """
        return []

    paramtypedict = {
        'str': [stringlayout, PARAM_WINDOWS_NORMAL_SIZE],
        'ipaddress': [ipaddresslayout, PARAM_WINDOWS_NORMAL_SIZE],
        'password': [passwordlayout, PARAM_WINDOWS_NORMAL_SIZE],
        'sqlstr': [sqlstrlayout, PARAM_WINDOWS_MIDDLE_SIZE],
        'object': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'strcombo': [stringcombolayout, PARAM_WINDOWS_NORMAL_SIZE],
        'columns': [columnslayout, PARAM_WINDOWS_LONG_SIZE],
        'sourcecolumns': [columnslayout, PARAM_WINDOWS_LONG_SIZE],
        'targetcolumns': [columnslayout, PARAM_WINDOWS_LONG_SIZE],
        'rowvaluelist': [rowvaluelayout, PARAM_WINDOWS_LONG_SIZE],
        'columnname': [columnnamelayout, PARAM_WINDOWS_LONG_SIZE],
        'rows': [rowslayout, PARAM_WINDOWS_NORMAL_SIZE],
        'position': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'list': [debuglayout, PARAM_WINDOWS_LONG_SIZE],
        'bool': [combolayout, PARAM_WINDOWS_NORMAL_SIZE],
        'int': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'intcombo': [combolayout, PARAM_WINDOWS_NORMAL_SIZE],
        'float': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'combo': [combolayout, PARAM_WINDOWS_NORMAL_SIZE],
        'dict': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'newtable': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'example': [debuglayout, PARAM_WINDOWS_NORMAL_SIZE],
        'querylist': [querylistlayout, PARAM_WINDOWS_WIDE_SIZE],
        'savefile': [savefilelayout, PARAM_WINDOWS_NORMAL_SIZE],
        'readfile': [readfilelayout, PARAM_WINDOWS_NORMAL_SIZE],
    }

    paramtaillayout = [
        [Sg.Col([[
            Sg.Frame("",
                     [[Sg.Button('确 定', k=PARAM_EDIT_OK),
                       Sg.Button('取 消', k=PARAM_EDIT_CANCEL)]],
                     vertical_alignment='top', element_justification='center', expand_x=True, border_width=0)
        ]], justification='center', expand_x=True)]]

    # 组合当前param 编辑页面
    currentlayout = paraminfolayout + paramtypedict[paramtype][0](paramtype) + paramtaillayout

    # 开启paramwindows
    paramwindow = Sg.Window(
        '操作选项编辑',
        currentlayout,
        font=DEF_FT_L,
        icon=LOCAL_SYSTEM_ICON,
        use_ttk_buttons=True,
        return_keyboard_events=True,  # 把mouse事件暂时由主窗口屏蔽
        resizable=True,
        size=paramtypedict[paramtype][1],
        modal=True,
        # element_justification='center',
        keep_on_top=False,
        finalize=True
    )

    def parameditcolumns():
        """
        处理PARAM_EDIT_COLUMNS_NAME|PARAM_EDIT_COLUMNS_NAME，同步显示列名、列序号、选择的列清单
        :return:
        """
        currentchoosed = paramwindow[event].get_indexes()
        # 交互刷新PARAM_EDIT_COLUMNS_NAME, PARAM_EDIT_COLUMNS_INDEX
        if event == PARAM_EDIT_COLUMNS_NAME:
            # 刷新PARAM_EDIT_COLUMNS_INDEX
            paramwindow[PARAM_EDIT_COLUMNS_INDEX].update(set_to_index=currentchoosed)
        else:
            # 刷新 PARAM_EDIT_COLUMNS_NAME
            paramwindow[PARAM_EDIT_COLUMNS_NAME].update(set_to_index=currentchoosed)
        paramwindow[PARAM_EDIT_RESULT].update(
            value=str([paramwindow[PARAM_EDIT_COLUMNS_INDEX].get(), paramwindow[PARAM_EDIT_COLUMNS_NAME].get()]))

    def parameditok() -> list:
        """
        处理点击OK 按钮
        :return:                list： [True 获取返回结果成功并准备关闭窗口, dict] | [False：获取返回结果失败，继续留在窗口, {}]
        """
        # 检查结果的语法合法性
        # 首先判断是否要做str到类型的转换，如果要做，先做转换
        if paramtypetransmap[paramtype][PARAM_TYPE_TRANS_FLAG]:
            try:
                if paramtype == 'ipaddress':
                    tempresult = values[PARAM_EDIT_RESULT]
                elif paramtype == 'password':
                    tempresult = dftrans_simple_encrypt(values[PARAM_EDIT_RESULT])
                    tempresult1 = dftrans_simple_encrypt(values[PARAM_EDIT_RESULT_CONFIRM])
                    if tempresult != tempresult1:
                        Sg.popup_error("输入密码不一致！", modal=True, keep_on_top=True)
                        return [False, {}]
                else:
                    tempresult = ast.literal_eval(str(values[PARAM_EDIT_RESULT]))
            except Exception as err:
                errstr = "{}命令{}参数{}转换错误：{}".format(currentcommand, argparam[0], argvalue[0], err)
                if debugflag:
                    print(errstr)
                Sg.popup_error(errstr,
                               modal=True, keep_on_top=True)
                return [False, {}]

            # 转换之后，检查转换结果是否合法
            if paramtype == 'ipaddress':  # ipaddress对应的是检查函数， 其他检查类型
                if paramtypetransmap[paramtype][PARAM_TYPE_VALID](tempresult) is False:
                    if debugflag:
                        print("{}命令{}参数{}不是IP地址格式".format(currentcommand, argparam[0], argvalue[0]))
                    Sg.popup_error("{}命令{}参数{}不是IP地址格式".format(currentcommand, argparam[0], argvalue[0]),
                                   modal=True, keep_on_top=True)
                    return [False, {}]
            elif isinstance(tempresult, (paramtypetransmap[paramtype][PARAM_TYPE_VALID], type(None))) is False:
                if debugflag:
                    print("{}命令{}参数{}类型{}错误：{}".format(
                        currentcommand, argparam[0], argvalue[0],
                        paramtypetransmap[paramtype][PARAM_TYPE_VALID], type(tempresult)))
                Sg.popup_error("{}命令{}参数{}类型{}错误：{}".format(
                    currentcommand, argparam[0], argvalue[0],
                    paramtypetransmap[paramtype][PARAM_TYPE_VALID], type(tempresult)),
                    modal=True, keep_on_top=True)
                return [False, {}]
        else:
            # 不做格式检查，结果直接获取
            tempresult = values[PARAM_EDIT_RESULT]
        # 根据配置界面组合paramcontent
        paramresult = {
            argparam[0]: str(tempresult)
        }
        return [True, paramresult]

    def tupleeventprocess():
        """
        对于元组类事件的处理
        :return:
        """
        if [event[0], event[2]] == [PARAM_EDIT_COLUMNNAMES, 1]:  # 对应于PARAM_EDIT_COLUMNNAMES 新列名的事件
            # 获取当前编辑表的列数
            # 当前表号
            currentdfid = ast.literal_eval(currentdf)[0]
            # 当前表的列名list
            currentcolumnsname = currentdfcolumnlist[currentdfid]
            # 有编辑事件，重新拼接新列名
            namelist = [values[(event[0], x, event[2])] for x in range(len(currentcolumnsname))]
            # 更新当前result
            paramwindow[PARAM_EDIT_RESULT].update(value=str(namelist))

    def paramsavefilename():
        """
        处理更改输出文件名事件 PARAM_SAVE_FILENAME
        :return:
        """
        tempdir = os.path.dirname(argvalue[0])
        tempname = os.path.basename(argvalue[0])
        filetemp = Sg.popup_get_file('选择文件',
                                     save_as=True,
                                     file_types=(('Excel文件', '*.xlsx'), ('CSV文件', '*.csv'), ('文本文件', '*.txt')),
                                     initial_folder=tempdir,
                                     default_path=argvalue[0],
                                     history_setting_filename=tempname,
                                     keep_on_top=True, modal=True,
                                     no_window=True, icon=LOCAL_SYSTEM_ICON)
        if filetemp:
            # 通过index修改页面中对应的文件名输入框中的值
            paramwindow[PARAM_EDIT_RESULT].update(value=filetemp)

    def paramreadfilename():
        """
        处理更改输出文件名事件 PARAM_READ_FILENAME
        :return:
        """
        tempdir = os.path.dirname(argvalue[0])
        tempname = os.path.basename(argvalue[0])
        filetemp = Sg.popup_get_file('选择文件',
                                     save_as=False,
                                     file_types=(('Excel文件', '*.xlsx'),
                                                 ('CSV文件', '*.csv'),
                                                 ('文本文件', '*.txt'),
                                                 ('jsonl文件', '*.jsonl')
                                                 ),
                                     initial_folder=tempdir,
                                     default_path=argvalue[0],
                                     history_setting_filename=tempname,
                                     keep_on_top=True, modal=True,
                                     no_window=True, icon=LOCAL_SYSTEM_ICON)
        if filetemp:
            # 通过index修改页面中对应的文件名输入框中的值
            paramwindow[PARAM_EDIT_RESULT].update(value=filetemp)

    def paramselectall():
        # 获取所有的列序号
        listindex = paramwindow[PARAM_EDIT_COLUMNS_INDEX].get_list_values()
        # 选择所有的列序号和列名字
        paramwindow[PARAM_EDIT_COLUMNS_INDEX].update(set_to_index=listindex)
        paramwindow[PARAM_EDIT_COLUMNS_NAME].update(set_to_index=listindex)
        # 更新参数
        paramwindow[PARAM_EDIT_RESULT].update(value=str([
            list(paramwindow[PARAM_EDIT_COLUMNS_INDEX].get_list_values()),
            list(paramwindow[PARAM_EDIT_COLUMNS_NAME].get_list_values())])
        )
        return

    def paramclearall():
        # 选择所有的列序号和列名字
        paramwindow[PARAM_EDIT_COLUMNS_INDEX].update(set_to_index=[])
        paramwindow[PARAM_EDIT_COLUMNS_NAME].update(set_to_index=[])
        # 更新参数
        paramwindow[PARAM_EDIT_RESULT].update(value=str([[], []]))
        return


    def paramconditionquery():
        paramwindow[event[0]].update(
            commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
            currentevent=event, currentwindow=paramwindow, currentvalues=values)

        # 获取当前的筛选条件list并填写到PARAM_EDIT_RESULT
        tempdictlist = paramwindow[event[0]].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
        print("tempdict:{}".format(tempdictlist))
        # 拼接筛选list
        tempresult = []
        tempmarkstack = []
        # 初始化括号检测的弹出项
        popelement = True
        for rownumber, tempitem in enumerate(tempdictlist):
            # 如果仅仅只有[ 或者 ], 本次只是层级括号，没有实际筛选条件
            currentlist = [x.strip() if isinstance(x, str) else x for x in tempitem.values()]
            print(currentlist)
            if currentlist == ["", "", "", "", "", "", ""]:
                # 跳过空行
                continue
            if currentlist == ["[", "", "", "", "", "", ""]:
                # 左[, 将行号压栈
                tempmarkstack.append(rownumber)
                tempresult.append(LEFT_MARK_FLAG)
                continue  # 暂时不处理
            elif currentlist == ["", "", "", "", "", "]", ""]:
                # 右], 处理对应[之间包含的内容，逐项弹出直到找到LEFTMARKFLAG, 然后将所有弹出的元素组成单一list调转顺序重新压入
                poplist = []
                popelement = tempresult.pop() if len(tempresult) > 0 else None
                while popelement not in [LEFT_MARK_FLAG, None]:
                    # 将有效的弹出项压入临时list
                    poplist.append(popelement)
                    popelement = tempresult.pop() if len(tempresult) > 0 else None
                # 如果popelemnt 是None, 说明没有找到对应的左括号，失败
                if popelement is None:
                    break
                # 将poplist跳转顺序（因为最后的最先弹出）
                tempresult.append(poplist[::-1])
                # 弹出当前对应的左[行号
                tempmarkstack.pop() if len(tempmarkstack) > 0 else None
                continue
            temp1 = [DF_QUERY_FLAG_STRING]
            # 去掉本行字典记录中的[, ]或者最左、左右的无用数据,先弹出最后一个，再弹出最开始，避免顺序
            tempitem.pop(list(tempitem)[5])  # 需要使用字典的key值pop
            tempitem.pop(list(tempitem)[0])

            for key, value in tempitem.items():
                temp1.append(value)
            # temp1[1] 列名，temp1[2] 筛选方式， temp1[3] 比较值， temp1[4] 比较列， temp1[5] 组合条件
            # 检查“比较值’存在而且操作表格也存在（需要列类型）和选择的列类型对应关系，并做转换
            # 需要获取命令对应的表号，并判断是否存在 TODO 目前仅对int，float, isin做转换，
            if temp1[2] in QUERY_FILTER_NEED_TO_STR_EVAL:  # isin 对应的通常是list，需要转换
                try:
                    temp1[3] = ast.literal_eval(temp1[3])
                except Exception as err:
                    print("{} ast.literal_eval err:{}".format(temp1[3], err))
                    pass
            elif isinstance(temp1[1], str) and temp1[3] != "":  # 列名、比较值有内容时
                targetdfid = ast.literal_eval(currentdf)[0]  # 获取当前表号
                if temp1[1].strip() != "" and temp1[1] in specialdflist[targetdfid].dfdata.columns:
                    temptype = str(specialdflist[targetdfid].dfdata[temp1[1]].dtypes)  # 获取当前字段类型
                    # 确定是否使用eval
                    if "int" in temptype or "float" in temptype:
                        try:
                            temp1[3] = ast.literal_eval(temp1[3])
                        except Exception as err:
                            print("{} ast.literal_eval err:{}".format(temp1[3], err))
                            pass

            tempresult.append(temp1)

        # 如果堆栈中依然后残留的左括号，说明括号数量不匹配，
        if len(tempmarkstack) != 0 or popelement is None:
            if debugflag:
                print("命令括号不匹配，剩余行号{}无法找到对应括号".format(tempmarkstack))
            paramwindow[PARAM_EDIT_RESULT].metadata = \
                [False, "命令括号不匹配，剩余行号{}无法找到对应括号".format(tempmarkstack)]
            # Sg.popup_error(("命令括号不匹配，剩余行号{}无法找到对应括号".format(tempmarkstack)), modal=True, keep_on_top=True)
        else:
            # 数据正确，填写到PARAM_EDIT_RESULT
            paramwindow[PARAM_EDIT_RESULT].update(value=str(tempresult))
            paramwindow[PARAM_EDIT_RESULT].metadata = [True, ""]
        # 数据正确，填写到PARAM_EDIT_RESULT
        # paramwindow[PARAM_EDIT_RESULT].update(value=str(tempresult))

    # 本窗口事件处理字典
    paramediteventprocessdict = {
        PARAM_EDIT_COLUMNS_NAME: parameditcolumns,
        PARAM_EDIT_COLUMNS_INDEX: parameditcolumns,
        PARAM_SAVE_FILENAME: paramsavefilename,
        PARAM_READ_FILENAME: paramreadfilename,
        PARAM_SELECT_ALL: paramselectall,
        PARAM_CLEAR_ALL: paramclearall,
        PARAM_EDIT_OK: parameditok,
        # PARAM_EDIT_CANCEL:
    }
    paramcontent = {}
    # 使用PARAM_EDIT_RESULT的meta记录数据格式的正确性标记
    paramwindow[PARAM_EDIT_RESULT].metadata = [True, ""]

    # 如果时数条件筛选窗口，因为使用了SpecialTable， 需要单独绑定mouse
    # 确认table是否存在，如果存在就bind mouse
    # TODO: 暂时不处理mouse，因为需要判读表格和非表格的元组事件，目前判断条件不充分
    # # paramwindow也将mouse事件屏蔽掉： return_keyboard_events=True
    # if not isinstance(paramwindow.find_element(PARAM_EDIT_QUERY_TABLE, silent_on_error=True), Sg.ErrorElement):
    #     paramwindow[PARAM_EDIT_QUERY_TABLE].update(commandtype=SPECIAL_TABLE_SET_BIND, currentwindow=paramwindow)

    # 处理循环
    while True:
        event, values = paramwindow.read()
        if debugflag:
            print("paramwindow event:{}".format(event))
        # --- Process buttons --- #
        if isinstance(event, tuple):
            # 判断是哪个页面产生的元组事件
            # 如果是条件查询表格，处理条件查询表格事件
            if event[0] == PARAM_EDIT_QUERY_TABLE:
                paramconditionquery()
                continue
            # 其他的layout产生的元组事件
            # 事件是元组类型，来自于非SpecialTable的表格处理
            tupleeventprocess()
            continue

        if event in (Sg.WIN_CLOSED, '_close_'):
            paramcontent = {}
            break

        elif event == PARAM_EDIT_OK:
            returnflag, paramcontent = paramediteventprocessdict[event]()
            if returnflag:
                # 返回成功，关闭窗口
                if paramwindow[PARAM_EDIT_RESULT].metadata[0] is True:
                    break
                else:
                    Sg.popup_error(paramwindow[PARAM_EDIT_RESULT].metadata[1], modal=True, keep_on_top=True)
                    continue
            else:
                # 返回失败，留在窗口
                continue

        elif event == PARAM_EDIT_CANCEL:
            paramcontent = {}
            break

        # 先处理普通返回的元组事件
        elif event in (PARAM_EDIT_COLUMNS_NAME, PARAM_EDIT_COLUMNS_INDEX, PARAM_SAVE_FILENAME, PARAM_READ_FILENAME,
                       PARAM_SELECT_ALL, PARAM_CLEAR_ALL):
            paramediteventprocessdict[event]()
            continue

        else:
            # print("paramwindow unknown event:{}".format(event))
            continue

    paramwindow.close()
    # 返回结果字典
    return paramcontent


def commandinfofill(currentwindow, currentcommandlist):
    """
    根据commandlist填写所有命令配置页的关联elements
    :param currentwindow:                   当前窗口
    :param currentcommandlist:              命令structure
    :return:
    """
    # 如果是导入数据命令，忽略当前选择的表格
    # chooseddf = currentcommandlist[CURRENT_OPERATE_DFS]
    chooseddf = currentcommandlist[CURRENT_OPERATE_DFS] \
        if commanddict[currentcommandlist[CURRENT_COMMAND]][COMMAND_TYPE] != COMMAND_NEW_TABLE_IMPORT else []

    # 对多表选择把已选表都填入
    currentwindow[DF_MULTI_CHOOSE].set_value(chooseddf)
    # 初始化选择的表格结果
    currentwindow[DF_CHOOSE_RESULT].update(value=str(chooseddf))
    # 填写命令选项的当前赋值替代默认值
    # 刷新argvvalue的当前值
    argvdict = currentcommandlist[CURRENT_COMMAND_PARAMS + 1]
    # 获取argv的默认list
    argvlist = currentwindow[ARGV_CONFIG].get_list_values()
    # 获取argvvalue的默认list
    argvvaluelist = currentwindow[ARGV_CONFIG_VALUE].get_list_values()
    # 对于所有argvvalue的当前值，根据对应的argv填写到list相应的位置
    for key, value in argvdict.items():
        argvvaluelist[argvlist.index(key)] = str(value)
    # 获取argv选中项
    argcurrentindex = currentwindow[ARGV_CONFIG].get_indexes()
    # 回写当前值的list到listbox及当前选中项
    currentwindow[ARGV_CONFIG_VALUE].update(values=argvvaluelist, set_to_index=argcurrentindex)

    # 获取argc_value的选中项
    argcurentindex = currentwindow[ARGC_CONFIG].get_indexes()
    # 刷新argcvalue的当前值及当前选中项
    argclist = currentcommandlist[CURRENT_COMMAND_PARAMS + 2:]
    # 刷新argcvalue的选中项
    currentwindow[ARGC_CONFIG_VALUE].update(values=[str(x) for x in argclist], set_to_index=argcurentindex)

    # 刷新命令语句和命令语义
    currentwindow[COMMAND_STRUCTURE].update(value=str(currentcommandlist))
    currentwindow[COMMAND_SENTENCE].update(value=command2sentence(currentcommandlist))


def commandgenerate(currentwindow, event, values) -> bool:
    """
    点击命令生成按钮后，根据命令行语法转译成命令说明语句并填写到对应的文件框
    :param currentwindow:                  当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:                        bool, True 成功，False：失败
    """
    try:
        commandstructure = ast.literal_eval(values[COMMAND_STRUCTURE])
    except Exception as err:
        if debugflag:
            print("{}命令生成错误：{}".format(values[COMMAND_STRUCTURE], err))
        Sg.popup_error("{}命令生成错误：{}".format(values[COMMAND_STRUCTURE], err), modal=True, keep_on_top=True)
        return False

    # # 更新命令配置页信息
    commandinfofill(currentwindow, commandstructure)

    sentence = command2sentence(commandstructure)
    if sentence != "":
        currentwindow[COMMAND_SENTENCE].update(value=sentence)
        return True
    else:
        Sg.popup_error("命令转换：{} 失败！".format(values[COMMAND_STRUCTURE]), modal=True, keep_on_top=True)
        return False


def commandshowrefresh(currentwindow, event, values):
    """
    命令相关配置改变后，刷新页面的相关elements
    :param currentwindow:                  当前windows
    :param event:                   事件
    :param values:                  当前windows的values
    :return:
    """
    # 获取argc信息
    argcnamelist = [x for x in currentwindow[ARGC_CONFIG].get_list_values()]
    argclist = [x for x in currentwindow[ARGC_CONFIG_VALUE].get_list_values()]
    currentcommand = currentwindow[COMMAND_LIST].get()
    # 由于参数在界面编辑时使用str()进行了转换，拼接structure时需要反向eval，但是原str类型不能eval
    # 对argc逐项获取paramtype并确定是否执行eval
    try:
        for i, argcname in enumerate(argcnamelist):
            # 获取该param的对应条目
            # ['type', FUCNTION_ARG_VALIDVALUE, FUNCTION_ARG_DEFAULTVALUE, FUNCTION_ARG_COMMENT, FUNCTION_ARG_LONG_COMMENT]
            resultlist = argparaminfoget(currentcommand, ARGC_PARAM_EDIT, argcname)
            if resultlist is []:
                return
            if paramtypetransmap.get(resultlist[0])[PARAM_TYPE_TRANS_FLAG] and \
                    resultlist[0] not in ['ipaddress', 'password']:
                argclist[i] = ast.literal_eval(argclist[i])
    except Exception as err:
        if debugflag:
            print("{}命令参数转换错误：{}".format(currentcommand, err))
        Sg.popup_error("{}命令参数转换错误：{}".format(currentcommand, err),
                       modal=True, keep_on_top=True)
        return

    # 获取argv信息
    argvdict = dict(zip(currentwindow[ARGV_CONFIG].get_list_values(),
                        currentwindow[ARGV_CONFIG_VALUE].get_list_values()))
    # 对argv逐项获取类型并确定是否使用eval
    try:
        for key, value in argvdict.items():
            # 获取该param的对应条目
            # ['type', FUCNTION_ARG_VALIDVALUE, FUNCTION_ARG_DEFAULTVALUE, FUNCTION_ARG_COMMENT, FUNCTION_ARG_LONG_COMMENT]
            resultlist = argparaminfoget(currentcommand, ARGV_PARAM_EDIT, key)
            if resultlist is []:
                return
            if paramtypetransmap.get(resultlist[0])[PARAM_TYPE_TRANS_FLAG] and \
                    resultlist[0] not in ['ipaddress', 'password']:
                argvdict[key] = ast.literal_eval(value)
    except Exception as err:
        if debugflag:
            print("{}命令参数转换错误：{}".format(currentcommand, err))
        Sg.popup_error("{}命令参数转换错误：{}".format(currentcommand, err),
                       modal=True, keep_on_top=True)
        return

    commandstructure = [values[COMMAND_LIST], currentwindow[DF_MULTI_CHOOSE].get(), argvdict] + argclist
    # 更新命令sentence
    currentwindow[COMMAND_SENTENCE].update(value=command2sentence(commandstructure))
    currentwindow[COMMAND_STRUCTURE].update(value=str(commandstructure))


# 事件对应的处理函数字典
editwindowprocess = {
    COMMAND_LIST: commandchoosed,
    DF_MULTI_CHOOSE: dfmultichoosed,
    ARGC_CONFIG: argchoosed,
    ARGC_CONFIG_VALUE: argchoosed,
    ARGC_CONFIG_COMMENT: argchoosed,
    ARGV_CONFIG: argchoosed,
    ARGV_CONFIG_VALUE: argchoosed,
    ARGV_CONFIG_COMMENT: argchoosed,
    COMMAND_GENERATE: commandgenerate,
    ARGC_PARAM_EDIT: argparamedit,
    ARGV_PARAM_EDIT: argparamedit,
}

subeditporcess: {
    DF1_CHOOSE: df1_2choosed,
    DF1_COLUMN_CHOOSE: eventnull,
    DF1_ROWS_INPUT: eventnull,
    DF2_CHOOSE: df1_2choosed,
    DF2_COLUMN_CHOOSE: eventnull,
    DF2_ROWS_INPUT: eventnull,
}


def checkcommandcolumnvalid(commandid, command, commandconfig, inputcheckallyes: bool = False) -> list:
    """
    检查当前命令串涉及的列
    1、是否仅仅有列序号的旧格式
    2、列序号和列名是否和当前表格信息相符
    否则提醒用户是否替换相关数据，如果替换，返回[True, 新的命令】， 否则返回[False， “”]
    :param commandid                    当前命令的序号
    :param command:                     当前命令list
    :param commandconfig:               当前命令对应的命令配置
    :param inputcheckallyes:            bool, True，自动处理不提示，False：提示等待用户选择
    :return:                            list [True(更改）|False（不更改），
                                              command（True有效）|”“（Fales有效）|errstr（False有效),
                                              True(后续自动处理）|False（后续人工处理）]
    """
    checkallyes = inputcheckallyes
    global originfunctiondict
    print("第{}条命令列参数检查：{}".format(commandid, command))
    # 1、确认当前命令所有参数中是否有columns, startcolunms, targetcolumns,如果没有直接返回[False,""]
    # 1.1、获取当前命令对应函数的配置
    commandfunctionconfig = originfunctiondict.get(commandconfig[COMMAND_FUNCTION_NAME], None)
    if commandfunctionconfig is None:
        return [False, "", ""]
    argtempdict = {}
    # 1.2、检查所有的argc, 记录有columns的argc名,偏移量及属性
    for item, argcparam in enumerate(commandfunctionconfig["argcitems"]):
        # 获取该argc的说明
        paramtype = commandfunctionconfig['argc'][argcparam]['type']
        if paramtype in ['columns', 'sourcecolumns', 'targetcolumns']:
            argtempdict[argcparam] = [paramtype, item]

    # 1.3、检查命令使用的argv， 记录有columns的argv名及属性
    for argvparam in commandconfig[COMMAND_FUNCTION_PARAM]:
        # 获取argv的说明
        paramtype = commandfunctionconfig['argv'][argvparam]['type']
        if paramtype in ['columns', 'sourcecolumns', 'targetcolumns']:
            argtempdict[argvparam] = [paramtype, -1]
    # dict "paramname":["paramtype", 偏移量，-1代表argv，否则argc]
    # 1.4、没有涉及columns的选项，直接返回
    if argtempdict == {}:
        return [False, "", ""]

    print("列参数相关项：\n{}".format(argtempdict))
    # 2、开始根据记录的argc和argv循环替换所有和columns相关的参数
    # 获取当前所有specialdflist列信息：当前specialdflist的名字列表，用于选择操作表
    # 2.1、当前所有specialdflist的column列表，用于选择操作列 .list(df) => df的column list
    currentdfcolumnlist = [list(x.dfdata) for x in specialdflist]
    changedflag = False

    def acceptwin(windowtitle, inputcheckallyes):
        mycheckallyes = inputcheckallyes
        thistimeyes, changedflag, oldchangeflag = False, False, False
        if mycheckallyes is False and guiflag:
            layout = [
                [Sg.Text(mentionstr, size=(80, 6))],
                [Sg.Button("  是  ", k="_ok_", focus=True),
                 Sg.Button("  否  ", k="_close_"),
                 Sg.Button("以下全是", k="_allyes_")]
            ]

            acceptwindow = Sg.Window(windowtitle, layout, icon=LOCAL_SYSTEM_ICON,
                                     font=DEF_FT_L, finalize=True, resizable=True, modal=True, keep_on_top=True)
            thistimeyes = False
            while True:
                event, values = acceptwindow.read()
                # --- Process buttons --- #
                if event in (Sg.WIN_CLOSED, '_close_'):
                    thistimeyes, mycheckallyes = False, False
                    break

                # 确定文件
                elif event in ('_ok_', '_allyes_'):
                    thistimeyes = True
                    # 如果选择了allyes，记录后准备回传
                    if event == '_allyes_':  # 后续是否自动修改剩余命令标记
                        mycheckallyes = True
                    break
                else:
                    continue
            # 点击close或者关闭，不修改任何值，返回
            acceptwindow.close()

        # 如果本次替换或者全部自动替换
        if mycheckallyes or thistimeyes:
            # 修改命令
            if argparamitem >= 0:
                command[CURRENT_COMMAND_PARAMS + 2 + argparamitem] = newparamvalue
            else:
                command[CURRENT_COMMAND_PARAMS + 1][argparam] = newparamvalue
            # 是否修改本命令标记
            changedflag = True
            print("第{}条命令{}\n参数{}的列信息{}替换为新值{}".format(
                commandid, command, argparam, currentparamvalue, newparamvalue))
            # 旧格式做了已修改标记
            oldchangeflag = True  # 仅在处理旧格式分析的时候有效，后续无作用
        return [changedflag, oldchangeflag, mycheckallyes]

    # 2.3、循环处理argtempdict
    try:
        for argparam, [argtype, argparamitem] in argtempdict.items():
            # 获取该param的实际值
            currentparamvalue = command[CURRENT_COMMAND_PARAMS + 2 + argparamitem] \
                if argparamitem >= 0 else command[CURRENT_COMMAND_PARAMS + 1][argparam]

            # 获取当前操作的表格号
            if argtype in ['columns', 'sourcecolumns']:  # 单表或者是源数据表列
                currenttable = command[CURRENT_COMMAND_PARAMS][0]
            else:  # 目标表列
                currenttable = command[CURRENT_COMMAND_PARAMS][-1]

            # 2.3.1、判断是否旧格式
            oldchangeflag = False
            if not isinstance(currentparamvalue[0], list):
                # 2.3.2、list中的元素不是list，说明时旧格式
                # 获取旧格式对应的新格式的list
                newparamvalue = [currentparamvalue, [currentdfcolumnlist[currenttable][x] for x in currentparamvalue]]
                mentionstr = "第{}条命令{}\n\n参数{}的列信息：{}为旧格式\n\n是否替换为新格式：{}".format(
                    commandid, command, argparam, currentparamvalue, newparamvalue)
                # 确认
                changedflag, oldchangeflag, checkallyes = acceptwin("格式替换确认", checkallyes)
            # 如果是旧值替换，此时刚刚替换成功，不需要再做列名判断
            if oldchangeflag:
                continue

            # 2.4.1、没有进行旧格式替换，进行列名列序号对应关系的对比
            newcolumnsnumberlist = [currentdfcolumnlist[currenttable].index(x) for x in currentparamvalue[1]]
            # 2.4.2、列名对应的新列序号和以前不一致
            if newcolumnsnumberlist != currentparamvalue[0]:
                newparamvalue = [newcolumnsnumberlist, currentparamvalue[1]]
                mentionstr = "第{}条命令{}\n\n参数{}对应的列序号和列名：{}与现有表格信息不符\n\n是否替换为新值：{}".format(
                    commandid, command, argparam, currentparamvalue, newparamvalue)
                # 3.2 确认
                changedflag, oldchangeflag, checkallyes = acceptwin("命令列替换确认", checkallyes)

    except Exception as err:
        print("第{}条命令{}列信息检查错误：{}".format(commandid, command, err))
        return [False, "第{}条命令{}列信息检查错误：{}".format(commandid, command, err), ""]

    if changedflag:
        return [True, command, checkallyes]
    else:
        return [False, "", ""]


COMMAND_PROCESS_BAR = '-COMMAND_PROCESS_TEXT-'
COMMAND_PROCESS_COMMENT = '-COMMAND_PROCESS_COMMENT_TEXT-'
TOTAL_PROCESS_BAR = '-TOTAL_PROCESS_TEXT-'
TOTAL_PROCESS_COMMENT = '-TOTAL_PROCESS_COMMENT_TEXT-'


def globalcommandrun(method: int = None, currentevent=None, currentwindow=None, currentvalues=None) -> bool:
    """
    运行命令
    :param method:             STEP_RUN：单步， TO_CURRENT_RUN: 运行到当前选中行，ALL_RUN：全速
    :param currentevent:
    :param currentwindow:
    :param currentvalues:
    :return:                   bool: True 运行完成， False： 运行失败
    """
    global guiflag, specialdflist, barwindow
    # 如果是运行到选中行，先判断是否有当前选中行
    if guiflag:
        currentrow = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_CURRENTROW)
        if method == TO_CURRENT_RUN:
            if currentrow is None:
                # 未选择需要执行到的命令行
                Sg.popup_ok("未选择需要执行到的命令行！", keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
                return False

        # 获取当前命令列表
        commanddictlist = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
        # 如果是运行到指定行并且指定行对应命令已经执行
        if method == TO_CURRENT_RUN and commanddictlist[currentrow][columninfodic["已执行"]] == '是':
            # 指定运行到的命令已经执行
            if guiflag:
                Sg.popup_ok("选择的命令行已经执行！", keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
            return False

        # 需要执行的命令列表
        processlist = []
        # 需要执行的命令涉及的表格集合
        processedtablelist = set()
        # 记录当前的表格数
        oldspecialdflistnumber = len(specialdflist)
        # 已经执行的命令条数
        commandfinished = 0
        for count, commandrow in enumerate(commanddictlist):
            # 只获取未执行的命令
            if commandrow[columninfodic['已执行']] == '否':
                # 将当前命令语句的字符串还原为list后加入list数组
                processlist.append(ast.literal_eval("{}".format(commandrow[columninfodic['命令语句']])))
                # 单步运行，只需要找到第一个未执行的命令
                if method == STEP_RUN:
                    break
                # 运行到指定行
                elif method == TO_CURRENT_RUN:
                    # 目前是指定运行到的命令行
                    if currentrow == count:
                        break
            else:
                # 当前命令是已执行过的，并且指定运行到的命令行, 在开始应判断并返回
                commandfinished += 1
        if len(processlist) == 0:
            # 命令已经全部执行
            if guiflag:
                Sg.popup_ok("命令已经全部执行完成！", keep_on_top=True, modal=True, icon=LOCAL_SYSTEM_ICON)
            else:
                print("命令已经全部执行完成！")
            return True
    else:  # nogui方式下，把所有命令全部执行
        # 需要执行的命令列表
        processlist = [x[0] for x in totalprocesslist]  # 过滤掉linecomment
        # 需要执行的命令涉及的表格集合
        processedtablelist = set()
        # 存储需要后处理的命令返回信息
        needchangetable = []
        # 已经执行的命令条数
        commandfinished = 0

    # 逐条执行命令
    successflag = True
    currentitem = 0

    if guiflag:
        # gui方式下，启动处理进度条初始窗口
        barlayout = [[Sg.Text('', size=(50, 1), relief='sunken',
                              text_color='blue', background_color='white',
                              k=COMMAND_PROCESS_BAR, metadata=0)],
                     [Sg.Text('', size=(50, 1), relief='sunken',
                              text_color='white',  # background_color='white',
                              k=COMMAND_PROCESS_COMMENT, metadata=0)],
                     [Sg.Text('', size=(50, 1), relief='sunken',
                              text_color='blue', background_color='white',
                              k=TOTAL_PROCESS_BAR, metadata=0)],
                     [Sg.Text('', size=(50, 1), relief='sunken',
                              text_color='white',  # background_color='white',
                              k=TOTAL_PROCESS_COMMENT, metadata=0)]
                     ]

        barwindow = Sg.Window('命令执行进度', barlayout,
                              keep_on_top=False,
                              modal=True,
                              finalize=True, icon=LOCAL_SYSTEM_ICON)
        bartext = barwindow[COMMAND_PROCESS_BAR]
        barcommentext = barwindow[COMMAND_PROCESS_COMMENT]
        totalbartext = barwindow[TOTAL_PROCESS_BAR]
        bartotalcommenttext = barwindow[TOTAL_PROCESS_COMMENT]
        bartotalcommenttext.update("开始执行第1条命令......")
        barwindow.refresh()
    # 当非GUI方式运行时而且设置了使用columnname，自动在执行时通过columnname置换columnid然后执行
    # GUI方式和非columnname方式，需要人工确认或者使用columnid 运行，有问题返回错误
    checkallyes = True if usecolumnnameforprocess and not guiflag else False
    # 记录命令中删除表格命令影响的最小表号
    dropedmintablenumber = MAX_TABLE_NUMBER + 1
    totalstarttime = datetime.now()
    for itemstart, command in enumerate(processlist):
        # processlist只记录的第一条未执行命令到当前执行结束的命令，实际命令序号item需要从起始位置算起
        currentitem = itemstart + commandfinished
        try:
            # 获取当前命令行的配置
            # currentcommandconfig = commanddict.get(command[CURRENT_COMMAND], None)
            currentcommandconfig = getcommandconfig(command[CURRENT_COMMAND])
            # 更新当前命令的进度条为0%
            if guiflag:
                bartext.update(Sg.SYMBOL_SQUARE * 0)
                barwindow.refresh()
            if currentcommandconfig is None:
                print("命令组装：读取命令字典{}，key：{} 出错！".format(commanddict, command[CURRENT_COMMAND]))
            # 在gui模式下，1、检查当期命令是否包含列序号和列名不一致的情况 2、检查当前命令是否有旧格式只有列序号没有列名的参数，
            # 以上提醒用户确认是否自动更改
            # 根据不同配置进行不同操作
            result = checkcommandcolumnvalid(currentitem, command, currentcommandconfig, checkallyes)
            # resut [True|False, newcommand|""|False|, 是否全部选是]
            if result[0] is True:  # 表示需要更改现有命令串
                checkallyes = result[2]
                # 更改当前命令列表
                processlist[itemstart], command = result[1], result[1]
                # 更改当前命令
                command = result[1]
                # 更改当前显示窗口中的该条命令解释
                if guiflag:
                    commandrowcontent = ["否", command2sentence(command), str(command)]
                    mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_ROWVALUE,
                                                       currentwindow=mainwindow,
                                                       rownumber=currentitem,
                                                       newrowcontent=commandrowcontent)
                    # 命令启动前，小幅推进进度条
                    bartext.update(Sg.SYMBOL_SQUARE * 2)
                    barwindow.refresh()
            elif result[1] != "":  # 当前命令列检查错误，直接执行出错停止执行并提示
                if guiflag:
                    Sg.popup_error(result[1], modal=True, keep_on_top=True)
                successflag = False
                break

            # 形成当前命令涉及的df 的列表字符串  [0, 1, .......] --> '[specialdflist[0], specialdflist[1], ......]'
            # print("命令组装：currentcommandconfig:{}".format(currentcommandconfig))
            currentspecialdflist = \
                "[{0}]".format(
                    ", ".join(["{0}[{1}]".format(dfcurrentprefix, x) for x in command[CURRENT_OPERATE_DFS]]))
            # print("命令组装：currentspecialdflist:{}".format(currentspecialdflist))
            # print("当前处理的df的列表{0}".format(currentspecialdflist))
            # 组合当前命令代码串
            # {0}：函数名 {1}:dfprefix， {2}:当前处理df列表, {3}：当前处理df下标列表  {4}:字典参数：删除行的序号列表 {5}..其他位置参数
            # 'functionname', 'specialdflist', '[specialdflist[0], specialdflist[1], ...]', [0, 1, ...], {"a": x1, "b": x2...},...
            if currentcommandconfig[COMMAND_SEND_PROCCESSING_EVENT] == SEND_PROCESSING_EVENT_YES and guiflag:
                #  判断是否加入当前命令进度参数, 将字典参数添加processingbarevent关键字项，
                #  如果直接mainwindow作为字典项，会被解释为对象的地址，后续eval无法使用
                tempcommandparamlist = [command[CURRENT_COMMAND_PARAMS]] + \
                                       [dict(command[CURRENT_COMMAND_PARAMS + 1],
                                             **{"processingbarevent": ("barwindow_for_replace",
                                                                       COMMAND_PROCESS_BAR,
                                                                       COMMAND_PROCESS_COMMENT)})] + \
                                       command[CURRENT_COMMAND_PARAMS + 2:]
            else:
                tempcommandparamlist = command[CURRENT_COMMAND_PARAMS:]

            commandstr = currentcommandconfig[COMMAND_FORMAT].format(
                currentcommandconfig[COMMAND_FUNCTION_NAME],
                dfcurrentprefix,
                currentspecialdflist,
                *tempcommandparamlist)

            if currentcommandconfig[COMMAND_SEND_PROCCESSING_EVENT] == SEND_PROCESSING_EVENT_YES and guiflag:
                #  判断是否加入当前命令进度参数, 将字典参数在命令串中替换为真正的主窗口名，
                #  如果直接mainwindwo作为字典项，会被解释为对象的地址，后续eval无法使用
                commandstr = commandstr.replace("'barwindow_for_replace'", "barwindow")
            print("命令组装：commandstr:{}".format(commandstr))
        except Exception as err:
            print("组装第{0}条命令{1} 错误:{2}".format(currentitem, command, err))
            successflag = False
            break
        print("执行第{0}条命令{1} 对应代码: {2}...".format(currentitem, command, commandstr))
        print(command2sentence(command))
        try:
            # 执行命令行对应的代码
            if guiflag:
                bartext.update(Sg.SYMBOL_SQUARE * 4)  # 命令组装完成，再次推进进度条
                barwindow.refresh()
            starttime = datetime.now()
            result = eval(commandstr)  # eval执行相关代码
            endtime = datetime.now()
            print("执行第{0}条命令{1} 用时 {2}({3} -> {4})".format(
                currentitem, command, endtime - starttime, starttime, endtime))
        except Exception as err:
            print("执行第{0}条命令{1} 对应代码: {2} 错误: {3}".format(currentitem, command, commandstr, err))
            if guiflag:
                Sg.popup_error("执行第{0}条命令{1} 对应代码: {2} 错误: {3}".format(
                    currentitem, command, commandstr, err),
                    modal=True, keep_on_top=True)
            successflag = False
            break
        if isinstance(result, type([])):  # 自定义函数的返回值 [True|False, errstring]
            if result[0] is False and len(result) == 2:
                print("执行第{0}条命令{1} 对应代码: {2} 错误: {3}".format(
                    currentitem, command, commandstr, result[1]))
                if guiflag:
                    Sg.popup_error("执行第{0}条命令{1} 对应代码: {2} 错误: {3}".format(
                        currentitem, command, commandstr, result[1]),
                        modal=True, keep_on_top=True)
                successflag = False
                break

        # 记录本次处理涉及到变化的表格
        # tempcommandinfo = commanddict.get(command[CURRENT_COMMAND], None)
        tempcommandinfo = getcommandconfig(command[CURRENT_COMMAND])
        if tempcommandinfo is not None:
            if tempcommandinfo[COMMAND_NEW_TABLE_FLAG] == NOT_GENERATE_NEW_TABLE:
                # 没有生成新表
                for item in command[CURRENT_OPERATE_DFS]:
                    processedtablelist.add(item)
            else:
                # 生成新表
                # processedtablelist.add(command[CURRENT_MULTI_TABLE_RESULT])           # 新表从单表的序号该表的序号list
                for item in command[CURRENT_MULTI_TABLE_RESULT]:
                    processedtablelist.add(item)

        if guiflag:
            # 当optionindex + 1 对应下一条命令时，说明将执行当期命令，更新进度条
            currentprocess = itemstart / len(processlist)
            # 更新进度条, 进度条显示0.88, 保留少量到结束时显示。
            totalbartext.metadata = (int(currentprocess * 50 * 0.88)) % 51
            totalbartext.update(Sg.SYMBOL_SQUARE * totalbartext.metadata)
            barcommentext.update("执行第{0}/{1}条命令[{2}]用时:{3}".format(
                itemstart + 1, len(processlist), command[0], endtime - starttime))
            bartext.update(Sg.SYMBOL_SQUARE * 51)
            bartotalcommenttext.update("总用时：{}".format(endtime - totalstarttime))
            barwindow.refresh()
            # 修改"已执行“标记为“是”
            mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_CELLVALUE, currentwindow=mainwindow,
                                               location=(currentitem, COMMAND_EXECUTED_FLAG), value='是')
            # 修改已执行的命令的颜色
            defaultcolor = (COMMAND_EXECUTED_COLOR, COMMAND_EXECUTED_BACKGROUND_COLOR)
            mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                                               currentwindow=mainwindow, rownumber=currentitem, color=defaultcolor)

    if guiflag:
        # 颜色设置必须单独设置循环全部重新设置，否则受setcellvalue影响
        fillitems = currentitem + (1 if successflag is True and len(processlist) > 0 else 0)
        for item in range(fillitems):
            # 修改已执行的命令的颜色
            defaultcolor = (COMMAND_EXECUTED_COLOR, COMMAND_EXECUTED_BACKGROUND_COLOR)
            mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                                               currentwindow=mainwindow, rownumber=item, color=defaultcolor)

    print("original processedtable:{}".format(processedtablelist))
    # 根据本次运行涉及到的结果表，更新表格中的数据，显示执行结果，
    # 刷新相关的表格显示和tab
    if guiflag:
        # 更新表格数据
        print("刷新表格显示数据......")
        bartext.update(Sg.SYMBOL_SQUARE * 2)
        barwindow.refresh()
        starttime = datetime.now()
        currentshowtable = mainwindow[GROUP_TAB_KEY].get()
        refreshtable = currentshowtable[1] if currentshowtable is not None else -1
        # 如果当前表对应的specialspecialdflist还存在，并且表格数量未变，直接刷新当前表， 否则刷新第一张表即可，不需要全局刷新
        # 如果命令只涉及一张表，并且改表在specialdflist范围之类，只刷新该表
        # oldspecialdflist 和 len(specialdflist)不同，说明表格有增减
        if len(processedtablelist) == 1 and list(processedtablelist)[0] < len(specialdflist) \
                and oldspecialdflistnumber == len(specialdflist):
            print("只刷新唯一变化的表[{}]".format(list(processedtablelist)[0]))
            mainwindow[GROUP_TAB_KEY].update(
                commandtype=SPECIAL_TABLE_GROUP_TRIGGER_TAB,
                currentvalues=currentvalues,
                currentwindow=mainwindow,
                triggertable=list(processedtablelist)[0])
        elif oldspecialdflistnumber == len(specialdflist) and refreshtable in list(processedtablelist):
            print("表格数未变，刷新当前表[{}]".format(refreshtable))
            mainwindow[GROUP_TAB_KEY].update(
                commandtype=SPECIAL_TABLE_GROUP_TRIGGER_TAB, currentwindow=mainwindow,
                currentvalues=currentvalues, triggertable=refreshtable)
        else:  # 不是刷新仅仅刷新某张表，可能表格有增加或者减少，
            print("刷新所有表并显示表[0]")
            mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH,
                                             currentevent=currentevent, currentvalues=currentvalues,
                                             currentwindow=mainwindow)

        endtime = datetime.now()
        # 刷新进度条说明
        bartext.update(Sg.SYMBOL_SQUARE * 51)
        barcommentext.update("刷新表格数据用时：{}".format(endtime - starttime))
        bartotalcommenttext.update("总用时：{}".format(endtime - totalstarttime))
        barwindow.refresh()
        mainwindow.refresh()
        print("刷新表格显示数据用时：{}".format(endtime - starttime))
        print("总用时：{}".format(endtime - totalstarttime))

        # 刷新全局变量
        global currentdfcolumnlist, currentdfnamelist
        # 当前specialdflist的名字列表，用于选择操作表
        currentdfnamelist = [x for x in range(len(specialdflist))]
        # 当前所有specialdflist的column列表，用于选择操作列 .list(df) => df的column list
        currentdfcolumnlist = [list(x.dfdata) for x in specialdflist]

        # 运行完成前满格进度条然后关闭进度窗
        totalbartext.metadata = 50
        totalbartext.update(Sg.SYMBOL_SQUARE * totalbartext.metadata)
        if successflag:
            Sg.popup_ok("运行完成！", modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
        barwindow.close()

    return successflag


def command_item_edit(rowcontent: list) -> list or None:
    """
    编辑操作命令行，
    :param rowcontent:                  list： [str：是否已经执行，str：命令解释， str（list）：命令语句， str：命令备注]
    :return:                            list： [str：‘否’，str：命令解释， str（list）：命令语句， str：命令备注]
    """
    global currentdfnamelist, currentdfcolumnlist, useroperatedict
    # default command string.
    # 新增方式，没有选中当前行，没有任何数据，使用一个初始数据串
    if rowcontent[2].strip() == "":
        rowcontent = ['否', "", '["行删除", [0], {}, [0]]', ""]
    try:
        currentcommandlist = ast.literal_eval(rowcontent[2])
    except Exception as err:
        print("行编辑内容{}转换失败：{}".format(rowcontent[2], err))
        Sg.popup_error("行编辑内容{}转换失败：{}".format(rowcontent[2], err),
                       modal=True, keep_on_top=True, )
        return None

    # 当前specialdflist的名字列表，用于选择操作表
    currentdfnamelist = [x for x in range(len(specialdflist))]
    # 当前所有specialdflist的column列表，用于选择操作列 .list(df) => df的column list
    currentdfcolumnlist = [list(x.dfdata) for x in specialdflist]

    # 1、命令选择、操作对象选择、字典参数、位置参数、生成按钮
    layoutcommand = [
        Sg.Frame("命令行配置", [[
            Sg.Col([[
                Sg.Frame("命令选择", [[
                    Sg.Combo(commandcombolist, readonly=True, k=COMMAND_LIST,
                             # background_color=HIGHLIST_SELECTED_COLOR,
                             text_color=HIGHLIST_SELECTED_COLOR,
                             button_background_color=HIGHLIST_SELECTED_COLOR,
                             # button_arrow_color=HIGHLIST_SELECTED_COLOR,
                             # highlight_text_color='white',
                             enable_events=True, pad=DEF_PD_L, size=(16, 1))]], border_width=0)
            ]]),
            Sg.Col([[
                Sg.Frame("已选操作表", [[
                    Sg.Input("", k=DF_CHOOSE_RESULT, enable_events=True, readonly=True,
                             pad=DEF_PD_L, size=(16, 1))]],
                         k=DF_CHOOSE_RESULT_FRAME, border_width=0, visible=False)
            ]]),
            Sg.Col([
                [
                    Sg.Frame("自动生成命令解释", [[
                        Sg.Input(rowcontent[1], k=COMMAND_SENTENCE, enable_events=True,
                                 readonly=True, pad=DEF_PD_L, size=(99, 1))]], border_width=0)
                ]
            ]),
        ]])
    ]
    # 2、操作对象表字段列表、字典参数、位置参数选择框
    layoutparaminfo = [
        Sg.Frame("操作表格选择", [
            [
                Sg.Col([
                    [
                        Sg.Listbox(currentdfnamelist,
                                   k=DF_MULTI_CHOOSE,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   enable_events=True,
                                   tooltip="选择需操作的表格\n根据命令不同，可以选择一张或者多张表",
                                   pad=DEF_PD_L, size=(12, 26))
                    ]
                ], vertical_alignment='top'),
            ],
        ], k=OPERATE_DFS_CHOOES_FRAME, vertical_alignment='top'),
        Sg.Frame("操作选项配置", [[
            Sg.Col([
                [
                    Sg.Frame("位置参数选项", [[
                        Sg.Listbox([],
                                   k=ARGC_CONFIG_COMMENT,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项说明",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(26, 11)),
                        Sg.Listbox(currentdfnamelist,
                                   k=ARGC_CONFIG,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项名称",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(18, 11)),
                        Sg.Listbox(currentdfnamelist,
                                   k=ARGC_CONFIG_VALUE,
                                   text_color=ARG_PARAM_VALUE_COLOR,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项当前值",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(50, 11)),
                        Sg.Button('修改选项', k=ARGC_PARAM_EDIT, pad=DEF_PD_L)
                    ]], vertical_alignment='top', k=ARGC_CONFIG_FRAME, pad=DEF_PD_L),
                ],
                [
                    Sg.Frame("可选字典参数选项", [[
                        Sg.Listbox([],
                                   k=ARGV_CONFIG_COMMENT,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项说明",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(26, 12)),
                        Sg.Listbox(currentdfnamelist,
                                   k=ARGV_CONFIG,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项名称",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(18, 12)),
                        Sg.Listbox(currentdfnamelist,
                                   k=ARGV_CONFIG_VALUE,
                                   text_color=ARG_PARAM_VALUE_COLOR,
                                   highlight_background_color=HIGHLIST_SELECTED_COLOR,
                                   highlight_text_color='white',
                                   enable_events=True,
                                   no_scrollbar=True,
                                   tooltip="选项当前值",
                                   # select_mode=Sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                   pad=(0, 0),
                                   size=(50, 12)),
                        Sg.Button('修改选项', k=ARGV_PARAM_EDIT, pad=DEF_PD_L)
                    ]], vertical_alignment='top', k=ARGV_CONFIG_FRAME, pad=DEF_PD_L)
                ]
            ]),
        ]], vertical_alignment='top'),
    ]
    # 2.5、命令备注
    layoutcomment = [
                        Sg.Frame("命令备注", [[
                            Sg.Input(rowcontent[3], k=COMMAND_COMMENT, enable_events=False,
                                     readonly=False, pad=(DEF_PD_L[0] + 4, DEF_PD_L[1]), size=(126, 1))]])
                    ],

    # 3、生成结果：命令行语句及对应的解释
    layoutresult = [
        Sg.Frame("手工输入命令", [[
            Sg.Col([[
                Sg.Frame("命令语句", [[
                    Sg.Input(rowcontent[2], k=COMMAND_STRUCTURE, enable_events=True,
                             readonly=False, pad=DEF_PD_L, size=(112, 1))]], border_width=0)
            ]]),
            Sg.Col([[
                Sg.Button('命令生成', k=COMMAND_GENERATE, pad=DEF_PD_L, )
            ]]),
        ]], tooltip="可手工按命令格式输入命令语句，然后点击<命令生成>按钮完成相关更新")
    ]

    # 4、选择按钮
    layouttail = [[Sg.Col([[
        Sg.Frame("",
                 [[Sg.Button('确定', k=EDIT_WIN_OK),
                   Sg.Button('取消', k=EDIT_WIN_CANCEL)]],
                 vertical_alignment='top', element_justification='right', expand_x=True)
    ]], justification='right')]]

    layout = [layoutcommand, layoutparaminfo, layoutcomment, layoutresult, layouttail]

    global editwindow
    editwindow = Sg.Window(
        '命令配置',
        layout,
        font=DEF_FT_L,
        icon=LOCAL_SYSTEM_ICON,
        use_ttk_buttons=True,
        return_keyboard_events=False,  # 把mouse事件交给内部组建，不由主页面处理
        resizable=True,
        modal=True,
        # keep_on_top=True,
        finalize=True)

    simulatevalues = {}
    # 将currentcommand 赋值给配置页面的element，模拟事件触发事件处理进行初始化
    # 处理选择的命令， 模仿commandchoosed事件相关的事件event和values
    simulateevent = COMMAND_LIST
    #   案例：   ["行删除", [0], {}, [0, 8]],
    currentcommand = currentcommandlist[CURRENT_COMMAND]
    editwindow[simulateevent].update(value=currentcommand)
    simulatevalues[COMMAND_LIST] = currentcommand
    # 通过模仿commandchoosed，将表格、以及函数对应的选项和默认值填写到相应的elements
    commandchoosed(editwindow, simulateevent, simulatevalues)
    # 填写当前命令选择的表格以及对应的选项
    commandinfofill(editwindow, currentcommandlist)

    def useroperaterecord():
        # 判断当前命令是否要记录用户输入的参数值，如果需要，
        # 获取当前命令
        currentcommand = ast.literal_eval(values[COMMAND_STRUCTURE])[0]
        # 获取当前命令的配置
        # currentcommandconfig = commanddict.get(currentcommand, None)
        currentcommandconfig = getcommandconfig(currentcommand)
        if currentcommandconfig is None:
            return
        # 获取当前命令使用的函数
        functionname = currentcommandconfig.get(COMMAND_FUNCTION_NAME, None)
        if functionname is None:
            return
        # 无论是否使用用户操作，都记录本次最新的数据
        # userdefaultflag = currentcommandconfig.get(COMMAND_USER_INPUT_PARAM, None)
        # 先复制格式

        useroperatedict[functionname] = copy.deepcopy(originfunctiondict[functionname])
        for argtype in ["argc", "argv"]:
            if argtype == "argc":
                # 获取argclist和对应的值，
                arglist = editwindow[ARGC_CONFIG].get_list_values()
                argvalues = editwindow[ARGC_CONFIG_VALUE].get_list_values()
            else:
                # 获取argclist和对应的值，
                arglist = editwindow[ARGV_CONFIG].get_list_values()
                argvalues = editwindow[ARGV_CONFIG_VALUE].get_list_values()
            for i, name in enumerate(arglist):
                if useroperatedict[functionname][argtype].get(name, None) is not None:
                    # 根据参数类型判断参数是否需要转换
                    checkresult = paramtypevalidcheckandtrans(
                        argvalues[i], useroperatedict[functionname][argtype][name]['type'])
                    if checkresult[0] is True:  # 转换成功则记录动态值
                        useroperatedict[functionname][argtype][name][FUNCTION_ARG_DEFAULTVALUE] = checkresult[1]

    # 选择的参数
    while True:
        event, values = editwindow.read()
        if debugflag:
            print("editwindow event:{}".format(event))
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            rowcontent = None
            break

        elif event == EDIT_WIN_OK:
            # 根据配置界面组合rowcontent
            # 启动“命令生成”，同时检查合法性
            # 返回rowcontent
            rowcontent = ["否", values[COMMAND_SENTENCE], values[COMMAND_STRUCTURE], values[COMMAND_COMMENT]]
            # 记录当前用户填写的值
            useroperaterecord()
            break

        elif event == EDIT_WIN_CANCEL:
            rowcontent = None
            break

        elif event in editwindowprocess.keys():
            editwindowprocess[event](editwindow, event, values)
            continue

        else:
            continue

    editwindow.close()
    return rowcontent


CELL_EDITABLE = True
COMMAND_RUN_KEY = "_run_"
COMMAND_STEPRUN_KEY = "_steprun_"
COMMAND_STEPBACK_KEY = "_stepback_"
COMMAND_RUNTOCURRENT_KEY = "_runtocurrent_"
COMMAND_RESET_KEY = "_commandreset_"
MAINWINDOW_CLOSE = '_mainwin_close_'
GROUP_TAB_KEY = "group_tab_key"
RUN_LOG_SWITCH = '_run_log_switch_'
RUN_LOG_SAVE = '_run_log_save_'
LOG_FOR_DFTRANS = '_log_for_dftrans_'

GROUP_TABLE_SIZE = (1180, 320)
COMMAND_TABLE_SIZE = (1180, 486)
GROUP_TAB_SIZE = (1166, 290)
COMMAND_WINDOW_SIZE = (1180, 500)
LOG_301_LONG_ROWS = 6
WHOLE_WINDOW_SIZE = (1240, 976)
GROUP_TABLE_ROWS = 13
COMMAND_TABLE_ROWS = 20

GROUP_TABLE_SHORT_SIZE = (1180, 200)
COMMAND_TABLE_SHORT_SIZE = (1180, 346)
GROUP_TAB_SHORT_SIZE = (1166, 170)
COMMAND_WINDOW_SHORT_SIZE = (1180, 370)
LOG_301_SHORT_ROWS = 4
WHOLE_WINDOW_SHORT_SIZE = (1240, 708)
GROUP_TABLE_SHORT_ROWS = 6
COMMAND_TABLE_SHORT_ROWS = 12


def commandeditgui(commandlist: list, dfcurrentprefix: str = 'specialdflist', globalrunflag=False) -> None:
    """
    命令编辑窗口
    :param commandlist:                     处理的命令列表
    :param dfcurrentprefix                  用于存储df的specialdflist变量名,本函数的第一个变量
    :param globalrunflag                    bool: True 表示启动后即刻全速运行命令文件
    :return:
    """
    global specialdflist

    systemx, systemy, realx, realy = getsystemresolution()
    # systemy = 700
    if systemy > WHOLE_WINDOW_SIZE[1] + 100:
        longwindowflag = True
        grouptablesize = GROUP_TABLE_SIZE  # (1180, 350)
        grouptablerows = GROUP_TABLE_ROWS
        commandtablesize = COMMAND_TABLE_SIZE  # (1180, 350)
        commandtablerows = COMMAND_TABLE_ROWS
        grouptabsize = GROUP_TAB_SIZE  # (1166, 360)
        command_window_size = COMMAND_WINDOW_SIZE  # (1180, 430)
        wholewindowsize = WHOLE_WINDOW_SIZE  # (1240, 968)
    else:
        longwindowflag = False
        grouptablesize = GROUP_TABLE_SHORT_SIZE  # (1180, 350)
        grouptablerows = GROUP_TABLE_SHORT_ROWS
        commandtablesize = COMMAND_TABLE_SHORT_SIZE  # (1180, 350)
        commandtablerows = COMMAND_TABLE_SHORT_ROWS
        grouptabsize = GROUP_TAB_SHORT_SIZE  # (1166, 360)
        command_window_size = COMMAND_WINDOW_SHORT_SIZE  # (1180, 430)
        wholewindowsize = WHOLE_WINDOW_SHORT_SIZE  # (1240, 968)

    temptablegroup = SpecialTableGroup(
        tablegroupkey=GROUP_TAB_KEY,
        specialdflist=specialdflist,
        # dflist=None,
        max_rows=grouptablerows,
        right_click_menu=commandmenulist,
        max_columns=14,
        enable_events=True,
        display_row_numbers=True,
        showcolnamewithid=True,
        showcolumnname=True,
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        use_inner_right_click_menu=True,
        input_text_color='blue',
        input_text_background_color='white',
        itemeditfunc=None,
        v_slider_resolution=0.1,
        h_slider_resolution=0.1,
        slider_every_row_column=True,
        # col_widths=col_widths,
        pad=(0, 0),
        border_width=1,
        text_color="blue",
        size=grouptabsize,
        slider_relief=Sg.RELIEF_FLAT,
        v_slider_show=True,
        h_slider_show=True,
        relief=Sg.RELIEF_SUNKEN,
        disable_slider_number_display=True,
        # select_mode=SPECIAL_TABLE_LISTBOX_SELECT_MODE_SINGLE,
        # select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        # select_mode=SPECIAL_TABLE_SELECT_MODE_NONE,
        select_mode=SPECIAL_TABLE_SELECT_MODE_EXTENDED,
        cell_editable=CELL_EDITABLE,
        edit_button_visible=False,
        move_row_button_visible=False,
        filter_visible=False,
        filter_set_value_visible=False
    ).layout

    # Special'Table字段中文解释与标签的对应字典
    global columninfodic
    columninfodic = {
        '已执行': 'commandfinished',
        '命令解释': 'commandstring',
        '命令语句': 'commandparam',
        '命令备注': 'linecomment'
    }
    # Special'Table标签前缀
    global commandtablekey
    commandtablekey = "_commandtable_"
    # 点击“编辑”，“添加”是的钩子函数参数
    tempfuncargs = {}

    # Special'Table字段的取值范围
    colvaluesecale = [
        None,  # 已执行标记
        None,  # 命令注释
        None,  # 命令行
        None,  # 命令行备注
    ]
    # Special'Table字段的显示宽度
    column_widths = [8, 56, 56, 28]
    # Special'Table字段的显示map
    visible_column_map = [True, True, True, True]

    global commandtabledictlist
    # 记录执行窗口按钮和右键菜单的对应关系
    runcommandmenueventdict = {
        '单步执行': COMMAND_STEPRUN_KEY,
        '单步回退': COMMAND_STEPBACK_KEY,
        '执行到选中': COMMAND_RUNTOCURRENT_KEY,
        '全部执行': COMMAND_RUN_KEY,
        '执行重置': COMMAND_RESET_KEY,
        '导入命令': LOAD_COMMAND,
        '导出命令': SAVE_COMMAND,
        '生成注释': GENERATE_COMMAND_FILE_COMMENT,
    }
    runcommandmenueventlist = list(runcommandmenueventdict)

    layouttable = SpecialTable(
        commandtablekey,
        specialdf=None if commandtabledictlist != []
        else SpecialDf(dfdata=pd.DataFrame([], columns=list(columninfodic.values())), headings=list(columninfodic)),
        display_row_numbers=True,
        v_slider_resolution=0.1,
        h_slider_resolution=0.1,
        right_click_menu=[["", runcommandmenueventlist]],
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        slider_every_row_column=True,
        text_color=TEXT_COLOR,
        text_background_color=TEXT_BACKGROUND_COLOR,
        input_text_color=INPUT_TEXT_COLOR,
        input_text_background_color=INPUT_TEXT_BACKGROUND_COLOR,
        cell_editable=CELL_EDITABLE,
        filter_visible=True,
        edit_button_visible=True,
        move_row_button_visible=True,
        v_slider_show=True,
        h_slider_show=False,
        tabledatadictlist=commandtabledictlist,
        headings=list(columninfodic),
        itemeditfunc=command_item_edit,  # 编辑记录行时的钩子函数
        itemeditfuncargsdic=tempfuncargs,  # 编辑函数的参数列表
        indexcol=None,  # 记录可以重复
        font=('黑体', 10),
        pad=(0, 0),
        border_width=1,
        size=commandtablesize,
        cell_justification='l',
        max_rows=commandtablerows,
        max_columns=len(visible_column_map),
        visible_column_map=visible_column_map,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        col_widths=column_widths,
        col_value_scale=colvaluesecale,
        vertical_scroll_only=False,
        relief=Sg.RELIEF_SUNKEN,
        disable_slider_number_display=True,
    ).layout

    # 数据表格编辑toolbar
    toolbar_buttons = [
        Sg.ButtonMenu(x.center(4), menu_def=[x, y], k=x, pad=(0, 2), border_width=1)
        for x, y in commandmenudict.items()
    ]

    # 尝试使用图标button，测试用
    def tbuttonmenu(image_data, menu_def, k='', tooltip=''):
        return Sg.ButtonMenu('', menu_def=menu_def, image_data=image_data, button_color=('grey', 'white'),
                             pad=(1, 1), k=k, border_width=1, tooltip=tooltip)

    imagetoolbaricondict = {
        COMMAND_ROW_PROCESS: "CLOSE64",
        COMMAND_COLUMN_PROCESS: "TIMER64",
        COMMAND_SINGLE_DF_PROCESS: "HOUSE64",
        COMMAND_TWO_DF_PROCESS: "CPU64",
        COMMAND_MULTI_DF_PROCESS: "CAMERA64",
        COMMAND_NEW_TABLE_IMPORT: "COOKBOOK64",
        COMMAND_OTHER: "CHECKMARK64"
    }
    toolbar_buttons1 = [
        tbuttonmenu(image_data=icondict[imagetoolbaricondict[y[0]]][22:], menu_def=[y[0], y[1]], k=y[0])
        for x, y in enumerate(commandmenulist)
    ]

    layouthead = [
        [Sg.Frame("", temptablegroup, border_width=0, pad=(0, 0))],
        [
            Sg.Col([[
                Sg.Frame("", [[Sg.Text(" 数据操作 ")] + toolbar_buttons], k=DATA_TABLE_OPERATE_FRAME,
                         pad=(2, 2), visible=True)
            ]], justification="c", element_justification="left"),
            Sg.Col([[
                Sg.Frame("", [[
                    Sg.Text(" 手工处理数据 "),
                    Sg.Button('文件导入', k=LOAD_DATA, pad=(0, 2)),
                    Sg.Button('文件导出', k=SAVE_DATA, pad=(0, 2)),
                    Sg.Button('SQL导入', k=LOAD_SQL, pad=(0, 2)),
                    Sg.Button('SQL导出', k=SAVE_SQL, pad=(0, 2)),
                    Sg.Button('删除数据表', k=DELETE_DATA, pad=(0, 2)),
                    Sg.Button('复位已选行', k=CLEAR_SELECTED_ROW, pad=(0, 2)),
                    Sg.Button('复位已选列', k=CLEAR_SELECTED_COL, pad=(0, 2)),
                    Sg.Button('图形显示', k=PLOT_SHOW_DATA, pad=(0, 2))
                ]]),
                Sg.Frame("", [[
                    Sg.Text(" 操作记录 "),
                    Sg.Button('开始记录', k=START_COMMAND_RECORD, pad=(1, 1),
                              disabled_button_color=('yellow', 'red'), button_color=("white", "green")),
                    Sg.Button('结束记录', k=STOP_COMMAND_RECORD, pad=(1, 1),
                              disabled_button_color=('white', 'grey'), disabled=True)
                ]], visible=False)
            ]], justification="c", element_justification="center")
        ]
    ]

    # 生成尾部保存、退出按钮
    layouttail = [
        [
            # Sg.Text("".rjust(5)),
            Sg.Frame("",
                     [[
                         Sg.Text(" 运行日志 "),
                         Sg.Button('日志开关', k=RUN_LOG_SWITCH, pad=(2, 2), button_color='green'),
                         Sg.Button('日志保存', k=RUN_LOG_SAVE, pad=(2, 2))]]),
            Sg.Frame("",
                     [[
                         Sg.Text(" 命令调试 "),
                         Sg.Button('单步执行', k=COMMAND_STEPRUN_KEY, pad=(2, 2)),
                         Sg.Button('单步回退', k=COMMAND_STEPBACK_KEY, pad=(2, 2)),
                         Sg.Button('执行到选中', k=COMMAND_RUNTOCURRENT_KEY, pad=(2, 2)),
                         Sg.Button('全部执行', k=COMMAND_RUN_KEY, pad=(2, 2)),
                         Sg.Button('执行重置', k=COMMAND_RESET_KEY, pad=(2, 2))]]),
            Sg.Frame("",
                     [[
                         Sg.Text(" 命令文件 "),
                         Sg.Button('导入命令', k=LOAD_COMMAND, pad=(2, 2)),
                         Sg.Button('导出命令', k=SAVE_COMMAND, pad=(2, 2)),
                         Sg.Button('生成注释', k=GENERATE_COMMAND_FILE_COMMENT, pad=(2, 2)),
                     ]]),
            Sg.Frame("",
                     [[
                         Sg.Text(" 系统配置 "),
                         Sg.Button('配置编辑', k=EDIT_CONFIG, pad=(2, 2)),
                     ]]),
            Sg.Button(' 关  闭 ', k=MAINWINDOW_CLOSE, pad=(10, 10))
        ]
    ]
    # 打印信息显示
    logging_301_layout = [
        # [Sg.Text("所有的运行信息都将在此显示!")],
        [Sg.Multiline(size=(60, LOG_301_LONG_ROWS if longwindowflag else LOG_301_SHORT_ROWS),
                      font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      autoscroll=True, auto_refresh=True, k=LOG_FOR_DFTRANS,
                      reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                      visible=False, disabled=True, metadata=False)]
    ]

    # # 拼接页面配置
    layout = [[Sg.Col(
        [[Sg.Frame("相关数据表", layouthead)]] +
        [[Sg.Frame("相关命令配置", layouttable, size=command_window_size, expand_y=True)]] +
        layouttail +
        logging_301_layout,
        justification='center',
        element_justification='center',
        expand_x=False
    )]]
    # 设置主页面
    global mainwindow
    mainwindow = Sg.Window(
        '数据批量转换工具',
        layout,
        font=DEF_FT_L,
        # ttk_theme="clam",
        use_ttk_buttons=True,
        icon=LOCAL_SYSTEM_ICON,
        return_keyboard_events=False,  # 把mouse事件交给内部组建，不由主页面处理
        resizable=True,
        # size=wholewindowsize,
        modal=True,
        # element_justification='center',
        # keep_on_top=True,
        finalize=True)
    mainwindow.disappear()
    # 初始化为True，启动后设置为False，避免占位差异。
    # mainwindow[DATA_TABLE_OPERATE_FRAME].update(visible=False)            # 改为一直显示，不用开始记录、结束记录进行切换
    # 获取需要特殊处理的事件列表
    needprocesslist = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_SPECIALEVENTLIST)
    # 初始化mousewheel updown相关的环境
    # 命令表处理
    mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_BIND, currentwindow=mainwindow)
    # 数据表处理
    mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_SET_BIND, currentwindow=mainwindow)
    # 如果specaildflist为空，刷新tab显示，关闭所有tab
    if len(specialdflist) == 0:
        mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH,
                                         currentevent='', currentvalues={},
                                         currentwindow=mainwindow)

    def commandstepback(errorflag: bool = False):
        """
        利用_add_当前执行的命令，并执行到上一条
        :param errorflag:                 bool : True, 用于出错处理回退，不打印提示信息，False：正常回退调试，打印
        :return:
        """
        # 获取当前命令列表 并获取当前已执行行
        commanddictlist = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
        # 计算当前已经执行的命令行数，通过计算‘是’的数量
        executednumber = \
            [commanddictlist[x][columninfodic["已执行"]] for x in range(len(commanddictlist))].count('是')
        if executednumber in (None, 0):
            if errorflag is False:
                Sg.popup_quick_message("没有执行任何命令，无法回退！",
                                       modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
            return
        # 复位所有命令
        commandreset()
        # 确定要执行的命令数
        if executednumber is not None and executednumber > 1:
            setrow = executednumber - 2
            mainwindow[commandtablekey].update(
                commandtype=SPECIAL_TABLE_SET_CURRENTROW,
                currentwindow=mainwindow, rownumber=setrow)
            # 如果需要重置执行情况，首先重置命令执行，然后执行到当前编辑行之前
            globalcommandrun(currentevent=event, currentwindow=mainwindow, currentvalues=values, method=TO_CURRENT_RUN)
            # 编辑完成后，恢复已执行命令行的颜色
            defaultcolor = (COMMAND_EXECUTED_COLOR, COMMAND_EXECUTED_BACKGROUND_COLOR)
            for currentitem in range(setrow + 1):
                # 修改已执行的命令的颜色
                mainwindow[commandtablekey].update(
                    commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                    currentwindow=mainwindow, rownumber=currentitem, color=defaultcolor)

    def commandreset():
        # 清空所有生成的df
        specialdflist.clear()
        # 恢复最原始的df
        for specialdfitem in specialdflistcopy:
            specialdflist.append(copy.deepcopy(specialdfitem))
        # 刷新所有表格的显示
        mainwindow[GROUP_TAB_KEY].update(commandtype=SPECIAL_TABLE_GROUP_REFRESH, currentwindow=mainwindow)

        # 重置所有命令为未执行。
        for itemp in range(mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_MAXROWNUMBER)):
            # 修改"已执行“标记为“否”
            mainwindow[commandtablekey].update(
                commandtype=SPECIAL_TABLE_SET_CELLVALUE,
                currentwindow=mainwindow, location=(itemp, COMMAND_EXECUTED_FLAG), value='否')

        # 重置所有命令的颜色
        for currentitem in range(mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_MAXROWNUMBER)):
            # 修改已执行的命令的颜色
            defaultcolor = (INPUT_TEXT_COLOR, INPUT_TEXT_BACKGROUND_COLOR) \
                if CELL_EDITABLE else (TEXT_COLOR, TEXT_BACKGROUND_COLOR)
            mainwindow[commandtablekey].update(
                commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                currentwindow=mainwindow, rownumber=currentitem, color=defaultcolor)
        mainwindow.refresh()

    def commandedit(currentevent) -> int:
        """
        对于 命令行表格的事件，额外针对当前调试状态做处理。
        :param currentevent:                当前的事件
        :return:                            调整后已经执行的命令行条数
        """
        # 当使用编辑 命令行的按钮时，需要把目前已经调试执行的命令行，恢复到当前编辑行的前一条
        # 如果是编辑命令，需要判断当前已经执行到的命令行，如果已经执行的>=当前编辑行，需要回退执行，否则不用回退，但是要刷新执行状态；
        # 如果是增加命令行，因为是在命令末尾添加，所以不需要改变，但是需要刷新执行状态
        # eventlist 最后一项为移动的目标行，其他均为button
        # 获取当前命令列表 并获取当前已执行行
        commanddictlist = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
        # 计算当前已经执行的命令行数，通过计算‘是’的数量
        executednumber = \
            [commanddictlist[x][columninfodic["已执行"]] for x in range(len(commanddictlist))].count('是')
        # 执行数为0，直接返回
        if executednumber == 0:
            return 0

        # 获取当前编辑行
        currentrow = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_CURRENTROW)
        # 获取当前命令和状态下，不受影响的最小行数（不是行号）
        setrow = mainwindow[commandtablekey].get(attribute=SPECIAL_TABLE_GET_EVENTINFLUENCEROW,
                                                 currentevent=currentevent, currentwindow=mainwindow,
                                                 currentvalues=values, executednumber=executednumber)

        if setrow == executednumber:  # 不受影响的行数和当前已经执行的行数一样，不需要重新复位和执行
            return setrow
        elif setrow > executednumber or setrow < 0:
            print("命令{}不受影响的行数{}大于已经执行的行数{}，不合法!".format(currentevent, setrow, executednumber))
            return 0
        else:
            commandreset()
            if setrow > 0:
                # 上移到了顶部，setrow为None，重置后不需要执行语句
                mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_CURRENTROW,
                                                   currentwindow=mainwindow, rownumber=setrow - 1)
                # 如果需要重置执行情况，首先重置命令执行，然后执行到当前编辑行之前
                globalcommandrun(currentevent=event, currentwindow=mainwindow,
                                 currentvalues=values, method=TO_CURRENT_RUN)
            # 记录实际执行的命令行数
            executednumber = setrow

            # 执行完成后，再次恢复currentrow以进行实际编辑操作。
            mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_CURRENTROW,
                                               currentwindow=mainwindow, rownumber=currentrow)
        return executednumber

    mainwindow.reappear()
    originwindowsize = copy.deepcopy(mainwindow.size)
    print("orrginsize record:{}".format(originwindowsize))
    # 窗口过小
    if originwindowsize[1] < WHOLE_WINDOW_SHORT_SIZE[1] - 200:
        originwindowsize = WHOLE_WINDOW_SIZE if longwindowflag else WHOLE_WINDOW_SHORT_SIZE
        print("originsize too small , adjust to:{}".format(originwindowsize))
    extendwindowsize = None

    # 如果配置了全速运行命令并且命令文件已经加载，触发全速运行事件
    if globalrunflag:
        mainwindow.write_event_value(COMMAND_RUN_KEY, {})

    while True:
        event, values = mainwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, MAINWINDOW_CLOSE):
            # 用户输入的动态值回写到用户记录文件
            global useroperateconfig, useroperatedict, manualbuttonoperatedict, useroperateconfig
            try:
                with open(useroperateconfig, 'w', encoding='utf8') as fp:
                    json.dump(
                        {"useroperatedict": useroperatedict, "manualbuttonoperatedict": manualbuttonoperatedict},
                        fp, ensure_ascii=False, sort_keys=False, indent=4)
                    fp.flush()
                    fp.close()
            except Exception as err:
                Sg.popup_error("保存用户文件：{} 失败：{}".format(useroperateconfig, str(err)),
                               modal=True,
                               keep_on_top=True,
                               icon=LOCAL_SYSTEM_ICON)
                break
            # Sg.popup_quick_message("保存用户文件{}完成！".format(useroperateconfig), auto_close_duration=0.5,
            #                        modal=True, keep_on_top=True, text_color='white', background_color='dark blue')
            break

        # 执行窗口的右键菜单，直接出发对应的按钮
        elif event in runcommandmenueventlist:
            mainwindow.write_event_value(runcommandmenueventdict[event], values)
            continue

        elif event in datatablebuttonmenuevent or event in datatablerightclickevent:
            # 处理鼠标右键菜单事件和button菜单的事件
            # 1.0、获取当前的底层事件，commandbutton需要获取value对应的事件
            if event in datatablebuttonmenuevent:
                currentdfevent = values[event]
            else:
                # 右键菜单直接获取事件
                currentdfevent = event
            print("get event {}: {}".format(event, currentdfevent))
            # 处理方法1、根据当前选择的表格、行列、命令类型组织好命令行 2、调用“增加”按钮、3、调用单步执行按钮
            # 组织初始化命令语句，需要根据命令行的格式配置进行处理，从表格编辑页面，目前仅能获取的内容：当前表号、当前选中行号、当前选中列号
            # 1.1、获取当前表号
            currentsubtable = mainwindow[GROUP_TAB_KEY].get()
            # 如果没有当前表格， 而且命令不是表格导入命令
            if currentsubtable is None and event != COMMAND_NEW_TABLE_IMPORT:
                Sg.popup_ok("当前没有可供编辑并自动记录操作的表格，请使用手工方式添加命令！", modal=True, keep_on_top=True,
                            icon=LOCAL_SYSTEM_ICON)
                continue
            # 对于”行修改“、”行新增“, 可以直接触发系统的”编辑“，”修改“按钮
            currentrowcontent = None
            if event in ["行新增", "行修改"]:
                currentrowcontent = mainwindow[GROUP_TAB_KEY].get(attribute=SPECIAL_TABLE_GET_CURRENTROW_CONTENT)
            # 对于列命名，获取当前列名
            currentcolumnname = []
            if event == "列命名":
                currentcolumnname = mainwindow[GROUP_TAB_KEY].get(attribute=SPECIAL_TABLE_GET_COLUMNN_NAME)

            # 1.2、获取当前表号选中的行列
            currentrowcontent = str(currentrowcontent) if currentrowcontent is not None else None
            currentcolumnname = str(currentcolumnname)
            selectedrowcolumn = mainwindow[GROUP_TAB_KEY].get(attribute=SPECIAL_TABLE_GET_SELECTED_ROWCOLUMN)
            selectedrow = list(selectedrowcolumn[0])
            selectedcolumn = list(selectedrowcolumn[1])
            # 根据选中的列序号确定列名
            selectedcolumnname = [list(specialdflist[currentsubtable[1]].dfdata)[x] for x in selectedcolumn]
            # 1.3、根据行、列命令和命令格式组合命令行
            # currentcommandconfig = commanddict.get(currentdfevent, None)
            currentcommandconfig = getcommandconfig(currentdfevent)
            commandformat = currentcommandconfig[COMMAND_USED_INPUT_FORMAT]
            # 传递给格式串的数据多于每个串需要的数据，各个串根据需要获取其中一部分数据整合到整个串
            # {0} currentsubtab[1], {1} selectedrow, {2} selectedcolumn,
            # {3} currentrowcontent, {4} currentcolumnname, {5} len(specialdflist) , {6}specialdflist"
            tempstr = commandformat.format(currentsubtable[1] if currentsubtable is not None else None, selectedrow,
                                           [selectedcolumn, selectedcolumnname],
                                           currentrowcontent, currentcolumnname, len(specialdflist), specialdflist)
            commandrow = ["否", "", "['{0}', {1}]".format(currentdfevent, tempstr), ""]

            # 2、调用增加命令行
            ret = mainwindow[commandtablekey].update(
                commandtype=SPECIAL_TABLE_SET_ADD_NEWROW, currentwindow=mainwindow, newrowcontent=commandrow)
            if ret:
                # 3、完成命令行增加的命令后，执行单步操作，直接出发单步按钮点击事件即可
                # 如果添加成功，就单步执行
                mainwindow.write_event_value(COMMAND_STEPRUN_KEY, None)

            continue

        elif event == LOAD_COMMAND:
            # 加载命令文件
            loadcommandfile(initialflag=False)
            continue

        elif event == SAVE_COMMAND:
            # 保存当前的命令文件
            savecommandfile()
            continue

        elif event == GENERATE_COMMAND_FILE_COMMENT:
            # 生成注释
            generatecommandfilecomment()
            continue

        elif event == EDIT_CONFIG:
            # 编辑系统配置（函数、命令）
            editsystemconfig()
            continue

        elif event == START_COMMAND_RECORD:
            mainwindow[STOP_COMMAND_RECORD].update(disabled=False)
            mainwindow[DATA_TABLE_OPERATE_FRAME].update(visible=True)
            mainwindow[START_COMMAND_RECORD].update(disabled=True)
            # 开始记录
            continue

        elif event == STOP_COMMAND_RECORD:
            mainwindow[START_COMMAND_RECORD].update(disabled=False)
            mainwindow[DATA_TABLE_OPERATE_FRAME].update(visible=False)
            mainwindow[STOP_COMMAND_RECORD].update(disabled=True)
            # 停止记录
            continue

        elif event == LOAD_DATA:
            # 读取数据文件
            loaddatafromfilebutton()
            continue

        elif event == LOAD_SQL:
            # sql从数据库导入
            loaddatafromdatabasebysql()
            continue

        elif event == SAVE_SQL:
            # sql 将df写入数据库
            savedatatodatabasebysql()
            continue

        elif event == SAVE_DATA:
            savedatatofilebutton()
            # 保存数据文件
            continue

        elif event == DELETE_DATA:
            deletedatatable()
            continue

        elif event == CLEAR_SELECTED_COL:
            clearselected(values=values, rowflag=False)
            continue

        elif event == CLEAR_SELECTED_ROW:
            clearselected(values=values, rowflag=True)
            continue

        elif event == PLOT_SHOW_DATA:
            plotshowdf()
            # plotshowdf()
            continue

        elif event == COMMAND_RUN_KEY:
            # 全速运行剩余命令
            globalcommandrun(currentevent=event, currentwindow=mainwindow, currentvalues=values, method=ALL_RUN)
            continue

        elif event == COMMAND_STEPRUN_KEY:
            # 单步运行当前的命令然后刷新表格
            globalcommandrun(currentevent=event, currentwindow=mainwindow, currentvalues=values, method=STEP_RUN)
            continue

        elif event == COMMAND_STEPBACK_KEY:
            commandstepback(errorflag=False)
            continue

        elif event == COMMAND_RUNTOCURRENT_KEY:
            # 执行到当前行
            globalcommandrun(currentevent=event, currentwindow=mainwindow, currentvalues=values, method=TO_CURRENT_RUN)
            continue

        elif event == COMMAND_RESET_KEY:
            commandreset()
            continue

        elif isinstance(event, tuple):
            # TABLE 被点击后，会连续输出两个事件，一个是元组，格式如下，包含了点击的（行号，列号），行号-1表示点击的是heading
            # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
            # 第二个事件是表格本身key事件, 表格点击事件, 因为处理了第一个元组事件，第二个可以忽略
            # 对于表格相关事件，针对调试过程中的已处理命令行，先做好预处理。针对不同命令以及不同位置做相应的执行命令回滚。
            # 兼容Sg.table和Special element方式
            # 处理鼠标wheel, 目前 （tablekey,x, y), "mousewheel", 不再需要兼容Sg.Table
            currenttable = event[0][0] if isinstance(event[0], tuple) else event[0]

            if event in needprocesslist:
                # 判断当前事件是否有影响现有数据并重新执行到新的行，
                executednumber = commandedit(event)

            mainwindow[currenttable].update(
                commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
                currentevent=event, currentwindow=mainwindow, currentvalues=values)

            # 执行完正常事件处理后，恢复已执行标记
            if event in needprocesslist:
                # 编辑完成后，恢复已执行命令行的颜色
                if executednumber is not None:
                    for item in range(executednumber):
                        # 修改已执行的命令的颜色
                        defaultcolor = (COMMAND_EXECUTED_COLOR, COMMAND_EXECUTED_BACKGROUND_COLOR)
                        mainwindow[commandtablekey].update(commandtype=SPECIAL_TABLE_SET_ROWCOLOR,
                                                           currentwindow=mainwindow, rownumber=item,
                                                           color=defaultcolor)

            continue

        elif event == RUN_LOG_SWITCH:
            logswithflag = mainwindow[LOG_FOR_DFTRANS].metadata
            if logswithflag:
                # 从True切换为False，关闭
                mainwindow[LOG_FOR_DFTRANS].metadata = False
                mainwindow[LOG_FOR_DFTRANS].update(visible=False, disabled=True)
                mainwindow[LOG_FOR_DFTRANS].restore_stdout()
                mainwindow[LOG_FOR_DFTRANS].restore_stderr()
                mainwindow[RUN_LOG_SWITCH].update(button_color='green')
                print("zoom in : nowsize:{}, targetsize:{}".format(mainwindow.size, originwindowsize))
                extendwindowsize = mainwindow.size
                mainwindow.size = originwindowsize
            else:
                # 从False切换为True， 打开
                mainwindow[LOG_FOR_DFTRANS].metadata = True
                mainwindow[LOG_FOR_DFTRANS].update(visible=True, disabled=False)
                mainwindow[LOG_FOR_DFTRANS].reroute_stdout_to_here()
                mainwindow[LOG_FOR_DFTRANS].reroute_stderr_to_here()
                mainwindow[RUN_LOG_SWITCH].update(button_color='red')
                # 第一次点击，同时窗口比原始窗口大，窗口自动扩展，同时记录扩展的size
                if extendwindowsize is None and \
                        mainwindow.size[1] > originwindowsize[1] \
                        and mainwindow.size[0] >= originwindowsize[0]:
                    print("reccord size : nowsize:{}, oldsize:{}, originsize:{}".format(
                        mainwindow.size, extendwindowsize, originwindowsize))
                    extendwindowsize = mainwindow.size
                else:
                    print("zoom out : nowsize:{}, targetsize:{}".format(mainwindow.size, extendwindowsize))
                    mainwindow.size = extendwindowsize

        elif event == RUN_LOG_SAVE:
            logcontent = mainwindow[LOG_FOR_DFTRANS].get()
            filetemp = Sg.popup_get_file('选择文件',
                                         save_as=True,
                                         file_types=(("日志文件", "*.log"),),
                                         initial_folder="D:/temp/",
                                         default_path="D:/temp/301temp.log",
                                         history_setting_filename="301temp.log",
                                         keep_on_top=True, modal=True,
                                         no_window=True, icon=LOCAL_SYSTEM_ICON)
            if filetemp:
                try:
                    with open(filetemp, 'w', encoding='utf8') as fp:
                        fp.write(logcontent)
                        fp.flush()
                        fp.close()
                        Sg.popup_ok("输出日志文件{}完成！".format(filetemp),
                                    modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)
                except Exception as err:
                    Sg.popup_error("错误", "写入日志文件{}出错：{}".format(filetemp, err),
                                   modal=True, keep_on_top=True, icon=LOCAL_SYSTEM_ICON)

        elif event == '-close-':
            # print("test windwos event send: step run")
            # mainwindow.write_event_value(COMMAND_STEPRUN_KEY, None)
            continue

        else:
            print("Get unknow event: {} and do nothing!".format(event))
            continue
    # 关闭窗口
    mainwindow.close()


def commmandstructurestringcheck():
    diff_a, diff_b = 0, 0
    for tempcommand, tempcommandconfig in commanddict.items():
        a, b, c, d = commandfunctionchoose2config(
            tempcommandconfig[COMMAND_FUNCTION_NAME],
            tempcommandconfig[COMMAND_TYPE],
            tempcommandconfig[COMMAND_NEW_TABLE_FLAG],
            tempcommandconfig[COMMAND_MULTI_DF_FLAG],
            tempcommandconfig[COMMAND_FUNCTION_PARAM]
        )

        if a != tempcommandconfig[COMMAND_FORMAT]:
            diff_a += 1
            print("-----------------------------------------------------")
            print("{}、{}--》format:{} , auto_a: {}, system_a:{}".format(
                diff_a,
                tempcommand, a == tempcommandconfig[COMMAND_FORMAT],
                a, tempcommandconfig[COMMAND_FORMAT]
            ))
        if b != tempcommandconfig[COMMAND_USED_INPUT_FORMAT]:
            diff_b += 1
            print("-----------------------------------------------------")
            print("{}、{}--》format:{} , auto_b: {}, system_b:{}".format(
                diff_b,
                tempcommand, b == tempcommandconfig[COMMAND_USED_INPUT_FORMAT],
                b, tempcommandconfig[COMMAND_USED_INPUT_FORMAT]
            ))
            # 临时自动更新基础文件配置，仅偶尔使用
            # commanddict[tempcommand][COMMAND_USED_INPUT_FORMAT] = b


def dynamicloadusermodule():
    # 动态import 用户自定义module
    try:
        # base_dir = os.path.join(os.getenv("LOCALAPPDATA"), useroperatedir)
        # sys.path.append(base_dir)
        # p = __import__(name, globals(), locals(), level=0)
        # globals()[name] = p.__dict__[name]
        # 使用__import__方法动态导入

        global usermodule
        # usermodule = __import__(USER_FUNCTION_MODULE, globals(), locals(), level=0,))
        # 先导入模块
        usermodule = importlib.import_module(USER_FUNCTION_MODULE)
        # 找到模块中的函数
        functions_list = [x[0] for x in getmembers(usermodule, isfunction)]
        # 将函数登记到globals() 和 locals()
        for name in functions_list:
            globals()[name] = usermodule.__dict__[name]
            locals()[name] = usermodule.__dict__[name]
            print("自定义模块加载函数：{}".format(name))
    except Exception as err:
        errstr = "动态加载用户module：{}失败：{}".format(USER_FUNCTION_MODULE, err)
        print("动态加载用户module：{}失败：{}".format(USER_FUNCTION_MODULE, err))
        if guiflag:
            Sg.popup_quick_message(errstr,
                                   modal=True, keep_on_top=True, text_color='white',
                                   background_color='dark blue')


def initialconfig():
    global originfunctiondict, commanddict, commandcombolist
    global usecolumnnameforprocess, commandcomment, commandalias, showversioninfo, ramfilesuffix
    global useroperatedict, manualbuttonoperatedict, useroperateconfig
    # 系统初始化，判断fileprocconfig是否存在，如果不存在，尝试从系统config目录（pip，python的安装目录拷贝），系统目录也不存在则报错退出
    # 判断本地目录是否存在fileprocconfig
    result = sys_data_files_copy(DFTRANS_SYSTEM_DATA_FILES)
    if result[0] is False:
        print(result[1])
        sys.exit(-1)

    # 读取配置文件
    try:
        with open(fileprocconfig, 'r', encoding='utf8') as fp:
            fileprocdic = json.load(fp)
            fp.close()
    except Exception as err:
        print("读取配置文件：{}失败：{}".format(fileprocconfig, err))
        sys.exit(-1)
    # 获取底层的函数说明字典
    originfunctiondict = fileprocdic.get("originfunctiondict", None)
    if originfunctiondict is None:
        print("{}配置文件内容不符！\n {}".format(fileprocconfig, fileprocdic))
        sys.exit(-1)

    # 获取命令说明字典
    commanddict = fileprocdic.get("commanddict", None)
    if commanddict is None:
        print(fileprocdic)
        print("{}配置文件内容不符！\n {}".format(fileprocconfig, fileprocdic))
        sys.exit(-1)

    commandcomment = fileprocdic.get("commandcomment", {})

    commandalias = fileprocdic.get("commandalias", {})

    usecolumnnameforprocess = fileprocdic.get("usecolnameforprocess", False)
    print("use column name for proessing:{}".format(usecolumnnameforprocess))

    showversioninfo = fileprocdic.get("showversioninfo", True)
    print("show verison :{}".format(showversioninfo))

    ramfilesuffix = fileprocdic.get("ramfilesuffix", "RAMFS")
    print("ram file directory :{}".format(ramfilesuffix))
    # # 创建用于交换内部数据的内存文件目录， pyfakefs方式会完全替代现有fs，不适用。
    # try:
    #     patcher = Patcher()
    #     patcher.setUp()
    #     os.mkdir(ramfilesuffix)
    # except Exception as err:
    #     print("创建内存文件目录{}失败：{}".format(ramfilesuffix, err))

    # 形成所有命令的清单
    commandcombolist = list(commanddict)
    global commandmenudict
    commandmenudict = {
        COMMAND_ROW_PROCESS: [],
        COMMAND_COLUMN_PROCESS: [],
        COMMAND_SINGLE_DF_PROCESS: [],
        COMMAND_TWO_DF_PROCESS: [],
        COMMAND_MULTI_DF_PROCESS: [],
        COMMAND_NEW_TABLE_IMPORT: [],
        COMMAND_OTHER: []
    }
    # 形成所有命令对应的菜单, 将命令根据分类先形成分类字典
    for key, value in commanddict.items():
        # 跳过配置为不显示的命令的菜单
        if getcommandconfig(key, menuflag=True) is None:
            continue
        ret = commandmenudict.get(value[COMMAND_TYPE], None)
        if ret is not None:
            ret.append(key)
    # 根据字典形成二级菜单list
    global commandmenulist, datatablebuttonmenuevent, datatablerightclickevent
    commandmenulist = []
    datatablebuttonmenuevent = []
    datatablerightclickevent = []
    for key, value in commandmenudict.items():
        commandmenulist.append([key, value])
        datatablebuttonmenuevent.append(key)
        datatablerightclickevent.extend(value)

    dynamicloadusermodule()

    if guiflag:  # 图形方式下，读取用户操作记录配置
        # 读取用户配置文件
        # useroperateconfig
        try:
            # 获取用户localdata目录, 创建程序数据目录和配置文件
            useroperatepath = os.path.join(os.getenv("LOCALAPPDATA"), useroperatedir)
            useroperateconfig = os.path.join(useroperatepath, userconfigfile)
            # 判断目录是否存在
            if os.path.exists(useroperatepath) is False:
                os.makedirs(useroperatepath)
            # 如果文件不存在，就创建文件
            if Path(useroperateconfig).is_file() is False:
                # 创建用户配置文件并写入初始空值
                with open(useroperateconfig, 'w', encoding='utf8') as fp:
                    json.dump({"useroperatedict": originfunctiondict, "manualbuttonoperatedict": {}},
                              fp, ensure_ascii=False, sort_keys=False, indent=4)
                    fp.close()
                    infostr = "用户配置文件{}不存在, 已重新创建!".format(useroperateconfig)
                    print(infostr)
                    Sg.popup_quick_message(infostr,
                                           modal=True, keep_on_top=True, text_color='white',
                                           background_color='dark blue')
            with open(useroperateconfig, 'r', encoding='utf8') as fp:
                userfileprocdic = json.load(fp)
                fp.close()
                infostr = "用户配置文件{}读取完成!".format(useroperateconfig)
                print(infostr)
                # Sg.popup_quick_message(infostr,
                #                        modal=True, keep_on_top=True, text_color='white',
                #                        background_color='dark blue')
        except Exception as err:
            print("读取用户记录文件：{}失败：{}".format(useroperateconfig, err))
            sys.exit(-1)
        # 获取底层的函数说明字典
        useroperatedict = userfileprocdic.get("useroperatedict", None)
        # 获取界面手工按钮的记录字典
        manualbuttonoperatedict = userfileprocdic.get("manualbuttonoperatedict", None)
        if useroperatedict is None:
            print("{}用户记录文件内容不符！\n {}".format(useroperateconfig, userfileprocdic))
            sys.exit(-1)

    return


def DF_Trans_main(*args, **kwargs):
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
    print("result sys.argv:{}".format(sys.argv))


    # 获取命令参数
    # print(sys.path)

    # 默认输入文件名list
    warnings.filterwarnings('ignore')
    inputfilesdefault = []
    inputstringcolumns = []

    # 是否打印print调试信息
    debugswitchdefault = 'n'

    # 是否gui方式运行
    guiswitchdefault = 'n'

    # gui方式下，初始化，是否全速运行
    guiglobalrunflag = 'n'

    # 是否检测空值替换为NaN
    nancheckdefault = 'n'

    # 默认的模板拷贝输出区域坐标
    # 源数据，目的数据范围，开始、结束行号、开始结束列号、目标起始行、列号
    modelcopyblockscaledefault = [0, -1, 0, -1, 0, 0]

    # 默认输入批量文件的文件名清单
    inputinfofiledefault = []
    # 输出模板文件名 [输出文件名，子表号，表首行数，表尾行数]
    modelfiledefault = ["", "0", "0", "0"]
    # 默认输出文件名
    resultdefault = ""

    skiplinedefault = 0
    taillinedefault = 0
    headingsdefault = 0
    commandlistdefault = ""

    print("默认输入参数：{}".format(sys.argv[1:]))
    # 设置各个参数
    parser = argparse.ArgumentParser(description='Excel文件处理工具')
    # 输入文件大于0，文件名list，当只有一个文件时，复制该文件的数据，删除尾部
    parser.add_argument('-i', '-input', nargs="+", type=str, default=inputfilesdefault,
                        help='输入Excel文件（至少1个）, 默认值：{}'.format(inputfilesdefault))

    parser.add_argument('-l', '-stringcolumns', nargs="+", type=str, default=inputstringcolumns,
                        help='输入Excel文件的字符串列信息, 表格之间""分装, 表格内字符串用逗号分隔, 默认值：{}'.format(inputstringcolumns))

    # 输入文件清单文件:json
    parser.add_argument('-f', '-inputinfofile', nargs=2, type=str, default=inputinfofiledefault,
                        help='输入Excel文件的清单文件json及字典项, 默认值：{}'.format(inputinfofiledefault))
    # -f方式下，有两个输入参数：输入配置json文件、输入文件归类关键字；输入配置文件为json格式, 示例的格式可以如下：
    # {
    #   “files”: [“d:\temp\a.xlsx”, “d:\temp\b.xlsx”],
    #   “files-string-columns”: [[“test1”, “test2”], []]
    # }
    # 如果配置文件名为d:\temp\inputfile.json的示例等效命令为：
    # DFTrans.exe - f d:\temp\inputfile.json files - o  d:\temp\c.xlsx - c  d:\temp\command.jsonl
    # 命令的上游软件，只需要动态生成相应的输入配置json，对应双方约定好的配置文件名和内部关键字，就可以和本软件无缝衔接
    # 当 -g n后台全速运行时，可能希望多次循环相同的操作输出不同的结果，可以对上述json文件做如下配置，
    #  假设需要循环3轮，每轮都是在命令清单中输出“d:\temp\aoutput.xlsx”, “d:\temp\aoutput.xlsx”，
    #  其中“test1”, “test2”列需要按string方式导入：
    # {
    #   “files”: 3,
    #   “files-output”:[“d:\temp\aoutput.xlsx”, “d:\temp\boutput.xlsx”],
    #   “files1”: [“d:\temp\a1.xlsx”, “d:\temp\b1.xlsx”],
    #   “files-string-columns1”: [[“test1”, “test2”], []],
    #   “files2”: [“d:\temp\a2.xlsx”, “d:\temp\b2.xlsx”],
    #   “files-string-columns2”: [[“test1”, “test2”], []],
    #   “files3”: [“d:\temp\a3.xlsx”, “d:\temp\b3.xlsx”],
    #   “files-string-columns3”: [[“test1”, “test2”], []]
    # }
    # 以上配置文件，DFTrans.exe - g n - f d:\temp\inputfile.json files - c d:\temp\command.jsonl执行后，三轮输出的文件名为：
    # [“d:\temp\aoutput_files1.xlsx”, “d:\temp\boutput_files1.xlsx”]
    # [“d:\temp\aoutput_files2.xlsx”, “d:\temp\boutput_files2.xlsx”]
    # [“d:\temp\aoutput_files3.xlsx”, “d:\temp\boutput_files3.xlsx”]

    # 命令清单文件
    parser.add_argument('-c', '-command', type=str, default=commandlistdefault,
                        help='需执行的命令文件, 默认值：{}'.format(commandlistdefault))

    # 输出模板文件
    parser.add_argument('-m', '-model', nargs=4, type=str, default=modelfiledefault,
                        help='输出结果Excel文件及行首行尾数[输出文件名，子表号，表首行数，表尾行数], 表首表尾均为-1表示拷贝方式，默认值：{}'.format(
                            modelfiledefault))

    # 模板拷贝方式输出的源数据，目的数据范围，开始、结束行号、开始结束列号、目标起始行、列号
    parser.add_argument('-b', '-block', nargs=6, type=int, default=modelfiledefault,
                        help='源数据开始与结束行号、开始与结束列号、目标起始行、列号，默认值：{}'.format(
                            modelcopyblockscaledefault))

    parser.add_argument('-o', '-output', type=str, default=resultdefault,
                        help='输出结果Excel文件，默认值：{}'.format(resultdefault))

    # 表头跳过行数
    parser.add_argument('-s', '-skipline', type=int, default=skiplinedefault,
                        help='表头行数, 默认值：{}'.format(skiplinedefault))

    # 列名所在行数
    parser.add_argument('-n', '-headnameline', type=int, default=headingsdefault,
                        help='列名行数, 默认值：{}'.format(headingsdefault))

    # 表尾行数
    parser.add_argument('-t', '-tailline', type=int, default=taillinedefault,
                        help='表尾行数, 默认值：{}'.format(taillinedefault))

    # 是否打印调试信息
    parser.add_argument('-d', '-debugswitch', type=str, choices=("y", "n"), default=debugswitchdefault,
                        help='是否打印调试信息, 默认值：{}'.format(debugswitchdefault))

    # 是否gui运行
    parser.add_argument('-g', '-guiswitch', type=str, choices=("y", "n"), default=guiswitchdefault,
                        help='是否运行gui界面, 默认值：{}'.format(guiswitchdefault))

    # gui方式下，导入初始command文件后，是否全速运行
    parser.add_argument('-r', '-guiglobalrun', type=str, choices=("y", "n"), default=guiglobalrunflag,
                        help='gui方式下初始化全速运行, 默认值：{}'.format(guiglobalrunflag))


    # 是否检测空值赋值为NaN（np.nan)运行
    parser.add_argument('-v', '-nancheck', type=str, choices=("y", "n"), default=nancheckdefault,
                        help='是否检测空值并转换为NaN, 默认值：{}'.format(nancheckdefault))

    args, argv = parser.parse_known_args()
    if argv:
        print("命令错误，未知option：{}".format(argv))
        return 206
    args = parser.parse_args()

    global myinputfiles
    myinputfiles = [args.i]
    tempstringcolumns = args.l
    if tempstringcolumns == []:
        myinputstringcolumns = [[]]
    else:
        myinputstringcolumns = [[x.split(",") if len(x.strip()) > 0 else [] for x in tempstringcolumns]]
    myinputinfofile = args.f
    global mycommandlistfile
    mycommandlistfile = args.c
    myresultfile = [args.o]
    resultfilerenameflag = False
    renameaddtioninfo = ""
    mymodelfilelist = args.m
    mymodelcopyscale = args.b
    myskipline = args.s
    mytailline = args.t
    myheadline = args.n if args.n >= 0 else None
    mydebugswitch = args.d.lower()
    myguiswitch = args.g.lower()
    global debugflag
    debugflag = True if mydebugswitch == 'y' else False
    global guiflag
    guiflag = True if myguiswitch in ['y'] else False
    myglobalrunswitch = True if args.r.lower() == 'y' and mycommandlistfile != "" and guiflag else False
    mynafilter = True if args.v.lower() == 'y' else False
    usingcopymodel = False

    mymodelfile = mymodelfilelist[0]
    try:
        mymodelsheetnumber = int(mymodelfilelist[1])
        mymodelskipline = int(mymodelfilelist[2])
        mymodeltailline = int(mymodelfilelist[3])
        # 当模板表首、表尾均为-1时，使用拷贝方式输出
        if [mymodelskipline, mymodeltailline] == [-1, -1]:
            usingcopymodel = True
    except Exception as err:
        print("模板文件信息{}中子表号或则首尾行数不正确：{}".format(mymodelfilelist, err))
        return 206

    # 非图形方式下，如果输入的文件名和默认值一致，说明用户没有命令行输入文件名，而是使用fileinfo或者在jsonl文件里面导入文件。
    if myguiswitch == 'n' and myinputfiles == inputfilesdefault:
        myinputfiles = []

    fileok = True
    # 首先判断是否有 -f
    templen = len(myinputinfofile)
    if templen == 2:  # 有-f输入
        # -f 对应的输入文件不存在 或者内存文件
        if True not in [Path(myinputinfofile[0]).is_file(), is_mem_virtual_file_exist(myinputinfofile[0])]:
            print("输入信息文件{}不存在!".format(myinputinfofile[0]))
            return 201
        else:
            # 读取输入文件清单文件，如果数据合法，则放弃 -i 的输入
            # 读取配置文件
            try:
                # 是内存文件
                if is_mem_virtual_file_exist(myinputinfofile[0]):
                    print("读取输入信息内存虚拟文件{}......".format(myinputinfofile[0]))
                    inputdic = dict(load_object_from_virtual_file(myinputinfofile[0]))
                else:  # 是json配置文件
                    print("读取输入信息文件{}......".format(myinputinfofile[0]))
                    with open(myinputinfofile[0], 'r', encoding='utf8') as fp:
                        inputdic = json.load(fp)
                        fp.close()
            except Exception as err:
                print("读取配置文件：{}失败：{}".format(myinputinfofile[0], err))
                return 202
            # 读取信息中对应字典项的文件清单
            if myinputinfofile[1] not in inputdic.keys():
                print(inputdic)
                print("{}配置文件内容不符，{}没有 {} 项！\n".format(myinputinfofile[0], inputdic, myinputinfofile[1]))
                return 203

            # 判断文件清单是否合法
            # 获取输入json文件key的内容，如果是数字，表示循环次数，如果不是，直接作为myinputfiles
            tempvalue = inputdic.get(myinputinfofile[1], [])
            # 如果key的value是int，表示要循环，获取合理的循环值，如果key不是int而是list，直接作为输入文件列表
            if isinstance(tempvalue, int):
                if tempvalue <= 0:
                    print("配置文件{}错误：key:{}（循环次数）不合法！".format(myinputinfofile, tempvalue))
                    return 201
                resultfilerenameflag = True
                renameaddtioninfo = "_" + myinputinfofile[1]
                # 判断针对循环次数的所需要key是否存在
                allkey = [myinputinfofile[1] + str(x) for x in range(1, tempvalue + 1)]
                if not set(allkey).issubset(set(list(inputdic))):
                    print("配置文件{}错误：key:{}在文件key：{}中部分缺失！".format(myinputinfofile, allkey, list(inputdic)))
                    return 201
                myinputfiles, myinputstringcolumns = [], []
                # 根据循环次数获取每次循环的文件清单和对应的stringcolumns
                for basekey in allkey:
                    myinputfiles.append(inputdic.get(basekey, []))
                    # 当前清单数目合法性检查（文件名不能为空）
                    if len(myinputfiles[-1]) > 0 and "" not in [x.strip() for x in myinputfiles[-1]]:
                        print("使用{}配置的输入文件{}".format(myinputinfofile, myinputfiles))
                    else:
                        print("配置信息{}对应的文件数目不正确{}".format(myinputinfofile, myinputfiles[-1]))
                        return 201
                    myinputstringcolumns.append(inputdic.get(basekey + INPUTFILE_SRTING_COLUMNS, []))
                # 如果-f没有配置输入文件名，直接使用命令行参数的输入作为输出
                myresultfile = inputdic.get(myinputinfofile[1] + OUTPUTFILE_RENAME_KEY, [args.o])
            elif isinstance(tempvalue, list):
                myinputfiles = [tempvalue]
                # 确定是否有强制按字符串读取的列
                myinputstringcolumns = [inputdic.get(myinputinfofile[1] + INPUTFILE_SRTING_COLUMNS, [])]
            else:
                print("配置文件{}错误：key:{}不是整型（循环次数）或者列表（文件清单）！".format(myinputinfofile, tempvalue))
                return 201
            print("获取{} 文件 {} ：{}".format(myinputinfofile[0], myinputinfofile[1], myinputfiles))
    elif templen != 0 and myguiswitch != 'c':
        print("输入清单配置文件{}参数不正确".format(myinputinfofile))
        fileok = False

    # 判断string columns的个数（如果存在） 是否和输入文件名一致
    for item in range(len(myinputfiles)):
        if myinputstringcolumns[item] not in [[], None] and len(myinputstringcolumns[item]) != len(myinputfiles[item]):
            print("输入文件名称{}和强制字符串配置{}个数不一致".format(myinputfiles[item], myinputstringcolumns[item]))
            return 201

    # 如果是图形模式，只保留myinputfiles\myinputstringcolumns的第一组数据
    if myguiswitch in ['y']:  # -g y 只读取第一轮文件
        myinputfiles = myinputfiles[:1]
        myinputstringcolumns = myinputstringcolumns[:1]

    # 判断每个输入文件是否存在
    for filegroup in myinputfiles:
        for tempfile in filegroup:
            if not (Path(tempfile).is_file() or is_mem_virtual_file_exist(tempfile)):
                print("输入文件{}不存在!".format(tempfile))
                fileok = False

    if fileok is False:
        print("Excel处理所需文件不全！")
        return 201

    # 读取系统配置信息
    initialconfig()

    # 根据myinputfiles 和stringcloumns进行循环, 图形方式下，只有一次循环
    for mainloopitem in range(len(myinputfiles)):
        currentmyinputfiles, currentmyinputstringcolumns = \
            myinputfiles[mainloopitem], myinputstringcolumns[mainloopitem]
        if guiflag and showversioninfo:
            Sg.popup_quick_message('DFTrans v2.0.0\n\n稍等, 调取配置数据....',
                                   title="数据批量处理工具",
                                   auto_close=True,
                                   non_blocking=True,
                                   font='Default 10',
                                   keep_on_top=True,
                                   auto_close_duration=2,
                                   modal=True,
                                   no_titlebar=True,
                                   image=LOCAL_SYSTEM_IMAGE,
                                   icon=LOCAL_SYSTEM_ICON)

        # 读取数据文件到对应的specialdflist[n]
        global specialdflist, specialdflistcopy
        specialdflist = []
        for item, currentfile in enumerate(currentmyinputfiles):
            try:
                # # 读取时跳过表头行和表尾行
                print("读取文件{}......".format(currentfile))
                # 首先判断是否内存对象虚拟文件
                if is_mem_virtual_file_exist(currentfile):
                    print("读取内存虚拟文件{}......".format(currentfile))
                    tempdf = pd.DataFrame(load_object_from_virtual_file(currentfile))
                else:
                    if currentmyinputstringcolumns not in [None, []]:
                        tempcolumns = [x.strip() for x in currentmyinputstringcolumns[item]]
                        if tempcolumns not in [None, []] and isinstance(tempcolumns, list):
                            dtype = dict(zip(tempcolumns, [str for _ in range(len(tempcolumns))]))
                        else:
                            dtype = None
                    else:
                        dtype = None
                    print("读取文件{}， dtype:{}......".format(currentfile, dtype))
                    tempdf = pd.read_excel(currentfile,
                                           dtype=dtype,
                                           na_filter=mynafilter,
                                           header=myheadline,
                                           skiprows=myskipline,
                                           skipfooter=mytailline,
                                           sheet_name=0)

                # head需要转换为str以便后续处理
                tempdf.columns = tempdf.columns.map(str)
                specialdflist.append(SpecialDf(dfdata=tempdf))

            except Exception as err:
                print("读取第{}个文件：{}失败：{}".format(item, currentfile, err))
                return 202


        # 检查命令配置文件中命令结构串和命令记录串的语法结构
        commmandstructurestringcheck()

        # 读取命令文件
        loadcommandfile(initialflag=True)

        global dfcurrentprefix
        dfcurrentprefix = 'specialdflist'

        if guiflag:
            # 调用GUI界面
            # 保存原始数据的完整拷贝以备重置使用
            specialdflistcopy = [copy.deepcopy(specialdfitem) for specialdfitem in specialdflist]
            commandeditgui(totalprocesslist, dfcurrentprefix=dfcurrentprefix, globalrunflag=myglobalrunswitch)
        else:
            # 非GUI，直接运行命令清单文件并根据输出模板信息输出最后的df文件到结果文件
            # 判断是否有命令文件
            if mycommandlistfile == "":
                print("命令文件（jsonl）不能为空！")
                sys.exit(-1)
            print("循环{}:将{}按{}命令批处理处理生成文件{}......".format(
                mainloopitem + 1, currentmyinputfiles, mycommandlistfile, myresultfile))
            noguistarttime = datetime.now()
            if globalcommandrun(method=ALL_RUN):
                # 数据处理成功，开始导出
                starttime = datetime.now()
                # 对于-o的输出，使用args.o，当args.o不为空时输出文件
                result = True
                if args.o != "":
                    if not usingcopymodel:
                        # 模板赋值方式输出
                        result = savedatatofile(
                            args.o, len(specialdflist) - 1, sheetnumber=mymodelsheetnumber,
                            modelfilename=mymodelfile, headline=mymodelskipline, tailline=mymodeltailline)
                    else:
                        # 模板拷贝方式输出
                        result = savedatablocktofile(
                            args.o, len(specialdflist) - 1, sheetnumber=mymodelsheetnumber, modelfilename=mymodelfile,
                            sourcestartendrows=[mymodelcopyscale[0], mymodelcopyscale[1]],
                            sourcestartendcols=[[mymodelcopyscale[2], mymodelcopyscale[3]], ["", ""]],
                            targetstartrow=[mymodelcopyscale[4]],
                            targetstartcol=[mymodelcopyscale[5], [""]])
                # 根据配置将命令清单方式输出的文件更名加上key+loopnumber，只有-f resultfilerenameflag 才更名
                if resultfilerenameflag:
                    for originalfile in myresultfile:
                        try:
                            # x = "d:/temp/b/b.xlsx"
                            # os.path.basename(x)  -> 'b.xlsx'
                            # os.path.dirname(x) -> 'd:/temp/b'
                            filenamesplitlist = os.path.basename(originalfile).split(".")
                            targetfile = os.path.join(
                                os.path.dirname(originalfile),
                                ".".join([
                                    ".".join(filenamesplitlist[:-1]) + renameaddtioninfo + str(mainloopitem + 1),
                                    filenamesplitlist[-1]
                                ])
                            )
                            # 更名
                            print("循环{}:将文件{}更名为：{}".format(mainloopitem + 1, originalfile, targetfile))
                            shutil.move(originalfile, targetfile)
                        except Exception as err:
                            print("循环{}:将文件{}更名失败：{}".format(mainloopitem + 1, originalfile, err))
                            return 204
                endtime = datetime.now()
                if result:
                    print("循环{}:将{}按{}命令批处理生成文件{}完成，用时{}！".format(
                        mainloopitem + 1, currentmyinputfiles, mycommandlistfile, myresultfile, endtime - starttime))
                else:
                    print("循环{}:将{}按{}命令批处理，生成文件{}时出错！".format(
                        mainloopitem + 1, currentmyinputfiles, mycommandlistfile, myresultfile))
                    return -1
            else:
                print("循环{}:将{}按{}命令批处理，执行命令时出错！".format(
                    mainloopitem + 1, currentmyinputfiles, mycommandlistfile))
                return -1
            print("循环{}:将{}按{}命令批处理处理生成文件{}执行完成，共耗时:{}".format(
                mainloopitem + 1, currentmyinputfiles, mycommandlistfile,
                myresultfile, datetime.now() - noguistarttime))

    return 0


if __name__ == "__main__":
    sys.exit(DF_Trans_main())

