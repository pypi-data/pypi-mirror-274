
from setuptools import setup, find_packages
import sys
import os
from pathlib import Path


def init_data_files() -> list:
    """
    :return:    list 本模块需要拷贝数据文件的目录
    """
    specaildir = 'bat_inner_module'
    specialfilename = [
        'bat_inner_module/readme_for_inner.md',
        'bat_inner_module/inner_demo.py',
        'bat_inner_module/inner_demo1.py'
    ]
    originnonconfigdir = 'config/img'
    originconfigdir = 'config/batframe'
    configfilename = 'bat_tools_config.json'
    nonconfigfile = [
        'config/img/table_arrow9_transparent_64.ico',
        'config/img/little_bear.png',
        'config/img/Excel.png',
        'config/img/excel.gif'
    ]

    orginconfigfile = '{0}/{1}'.format(originconfigdir, configfilename)
    judgeconfigfile = '{0}/../{1}/{2}'.format(sys.exec_prefix, originconfigdir, configfilename)

    # 用于彩色打印字符串的前后缀串
    specialshowstartconfig = "\033[1;31;40m"
    specialshowendconfig = "\033[0m"

    # 判断当前模块安装是否在虚拟环境venv
    print("当前运行路径：{}".format(sys.exec_prefix))
    if sys.exec_prefix.endswith("venv"):
        data_files = []
        # 添加图像文件等非配置文件
        data_files.append(('{0}/../{1}'.format(sys.exec_prefix, originnonconfigdir), nonconfigfile))
        print("data_files 添加非配置文件: {}".format(data_files))
        # 添加特殊路径文件
        data_files.append(('{0}/../{1}'.format(sys.exec_prefix, specaildir), specialfilename))
        # 判断配置文件是否存在，如果存在，打印对比信息并提醒用户判断是否替换
        if Path(judgeconfigfile).is_file():
            copychoice = input("\n{0}文件：{1}已经存在，是否使用安装包中的同名文件替换(Yes/No){2}:".format(
                specialshowstartconfig, judgeconfigfile, specialshowendconfig))
            # 用户确认拷贝覆盖，文件存在且用户选择不拷贝，直接返回
            if copychoice.lower() not in ['y', 'yes']:
                return data_files
            else:
                # 覆盖方式，必须先删除原文件，否则强制覆盖好像有问题。
                try:
                    os.remove(judgeconfigfile)
                    print("删除原始文件：{}".format(judgeconfigfile))
                except Exception as err:
                    print("删除文件{}失败：{}".format(judgeconfigfile, err))
        # 文件不存在或者存在用户确认覆盖
        data_files.append(('{0}/../{1}'.format(sys.exec_prefix, originconfigdir), [orginconfigfile]))
        print("data_files 添加配置文件: {}".format(data_files))
    else:
        data_files = [
            (originnonconfigdir, nonconfigfile),
            (specaildir, specialfilename),
            (originconfigdir, [orginconfigfile]),
        ]
    return data_files


setup(
    name='batframes',
    version='1.0.1',
    description='可以配置将多个可执行文件和内部命令串接成一个完整命令执行的框架工具。（命令支持 多个option选项）',
    author='Frank Gong',
    author_email='583983716@qq.com',
    packages=find_packages(),        # 表示你要封装的包，find_packages用于系统自动从当前目录开始找包
    license="BSD",
    py_modules=['batframe_main', 'bat_menu_auto', 'bat_function_call_define', 'nuitka_dependency_files'],
    install_requires=['pandas~=1.5.2', 'numpy~=1.24.1', 'openpyxl', 'argparse', 'pathlib',
                      'selenium', 'requests', 'xlrd', 'bottle', 'PySimpleGUI~=4.59.0', 'prettytable',
                      'chardet', 'nuitka', 'PyQt5', 'pycryptodomex', 'datacompy',
                      'shortuuid', 'sqlalchemy==1.4.46', 'mysql-connector-python', 'ipy',
                      'pathos', 'pymysql', 'colorlog', 'matplotlib~=3.7.2', 'pypinyin', 'bs4',
                      'pyxlsb', 'jsonlines', 'Jinja2', 'psgspecialelements', 'DFTrans'],
    package_data={
        "bat_inner_module": ["inner_*.py", "*.md"]
    },
    data_files=init_data_files(),
    # classifiers=[
    #     # 发展时期,常见的如下
    #     #   3 - Alpha
    #     #   4 - Beta
    #     #   5 - Production/Stable
    #     'Development Status :: 5 - Stable',
    #     # 开发的目标用户
    #     'Intended Audience :: Developers',
    #     # 属于什么类型
    #     'Topic :: Software Development :: Tools',
    #     # 许可证信息
    #     'License :: OSI Approved :: BSD License',
    #     # 目标 Python 版本
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    # ]
)
'''
name : 打包后包的文件名
version : 版本号
author : 作者
author_email : 作者的邮箱
py_modules : 要打包的.py文件
packages: 打包的python文件夹
include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
license : 支持的开源协议
description : 对项目简短的一个形容
ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
ext_package : 定义extension的相对路径
requires : 定义依赖哪些模块
provides : 定义可以为哪些模块提供依赖
data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。
    # 希望被打包的文件
    package_data={
        '':['*.txt'],
        'bandwidth_reporter':['*.txt']
               },
    # 不打包某些文件
    exclude_package_data={
        'bandwidth_reporter':['*.txt']
        
        
    # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # 该文件入口指向 foo/main.py 的main 函数
    entry_points={
        'console_scripts': [
            'foo = foo.main:main'
        ]
    },

    # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # 执行 python setup.py install 后
    # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    scripts=['bin/foo.sh', 'bar.py']
'''


