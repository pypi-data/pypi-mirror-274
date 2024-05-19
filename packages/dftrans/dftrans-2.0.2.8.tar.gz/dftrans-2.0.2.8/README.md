# DFTrans
## 介绍
轻量级ETL工具，用于批量处理excel、sql数据库表、jsonl、csv等数据源的文件，并输出到数据库表或excel文件，可以对相关功能进行持续扩展。

## 软件架构
相关架构及高级用户使用说明参见使用说明。

## 安装教程
1. 该系统可以通过pypi安装：
```
pip install dftrans
```

2. 编译为独立运行的exe文件建议使用nuikta
```
nuitka --standalone --show-memory  --windows-disable-console --show-progress --enable-plugin=numpy --enable-plugin=pyqt5 --enable-plugin=tk-inter --show-modules
```

## 使用说明
参见data/DFTrans/user_manual
* 其中用户手册*.docx为各版本的word版本手册，后续将不再做更新。
* markdown目录下为各版本的markdown版本手册，后续更新将以markdown为主。

## 参与贡献
1. Fork 本仓库 
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

## 特技
1. 使用 Readme_XXX.md 来支持不同的语言，例如 Readme_en.md, Readme_zh.md
2. Gitee 官方博客 blog.gitee.com
3. 你可以 https://gitee.com/explore 这个地址来了解 Gitee 上的优秀开源项目
4. GVP 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5. Gitee 官方提供的使用手册 https://gitee.com/help
6. Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 https://gitee.com/gitee-stars/