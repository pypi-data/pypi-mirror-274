# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
###############################################################################################################
# BAT工具集成框架
# 用于集成相关的配套工具
# 可以通过配置文件增加工具
# Version 1.0.0
###############################################################################################################
"""
import argparse
from pathlib import Path
import json
import os
from bat_menu_auto import bat_tools_menu_auto_gui, edit_cmd_gui_config_file
import sys
import hashlib
import webbrowser
from hash_password import password_check, PasswordMatches, edit_account_dic
from psgspecialelements import *
from bat_function_call_define import cmdline_option_find, bat_function_call, dynamic_load_user_functions
from DFTrans_main import *


# 工具启动的整体配置文件
sysdefaultdirectory = "./config"
battoolsconfig = "./config/batframe/bat_tools_config.json"

commandtypelist = []
commandtype2valuedic = {}


def GraphicButton(text: str, key: str, image_data):
    text = text.replace('_', ' ')
    button = Sg.Button('', image_filename=image_data, image_size=(32, 32), image_subsample=3,
                       button_color=('white', '#9FB8AD'), font='Any 15', key=key,
                       border_width=2)
    text = Sg.Text(text, font='Any 10', size=(25, 1), justification='center', )
    return Sg.Column([[button], [text]], element_justification='c')


def itemedit(menuitem: list, method: int = None, current_row: int = None, index_col_value: list = None) -> list:
    """
    编辑或者增加表格行，增加行需要判断是否已经存在关键词相同的记录
    :param menuitem:                list, 表格行的一维列表
    :param method:                  EDIT_METHOD or ADD_METHOD
    :param current_row:             当前编辑的行号，用于判断是否重复
    :param index_col_value:         索引列的当前列值，用于判断是否重复值
    :return:
    :return :                       [a, b, c,......] or None
    """
    mymethod = method
    currentrow = current_row
    indexcolvalue = index_col_value
    item_tl = [[Sg.Text('菜单名称'.ljust(6)), Sg.Input("", size=(35, 0), key='_fn1_', pad=(5, 5))],
               [Sg.Text('是否使用'.ljust(6)), Sg.InputCombo(("是", "否"), key='_fn3_', pad=(5, 5),
                                                        size=(5, 0), default_value="是", readonly=True),
                Sg.Text('命令类型'.rjust(8)), Sg.InputCombo(commandtypelist, key='_fn4_', pad=(5, 5),
                                                        size=(12, 0), default_value="1", readonly=True)],

               ]
    item_l = [[Sg.Text("".center(6))]]
    item_md = [[Sg.Text("".center(6))]]
    item_tr = [[Sg.Image(filename='./config/img/excel.gif',
                         enable_events=True,
                         key="_icon_image_",
                         size=(64, 64),
                         pad=(1, 1)
                         )]]

    # 表格的编辑页面
    itemdefine = [
        [Sg.Col(item_l), Sg.Col(item_tr, justification='left'), Sg.Col(item_md), Sg.Col(item_tl), ],
        [Sg.Text('命令图标'.ljust(7)), Sg.Input("", size=(49, 0), key='_fn5_'),
         Sg.Button('更改图标', key='_iconfilebrowse_', pad=(5, 5))],
        [Sg.Text('菜单配置文件'.ljust(6)), Sg.Input('', size=(48, 0), key='_fn2_'),
         Sg.Button('更改配置', key='_filebrowse_', pad=(5, 5))],
        [Sg.Button('确定', key='_ok_'), Sg.Button('关闭', key='_close_')]
    ]

    subwindow = Sg.Window('编辑菜单项',
                          itemdefine,
                          icon=SYSTEM_ICON,
                          font=DEF_FT,
                          use_ttk_buttons=True,
                          finalize=True,
                          resizable=True,
                          # keep_on_top=True,
                          modal=True
                          )
    # 将原值填写到对应文本框中
    subwindow['_fn1_'](menuitem[0])
    subwindow['_fn2_'](menuitem[1])
    subwindow['_fn3_'](menuitem[2])
    subwindow['_fn4_'](menuitem[3])
    subwindow['_fn5_'](menuitem[4])
    subwindow['_icon_image_'].update(filename=menuitem[4], size=(64, 64))

    while True:
        event, values = subwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break
        elif event == '_filebrowse_':
            tmpdir = os.path.dirname(values['_fn2_'])
            tmpname = os.path.basename(values['_fn2_'])
            filetemp = Sg.popup_get_file('选择文件',
                                         icon=SYSTEM_ICON,
                                         file_types=(("Json菜单配置文件", "*.json"),),
                                         initial_folder=tmpdir,
                                         default_path=tmpdir,
                                         history_setting_filename=tmpname,
                                         no_window=True,
                                         keep_on_top=True,
                                         modal=True
                                         )

            if filetemp:
                subwindow['_fn2_'](filetemp)

        elif event in ('_icon_image_', '_iconfilebrowse_'):
            tmpdir = os.path.dirname(values['_fn5_'])
            tmpname = os.path.basename(values['_fn5_'])
            filetemp = Sg.popup_get_file('选择文件',
                                         icon=SYSTEM_ICON,
                                         file_types=(("图标文件", ["*.gif", "*.png"]),),
                                         initial_folder=tmpdir,
                                         default_path=tmpdir,
                                         history_setting_filename=tmpname,
                                         no_window=True,
                                         keep_on_top=True,
                                         modal=True
                                         )

            if filetemp:
                subwindow['_fn5_'](filetemp)
                subwindow['_icon_image_'].update(filename=filetemp, size=(64, 64))

        elif event == '_ok_':
            # 返回菜单项值
            cmd = values['_fn1_']
            exefile = values['_fn2_']
            usepermit = values['_fn3_']
            commandtype = values["_fn4_"]
            iconfile = values["_fn5_"]
            if cmd == '' or exefile == '':
                Sg.popup_error("各项值均不能为空！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 判断cmd是否重名
            valuevalide = True
            # 新增命名在现有命令列表中
            if cmd in indexcolvalue:
                cmdindex = indexcolvalue.index(cmd)
                # 如果是编辑方式而且是当前编辑行，说明没有重复
                if not (mymethod == EDIT_METHOD and cmdindex == currentrow):
                    # 新增内容和原有内容重复
                    valuevalide = False
                    Sg.popup_error("{}和第{}条记录同名！".format(cmd, cmdindex),
                                   keep_on_top=True, modal=True, icon=SYSTEM_ICON)
            # 没有重名情况， 关闭窗口，返回修改或者新增的值
            if valuevalide is True:
                subwindow.close()
                return [cmd, exefile, usepermit, commandtype, iconfile]

    # 点击close或者关闭，不修改任何值，返回 None
    subwindow.close()
    return None


def table_edit():
    """
    对配置文件进行记录的增删改
    """
    # 读取配置文件并填写到编辑表格中
    try:
        with open(battoolsconfig, 'r', encoding='utf8') as fp:
            configdic = json.load(fp)
            fp.close()
    except Exception as err:
        print(str(err))
        Sg.popup_error('配置文件读取失败:{}'.format(err), modal=True, keep_on_top=True, icon=SYSTEM_ICON)
        return False
    # 判断配置文件是否正确
    if 'menus' not in configdic.keys():
        print("{}配置文件内容不符!\n{}".format(battoolsconfig, configdic))
        exit(-1)

    Sg.popup_quick_message('稍等, 调取配置数据....', auto_close=True, non_blocking=True, font='Default 18',
                           keep_on_top=True, modal=True)
    Sg.set_options(element_padding=(0, 0))
    # 读取相关subprocess相关配置信息
    pipeoutconfig = configdic["subprocess_PIPE"]
    consoleshowconfig = configdic["subprocess_console"]
    # 命令类型字典 准成combo 显示list以及对应的值list
    commandtypedic = configdic["command_type_menu"]
    # 如果commandtypedic有值，说明全局变量已经初始化过，不需要再赋值
    if len(commandtypedic) == 0:
        for keys, values in commandtypedic.items():
            commandtypelist.append(values)
            commandtype2valuedic[values] = keys

    # column_widths = [20, 40, 8, 10, 40]
    column_widths = [33, 60, 10, 16, 56]
    visible_column_map = [True, True, True, True, True]
    paraminfo = configdic['menus']
    column_cell_edit_type_map = [
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_INPUT,
    ]
    for items in paraminfo:
        # 转换命令类型代码为相应的命令类型名称，保存字典时需要反向转换
        items["command_type"] = commandtypedic[items["command_type"]]
    # {
    #     "menu_name": "测试用例",
    #     "menu_configfile": "./config/menucfg_测试用例.json",
    #     "for_use": "是",
    #     "command_type": "1",
    #     "img_file": "./config/img/Excel.png"
    # },
    columninfodic = {
        '菜单名称': 'menu_name',
        '菜单配置文件': 'menu_configfile',
        '是否使用': 'for_use',
        '命令类型': 'command_type',
        '图标文件': 'img_file'
    }

    # 生成表格外独有部分
    layoutstatic = [
                      [Sg.Text('是否使用Pipeout'.ljust(10), pad=(10, 20)),
                       Sg.InputCombo((1, 0), key='_pipeout_', size=(4, 0),
                                     default_value=pipeoutconfig, enable_events=True, readonly=True),
                       Sg.Text("".ljust(10)),
                       Sg.Text('是否显示Console'.ljust(10), pad=(20, 20)),
                       Sg.InputCombo((1, 0), key='_show_console_', size=(4, 0),
                                     default_value=consoleshowconfig, enable_events=True, readonly=True),
                       ],
                      # [Sg.HSep(color="Grey"),],
                  ]

    tablekey = "_menutable_"
    tempfuncargs = {
        "method": EDIT_METHOD,
        "current_row": None,
        "index_col_value": []
    }

    colvaluesecale = [
        None,                         # 菜单名称，索引列，建议不要批处理修改
        [],                           # 菜单配置文件
        ['是', '否'],
        commandtypelist,              # 命令类型
        []                            # 图标文件
    ]
    # 生成表格编辑部分
    layouttable = SpecialTable(
        tablekey,
        pad=(0, 0),
        border_width=1,
        max_rows=19,
        max_columns=5,
        cell_justification='l',
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        tabledatadictlist=paraminfo,
        headings=list(columninfodic),
        itemeditfunc=itemedit,               # 用于编辑表格记录的钩子函数
        itemeditfuncargsdic=tempfuncargs,    # 编辑记录函数的参数信息
        indexcol=0,                           # 菜单名称不可重复，作为索引列
        visible_column_map=visible_column_map,
        col_widths=column_widths,
        col_value_scale=colvaluesecale,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        column_cell_edit_type_map=column_cell_edit_type_map,
        slider_every_row_column=True,
        disable_slider_number_display=True,
        cell_editable=True,
        v_slider_show=True,
        h_slider_show=False,
        size=(1380, 500),
        edit_button_visible=True,
        move_row_button_visible=True,
        filter_visible=True,
        filter_set_value_visible=True,
    ).layout

    # 生成尾部保存、退出按钮
    layouttail = [
        [
            Sg.Col([[
                Sg.Button('保存&退出', key='_save_', pad=(10, 10)),
                Sg.Text("".rjust(20)),
                Sg.Button(' 关  闭 ', key='_close_', pad=(10, 20))
            ]], justification='center')
        ]
    ]
    # 拼接页面配置
    layout = layoutstatic + [[Sg.Frame("相关菜单选项配置", layouttable, expand_x=False, expand_y=False)]] + layouttail

    window = Sg.Window('配置工具菜单',
                       layout,
                       font=DEF_FT,
                       size=(1380, 648),
                       icon=SYSTEM_ICON,
                       # return_keyboard_events=False,
                       resizable=False,
                       use_ttk_buttons=True,
                       modal=True,
                       # keep_on_top=True,
                       finalize=True)
    # 初始化mousewheel updown相关的环境
    window[tablekey].update(commandtype=SPECIAL_TABLE_SET_BIND, currentwindow=window)
    while True:
        event, values = window.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        elif event == '_save_':
            # 保存当前的数据到配置文件
            # 生成字典
            configdic['menus'] = window[tablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
            # 将表格编辑的结果中，命令类型名称反向转换成命令类型代码（因为在读取config时做过转换，所以需要反向转换后保存。
            for items in configdic["menus"]:
                items["command_type"] = commandtype2valuedic[items["command_type"]]
            configdic["subprocess_PIPE"] = values["_pipeout_"]
            configdic["subprocess_console"] = values["_show_console_"]
            print(configdic)
            try:
                with open(battoolsconfig, 'w', encoding='utf8') as fp:
                    json.dump(configdic, fp, ensure_ascii=False, sort_keys=False, indent=4)
                    fp.flush()
                    fp.close()
                    Sg.popup_ok("重启程序后将启用新<工具>菜单！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                    break
            except Exception as err:
                Sg.popup_error(str(err), modal=True, keep_on_top=True, icon=SYSTEM_ICON)
            # 保存结束后，将字典内容恢复到运行的内容。
            paraminfo = configdic['menus']
            for items in paraminfo:
                # 转换命令类型代码为相应的命令类型名称，保存字典时需要反向转换
                items["command_type"] = commandtypedic[items["command_type"]]
            continue

        # TABLE 被点击后，会连续输出两个事件，一个是元组，格式如下，包含了点击的（行号，列号），行号-1表示点击的是heading
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # 第二个事件是表格本身key事件
        elif isinstance(event, tuple):
            # 兼容Sg.table和Special element方式, 以及鼠标wheel处理
            # 处理鼠标wheel, 目前 （tablekey,x, y), "mousewheel", 不再需要兼容Sg.Table
            currenttable = event[0][0] if isinstance(event[0], tuple) else event[0]

            window[currenttable].update(
                commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
                currentevent=event, currentwindow=window, currentvalues=values)
            continue

    # 关闭窗口
    window.close()


def config_menu_change(closeflag=True):
    """
    修改配置文件是否可以编辑标志
    :param closeflag:            TRUE:关闭配置菜单， FALSE：打开配置菜单
    :return :                    修改失败返回False，修改成功直接退出程序等用户再次启动
    """
    # 读取配置文件
    try:
        with open(battoolsconfig, 'r', encoding='utf8') as fp:
            configdic = json.load(fp)
            fp.close()
    except Exception as err:
        print("读取配置文件：{}失败：{}".format(battoolsconfig, err))
        sys.exit(-1)
    if 'enable_config' not in configdic.keys():
        print(configdic)
        print("{}配置文件内容不符！\n {}".format(battoolsconfig, configdic))
        sys.exit(-1)

    passwordhash = configdic["config_password"][0]
    # 密码确认页面
    if password_check(passwordhash) is False:
        return False
    # 修改配置项

    try:
        configchoice = "0" if closeflag is True else "1"
        configutf = configchoice.encode('utf-8')
        sha1hash = hashlib.sha1()
        sha1hash.update(configutf)
        confighash = sha1hash.hexdigest()
    except Exception as err:
        Sg.popup_error("修改失败：hash error{}".format(str(err)), modal=True, keep_on_top=True,
                       icon=SYSTEM_ICON)
        return False
    configdic["config_password"][1] = confighash
    # 此处读取config文件和保存是成对出现，没有进行类型转换，所以无需反向转换成命令类型代码
    try:
        with open(battoolsconfig, 'w', encoding='utf8') as fp:
            json.dump(configdic, fp, ensure_ascii=False, sort_keys=False, indent=4)
            fp.flush()
            fp.close()
    except Exception as err:
        Sg.popup_error("修改失败：{}".format(str(err)), modal=True, keep_on_top=True,
                       icon=SYSTEM_ICON)
        return False

    # 修改成功
    Sg.popup_ok("修改成功，程序将关闭，重启后<配置>菜单将关闭！", modal=True, keep_on_top=True,
                icon=SYSTEM_ICON)
    sys.exit(0)


def bat_tools_menus():
    # 读取配置文件
    try:
        with open(battoolsconfig, 'r', encoding='utf8') as fp:
            configdic = json.load(fp)
            fp.close()
    except Exception as err:
        print("读取配置文件：{}失败：{}".format(battoolsconfig, err))
        sys.exit(-1)
    if 'enable_config' not in configdic.keys():
        print(configdic)
        print("{}配置文件内容不符！\n {}".format(battoolsconfig, configdic))
        sys.exit(-1)

    # 系统名称
    system_name = configdic["system_name"]
    # 版本信息
    system_version = configdic["version"]
    # 命令类型字典， 系统根据命令类型，将各种命令分配到对应的类型子菜单以及grouptab
    commandtypesubcmddict = {}
    commandtypedic = configdic["command_type_menu"]
    # 先形成菜单对应的字典（使用values）
    # 命令类型字典 准成combo 显示list以及对应的值list
    for commandtypekeys, commandtypevalues in commandtypedic.items():
        # 命令类型对应下属子命令清单列表的字典
        commandtypesubcmddict[commandtypevalues] = []
        # 命令类型列表
        commandtypelist.append(commandtypevalues)
        # 命令类型编号和命令说明的反向字典
        commandtype2valuedic[commandtypevalues] = commandtypekeys

    # 系统错误编码字典
    errordefinedic = configdic["error_define"]

    # 获取账号菜单的相关配置
    accountsubmenudic = configdic["account_sub_menu_dic"]

    # 账户子菜单列表
    accountsubmenu = list(accountsubmenudic)

    # 账户子菜单类别字典(包含登录账号密码信息）
    accounttypedic = configdic["account_type_dic"]

    # 可以调用的函数说明字典
    functioncalldic = configdic["function_call"]

    # 动态加载自定义函数
    if dynamic_load_user_functions(functioncalldic) != 0:
        print("动态加载自定义函数：{}失败".format(functioncalldic))


    # 加入“设置账号” 一级菜单
    accountmenu = ["设置(&S)", ["账号", accountsubmenu]]
    # 加入“配置” 一级菜单
    enable_config = PasswordMatches("1", configdic["config_password"][1])
    pipeout = True if configdic["subprocess_PIPE"] == 1 else False
    consoleshow = True if configdic["subprocess_console"] == 1 else False
    innerfunctioncall = configdic["inner_function_exe"]
    # ------ Menu Definition ------ #
    if enable_config is True:
        configmenu = ['系统配置(&C)', ['编辑<工具>菜单', '界面配置文件', ['新建', '修改', ],
                                   '数据分析流程配置', '关闭<系统配置>菜单']]
    else:
        configmenu = ['系统配置(&C)', ['打开<系统配置>菜单']]

    # 加入“关于”一级菜单
    menu_def = [
        accountmenu,
        configmenu,
        ['帮助(&H)', ['关于...', '操作说明']],
    ]

    # 初始化工具命令菜单项主项
    commandmenu = ['工具(&T)']
    # 对所有的"menu_name": "菜单1",
    #        "menu_configfile": "./config/menucfg_菜单1.json",
    #        "for_use": "是",
    #        "command_type": "1",
    #        "img_file": "./config/img/Excel.png"字典项，逐项把工具名称分命令类型加入到不同的子菜单中，相当于处理二维list
    # 针对不同命令类型，组合相关的子菜单形成列表
    commandsubmenu = []
    toolmenuconfigdic = configdic["menus"]
    # 当菜单允许使用时，按命令分类加入菜单列表
    # 填写菜单分级的字典
    commandicondict = {}
    # 所有命令对应的事件清单
    commandeventlist = []
    for items in toolmenuconfigdic:
        # 转换命令类型代码为相应的命令类型名称，保存字典时需要反向转换
        items["command_type"] = commandtypedic[items["command_type"]]
        # 记录所有的命令名，作为后续事件处理的事件列表
        commandeventlist.append(items["menu_name"])
        if items["for_use"] == "是":
            # 每个命令类型下的实际允许执行的命令名称
            commandtypesubcmddict[items["command_type"]].append(items["menu_name"])
            # 每个可执行命令对应的图标文件
            commandicondict[items["menu_name"]] = items["img_file"]
    # 将二级菜单拼接为一级菜单
    for keys, values in commandtypesubcmddict.items():
        # 当底层菜单有值时才显示上级菜单
        if len(values) > 0:
            commandsubmenu.append(keys)
            commandsubmenu.append(values)

    # 第一列菜单最后为‘退出’
    commandsubmenu.append('退出')
    # 把工具命令子菜单挂接到工具菜单
    commandmenu.append(commandsubmenu)
    # 把工具菜单放到菜单栏第一项
    menu_def.insert(0, commandmenu)

    # ------ GUI Defintion ------ #
    Sg.Menu(menu_def, tearoff=False, pad=(200, 1), font=('宋体', 10))

    # 整理所有的工具命令
    all_running_files = []
    for values3 in commandtypesubcmddict.values():
        all_running_files.append(values3)

    # 为每个命令type准备对应的layout，并按顺序放置到grouplist
    commandgrouplaylist = [[] for _ in list(commandtypedic)]
    # 用于保存图标相关的内容，保证每个tab的图标都是每行4个
    for h, i, j in zip([[] for _ in commandgrouplaylist], commandgrouplaylist, all_running_files):
        for num, element in enumerate(j):
            h.append(element)
            if (num + 1) % 4 == 0 and num < len(j):
                i.append([GraphicButton(h[x], h[x], commandicondict[h[x]]) for x in range(4)])
                h = []
            elif num + 1 == len(j):
                i.append([GraphicButton(h[x], h[x], commandicondict[h[x]]) for x in range(len(h))])

    RUN_LOG_SWITCH = '_run_log_switch_'
    LOG_FOR_001 = '_log_for_001_'

    logging_layout = [[Sg.Button('日志开关', key=RUN_LOG_SWITCH, pad=(2, 2), button_color='green'),
                       Sg.Text("所有的运行信息都将在此显示!")],
                      [Sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                                    autoscroll=True,
                                    auto_refresh=True, key=LOG_FOR_001, visible=False, disabled=True, metadata=False)]
                      ]

    # 菜单栏的layout
    layout1 = [
        [Sg.Menu(menu_def, tearoff=False, pad=(200, 1), font=('宋体', 10))],
    ]
    # 底部按钮layout
    layout2 = [[Sg.Text('退出', size=(35, 1), justification='center', font=("Helvetica", 15), relief=Sg.RELIEF_RIDGE,
                        key='Exit', enable_events=True),
                Sg.Text('保存日志', size=(35, 1), justification='center', font=("Helvetica", 15), relief=Sg.RELIEF_RIDGE,
                        key='_save_log_', enable_events=True, visible=True),
                ]]

    # tabgroup的整体layout， 包含日志tab
    layout = [layout1, [Sg.TabGroup([
        [
            Sg.Tab(x, [[Sg.Col(y,
                               scrollable=True,
                               size=(800, 500), expand_x=True,
                               expand_y=True,
                               # size_subsample_height=1
                               )]])
            for x, y in zip(list(commandtypedic.values()), commandgrouplaylist)
        ] +
        [
            Sg.Tab('日志输出', logging_layout)
        ]
    ], key='-TAB GROUP-', expand_x=True, expand_y=True)], layout2]

    layout[-1].append(Sg.Sizegrip())

    window = Sg.Window(system_name, layout,
                       icon=SYSTEM_ICON,
                       font=("宋体", 10),
                       location=(300, 300),
                       size=(860, 600),
                       # use_ttk_buttons=True,
                       resizable=True,
                       finalize=True,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1))
    window.set_min_size(window.size)

    # 获取全局multiline对象，以便后续做输出重定向
    globalmultiline = window[LOG_FOR_001]

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event in (Sg.WIN_CLOSED, '退出'):
            break
        # ------ Process menu choices ------ #
        if event in accountsubmenu:
            accounttype = accountsubmenudic[event]
            # 调取设置账号界面
            tempaccinfodic = edit_account_dic(accounttypedic[accounttype], accounttype)
            if tempaccinfodic is not None:
                configdic["account_type_dic"][accounttype] = tempaccinfodic
                # 将表格编辑的结果中，命令类型名称反向转换成命令类型代码（因为在读取config时做过转换，所以需要反向转换后保存。
                for items in configdic["menus"]:
                    items["command_type"] = commandtype2valuedic[items["command_type"]]
                print(configdic)
                # 保存到json
                try:
                    with open(battoolsconfig, 'w', encoding='utf8') as fp:
                        json.dump(configdic, fp, ensure_ascii=False, sort_keys=False, indent=4)
                        fp.flush()
                        fp.close()
                except Exception as err:
                    Sg.popup_error("保存配置失败：{}".format(str(err)),
                                   modal=True,
                                   keep_on_top=True,
                                   icon=SYSTEM_ICON)
                    continue
                # Sg.popup_ok("{}完成！".format(event), modal=True, keep_on_top=True,  icon=SYSTEM_ICON)
                # 保存结束，将字典内容恢复到运行的内容。
                paraminfo = configdic['menus']
                for items in paraminfo:
                    # 转换命令类型代码为相应的命令类型名称，保存字典时需要反向转换
                    items["command_type"] = commandtypedic[items["command_type"]]
                continue
            continue

        if event == '关于...':
            # window.disappear()
            Sg.popup('关于本程序', 'Version ' + system_version, system_name, '',
                     # custom_text="确定",
                     grab_anywhere=True,
                     modal=True,
                     keep_on_top=True,
                     icon=SYSTEM_ICON)
            # window.reappear()
        if event == '操作说明':
            webbrowser.open('https://www.baidu.com/')

        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        elif event == '编辑<工具>菜单':
            # 调用配置工具菜单相关页面
            table_edit()
            continue

        elif event == '新建':
            # 获取新建文件的文件名
            filetemp = Sg.popup_get_file('选择文件',
                                         save_as=True,
                                         file_types=(("Json菜单配置文件", "*.json"),),
                                         initial_folder='./config',
                                         default_path='./menucfg_config_new',
                                         keep_on_top=True, modal=True,
                                         no_window=True)
            if filetemp:
                # 先创建一个基础文件，然后调用修改程序
                tempdic = dict(
                    window_title='',
                    exe_call=[
                        {
                            "exe_unit": "",
                            "need_password": "",
                            "account_type": "",
                            "cmd_option": "",
                            "item_name": "",
                            "file_name": "",
                            "file_type_info": "",
                            "file_type": "",
                            "save_mode": "",
                            "changable": ""
                        }
                    ]
                )
                # tempdic['window_title'] = ''
                # tempdic['exe_call'] = []
                try:
                    with open(filetemp, 'w', encoding='utf8') as fp:
                        json.dump(tempdic, fp, ensure_ascii=False, sort_keys=False, indent=4)
                        fp.flush()
                        fp.close()
                except Exception as err:
                    Sg.popup_error("生成文件：{} 失败:{}！".format(filetemp, err),
                                   modal=True, keep_on_top=True, )
                    continue
                edit_cmd_gui_config_file(filetemp, accounttypedic, functioncalldic)

        elif event == '修改':
            # 获取修改文件的文件名
            filetemp = Sg.popup_get_file('选择文件',
                                         save_as=False,
                                         file_types=(("Json菜单配置文件", "*.json"),),
                                         initial_folder='./config',
                                         default_path='./config',
                                         keep_on_top=True, modal=True,
                                         no_window=True)
            if filetemp:
                edit_cmd_gui_config_file(filetemp, accounttypedic, functioncalldic)
                # 调用修改程序
            continue

        elif event == '数据分析流程配置':
            DF_Trans_main(g='y')
            continue

        elif event == RUN_LOG_SWITCH:
            logswithflag = window[LOG_FOR_001].metadata
            if logswithflag:
                # 从True切换为False，关闭
                window[LOG_FOR_001].metadata = False
                window[LOG_FOR_001].update(visible=False, disabled=True)
                window[LOG_FOR_001].restore_stdout()
                window[LOG_FOR_001].restore_stderr()
                window[RUN_LOG_SWITCH].update(button_color='green')
                # print("zoom in : nowsize:{}, targetsize:{}".format(mainwindow.size, originwindowsize))
                extendwindowsize = window.size
                # window.size = originwindowsize
            else:
                # 从False切换为True， 打开
                window[LOG_FOR_001].metadata = True
                window[LOG_FOR_001].update(visible=True, disabled=False)
                window[LOG_FOR_001].reroute_stdout_to_here()
                window[LOG_FOR_001].reroute_stderr_to_here()
                window[RUN_LOG_SWITCH].update(button_color='red')

        elif event == '关闭<系统配置>菜单':
            # 调用页面，弹出密码输入框确认
            # 修改允许配置标记为允许
            # 提示将退出程序并在重启后将关闭<配置菜单>
            config_menu_change(closeflag=True)
            continue

        elif event == '打开<系统配置>菜单':
            # 调用页面，弹出密码输入框确认
            # 修改允许配置标记为不允许
            # 提示将退出程序并在重启后将打开<配置菜单>
            config_menu_change(closeflag=False)
            continue

        # elif event in toolmenuconfigdic.keys():  # 判断事件是否在命令菜单字典中
        elif event in commandeventlist:     # 判断事件是否在命令名事件清单中
            # 事件在命令事件列表中，根据列表index，获取命令菜单字典中的命令配置文件
            cmdmenuconfig = toolmenuconfigdic[commandeventlist.index(event)]["menu_configfile"]
            print(cmdmenuconfig)
            # 调用相应处理页面
            # 执行命令配置文件相关命令
            resulttemp = bat_tools_menu_auto_gui(cmdmenuconfig, accounttypedic, errordefinedic,
                                                 pipeout, consoleshow, innerfunctioncall, globalmultiline)
            if resulttemp != 0:
                if str(resulttemp) in errordefinedic.keys():
                    errorstr = errordefinedic[str(resulttemp)]
                else:
                    errorstr = str(resulttemp)
                Sg.popup_error("错误", "运行错误：{}:{}\r\n".format(resulttemp, errorstr),
                               modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue

        elif event == "_save_log_":
            logcontent = window[LOG_FOR_001].get()
            filetemp = Sg.popup_get_file('选择文件',
                                         save_as=True,
                                         file_types=(("日志文件", "*.log"),),
                                         initial_folder="D:/temp/",
                                         default_path="D:/temp/battemp.log",
                                         history_setting_filename="battemp.log",
                                         keep_on_top=True, modal=True,
                                         no_window=True, icon=SYSTEM_ICON)
            if filetemp:
                try:
                    with open(filetemp, 'w', encoding='utf8') as fp:
                        fp.write(logcontent)
                        fp.flush()
                        fp.close()
                        Sg.popup_ok("输出日志文件{}完成！".format(filetemp),
                                    modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                except Exception as err:
                    Sg.popup_error("错误", "写入日志文件{}出错：{}".format(filetemp, err),
                                   modal=True, keep_on_top=True, icon=SYSTEM_ICON)

    window.close()


def bat_main(*args,**kwargs):
    # 判断开始运行时是否有--cmdline参数，如果有，表明不是启动菜单界面，而是调用内部的function
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
    # 如果返回值不为空，代表是后天调用内部函数
    functioncallname = cmdline_option_find(sys.argv)
    if functioncallname != "":
        # 去掉用于传输 调用函数名的 --cmdline的选项以及对应的函数名
        sys.argv.remove("--cmdline")
        sys.argv.remove(functioncallname)
        return bat_function_call(functioncallname)
    else:
        # 如果带--console -f 菜单命令文件，说明是console方式运行菜单命令后退出。
        # 默认命令文件名
        commandfile = 'menucfg_config_new.json'

        # 调试环境下文件使用的目录， 使用os.path.join 实现windows和linux跨平台兼容
        debugpathstring = os.path.join(".", "config")
        debugpath = Path(debugpathstring)

        # 在调试环境下，使用子目录存储和处理相关文件
        if debugpath.is_dir():
            commanddefaultfile = os.path.join(debugpathstring, commandfile)
        else:
            commanddefaultfile = os.path.join(".", commandfile)

        debugswitchdefault = 'n'

        # 读取配置文件
        try:
            with open(battoolsconfig, 'r', encoding='utf8') as fp:
                configdic = json.load(fp)
                fp.close()
        except Exception as err:
            print("读取配置文件：{}失败：{}".format(battoolsconfig, err))
            sys.exit(-1)
        if 'enable_config' not in configdic.keys():
            print(configdic)
            print("{}配置文件内容不符！\n {}".format(battoolsconfig, configdic))
            sys.exit(-1)

        # 系统名称
        system_name = configdic["system_name"]
        # 版本信息
        system_version = configdic["version"]

        print("默认输入参数：{}".format(sys.argv[1:]))
        parser = argparse.ArgumentParser(description="{0} {1}".format(system_name, system_version))
        parser.add_argument('-cmdfile', type=str, default=commanddefaultfile,
                            help='命令文件, 默认值：' + commanddefaultfile)
        parser.add_argument('-console', type=str, choices=("y", "n"), default=debugswitchdefault,
                            help='是否以console方式运行, 默认值：{}'.format(debugswitchdefault))

        args, argv = parser.parse_known_args()
        if argv:
            print("命令错误，未知option：{}".format(argv))
            return 206
        args = parser.parse_args()
        mycommandfile = args.cmdfile
        consolechoose = args.console
        myconsoleflag = True if consolechoose == 'y' else False

        # 如果不是console方式运行，调用GUI
        if myconsoleflag is False:
            bat_tools_menus()
        else:
            return(bat_tools_consoles_run(mycommandfile))


def bat_tools_consoles_run(commandfile:str):
    """
    console方式运行菜单命令
    :param commandfile:         str：命令文件名
    :return:
    """
    print("console run：{}".format(commandfile))

    # 读取配置文件
    try:
        with open(battoolsconfig, 'r', encoding='utf8') as fp:
            configdic = json.load(fp)
            fp.close()
    except Exception as err:
        print("读取配置文件：{}失败：{}".format(battoolsconfig, err))
        sys.exit(-1)
    if 'enable_config' not in configdic.keys():
        print(configdic)
        print("{}配置文件内容不符！\n {}".format(battoolsconfig, configdic))
        sys.exit(-1)

    # 命令类型字典
    tempmenudic = {}
    commandtypedic = configdic["command_type_menu"]
    # 先形成菜单对应的字典（使用values）
    for values in commandtypedic.values():
        tempmenudic[values] = []

    errordefinedic = configdic["error_define"]

    accounttypedic = {}           # 非gui下，不需要账号信息，无rpa功能
    pipeout = False
    consoleshow = False
    resulttemp = bat_tools_menu_auto_gui(commandfile, accounttypedic, errordefinedic,
                                         pipeoutput=pipeout, consoleshow=consoleshow, guimode=False)
    if resulttemp != 0:
        if str(resulttemp) in errordefinedic.keys():
            errorstr = errordefinedic[str(resulttemp)]
        else:
            errorstr = str(resulttemp)
        print("错误", "运行错误：{}:{}\r\n".format(resulttemp, errorstr))
        return -1
    else:
        print("运行完成")
        return 0


if __name__ == '__main__':
    if bat_main() != 0:
        sys.exit(-1)
    else:
        sys.exit(0)
