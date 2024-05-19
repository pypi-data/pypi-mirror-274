# -*- coding: utf-8 -*-
"""
###############################################################################################################
# BAT工具集成环境 调用命令页面
# 用于集成相关的配套工具
# 可以通过配置文件增加工具
# Version 1.1
###############################################################################################################
"""

import subprocess
import os
import chardet
import json
import sys
from psgspecialelements import *
from hash_password import dftrans_choice_account
from bat_function_call_define import bat_function_call


# 用于本module调试的配置文件
guimenuconfig = "./config/menucfg_bat_test.json"
filetypedic = {
    "日期格式": 'Datumsformat',
    "目录": 'directory',
    '任意文件': '*.*',
    'Json文件': '*.json',
    'Josnl文件': '*.jsonl',
    '表格文件': '*.xlsx',
    'CSV文件': '*.csv',
    '可执行文件': '*.exe',
    '文本文件': '*.txt',
    'basic文件': '*.bas',
    '批处理程序': '*.bat',
    '压缩文件': '*.zip'
}


def bat_tools_menu_auto_gui(menuconfigfile, accounttypedic, errordefinedic,
                            pipeoutput=True, consoleshow=False, innerfunctioncall="",
                            globalmultiline=None, guimode=True):
    """
    根据命令执行配置文件自动生成交互界面并可执行相关命令
    :param menuconfigfile:                   命令执行配置文件
    :param accounttypedic:                  字典，记录账号类型和对应的values
    :param errordefinedic:                  调用subprocess返回退出错误码的说明字典
    :param pipeoutput:                      是否采用PIPE方式处理subprocess
    :param consoleshow:                     是否关闭console的显示窗口
    :param innerfunctioncall                用于内部调用函数的可执行文件（exe，为“”时，直接修改argv并内部调用函数
    :param globalmultiline:                 全局日志输出的multiline对象
    :param guimode:                         是否以gui方式运行
    :return                                 0 ，success， other： fail
    """
    # 读取配置文件
    myguimode = guimode
    try:
        menuconfigdic = json.load(open(menuconfigfile, 'r', encoding='utf8'))
    except Exception as err:
        if myguimode:
            Sg.popup_error("{}配置文件读取失败：{}".format(menuconfigfile, str(err)), modal=True,
                           keep_on_top=True, icon=SYSTEM_ICON)
        else:
            print("{}配置文件读取失败：{}".format(menuconfigfile, str(err)))
        return 202
    if "window_title" not in menuconfigdic.keys():
        if myguimode:
            Sg.popup_error("{}配置文件格式不符！\n{}".format(menuconfigfile, menuconfigdic), modal=True,
                           keep_on_top=True, icon=SYSTEM_ICON)
        else:
            print("{}配置文件格式不符！\n{}".format(menuconfigfile, menuconfigdic))
        return 203

    # 获取窗口标题信息
    windowtitle = menuconfigdic["window_title"]

    # 动态生成file相关界面配置
    filemenu = []
    paraminfo = menuconfigdic["exe_call"]
    # 逐行处理动态菜单项
    # 用于记录是否需要账户及对应的账号类型
    needpassword = []
    accounttype = []
    currentaccounttypelist = []
    # 用于记录有命令行命令的index
    commandmarkarrary = []
    # 文件功能描述
    itemname = []
    # 文件名 输入
    filename = []
    # 文件是读方式还是写方式，写方式将检查当前输入的文件名是否已经存在
    savemode = []
    # open , save 时用到的文件类型，file_type_info 和file_type相互对应
    filetypeinfo = []
    filetype = []
    # 确定记录的option（‘ ’ or '-a' --> 'z'）
    cmdoption = []
    # 确定本条记录行内容可否被更改
    changable = []

    # 如果在调用Sg后，没有创建windows程序就返回，系统好像无法释放资源，所以程序如果有出错处理在函数中途返回，需要放在Sg的相关操作之前！！！。
    for i in range(len(paraminfo)):
        menuinfodic = paraminfo[i]
        # 是否需要账号和password，对于RPA工具，因为要访问网络页面并登录，所以需要输入账号、密码，
        # 要获取账号、密码并在subprocess中增加-u user -p password选项
        tempneedpassword = menuinfodic["need_password"]
        tempaccountype = str(menuinfodic["account_type"])
        # 保存到记录
        needpassword.append(tempneedpassword)
        accounttype.append(tempaccountype)
        # 记录需要的账号类型以便后续获取
        if (tempneedpassword == "是" and tempaccountype != ""
                and tempaccountype not in currentaccounttypelist):
            currentaccounttypelist.append(tempaccountype)
    # 获取本次命令需要的账号密码
    # 确定当前账号密码，仅仅在gui方式下可以用账号rpa调用
    if myguimode:
        if len(currentaccounttypelist) > 0:
            returndic = dftrans_choice_account(accounttypedic, currentaccounttypelist)
            if returndic is None:  # 没有选择账号、密码, 直接返回
                return 205
            else:
                currentaccountdic = returndic
        else:
            currentaccountdic = {}

    # 用于记录该菜单对应的事件keys events的list，用户点击后，可以确定是否是当前list中的事件
    # 通过确定list的index，可以确定是哪一个更改的按钮被点击（因为更改按钮是动态生成，每个程序的个数不同。
    filechangeindex = []
    #   把动态界面每行的各类元素分别保存到一个list中
    for i in range(len(paraminfo)):
        menuinfodic = paraminfo[i]
        # 标记命令行命令index，用于后续执行命令时判断是否某个命令相关option结束
        tempcmd = menuinfodic["exe_unit"].strip()
        if tempcmd != "":
            commandmarkarrary.append(i)

        # 压入 命令记录的总数，作为命令处理的结束标记
        commandmarkarrary.append(len(paraminfo))
        # 文件功能描述
        itemname.append(menuinfodic['item_name'].ljust(16))
        # 文件名 输入
        filename.append(menuinfodic['file_name'])
        # 文件是读方式还是写方式，写方式将检查当前输入的文件名是否已经存在
        savemode.append(menuinfodic['save_mode'])
        # open , save 时用到的文件类型，file_type_info 和file_type相互对应
        filetypeinfo.append(menuinfodic['file_type_info'])
        filetype.append(menuinfodic['file_type'])
        # 确定记录的option（‘ ’ or '-a' --> 'z', 也可以手工输入。
        cmdoption.append(menuinfodic['cmd_option'])
        # 确定本条记录行内容可否被更改，如果不可更改，就不显示，旧版本是不能修改，但是显示出来。
        changable.append(menuinfodic['changable'])
        if myguimode:
            visibleflag = False if changable[i] == '否' else True
            # 当本行菜单的文件类型是'*.*'时，说明对应的实际不是文件而是命令行参数，不显示button“更改”
            buttonchangevisible = False if filetype[i] == "*.*" else True
            filemenu.append([Sg.Text(itemname[i], size=(20, 1), visible=visibleflag, font=DEF_FT, pad=(5, 5)),
                             Sg.Input(filename[i], key='fn' + str(i), visible=visibleflag, font=DEF_FT, pad=(5, 5)),
                             Sg.Button('更改', key='c' + str(i), visible=visibleflag & buttonchangevisible)])

            # 用于记录该菜单对应的事件keys events的list，用户点击后，可以确定是否是当前list中的事件
            # 通过确定list的index，可以确定是哪一个更改的按钮被点击（因为更改按钮是动态生成，每个程序的个数不同。
            filechangeindex.append('c' + str(i))

    def run_command(guimode=True):
        """
        运行命令，
        :param guimode:                     True: gui方式， False：命令行方式
        :return:
        """
        # 遍历当前paraminfo，当exe_unit!="", 表示开始执行一个新的命令，
        optionindex = 0
        runok = True
        if guimode:
            # 方式下，启动处理进度条初始窗口
            barlayout = [[Sg.Text('', size=(50, 1), relief='sunken',
                                  text_color='blue', background_color='white', key='-TEXT-', metadata=0)]]
            barwindow = Sg.Window('处理进度', barlayout,
                                  keep_on_top=False,
                                  modal=True,
                                  use_ttk_buttons=True,
                                  finalize=True, icon=SYSTEM_ICON)
            bartext = barwindow['-TEXT-']
        else:
            print("开始运行命令文件：{}".format(menuconfigfile))

        # 清理内部调用函数的参数
        del sys.argv[1:]
        for commandinfo in paraminfo:
            commandname = commandinfo["exe_unit"].strip()
            # 无论是exe还是agv运行，同步填写argv， ""值不要填入到option list中
            if paraminfo[optionindex]['cmd_option'] != "":
                sys.argv.append(paraminfo[optionindex]['cmd_option'])

            if guimode:
                # gui描述下，用户可能在界面修改文件名，需要读取信息 对于多个值空格隔开，需要拆分成多个list项添加
                if runvalues['fn' + str(optionindex)] != "":
                    for substr in runvalues['fn' + str(optionindex)].split():
                        sys.argv.append(substr)
            else:
                # 非GUI下，直接使用option
                if filename[optionindex] != "":
                    sys.argv.append(filename[optionindex])

            # 判断是否一个新的命令串
            if commandname != "":
                # 开始一个新的命令串
                subcmd = commandname
                currentcommand = commandname
                #  判断是否要账号密码执行
                if paraminfo[optionindex]['need_password'] == "是":
                    if guimode:
                        # 获取账号密码加密串
                        tempaccountype = paraminfo[optionindex]['account_type']
                        if tempaccountype not in currentaccountdic.keys():
                            # 配置的账号类型找不到对应的账号密码
                            return 205
                        else:
                            currentaccount = currentaccountdic[tempaccountype][0]
                            currentpassword = currentaccountdic[tempaccountype][1]
                            subcmd = subcmd + " -u " + currentaccount + " -p " + currentpassword
                            # argv也同步处理
                            sys.argv.append("-u"),
                            sys.argv.append(currentaccount)
                            sys.argv.append("-p")
                            sys.argv.append(currentpassword)
                    else:
                        print("非GUI方式下，无法运行账号RPA方式")
                        return 205
                if guimode:
                    # guimode读取界面参数
                    subcmd += ' ' + paraminfo[optionindex]['cmd_option'] + ' ' + runvalues['fn' + str(optionindex)]
                else:
                    subcmd += ' ' + paraminfo[optionindex]['cmd_option'] + ' ' + filename[optionindex]
            else:
                if guimode:
                    # guimode读取界面参数
                    subcmd += ' ' + paraminfo[optionindex]['cmd_option'] + ' ' + runvalues['fn' + str(optionindex)]
                else:
                    subcmd += ' ' + paraminfo[optionindex]['cmd_option'] + ' ' + filename[optionindex]

            # 如果下一条记录存在命令，说明本条记录已经到了本次命令的最后一条，执行相关命名，否则处理下一条
            if optionindex + 1 not in commandmarkarrary:
                optionindex += 1
                continue
            else:
                # 当optionindex + 1 对应下一条命令时，说明将执行当期命令，更新进度条
                currentprocess = commandmarkarrary.index(optionindex + 1) / len(commandmarkarrary)
                # 更新进度条
                if guimode:
                    bartext.metadata = (int(currentprocess * 50)) % 51
                    bartext.update(Sg.SYMBOL_SQUARE * bartext.metadata)
                optionindex += 1

            # 判断当前命令是exe\bat还是内部函数调用，还不函数则直接调用函数直接使用inner函数调用
            if currentcommand.endswith(".exe") is not True and currentcommand.endswith(".bat") is not True:
                # 虽然是内部函数，但是使用壳exe调用，
                if innerfunctioncall != "":
                    subcmd = innerfunctioncall + " --cmdline " + subcmd
                else:
                    # 调用运行内部函数的功能
                    try:
                        print("current command：{}".format(currentcommand))
                        tempresult = bat_function_call(currentcommand.strip())
                        # 清理argv为下一轮命令做准备
                        del sys.argv[1:]
                        if tempresult == 0:
                            # 运行成功
                            continue
                            # Sg.popup_ok("运行完成！", modal=True, icon=SYSTEM_ICON)
                        else:
                            if str(tempresult) in errordefinedic.keys():
                                resultstr = errordefinedic[str(tempresult)]
                            else:
                                resultstr = str(tempresult)

                            if guimode:
                                Sg.popup_error("错误", "内部函数调用{}错误返回值{}：{}\r\n".format(
                                    currentcommand, tempresult, resultstr),
                                               modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                            else:
                                print("错误", "内部函数调用{}错误返回值{}：{}\r\n".format(currentcommand,
                                                                            tempresult, resultstr))
                            runok = False
                            break
                    except Exception as err:
                        if guimode:
                            Sg.popup_error("错误", "内部函数调用{}失败\r\n：{}".format(currentcommand, str(err)),
                                           modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                        else:
                            print("错误", "内部函数调用{}失败\r\n：{}".format(currentcommand, str(err)))
                        runok = False
                        break
                    continue

            # 根据option选项和命令，拼接需要执行的命令串
            print(subcmd)

            # 执行相关命令 True:使用check_out 方式， 否则采用Popen方式
            if not pipeoutput:
                try:
                    # 运行相关命令串
                    strtemp = subprocess.check_output(subcmd)
                except subprocess.CalledProcessError as err:
                    runok = False
                    returncode = err.returncode
                    # 判断子进程退出码是否在自定义字典中
                    if str(returncode) in errordefinedic.keys():
                        if guimode:
                            Sg.popup_error(
                                "subprocess check_output {} 返回值非0:{}-{}".format(subcmd,
                                                                                returncode,
                                                                                errordefinedic[str(returncode)]),
                                modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                        else:
                            print("subprocess check_output {} 返回值非0:{}-{}".format(subcmd,
                                                                                  returncode,
                                                                                  errordefinedic[str(returncode)]))
                    else:
                        if guimode:
                            Sg.popup_error("subprocess check_output 返回值非0:{}".format(returncode),
                                           modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                        else:
                            print("subprocess check_output 返回值非0:{}".format(returncode))
                    break
                except Exception as err:
                    runok = False
                    if guimode:
                        Sg.popup_error("subprocess check_output error:{}".format(str(err)),
                                       modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                    else:
                        print("subprocess check_output error:{}".format(str(err)))
                    break

                # 判断子进程输出的编码格式
                codetype = chardet.detect(strtemp)
                print("编码格式：{}".format(codetype))
                try:
                    # 将返回值按decode结果解码串
                    strtemp = strtemp.decode(codetype['encoding'])
                except Exception as err:
                    if guimode:
                        Sg.popup_error(str(err), modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                    else:
                        print(str(err))
                    continue
                    # 编码错误不退出，继续

                # 打印输出
                if strtemp != "":
                    print(strtemp)
                continue
            else:
                # 使用Popen 方式 ，pipeout方式
                try:
                    # 设置静默方式，不打开cmd窗口
                    if guimode:
                        IS_WIN32 = 'win32' in str(sys.platform).lower()
                        # 如果是windows环境并且不打开console
                        if consoleshow is False and IS_WIN32:
                            startupinfo = subprocess.STARTUPINFO()
                            startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
                            # 如果配置为关闭console窗口，则设置隐藏console窗口
                            startupinfo.wShowWindow = subprocess.SW_HIDE
                            p = subprocess.Popen(subcmd,
                                                 startupinfo=startupinfo,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 bufsize=1024 * 1024)
                        else:  # 非windows环境不适用startupinfo 以及 windows不关闭console
                            p = subprocess.Popen(subcmd,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 bufsize=1024 * 1024)
                    else:
                        print("非GUI环境，不做stdout、stderr重定向")
                except Exception as err:
                    runok = False
                    if guimode:
                        Sg.popup_error("错误", "subprocess Popen 失败\r\n：{}".format(str(err)),
                                       modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                    else:
                        print("错误", "subprocess Popen 失败\r\n：{}".format(str(err)))
                    break
                try:
                    print("命令执行中......")
                    # 使用communicate 获取子进程的标准输出和标准出错
                    subprcout, subprcerr = p.communicate()
                    returncode = p.returncode
                    # 判断子进程退出码是否在自定义字典中
                    if int(returncode) != 0:
                        if str(returncode) in errordefinedic.keys():
                            if guimode:
                                Sg.popup_error(
                                    "subprocess check_output {} 返回值非0:{}-{}".format(subcmd,
                                                                                    returncode,
                                                                                    errordefinedic[str(returncode)]),
                                    modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                            else:
                                print("subprocess check_output {} 返回值非0:{}-{}".format(subcmd,
                                                                                      returncode,
                                                                                      errordefinedic[str(returncode)]))
                        else:
                            if guimode:
                                Sg.popup_error("subprocess check_output 返回值非0:{}".format(returncode),
                                               modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                            else:
                                print("subprocess check_output 返回值非0:{}".format(returncode))
                    # 检测返回值数据字符类型（中文字符识别）
                    strtemp1, strtemp = '', ''
                    if subprcout != '' and subprcout != b'':
                        codetype = chardet.detect(subprcout)
                        try:
                            # 根据检测结果转换标准输出信息
                            strtemp = subprcout.decode(codetype['encoding'])
                        except Exception as err:
                            print("stdout decode err: {},".format(err))

                    if subprcerr != '' and subprcerr != b'':
                        codetype = chardet.detect(subprcerr)
                        try:
                            # 根据检测结果转换标准错误信息
                            strtemp1 = subprcerr.decode(codetype['encoding'])
                        except Exception as err:
                            print("stderr decode err: {},".format(err))

                    # 打印输出标准输出和标准错误信息
                    if strtemp != "":
                        print("stdout:{}".format(strtemp))
                    if strtemp1 != "":
                        print("stderr:{}".format(strtemp1))
                except Exception as err:
                    # communicate 出错
                    print("p.communicate error:{}".format(err))
                    runok = False
                    break

        # 运行成功 , 保存更改后的文件配置(仅仅在gui方式下）
        if runok is True:
            if guimode:
                for i in range(len(paraminfo)):
                    menuconfigdic["exe_call"][i]["file_name"] = runvalues['fn' + str(i)]
                # 保存到配置文件
                json.dump(menuconfigdic,
                          open(menuconfigfile, 'w', encoding='utf8'),
                          ensure_ascii=False, sort_keys=False, indent=4)
                # 运行完成前满格进度条然后关闭进度窗
                bartext.metadata = 50
                bartext.update(Sg.SYMBOL_SQUARE * bartext.metadata)
                barwindow.close()
                Sg.popup_ok("运行完成！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                return 0
            else:
                # print("运行完成100%！")
                return 0
        else:
            # 运行事变直接关闭进度窗
            if guimode:
                barwindow.close()
                return 0
            else:
                # print("运行不成功！")
                return -1

    # 非GUI方式下，直接运行返回
    if not guimode:
        return (run_command(guimode=False))

    RUN_LOG_SWITCH = '_run_log_switch_'
    LOG_FOR_RUNMAIN = '_log_for_runmain_'
    # 生成命令相关的运行界面
    layoutstatictail = [
        [Sg.Button('日志开关', key=RUN_LOG_SWITCH, pad=(2, 2), button_color='green'), Sg.Text("点击后运行信息将在下方显示!")],
        [Sg.Text("".ljust(22), key='s1'), Sg.Button('运行', key='_run_'),
         Sg.Text("".ljust(20), key='s2'), Sg.Button('关闭', key='_run_close_')],
        [Sg.Multiline(size=(60, 15), font=("宋体", 9), expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=False, reroute_stderr=False, echo_stdout_stderr=False,
                      autoscroll=True,
                      auto_refresh=True, pad=(10, 10), key=LOG_FOR_RUNMAIN, visible=False, disabled=True,
                      metadata=False)]
        ]

    # 将动态界面部分与后面的静态部分合并为完整页面
    layout = filemenu + layoutstatictail
    # 启动界面窗口
    runwindow = Sg.Window(
        windowtitle, layout,
        modal=True,
        icon=SYSTEM_ICON,
        font=DEF_FT,
        use_ttk_buttons=True,
        # keep_on_top=True,
        default_element_size=(50, 1),
        finalize=True)
    print("选择相关文件后点击'运行'")
    # 获取当前multiline的previous_stdout, 如果是multiline 而且不是全局multiline，就修改当前multiline的previous_stdout\stderr
    # localloginfprevious = runwindow['_local_log_'].previous_stdout
    # if (isinstance(localloginfprevious, Sg.Multiline)
    #         and globalmultiline is not None
    #         and localloginfprevious != globalmultiline):
    #     runwindow['_local_log_'].previous_stdout = globalmultiline
    #     runwindow['_local_log_'].previous_stderr = globalmultiline
    localloginfprevious = runwindow[LOG_FOR_RUNMAIN].previous_stdout
    if (isinstance(localloginfprevious, Sg.Multiline)
            and globalmultiline is not None
            and localloginfprevious != globalmultiline):
        runwindow[LOG_FOR_RUNMAIN].previous_stdout = globalmultiline
        runwindow[LOG_FOR_RUNMAIN].previous_stderr = globalmultiline

    runwindow.reappear()
    originwindowsize = copy.deepcopy(runwindow.size)
    print("orginsize record:{}".format(originwindowsize))

    extendwindowsize = None

    # 进入事件主循环
    while True:
        event, runvalues = runwindow.read()
        if event == Sg.WIN_CLOSED:
            # 点击窗口X，该事件values == None,
            # 直接关闭
            break

        if event == '_run_close_':  # 如果用户关闭窗口或点击`关闭`
            # 保存更改后的文件配置
            for i in range(len(paraminfo)):
                menuconfigdic["exe_call"][i]["file_name"] = runvalues['fn' + str(i)]
            # 保存到配置文件
            json.dump(menuconfigdic,
                      open(menuconfigfile, 'w', encoding='utf8'),
                      ensure_ascii=False, sort_keys=False, indent=4)
            break

        # 处理文件相关事件（选择命令行的各个配置选项）
        # 用于记录该菜单对应的事件keys events的list，用户点击后，可以确定是否是当前list中的事件
        # 当点击的‘更改’按钮对应的文件类型是“目录”时，需要启动Sg.popup_get_folder 获取目录
        # 其他使用Sg.popup_get_file
        if event in filechangeindex:
            # 通过确定list的index，可以确定是哪一个更改的按钮被点击（因为更改按钮是动态生成，每个程序的个数不同。
            indexnum = filechangeindex.index(event)

            # 打开获取文件名对话框
            tempdir = os.path.dirname(runvalues['fn' + str(indexnum)])
            tempname = os.path.basename(runvalues['fn' + str(indexnum)])
            # # 判断是否目录
            if filetypeinfo[indexnum] == "目录":
                filetemp = Sg.popup_get_folder("选择目录",
                                               initial_folder=tempdir,
                                               default_path=tempdir,
                                               history_setting_filename=tempname,
                                               keep_on_top=True, modal=True,
                                               no_window=True, icon=SYSTEM_ICON)
            elif filetypeinfo[indexnum] == "日期格式":
                date = Sg.popup_get_date(close_when_chosen=True, icon=SYSTEM_ICON)
                if date:
                    month, day, year = date
                    filetemp = f"{year}-{month:0>2d}-{day:0>2d}"
            else:
                filetemp = Sg.popup_get_file('选择文件',
                                             save_as=(True if (savemode[indexnum] == '写') else False),
                                             file_types=((filetypeinfo[indexnum], filetype[indexnum]),),
                                             initial_folder=tempdir,
                                             default_path=tempdir,
                                             history_setting_filename=tempname,
                                             keep_on_top=True, modal=True,
                                             no_window=True, icon=SYSTEM_ICON)
            if filetemp:
                # 通过index修改页面中对应的文件名输入框中的值
                runwindow['fn' + str(indexnum)](filetemp)

        # 根据命令行的option选项，执行指定的命令
        if event == '_run_':
            # gui方式运行
            result = run_command(guimode=True)
            if result != 0:
                runwindow.close()
                return result

        elif event == RUN_LOG_SWITCH:
            logswithflag = runwindow[LOG_FOR_RUNMAIN].metadata
            if logswithflag:
                # 从True切换为False，关闭
                runwindow[LOG_FOR_RUNMAIN].metadata = False
                runwindow[LOG_FOR_RUNMAIN].update(visible=False, disabled=True)
                runwindow[LOG_FOR_RUNMAIN].restore_stdout()
                runwindow[LOG_FOR_RUNMAIN].restore_stderr()
                runwindow[RUN_LOG_SWITCH].update(button_color='green')
                # print("zoom in : nowsize:{}, targetsize:{}".format(mainwindow.size, originwindowsize))
                extendwindowsize = runwindow.size
                runwindow.size = originwindowsize
            else:
                # 从False切换为True， 打开
                runwindow[LOG_FOR_RUNMAIN].metadata = True
                runwindow[LOG_FOR_RUNMAIN].update(visible=True, disabled=False)
                runwindow[LOG_FOR_RUNMAIN].reroute_stdout_to_here()
                runwindow[LOG_FOR_RUNMAIN].reroute_stderr_to_here()
                runwindow[RUN_LOG_SWITCH].update(button_color='red')
                # 第一次点击，同时窗口比原始窗口大，窗口自动扩展，同时记录扩展的size
                if extendwindowsize is None and \
                        runwindow.size[1] > originwindowsize[1] \
                        and runwindow.size[0] >= originwindowsize[0]:
                    print("reccord size : nowsize:{}, oldsize:{}, originsize:{}".format(
                        runwindow.size, extendwindowsize, originwindowsize))
                    extendwindowsize = runwindow.size
                else:
                    print("zoom out : nowsize:{}, targetsize:{}".format(runwindow.size, extendwindowsize))
                    runwindow.size = extendwindowsize

    runwindow.close()
    return 0


# '命令', '账号需求', '账号类型 ', '选项', '项目描述', '默认文件', '文件类型', '文件后缀', '读/写',  '可更改'
# 类 TablewithitemeditDF 要调用的row编辑函数，输入参数需要用字典方式带入。以适应可变参数
def cmd_page_config_item_edit(menuitem: list,
                              functioncalldic: dict = {},
                              accounttypedic: dict = {},
                              ) -> list:
    """
    编辑或者增加表格行
    :param menuitem:                list, 表格行的一维列表, 固定参数, 不同表格这一参数都必须放在第一个
    :param functioncalldic:         调用函数说明字典，不同表格不同
    :param accounttypedic:          账号类型字典，不同表格不同
    :return:                         [a, b, c, d, e, f，g, h, i, j] or None
    """

    # functioncalldic = functioncalldic
    # accounttypedic = accounttypedic
    # headings=['项目描述', '默认文件', '文件类型信息', '文件后缀', '输入（0)/输出(1)', '命令选项']

    # 形成可以调用的函数的说明列表
    comboxfunctioncommentlist = list(functioncalldic.keys())
    # 形成可以调用的函数的列表
    comboxfunctioncalllist = list(functioncalldic.values())
    needpassword = menuitem[1]
    accounttype = menuitem[2]
    if needpassword == "是":
        accountvisible = True
    else:
        accountvisible = False

    # 账号类型列表
    comboxaccounttype = list(accounttypedic.keys())

    functioncallname = ""
    functioncallcomment = "无"
    exefilename = ""
    if menuitem[0].strip().endswith(".exe") is True or menuitem[0].strip().endswith(".bat") is True:
        exefilename = menuitem[0].strip()
    elif menuitem[0] != "":
        functioncallname = menuitem[0]
        # 当前条目为内部函数，找到functioncallname对应的comment
        if functioncallname in comboxfunctioncalllist:
            functioncallcomment = comboxfunctioncommentlist[comboxfunctioncalllist.index(functioncallname)]
        else:
            # 无效的函数名
            functioncallcomment = "无"
            functioncallname = ""

    filetypeinfolist = []
    filetypelist = []
    for key, value in filetypedic.items():
        filetypeinfolist.append(key)
        filetypelist.append(value)
    itemedit = [
        [Sg.Text('执行文件'.ljust(2)), Sg.Input(exefilename, key='_exefile_', size=(60, 1)),
         Sg.Button('更改文件', key='_filebrowseexe_')],
        [Sg.Text('函数说明'.ljust(2)),
         Sg.InputCombo(comboxfunctioncommentlist, key='_functioncomment_', size=(28, 1), readonly=True,
                       enable_events=True, default_value=functioncallcomment, pad=(5, 5)),
         Sg.Text('调用函数'.ljust(2)),
         Sg.InputCombo(comboxfunctioncalllist, key='_functioncall_', size=(28, 1), readonly=True,
                       enable_events=True, default_value=functioncallname)],
        [Sg.Text('账号密码登录'.ljust(6)),
         Sg.InputCombo(("是", "否"), key='_need_password_', size=(4, 0),
                       default_value=needpassword, enable_events=True, readonly=True),
         Sg.Text('账号类型'.ljust(4), key='_account_info_', visible=accountvisible),
         Sg.InputCombo(comboxaccounttype, key='_account_type_', size=(6, 0),
                       default_value=accounttype, visible=accountvisible, readonly=True)],
        [Sg.Text('项目描述'.ljust(2)), Sg.Input('', key='fn2', size=(60, 0), pad=(5, 5))],
        [Sg.Text('默认文件'.ljust(2)), Sg.Input('', key='fn3', size=(60, 0)), Sg.Button('更改文件', key='_filebrowse_')],
        [Sg.Text('文件类型'.ljust(2), pad=(5, 5)),
         Sg.InputCombo(filetypeinfolist, key='fn4', size=(10, 0), enable_events=True, readonly=True, pad=(5, 5)),
         Sg.Text('后缀'.ljust(2)),
         Sg.InputCombo(filetypelist, key='fn5', size=(8, 0), enable_events=True, readonly=True, pad=(5, 5)),
         Sg.Text('读取/写入'.ljust(2)),
         Sg.InputCombo(("读", "写"), key='fn6', size=(4, 0), default_value="读", readonly=True, pad=(5, 5)),
         Sg.Text('命令选项'.ljust(2)),
         Sg.InputCombo([''] + ['-' + chr(i) for i in range(ord('a'), ord('z') + 1)], key='fn1', size=(3, 0)),
         Sg.Text('可更改'.ljust(2), pad=(5, 5)),
         Sg.InputCombo(("是", "否"), key='fn7', size=(3, 0), default_value='是', readonly=True)],
        [Sg.Button('确定', key='_ok_'), Sg.Button('关闭', key='_close_')]
    ]
    subwindow = Sg.Window('编辑命令相关参数项',
                          itemedit,
                          icon=SYSTEM_ICON,
                          font=DEF_FT,
                          finalize=True,
                          resizable=True,
                          use_ttk_buttons=True,
                          # keep_on_top=True,
                          modal=True
                          )
    # 将原值填写到对应文本框中
    subwindow['fn1'](menuitem[3])  # option
    subwindow['fn2'](menuitem[4])  # 项目描述
    subwindow['fn3'](menuitem[5])  # 默认文件
    subwindow['fn4'](menuitem[6])  # 文件类型
    subwindow['fn5'](menuitem[7])  # 文件后缀
    subwindow['fn6'](menuitem[8])  # 读/写
    subwindow['fn7'](menuitem[9])  # 是否可见

    if functioncallname == "":
        # 当内部函数无效时，执行文件（exe/bat）配置有效
        subwindow["_exefile_"].update(disabled=False)
        subwindow["_filebrowseexe_"].update(disabled=False)
        # Sg.popup_quick_message("函数调用无效时，执行文件（exe/bat）有效！", keep_on_top=True)
    else:
        # 当内部函数有效时，执行文件（exe/bat）配置无效
        subwindow["_exefile_"].update(disabled=True)
        subwindow["_filebrowseexe_"].update(disabled=True)
        # Sg.popup_quick_message("函数调用有效时，执行文件（exe/bat）无效！", keep_on_top=True)

    while True:
        event, values = subwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break
        elif event == '_filebrowseexe_':
            # 打开获取文件名对话框
            tempdir = os.path.dirname(values['_exefile_'])
            tempname = os.path.basename(values['_exefile_'])
            filetemp = Sg.popup_get_file('选择文件',
                                         save_as=False,
                                         file_types=(("可执行文件", '*.exe'), ('批处理程序', '*.bat')),
                                         initial_folder=tempdir,
                                         default_path=tempdir,
                                         history_setting_filename=tempname,
                                         keep_on_top=True,
                                         modal=True,
                                         no_window=True)
            if filetemp:
                subwindow['_exefile_'](filetemp)

        elif event == '_functioncomment_':
            if values['_functioncomment_'] in comboxfunctioncommentlist:
                subwindow['_functioncall_'](comboxfunctioncalllist[comboxfunctioncommentlist.
                                            index(values['_functioncomment_'])])
            if values['_functioncomment_'] == "无":
                # 当内部函数无效时，执行文件（exe/bat）配置有效
                subwindow["_exefile_"].update(disabled=False)
                subwindow["_filebrowseexe_"].update(disabled=False)
                Sg.popup_quick_message("函数调用无效时，执行文件（exe/bat）有效！", modal=True, keep_on_top=True)
            else:
                # 当内部函数有效时，执行文件（exe/bat）配置无效
                subwindow["_exefile_"].update(disabled=True)
                subwindow["_filebrowseexe_"].update(disabled=True)
                Sg.popup_quick_message("函数调用有效时，执行文件（exe/bat）无效！", modal=True, keep_on_top=True)
            continue

        elif event == '_functioncall_':
            if values['_functioncall_'] in comboxfunctioncalllist:
                subwindow['_functioncomment_'](comboxfunctioncommentlist[comboxfunctioncalllist.
                                               index(values['_functioncall_'])])
            if values['_functioncall_'] == "":
                # 当内部函数无效时，执行文件（exe/bat）配置有效
                subwindow["_exefile_"].update(disabled=False)
                subwindow["_filebrowseexe_"].update(disabled=False)
                Sg.popup_quick_message("函数调用无效时，执行文件（exe/bat）有效！", modal=True, keep_on_top=True)
            else:
                # 当内部函数有效时，执行文件（exe/bat）配置无效
                subwindow["_exefile_"].update(disabled=True)
                subwindow["_filebrowseexe_"].update(disabled=True)
                Sg.popup_quick_message("函数调用有效时，执行文件（exe/bat）无效！", modal=True, keep_on_top=True)
            continue

        # 点击了是否需要配置账号，如果”否“，切换账号类型未不可用，如果"是", 切换账号类型为可用
        elif event == "_need_password_":
            if values["_need_password_"] == "是":
                subwindow["_account_info_"].update(visible=True)
                subwindow["_account_type_"].update(visible=True)
            else:
                subwindow["_account_type_"].update(visible=False)
                subwindow["_account_info_"].update(visible=False)

        elif event == '_filebrowse_':
            tempdir = os.path.dirname(values['fn3'])
            tempname = os.path.basename(values['fn3'])
            filetemp = Sg.popup_get_file(
                '选择文件',
                icon=SYSTEM_ICON,
                file_types=((values['fn4'], '*.*' if (values['fn4'] == '') else values['fn5']),),
                initial_folder=tempdir,
                default_path=tempdir,
                history_setting_filename=tempname,
                keep_on_top=True, modal=True,
                no_window=True)
            if filetemp:
                subwindow['fn3'](filetemp)
        # 文件类型和文件后缀相互联动
        elif event == 'fn4':
            if values['fn4'] in filetypeinfolist:
                subwindow['fn5'](filetypelist[filetypeinfolist.index(values['fn4'])])

        elif event == 'fn5':
            if values['fn5'] in filetypelist:
                subwindow['fn4'](filetypeinfolist[filetypelist.index(values['fn5'])])

        elif event == '_ok_':
            # 首先判断所有的必填项是否为空，命令option 可以为空，最后一项有默认值，不会为空
            valuevalid = True
            for i in range(2, 8):
                if values['fn' + str(i)] == '':
                    valuevalid = False
                    break
            # 如果必填项不完整，直接提示进入事件循环
            if valuevalid is False:
                Sg.popup_error("除’命令选项‘外均不能为空！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue

            # 判断账号类型是否合法
            if values['_need_password_'] == '是' and values['_account_type_'].strip() == '':
                Sg.popup_error("需要账号执行时‘账号类型’不能为空", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue

            # 没有命令时 无需账号
            if (values['_exefile_'].strip() == "" and
                    values['_functioncall_'] == "" and
                    (values['_need_password_'] == '是')):
                Sg.popup_error("没有相应命令时，无需账号设置", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 返回菜单项值
            retlist = []
            # 如果没有exe/bat和内部函数，压入空值
            if values['_functioncall_'].strip() == "":
                if values['_exefile_'].strip() == "":
                    # 都没有时压入空值
                    retlist.append("")
                else:
                    # 内部函数为空，外部不为空才压入外部调用
                    retlist.append(values['_exefile_'].strip())
            else:
                # 优先压入内部函数
                retlist.append(values['_functioncall_'].strip())

            # 压入是否需要账号及账号类型
            retlist.append(values['_need_password_'])
            if values['_need_password_'] == '是':
                retlist.append(values['_account_type_'])
            else:
                retlist.append("")

            for i in range(1, 8):
                retlist.append(values['fn' + str(i)])

            subwindow.close()
            return retlist

    # 点击close或者关闭，不修改任何值，返回 None
    subwindow.close()
    return None


def edit_cmd_gui_config_file(menuconfigfile, accounttypedic, functioncalldic):
    """
    编辑命令执行页面配置工具
    :param menuconfigfile:                  命令页面配置文件
    :param accounttypedic:                 字典： 记录账号类型和对应的values
    :param functioncalldic                 内部调用函数的字典
    """
    try:
        menuconfigdic = json.load(open(menuconfigfile, 'r', encoding='utf8'))
    except Exception as err:
        Sg.popup_error("{}配置文件读取失败：{}".format(menuconfigfile, str(err)),
                       keep_on_top=True, modal=True, icon=SYSTEM_ICON)
        return None
    if "window_title" not in menuconfigdic.keys() or "exe_call" not in menuconfigdic.keys():
        Sg.popup_error("{}配置文件格式不符！\n{}".format(menuconfigfile, menuconfigdic),
                       keep_on_top=True, modal=True, icon=SYSTEM_ICON)
        return None
    colvaluescale = [
        [],  # 命令
        ['是', '否'],  # 是否需要账号运行
        [a for a in accounttypedic.keys()],  # 账号类型
        [''] + ['-' + chr(i) for i in range(ord('a'), ord('z') + 1)],  # 命令选项
        [],  # 项目描述
        [],  # 默认文件
        None,  # 文件类型,与文件后缀需要互动， 因此不允许批量更改
        None,  # 文件后缀,与文件类型需要互动， 因此不允许批量更改
        ['读', '写'],  # 文件为读还是写
        ['是', '否']  # 是否可更改
    ]
    columninfodic = {
        '命令': 'exe_unit',
        '账号登录': 'need_password',
        '账号类型': 'account_type',
        '选项': 'cmd_option',
        '项目描述': 'item_name',
        '默认文件': 'file_name',
        '文件类型': 'file_type_info',
        '文件后缀': 'file_type',
        '读/写': 'save_mode',
        '可更改': 'changable'
    }
    windowtitle = menuconfigdic["window_title"]
    # 读取paraminfo，由于字典格式顺序可能不对，需要根据key和columninfodic的对应关系调整
    tempparaminfo = menuconfigdic['exe_call']
    paraminfo = [dict(zip(columninfodic.values(),
                          [x.get(y, None) for y in columninfodic.values()])) for x in tempparaminfo]


    # column_widths = [30, 4, 8, 3, 16, 40, 1, 6, 4, 4]
    column_widths = [28, 8, 8, 6, 32, 68, 10, 10, 6, 6]
    visible_column_map = [True, True, True, True, True, True, True, False, True, True]
    column_cell_edit_type_map = [
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_INPUT,
        SPECIAL_TABLE_CELL_COMBOX,
        SPECIAL_TABLE_CELL_COMBOX,
    ]


    # 配置页面有关输入、输出options的其他选项
    layoutstatic = [
        [Sg.Text('页面标题'.ljust(8), pad=(10, 20), ),
         Sg.Input(windowtitle, key='_win_title_', size=(80, 1))],
    ]

    tablekey = "_configtable_"
    tempfuncargs = {
        "accounttypedic": accounttypedic,
        "functioncalldic": functioncalldic,
    }

    # 生成表格编辑部分
    layouttable = SpecialTable(
        tablekey,
        pad=(0, 0),
        border_width=1,
        max_rows=19,
        max_columns=10,
        cell_justification='l',
        tabledatadictlist=paraminfo,
        headings=list(columninfodic),
        itemeditfunc=cmd_page_config_item_edit,  # 编辑记录行时的钩子函数
        itemeditfuncargsdic=tempfuncargs,  # 编辑函数的参数列表
        visible_column_map=visible_column_map,
        col_widths=column_widths,
        col_value_scale=colvaluescale,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        column_cell_edit_type_map=column_cell_edit_type_map,
        slider_every_row_column=True,
        disable_slider_number_display=True,
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        cell_editable=True,
        v_slider_show=True,
        h_slider_show=False,
        edit_button_visible=True,
        size=(1380, 500),
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
    layout = layoutstatic + [[Sg.Frame("相关命令选项配置", layouttable)]] + layouttail

    mainwindow = Sg.Window('配置命令界面',
                           layout,
                           font=DEF_FT,
                           size=(1400, 678),
                           icon=SYSTEM_ICON,
                           use_ttk_buttons=True,
                           return_keyboard_events=False,
                           resizable=True,
                           modal=True,
                           # keep_on_top=True,
                           finalize=True)
    # 初始化mousewheel updown相关的环境
    mainwindow[tablekey].update(commandtype=SPECIAL_TABLE_SET_BIND, currentwindow=mainwindow)
    while True:
        event, values = mainwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break

        # TABLE 被点击后，会连续输出两个事件，一个是元组，格式如下，包含了点击的（行号，列号），行号-1表示点击的是heading
        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
        # 第二个事件是表格本身key事件
        elif isinstance(event, tuple):
            # 兼容Sg.table和Special element方式, 以及鼠标wheel处理
            # 处理鼠标wheel, 目前 （tablekey,x, y), "mousewheel", 不再需要兼容Sg.Table
            currenttable = event[0][0] if isinstance(event[0], tuple) else event[0]

            mainwindow[currenttable].update(
                commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
                currentevent=event, currentwindow=mainwindow, currentvalues=values)
            continue
        elif event == "_save_":
            menuconfigdic['window_title'] = values['_win_title_']
            menuconfigdic['exe_call'] = mainwindow[tablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT)
            print(menuconfigdic)
            try:
                json.dump(menuconfigdic,
                          open(menuconfigfile, 'w', encoding='utf8'),
                          ensure_ascii=False, sort_keys=False, indent=4)
                break
            except Exception as err:
                Sg.popup_error(str(err), keep_on_top=True, modal=True, icon=SYSTEM_ICON)
            continue

    mainwindow.close()


def main_test():
    layoutstatic = [
        [Sg.Text('页面标题'.ljust(8)), Sg.Input("test", key='_win_title_', size=(80, 1))], ]

    tablekey = "_configtable_"
    tempfuncargs = {
        "accounttypedic": test_accounttypedic,
        "functioncalldic": test_functioncalldic,
    }

    layouttable = SpecialTable(
        tablekey,
        pad=(0, 0),
        border_width=1,
        max_rows=19,
        max_columns=10,
        cell_justification='l',
        combox_button_arrow_color='blue',
        combox_button_background_color='white',
        tabledatadictlist=test_parminfo,
        headings=list(test_columninfodic),
        itemeditfunc=cmd_page_config_item_edit,
        itemeditfuncargsdic=tempfuncargs,
        visible_column_map=test_visible_column_map,
        col_widths=test_column_widths,
        col_value_scale=test_colvaluescale,
        select_mode=SPECIAL_TABLE_SELECT_MODE_BROWSE,
        slider_every_row_column=True,
        disable_slider_number_display=True,
        cell_editable=True,
        v_slider_show=True,
        h_slider_show=True,
        edit_button_visible=True,
        move_row_button_visible=True,
        filter_visible=True,
        filter_set_value_visible=True,
    ).layout

    layouttail = [
        [
            Sg.Text("".rjust(48)),
            Sg.Button('保存&退出', key='_save_', pad=(10, 10)),
            Sg.Text("".rjust(20)),
            Sg.Button('  关闭  ', key='_close_', pad=(10, 20)),
        ]
    ]
    # 拼接页面配置
    layout = layoutstatic + layouttable + layouttail

    mainwindow = Sg.Window('配置命令界面test',
                           layout,
                           font=DEF_FT,
                           size=(1380, 680),
                           icon=SYSTEM_ICON,
                           return_keyboard_events=True,
                           resizable=True,
                           use_ttk_buttons=True,
                           modal=True,
                           # keep_on_top=True,
                           finalize=True)

    while True:
        event, values = mainwindow.read()
        # --- Process buttons --- #
        if event in (Sg.WIN_CLOSED, '_close_'):
            break
        elif isinstance(event, tuple):
            # 处理鼠标wheel, 目前 （tablekey,x, y), "mousewheel", 不再需要兼容Sg.Table
            currenttable = event[0][0] if isinstance(event[0], tuple) else event[0]

            mainwindow[currenttable].update(
                commandtype=SPECIAL_TABLE_TUPLE_EVENTPROCESS,
                currentevent=event, currentwindow=mainwindow, currentvalues=values)
            continue
        elif event == "_save_":
            print(mainwindow[tablekey].get(attribute=SPECIAL_TABLE_GET_RESULT_DICT))

    mainwindow.close()


if __name__ == '__main__':
    test_parminfo = [
        {
            "exe_unit": "u109_table_process",
            "need_password": "是",
            "account_type": "JDE",
            "cmd_option": "-r",
            "item_name": "JDE电费文件",
            "file_name": "D:/temp/origin_file_JDE导出电费.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "是"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-m",
            "item_name": "JDE电费预处理模板",
            "file_name": "./config/109_table_process/model_file_JDE_电费.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-c",
            "item_name": "JDE电费预处理配置",
            "file_name": "./config/109_table_process/cmdcfg_JDE_电费预处理.json",
            "file_type_info": "Json文件",
            "file_type": "*.json",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-o",
            "item_name": "JDE电费预处理输出",
            "file_name": "D:/temp/a_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "写",
            "changable": "否"
        },
        {
            "exe_unit": "u109_table_process",
            "need_password": "是",
            "account_type": "JDE",
            "cmd_option": "-r",
            "item_name": "JDE水费文件",
            "file_name": "D:/temp/origin_file_JDE导出水费.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "是"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-m",
            "item_name": "JDE水费预处理模板",
            "file_name": "./config/109_table_process/model_file_JDE_水费.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-c",
            "item_name": "JDE水费预处理配置",
            "file_name": "./config/109_table_process/cmdcfg_JDE_水费预处理.json",
            "file_type_info": "Json文件",
            "file_type": "*.json",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-o",
            "item_name": "JDE水费预处理输出",
            "file_name": "D:/temp/b_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "写",
            "changable": "否"
        },
        {
            "exe_unit": "u101_operate_table",
            "need_password": "是",
            "account_type": "UMD",
            "cmd_option": "-r",
            "item_name": "UMD水电费文件",
            "file_name": "D:/temp/UMD导出水电费.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "是"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-p",
            "item_name": "JDE电费预处理输出",
            "file_name": "D:/temp/a_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-m",
            "item_name": "UMD_JDE水电费对比模板",
            "file_name": "./config/101_operate_table/operate_model_UMD_JDE_水电费比较.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-c",
            "item_name": "UMD_JDE电费对比配置",
            "file_name": "./config/101_operate_table/cmdcfg_JDE_UMD_电费对比.json",
            "file_type_info": "Json文件",
            "file_type": "*.json",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-o",
            "item_name": "UMD_JDE电费对比输出",
            "file_name": "D:/temp/c_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "写",
            "changable": "否"
        },
        {
            "exe_unit": "u101_operate_table",
            "need_password": "是",
            "account_type": "EAS",
            "cmd_option": "-r",
            "item_name": "UMD_JDE电费对比结果",
            "file_name": "D:/temp/c_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-p",
            "item_name": "JDE水费预处理输出",
            "file_name": "D:/temp/b_JDE_UMD_temp.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-m",
            "item_name": "UMD_JDE水电费对比模板",
            "file_name": "./config/101_operate_table/operate_model_UMD_JDE_水电费比较.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-c",
            "item_name": "UMD_JDE水电费对比配置",
            "file_name": "./config/101_operate_table/cmdcfg_JDE_UMD_水电费对比.json",
            "file_type_info": "Json文件",
            "file_type": "*.json",
            "save_mode": "读",
            "changable": "否"
        },
        {
            "exe_unit": "",
            "need_password": "否",
            "account_type": "",
            "cmd_option": "-o",
            "item_name": "UMD_JDE水电费对比输出",
            "file_name": "D:/temp/UMD_JDE_水电费对比.xlsx",
            "file_type_info": "表格文件",
            "file_type": "*.xlsx",
            "save_mode": "写",
            "changable": "是"
        }
    ]
    test_column_widths = [30, 1, 8, 3, 16, 40, 1, 6, 4, 4]
    test_visible_column_map = [True, False, True, True, True, True, False, True, True, True]
    test_columninfodic = {
        '命令': 'exe_unit',
        '账号需求': 'need_password',
        '账号类型 ': 'account_type',
        '选项': 'cmd_option',
        '项目描述': 'item_name',
        '默认文件': 'file_name',
        '文件类型': 'file_type_info',
        '文件后缀': 'file_type',
        '读/写': 'save_mode',
        '可更改': 'changable'
    }
    test_accounttypedic = {
        "JDE": {
            "default_account": "f9b531805c280b9f61e0dfdd8e69c2fd",
            "account_password": {
                "b80e737706e4e197d4fee1d6f77943d3": "8c1c4ee262f8e0df3683b93c4d6325f7",
                "d43c20a211b5973f28367a6b7baccd45": "1551c13b3ce3388abb1a36cd336e7dd8",
                "1cd80dfa63ed99026a140f746af58aab": "8c1c4ee262f8e0df3683b93c4d6325f7",
                "3fb7d1752ce9d33ba0aa386333e694de": "13c505dc45de7c4a96c989f19d3ceea3",
                "74ee91079f4949dbe8c89a051b168f77": "938bdb239a9729a8dd2bc97e936f10fe"
            }
        },
        "UMD": {
            "default_account": "f9b531805c280b9f61e0dfdd8e69c2fd",
            "account_password": {
                "8972d94bf48b555e7524e56973558928": "8c1c4ee262f8e0df3683b93c4d6325f7",
                "d7737728298033be73071093b1e4c7ff": "8c1c4ee262f8e0df3683b93c4d6325f7",
                "6e0ee9cc5b7be5963b5c2a9ae94461ad": "13c505dc45de7c4a96c989f19d3ceea3",
                "be6401f2382ea07b0d8fe327bc123cbf": "13c505dc45de7c4a96c989f19d3ceea3",
                "17738c0347734e96b75fbbc40675ede7": "938bdb239a9729a8dd2bc97e936f10fe",
                "2ee82008f70c557bc941389ca99579d2": "fa33e44b0524f782f3006b06f6516c9f"
            }
        },
        "EAS": {
            "default_account": "45d2a8efdea386c3b3f400c5961cf84a",
            "account_password": {
                "f7ffdcef3d058ae127dd4b206e6872ab": "1551c13b3ce3388abb1a36cd336e7dd8",
                "a0d6adc7ed3a7d7769e4d4220cd50efd": "8fee0860393a4e26a6bc0b6f4658eb5a",
                "f5ba50a6cca7dab7887905b5bcb47387": "13c505dc45de7c4a96c989f19d3ceea3",
                "45d2a8efdea386c3b3f400c5961cf84a": "8c1c4ee262f8e0df3683b93c4d6325f7",
                "dfef1250c5030693ffc089bd2256c1dd": "5c90f1b4bc3d6ad4ba3a58a71b955e6b"
            }
        }
    }
    test_errdefinedic = {
        "101": "帐号为空",
        "102": "密码为空",
        "103": "密码错误",
        "104": "未知错误",
        "201": "命令所需文件不全",
        "202": "读取文件失败",
        "203": "文件格式不匹配",
        "204": "写入文件错误",
        "205": "未选择账号"
    }
    test_functioncalldic = {
        "无": "",
        "Excel表格合并": "u101_operate_table",
        "Excel表格拼接": "u102_excel_files_combine",
        "费用明细添加合同ID": "u103_fee_add_contractid",
        "系统违约金与手工核对": "u104_liquidated_damage_compare",
        "历史欠费格式化": "u105_history_owe_configrun",
        "Excel格式化拷贝": "u106_xlfmtcp",
        "租管表_收费明细核对": "u107_fee_compare_pd",
        "Excel表格预处理": "u109_table_process",
        "Excel表格数据差异": "u110_excel_diff"
    }
    test_colvaluescale = [
        [],  # 命令
        ['是', '否'],  # 是否需要账号运行
        [a for a in test_accounttypedic.keys()],  # 账号类型
        [''] + ['-' + chr(i) for i in range(ord('a'), ord('z') + 1)],  # 命令选项
        [],  # 项目描述
        [],  # 默认文件
        None,  # 文件类型,与文件后缀需要互动， 因此不允许批量更改
        None,  # 文件后缀,与文件类型需要互动， 因此不允许批量更改
        ['读', '写'],  # 文件为读还是写
        ['是', '否']  # 是否可更改
    ]
    # main_test()
    edit_cmd_gui_config_file(guimenuconfig, test_accounttypedic, test_functioncalldic)
