# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as Sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from enum import Enum
from psgspecialelements import *
import sys
from dataclasses import dataclass
import datacompy
import copy
import os

from openpyxl import load_workbook
from sqlalchemy import create_engine
from sqlalchemy.sql import default_comparator           # 必须加上否则nuikta编译后，找不到模块。并且需要好安装1.4.40版本
import shutil
import time

import inspect

import ast


class PlotType(Enum):
    PLOT = "折线图"                # 'line'
    BAR = "直方图"                 # 'bar'
    BARH = "横向条形图"             # 'barh'
    HIST = "柱状图"                # 'hist'
    BOX = "箱线图"                 # 'box'
    KDE = "密度估计图"              # 'kde' = ‘density’
    AREA = "面积区域图"             # 'area'
    PIE = "饼图"                   # 'pie'
    SCATTER = "散点图"             # 'scatter'
    HEXBIN = "蜂巢图"              # 'hexbin'


plottype2kinddict = {
    PlotType.PLOT: 'line',
    PlotType.BAR: 'bar',
    PlotType.BARH: 'barh',
    PlotType.HIST: 'hist',
    PlotType.BOX: 'box',
    PlotType.KDE: 'kde',
    PlotType.AREA: 'area',
    PlotType.PIE: 'pie',
    PlotType.SCATTER: 'scatter',
    PlotType.HEXBIN: 'hexbin'
}


plottypevalue2kinddict = {
    "折线图": 'line',
    "直方图": 'bar',
    "横向条形图": 'barh',
    "柱状图": 'hist',
    "箱线图": 'box',
    "密度估计图": 'kde',
    "面积区域图": 'area',
    "饼图": 'pie',
    "散点图": 'scatter',
    "蜂巢图": 'hexbin'
}


# DataFrame.plot([x, y, kind, ax, …])
# DataFrame.plot.area([x, y])
# DataFrame.plot.bar([x, y])
# DataFrame.plot.barh([x, y])
# DataFrame.plot.box([by])
# DataFrame.plot.density([bw_method, ind])
# DataFrame.plot.hexbin(x, y[, C, …])
# DataFrame.plot.hist([by, bins])
# DataFrame.plot.kde([bw_method, ind])
# DataFrame.plot.line([x, y])
# DataFrame.plot.pie(**kwargs)
# DataFrame.plot.scatter(x, y[, s, c])
# DataFrame.boxplot([column, by, ax, …])
# DataFrame.hist([column, by, grid, …])
# x : 横向标记位置,默认为None
# y : 纵向标记位置,默认为None
# kind 参数 : 绘制类型(字符串)
# ‘kind=line’ : 折线图模式
# ‘kind=bar’ : 纵向条形图模式
# ‘kind=barh’ : 横向条形图模式
# ‘kind=hist’ : 柱状图模式
# ‘kind=box’ : 箱线图模式
# ‘kind=kde’ : 密度估计图模式
# ‘kind=area’ : 面积区域图模式
# ‘kind=pie’ : 饼图模式
# ‘kind=scatter’ : 散点图模式
# ‘kind=hexbin’ : 蜂巢图模式
# df.plot(kind='line',color='b',title='数据变化')
# df.plot(kind='bar', title ="", figsize=(8, 5), legend=True, fontsize=12)
# df.plot 参数
# ax : 子图(如果没有设置，则使用当前matplotlib subplot**)
# subplots : 图片中是否有子图,默认为False
# sharex : 如果ax为None，则默认为True，否则为False
# sharey : 默认为False如果有子图，子图共y轴刻度，标签
# layout : 子图的行列布局
# figsize : 图片尺寸大小
# use_index : 默认为False,默认用索引做x轴
# title : 图片的标题用字符串
# grid : 默认为None,图片是否有网格
# legend : 子图图例,默认为True
# style : 每列折线图设置线的类型
# logx : 默认为False,设置x轴刻度是否取对数
# loglog : 默认为False,同时设置x，y轴刻度是否取对数
# xticks : 设置x轴刻度值，序列形式
# yticks : 设置y轴刻度值，序列形式
# xlim : 设置坐标轴的范围
# ylim : 设置坐标轴的范围
# rot : 默认为None,设置轴标签的显示旋转度数
# fontsize : 默认为None,设置轴刻度的字体大小
# colormap : 默认为None,设置图的区域颜色
# colorbar : 图片柱子
# position : 取值范围[0,1],默认为0.5表示中间对齐,设置图的区域颜色
# layout : 布局,几行几列
# table : 默认为False,选择DataFrame类型的数据并且转换匹配matplotlib的布局
# yerr : DataFrame, Series, array-like, dict and str
# xerr : same types as yerr.
# stacked : boolean, default False in line and
# sort_columns : 默认为False,对列名称进行排序,默认使用前列顺序
# secondary_y : 默认为False,是否要设置第二个Y轴
# mark_right : 默认为True,在使用第二个Y轴时在Y轴上的标签
# plt:
# plt.title("Georgia: true and predicted data at Phase 2 (EB-WB), 5 min")
# plt.xlabel('Time',labelpad=2)
# plt.ylabel('AOG')
# plt.legend(loc='best',fancybox=True)
# plt.grid(True)
# plt.xlim(0,288)
# plt.ylim(0,80)
# plt.show()


@dataclass
class DfsubPlot(object):
    dfdata: pd.DataFrame = None
    plottype: PlotType = None
    valuecolumns: list[list[int], list[str]] = None
    indexcolumn: list[list[int], list[str]] = None
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    showflag: bool = True

    """
    将数据dataframe根据配置绘制图表
    :param dfdata:                  pd.DataFrame 用于显示的df
    :param plottype:                str： 绘制的图标类型
    :param valuecolumns:            list[list[int], list[str]]: 数据值所在列序号、列名
    :param indexcolumn:             list[list[int], list[str]]:  用于标记X轴的值列号、列名，仅第一个有效
    :param title:                   str: 图形标题
    :param xlabel:                  str: x轴的名称
    :param ylabel:                  str：y轴的名称
    :param showflag:                bool: 是否显示图片
    :return:
    """
    def __post_init__(self):
        # 获取显示部分的df
        if self.valuecolumns is None:  # None表示所有列(除索引列)作为值列
            templist = self.dfdata.columns.tolist()
            # 将索引列从整个列名中剔除
            templist.remove(self.indexcolumn[1][0])
            # 形成列序号、列名的list（对应于dfdata）
            self.valuecolumns = [[self.dfdata.columns.tolist().index(x) for x in templist], templist]
        self.dfshowdata = self.dfdata[self.valuecolumns[1]]
        # x轴的值列赋值为图表df的index
        self.dfshowdata.index = self.dfdata[self.indexcolumn[1][0]].values
        # 初始化画板
        self.figure, self.ax = plt.subplots()
        # 确定图标类型
        if self.plottype == PlotType.PLOT:
            # 设置显示格式
            self.dfshowdata.plot(ax=self.ax, style='--o')
        elif self.plottype == PlotType.BAR:
            self.dfshowdata.plot.bar(ax=self.ax)
        # 设置显示参数
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 图中字体改为黑体以兼容中文
        plt.rcParams['axes.unicode_minus'] = False  # 负号显示的问题
        # 设置x，y轴的名称
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        if self.showflag:
            plt.show()

    def save_figure(self, filename):
        self.figure.savefig(filename, bbox_inches='tight')

    def get_figure(self):
        return self.figure


@dataclass
class DfPlot(object):
    dfdata: pd.DataFrame = None
    plottype: PlotType = None
    valuecolumns: list[list[int], list[str]] = None
    indexcolumn: list[list[int], list[str]] = None
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    figsize: tuple = (8, 6)         # 英寸
    grid: bool = False
    legend: bool = True
    stacked: bool = False
    showflag: bool = True
    subplots: bool = False
    sharex: bool = False
    sharey: bool = False
    use_index: bool = True
    logx: bool = False
    logy: bool = False
    secondary_y: bool = False
    mark_right: bool = True

    """
    将数据dataframe根据配置绘制图表
    :param dfdata:                  pd.DataFrame 用于显示的df
    :param plottype:                str： 绘制的图标类型
    :param valuecolumns:            list[list[int], list[str]]: 数据值所在列序号、列名
    :param indexcolumn:             list[list[int], list[str]]:  用于标记X轴的值列号、列名，仅第一个有效
    :param title:                   str: 图形标题
    :param xlabel:                  str: x轴的名称
    :param ylabel:                  str：y轴的名称
    :param figsz:                   tuple(int, int): 图像宽度和高度
    :param grid:                    bool: 是否显示网格
    :param legend:                  bool: 是否显示图例
    :param stacked:                 bool: 是否堆叠
    :param showflag:                bool: 是否单独显示图片
    :param subplots:                bool: 是否显示子图
    :param sharex:                  bool: 如果subplots=True, 如果有子图，子图共x轴刻度。
    :param sharey:                  bool: 如果subplots=True, y轴被隐藏.
    :param use_index:               bool: 默认 True 是否使用索引作为x轴的刻度
    :param logx:                    bool: default False 设置x轴刻度是否取对数
    :param logy:                    bool: default False 设置y轴刻度是否取对数
    :param secondary_y:             bool or sequence default False 置第二个y轴（右y轴）
    :param mark_right :             bool, default True, secondy_y 有值时，mark的位置是否右侧
    :return:
    """
    def __post_init__(self):
        # 获取显示部分的df
        if self.valuecolumns is None:  # None表示所有列(除索引列)作为值列
            templist = self.dfdata.columns.tolist()
            # 将索引列从整个列名中剔除
            templist.remove(self.indexcolumn[1][0])
            # 形成列序号、列名的list（对应于dfdata）
            self.valuecolumns = [[self.dfdata.columns.tolist().index(x) for x in templist], templist]
        self.dfshowdata = self.dfdata[self.valuecolumns[1]]
        # x轴的值列赋值为图表df的index
        self.dfshowdata.index = self.dfdata[self.indexcolumn[1][0]].values
        # 初始化画板
        self.figure = plt.figure(facecolor="lightgrey")
        self.ax = self.figure.add_subplot(1, 1, 1)
        try:
            self.dfshowdata.plot(
                ax=self.ax,
                kind=plottypevalue2kinddict[self.plottype],
                title=self.title,
                grid=self.grid,
                legend=self.legend,
                stacked=self.stacked,
                figsize=self.figsize,
                subplots=self.subplots,
                sharex=self.sharex,
                sharey=self.sharey,
                use_index=self.use_index,
                logx=self.logx,
                logy=self.logy,
                secondary_y=self.secondary_y,
                mark_right=self.mark_right
            )
            # 如果 plt.figure(figsize=(10,5)) 不起作用，
            # 因为 df.plot() 创建了自己的 matplotlib.axes.Axes 对象，创建对象后 无法更改其大小。
            # 可以在创建之前更改默认值 figsize ，方法是使用 plt.rcParams["figure.figsize"] = (width, height) 更改默认图大小
            # 设置显示参数 TODO: 暂时没有找到调整子图大小的方式
            # plt.subplots(figsize=(20, 20))
            # plt.subplots(width_ratios=2, height_ratios=2)
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 图中字体改为黑体以兼容中文
            plt.rcParams['axes.unicode_minus'] = False  # 负号显示的问题
            # # 设置x，y轴的名称
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)

            if self.showflag:
                plt.show()
        except Exception as err:
            print("plot error:{}".format(err))

    def save_figure(self, filename):
        self.figure.savefig(filename, bbox_inches='tight')

    def get_figure(self):
        return self.figure


@dataclass
class ExcelPlot(object):
    filename: str = ""
    sheetname: int = 0
    plottype: PlotType = None
    valuecolumns: list[str] = None
    indexcolumn: int = 0
    xlabel: str = ""
    ylabel: str = ""
    showflag: bool = True
    subplots: bool = False
    sharex: bool = False
    sharey: bool = False
    use_index: bool = True
    logx: bool = False
    logy: bool = False
    secondary_y: bool = False
    mark_right: bool = True
    """
    将数据excel文件根据配置绘制图表
    :param filename:                str： 数据文件名
    :param sheetname:               int:  数据子表号
    :param plottype:                str： 绘制的图标类型
    :param valuecolumns:            list[str]: 数据值所在列名
    :param indexcolumn:             int:  用于标记X轴的值列
    :param xlabel:                  str: x轴的名称
    :param ylabel:                  str：y轴的名称
    :param showflag:                bool: 是否显示图片
    :param subplots:                bool: 是否显示子图
    :param sharex:                  bool: 如果subplots=True, 如果有子图，子图共x轴刻度。
    :param sharey:                  bool: 如果subplots=True, y轴被隐藏.
    :param use_index:               bool: 默认 True 是否使用索引作为x轴的刻度
    :param logx:                    bool: default False 设置x轴刻度是否取对数
    :param logy:                    bool: default False 设置y轴刻度是否取对数
    :param secondary_y:             bool or sequence default False 置第二个y轴（右y轴）
    :param mark_right :             bool, default True, secondy_y 有值时，mark的位置是否右侧

    :return:
    """
    def __post_init__(self):
        # index_col=0,可以去掉没意义的第一列标号和unnamed：0
        self.dfdata = pd.DataFrame(pd.read_excel(self.filename, sheet_name=self.sheetname))
        self.dfplot = DfPlot(
            dfdata=self.dfdata,
            plottype=self.plottype,
            valuecolumns=None if self.valuecolumns is None
            else [[self.dfdata.columns.tolist().index(x) for x in self.valuecolumns], self.valuecolumns],
            indexcolumn=[[self.indexcolumn], [self.dfdata.columns[self.indexcolumn]]],
            xlabel=self.xlabel,
            ylabel=self.ylabel,
            showflag=self.showflag,
            subplots=self.subplots,
            sharex=self.sharex,
            sharey=self.sharey,
            use_index=self.use_index,
            logx=self.logx,
            logy=self.logy,
            secondary_y=self.secondary_y,
            mark_right=self.mark_right
        )


def draw_figure(figure, canvas, canvas_toolbar):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def canvas_clear(figure_canvas_agg):
    # 清除旧画布
    if figure_canvas_agg:
        if figure_canvas_agg.toolbar:
            figure_canvas_agg.toolbar.destroy()
        figure_canvas_agg.get_tk_widget().destroy()


if __name__ == "__main__":
    # 表格的编辑页面
    plotlayout = [
        [
            Sg.Button('确定', k='_ok_'), Sg.Button('关闭', k='_close_')
        ],
        [Sg.Canvas(key='-TOOLBAR-')],
        [Sg.Canvas(key='-CANVAS-')],

    ]

    plotwindow = Sg.Window(
        '数据图形显示',
        plotlayout,
        finalize=True,
        element_justification='center',
        use_ttk_buttons=True,
        return_keyboard_events=True,  # 把mouse事件暂时由主窗口屏蔽
        resizable=True,
        modal=True,
        keep_on_top=False
    )

    # 调用绘图函数
    dfdata = pd.DataFrame(pd.read_excel("d:/temp/pivotresult.xlsx", sheet_name=0))
    dfplot = DfPlot(
        dfdata=dfdata,
        # plottype=PlotType.PLOT,
        plottype=PlotType.BAR,
        # valuecolumns=[[1, 3], ["专用发票", "电子发票"]],
        indexcolumn=[[0], ["主体"]],
        title="测试图形",
        xlabel="主体",
        ylabel="发票上限",
        showflag=False
    )
    fig_canvas_agg = draw_figure(dfplot.get_figure(), plotwindow['-CANVAS-'].TKCanvas, plotwindow['-CANVAS-'].TKCanvas)

    # 等待界面输入
    while True:
        event, values = plotwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break
        elif event in ['_ok_']:

            # 获取各个参数，调用画图

            continue

    # 关闭窗体
    plotwindow.close()