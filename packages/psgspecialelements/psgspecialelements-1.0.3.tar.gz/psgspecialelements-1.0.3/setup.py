
from setuptools import setup, find_packages

setup(
    name='psgspecialelements',
    version='1.0.3',
    description='special elements based on pysimplegui elements',
    author='Frank Gong',
    author_email='583983716@qq.com',
    packages=find_packages(),        # 表示你要封装的包，find_packages用于系统自动从当前目录开始找包
    license="BSD",
    py_modules=['psgspecialelements', 'hash_password'],
    install_requires=['PySimpleGUI~=4.59.0', 'pandas~=1.5.2', 'numpy~=1.24.1', 'openpyxl', 'dataclasses', 'pycryptodomex'],
    data_files=[
        ('config/img', ['config/img/table_arrow9_transparent_64.ico']),
        # ('config',  ['cfg/data.cfg'])
    ],
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
    #     'Programming Language :: Python :: 3.9'
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
'''