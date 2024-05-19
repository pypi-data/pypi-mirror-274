# -*- coding: utf-8 -*-
"""
###############################################################################################################
# BAT工具集成环境 调用命令页面
# 定义菜单项功能可以调用的函数（第一期函数用nuitka编译为可以调用的独立exe，稳定后，第二期将能够直接调用的功能转换成函数在主程序直接调用，
# 函数用字典方式描述，相关描述保存在系统配置json文件的字典中
#     "function_call": {
#         "Excel表格合并": "101_operate_table",
#         "Excel表格拼接": "102_excel_file_combine",
#         "Excel表格预处理": "109_table_process",
#         "Excel表格数据差异": "110_excel_diff"
#         .......
#     },
# 调用关系配置在各个菜单项的字典中：
#      "exe_file": "./102_excel_files_combine.exe",
#     "function_call": "101_operate_table",
# 当function_call 不是”“时，系统优先调用函数，为”“时，调用exe
###############################################################################################################
"""
import sys
import argparse
import getopt
import json
import importlib
# 以下import主要为了编译exe时包含相关自定义内部函数
from DFTrans_main import DF_Trans_main
from nuitka_dependency_files import battoolsfunctions

USER_INNER_MODULE_FOLDER = 'bat_inner_module'


def call_function_test():
    """
    用于测试
    :return:
    """
    aa = "Test string rent!"
    parser = argparse.ArgumentParser(description='租管表合并工具')
    parser.add_argument('-r', type=str, nargs="+", default=aa,
                        help='租表Excel文件, 默认值：{}'.format(aa))
    parser.add_argument('-p', type=str, default=aa,
                        help='管表Excel文件, 默认值：{}'.format(aa))
    parser.add_argument('-m', type=str, default=aa,
                        help='租管表模板Excel文件，默认值：{}'.format(aa))
    parser.add_argument('-c', type=str, default=aa,
                        help='合并配置Json文件，默认值：{}'.format(aa))
    parser.add_argument('-o', type=str, default=aa,
                        help='输出结果Excel文件，默认值：{}'.format(aa))
    # 命令行方式时用于丢弃该参数，内部函数调用时，防止参数名出错，用于传递函数名给壳002 exe
    parser.add_argument('--cmdline', type=str, default="系统参数，请勿使用",
                        help='内部识别选项，命令行不能使用！默认值：{}'.format("系统参数，请勿使用"))

    args = parser.parse_args()
    myrentfile = args.r
    mypropertyfile = args.p
    mymodelfile = args.m
    myconfigfile = args.c
    myresultfile = args.o
    print("This is a test!")
    print("myrentfile: {}, mypropertyfile: {},mymodelfile: {}, myconfigfile: {}, myresultfile: {}".format(
        myrentfile,
        mypropertyfile,
        mymodelfile,
        myconfigfile,
        myresultfile))


# 菜单对应的为内部函数调用时，直接通过inner_function_call 调用对应函数，无需调用外部exe文件
def bat_function_call(cmdfunctionname):
    """
    # 用于编译形成内部调用菜单函数的壳exe，实现命令行参数传递给实际的执行函数
    """
    return eval(cmdfunctionname)()


# 返回 --cmdline对应的字符串，没有就返回“”
def cmdline_option_find(argv):
    # subprocess 调用此函数，内部命令选项 --cmdline 用于传递要调用的函数名
    # 分析-cmdline参数
    strallopts = "a:b:c:d:e:f:g:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z"
    helpmark = False
    # 先去掉 -h or --help 并标记继续
    if "-h" in argv:
        argv.remove("-h")
        helpmark = True
    if "--help" in argv:
        argv.remove("--help")
        helpmark = True

    # 获取option对应的arg
    try:
        opts, args = getopt.getopt(argv[1:], strallopts, ["cmdline="])
    except getopt.GetoptError as err:
        print("获取调用函数名相关cmdline选项错误:{}".format(err))
        sys.exit(-1)

    # 找到--cmdline对应的arg
    functioncallname = ""
    # 形成opts[i][0]的列表
    optslist = [a[0] for a in opts]
    if "--cmdline" in optslist:
        # 找到 "--cmdline" 在 opts[0]中的索引并取得对应的opts[i][1]
        functioncallname = opts[optslist.index("--cmdline")][1]

    # 恢复 -h
    if helpmark is True:
        argv.append('-h')

    return functioncallname


# 用于生成u002*.exe的代码，当相关内部函数整合到内部调用编译到001*.exe后，已无需编译002*.exe，可以只作为测试代码使用
def bat_sub_main():
    functioncallname = cmdline_option_find(sys.argv)
    # 调用cmdline对应的函数名
    if functioncallname.strip() == "":
        print("无法获取cmdline对应的调用函数名！")
        sys.exit(-1)
    # 清除--cmdline相关option后，调用相关函数
    sys.argv.remove("--cmdline")
    sys.argv.remove(functioncallname)
    return bat_function_call(functioncallname)


def generate_bat_nuitka_dependency():
    """
    根据./config/batframe/bat_tools_config.json中function_call配置，生成nuitka_dependency_files.py文件，以方便
    使用nuitka编译时，生成相关的内部函数调用依赖字典，
    :return:
    """
    dependcyfilehead = '''
# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
###############################################################################################################
# 该文件为自动生成，请勿修改！！！！！！
# BAT工具集nuitka编译需要用到的依赖
###############################################################################################################
"""
    '''

    dependcyfilename = "./nuitka_dependency_files.py"
    from batframe_main import battoolsconfig
    # 读取配置文件并填写到编辑表格中
    try:
        with open(battoolsconfig, 'r', encoding='utf8') as fp:
            configdic = json.load(fp)
            fp.close()
    except Exception as err:
        print(str(err))
        return False
    # 判断配置文件是否正确
    if 'menus' not in configdic.keys():
        print("{}配置文件内容不符!\n{}".format(battoolsconfig, configdic))
        return -1
    # 可以调用的函数说明字典
    functioncalldic = configdic.get("function_call", None)
    if functioncalldic is None:
        print("{}未配置内部调用函数：function_call".format(battoolsconfig))
        resultcontent = "battoolsfunctions = {}"
    else:
        # battoolsfunctions 字典，只针对inner_开头的内部函数
        resultcontent = "".join([
            "battoolsfunctions = {",
            ", ".join(["'{0}': {0}".format(x) for x in functioncalldic.values()
                       if x.strip().startswith('inner_')]),
            "}"
        ])
        if resultcontent.strip() != "battoolsfunctions = {}":
            # 添加import 信息
            resultcontent = "\n".join([
                "\n".join([
                    "from {0}.{1} import {1}".format(USER_INNER_MODULE_FOLDER, x)
                    for x in functioncalldic.values() if x.strip().startswith('inner_')]),
                resultcontent
            ])
    # 拼接整个文件内容
    totalcontent = "\n".join([dependcyfilehead, resultcontent])
    print(totalcontent)
    try:
        with open(dependcyfilename, "w", encoding="utf-8") as fp:
            fp.write(totalcontent + "\n")
            fp.close()
    except Exception as err:
        print("写入{}失败：{}".format(dependcyfilename, err))
        return -1
    return 0


def dynamic_load_user_functions(functioncalldic: dict) -> int:
    """
    根据用户定影函数的字典，逐项动态加载用户自定义函数
    :param functioncalldic:             dict ，用户自定义函数字典 {函数说明：函数名称}
    :return:                            0 -- 成功， -1 -- 失败
    """
    # 动态import 用户自定义inner_functions
    try:
        # base_dir = os.path.join(os.getenv("LOCALAPPDATA"), useroperatedir)
        # sys.path.append(base_dir)
        # p = __import__(name, globals(), locals(), level=0)
        # globals()[name] = p.__dict__[name]
        # 使用__import__方法动态导入
        # usermodule = __import__(USER_FUNCTION_MODULE, globals(), locals(), level=0,))
        # 整理自定义函数的清单
        userfunctionslist = [x for x in functioncalldic.values() if x.strip().startswith('inner_')]
        usermodulelist = ["{0}.{1}".format(USER_INNER_MODULE_FOLDER, x) for x in userfunctionslist]
        # 导入模块
        for userfunction in userfunctionslist:
            usermodule = importlib.import_module("{0}.{1}".format(USER_INNER_MODULE_FOLDER, userfunction))
            # 登记函数
            globals()[userfunction] = usermodule.__dict__[userfunction]
            locals()[userfunction] = usermodule.__dict__[userfunction]
            print("自定义模块加载函数：{}".format(userfunction))
    except Exception as err:
        errstr = "动态加载用户function失败：{}".format(err)
        print("动态加载用户funtion失败：{}".format(err))
        return -1
    return 0


if __name__ == "__main__":
    if generate_bat_nuitka_dependency() != 0:
        sys.exit(-1)
    else:
        sys.exit(0)
