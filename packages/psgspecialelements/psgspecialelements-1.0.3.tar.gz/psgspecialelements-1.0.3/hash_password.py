# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
###############################################################################################################
# 加密工具集 , 包含hash加密和AES加密两种方式及配套的GUI界面
# 用于集成相关的配套工具
# 可以通过配置文件增加工具
# Version 1.
###############################################################################################################
"""
import copy
import hashlib
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex
from psgspecialelements import *


"""
用于密码输入确认以及产生密码hash
"""
# 用于将账号密码信息传送给页面的列表（二维）
accinfotablevalues = []

SYS_ENCRYPT_KEY = "UMD_SYSTEM_KEY"

def hashgenerateorgui():
    """
    获取密码hash值gui页面
    """
    layout = [
        [Sg.Text('密码哈希生成器', size=(30, 1), font=("黑体", 15))],
        [Sg.Text('输入密码'.ljust(10), font=("宋体", 15)),
         Sg.Input(key='_password_', font=("宋体", 15))],
        [Sg.Text('SHA Hash'.ljust(10), font=("宋体", 15)),
         Sg.Input('', size=(40, 1), key='_hash_', font=("宋体", 15))],
    ]

    # 打开窗口并开始主循环
    window = Sg.Window('SHA 生成器', layout,
                       auto_size_text=False,
                       default_element_size=(10, 1),
                       text_justification='r',
                       return_keyboard_events=True,
                       # keep_on_top=True,
                       modal=True,
                       grab_anywhere=False)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        password = values['_password_']
        try:
            password_utf = password.encode('utf-8')
            sha1hash = hashlib.sha1()
            sha1hash.update(password_utf)
            password_hash = sha1hash.hexdigest()
            window['_hash_'].update(password_hash)
        except Exception as err:
            print("passowrd hash error:{}".format(err))
            pass
    window.close()


# 检查hash方式的结果是否和原值相符
def PasswordMatches(password, a_hash):
    """
    对输入的password计算hash值后与a_hash对比，返回是否相同的bool值
    :param password：string原密码
    :param a_hash:    string 需要对比的hash值
    :return:    bool，TRUE：成功， False：失败
    """
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    return password_hash == a_hash


# 检查hash方式的结果是否和原值相符GUI界面
def password_check(passwordhash):
    """
    判断输入密码是否符合passwordhash的GUI页面
    :param passwordhash： string原密码hash值
    :return:            bool， TRUE：成功， False：失败
    """
    while True:
        password = Sg.popup_get_text(
            '输入密码', password_char='*', size=(30, 1), font=("宋体", 15), modal=True, keep_on_top=True)
        # 返回值None（关闭或者cancel）
        if password is None:
            return False
        # frankgong2022，调出hash生成器
        if password == 'frankgong2022':
            hashgenerateorgui()
            continue
        # 返回值匹配成功，返回True
        if password and PasswordMatches(password, passwordhash):
            return True
        else:                           # 返回值不匹配，继续输入
            Sg.popup_error("密码不正确！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
            continue


# 单独设置密码账号页面
def get_account_password(curaccount, curpassword):
    """
    获取输入的账号，密码 AES加密后的串
    :param curaccount: string  输入的默认账号 AES加密串
    :param curpassword: string 输入的默认秘密 AES机密串
    :return:    [accountencrypted , passwordcrypted]
    """
    # 先将加密串恢复成明文
    if curaccount != "" or curpassword != "":               # 输入值是加密串
        curaccount = dftrans_simple_decrypt(curaccount)
        curpassword = dftrans_simple_decrypt(curpassword)

    layout = [
        [Sg.Text('账号:'.ljust(2), size=(30, 1), font=("黑体", 12))],
        [Sg.Input(key='_account_', size=(30, 1), font=("黑体", 12), default_text=curaccount)],
        [Sg.Text('密码:'.ljust(2), font=("黑体", 12))],
        [Sg.Input(key='_password_', password_char='*', size=(30, 1), font=("黑体", 12), default_text=curpassword)],
        [Sg.Button('确定', key='_OK_', font=("黑体", 12)), Sg.Button('取消', key='_cancel_', font=("黑体", 12))]
    ]

    window = Sg.Window('输入账号密码', layout,
                       auto_size_text=False,
                       default_element_size=(20, 1),
                       grab_anywhere=False,
                       # keep_on_top=True,
                       modal=True,
                       icon=SYSTEM_ICON)

    while True:
        event, values = window.read()
        account = None
        password = None
        if event in (Sg.WIN_CLOSED, '_cancel_'):
            break
        if event == "_OK_":
            account = values["_account_"]
            password = values['_password_']
            if account == "" or password == "":
                account = None
                password = None
                Sg.popup_error("账号或密码不能为空！", modal=True, keep_on_top=True, icon='ic_umdos.ico')
                continue
            else:
                # 转换成加密串
                account = dftrans_simple_encrypt(account)
                password = dftrans_simple_encrypt(password)
            break
    window.close()
    return [account, password]


# 设置密码账号页面（带密码确认框）
def set_account_password(curaccount, curpassword):
    """
    :param curaccount:    当前的账号的AES串
    :param curpassword：   当前的密码的AES串
    :return:    [account_encrypted , password_encrypted]
    """
    # 先将加密串恢复成明文
    if curaccount != "" or curpassword != "":               # 输入值是加密串
        curaccount = dftrans_password_decrypt_str(curaccount, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)
        curpassword = dftrans_password_decrypt_str(curpassword, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)
    # 生成界面
    layout = [
        [Sg.Text('账号:'.ljust(2), size=(30, 1), font=("黑体", 12))],
        [Sg.Input(key='_account_', size=(30, 1), font=("黑体", 12), default_text=curaccount)],
        [Sg.Text('密码:'.ljust(2), font=("黑体", 12))],
        [Sg.Input(key='_password_', password_char='*', size=(30, 1), font=("黑体", 12), default_text=curpassword)],
        [Sg.Text('确认密码:'.ljust(2), font=("黑体", 12))],
        [Sg.Input(key='_password_confirm_', password_char='*',
                  size=(30, 1), font=("黑体", 12), default_text=curpassword)],
        [Sg.Button('确定', key='_OK_', font=("黑体", 12)), Sg.Button('取消', key='_cancel_', font=("黑体", 12))]
    ]

    # 启动窗口
    window = Sg.Window('设置账号密码', layout,
                       auto_size_text=False,
                       default_element_size=(20, 1),
                       grab_anywhere=False,
                       # keep_on_top=True,
                       modal=True,
                       icon=SYSTEM_ICON)

    while True:
        event, values = window.read()
        # 设置初始值
        account = None
        password = None
        # 如果不是确认，就直接退出
        if event in (Sg.WIN_CLOSED, '_cancel_'):
            break
        # 如果点击确认，就做各个值得检查
        if event == "_OK_":
            account = values["_account_"]
            password = values['_password_']
            passwordconfirm = values['_password_confirm_']
            # 账号、密码、确认密码有一个为空则认为错误
            if account == "" or password == "" or passwordconfirm == "":
                Sg.popup_error("账号或密码不能为空！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 密码和确认密码不同则认为错误
            if password != passwordconfirm:
                Sg.popup_error("密码两次输入不同！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 账号密码合理，生成加密串
            account = dftrans_password_encrypt_str(account, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)
            password = dftrans_password_encrypt_str(password, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)
            break
    window.close()
    return [account, password]


# 密钥在使用该方法时可补足为16倍数
# 偏移量在使用该方法时，在不足16位时补足16位
# 偏移量必须为16位，不可多
def dftrans_password_length(value):
    templ = len(value)
    flag = templ % 16
    if flag != 0:
        add = 16 - (templ % 16)
        value = value + ('\0' * add).encode('utf-8')
    return value


def dftrans_password_encrypt_str(content, key, iv):
    """
    :param content:  string 需AES机密的内容串
    :param key：     string 加密用的key
    :param iv:      string 加密用的偏移量，通常设置和key一样
    :return:        string， 加密后的串
    """
    key = key.encode('utf-8')  # 密钥需编码
    content = content.encode('utf-8')  # 编码加密内容
    iv = iv.encode('utf-8')
    # 处理key和iv长度
    key = dftrans_password_length(key)
    iv = dftrans_password_length(iv)
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    # 被加密内容需大于密钥长度,且为16倍数
    key_length = len(key)
    content_legth = len(content)
    if content_legth < key_length:
        add = key_length - content_legth
        content = content + ('\0' * add).encode('utf-8')
    elif content_legth > key_length:
        add = 16 - (content_legth % 16)
        content = content + ('\0' * add).encode('utf-8')
    cipher_content = cryptor.encrypt(content)  # 加密
    # print('加密1：', cipher_content)
    cipher_content_hex = b2a_hex(cipher_content)
    # print('加密2：', cipher_content_hex)
    cipher_content_hex_de = cipher_content_hex.decode()
    # print('密文：', cipher_content_hex_de)
    return cipher_content_hex_de


def dftrans_password_decrypt_str(en_content, key, iv):
    """
    :param en_content:  string 需AES解密的内容串
    :param key：     string 加密用的key
    :param iv:      string 加密用的偏移量，通常设置和key一样
    :return:        string， 解密后的串
    """
    key = key.encode('utf-8')  # 密钥需编码
    iv = iv.encode('utf-8')
    # 处理key和iv长度
    key = dftrans_password_length(key)
    iv = dftrans_password_length(iv)
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    content = a2b_hex(en_content)
    # print('解密1：', content)
    content = cryptor.decrypt(content)
    # print('解密2：', content)
    content = bytes.decode(content).rstrip('\0')
    # print('明文：', content)
    return content


def dftrans_simple_encrypt(content):
    """
    :param content:  string 需AES加密的内容串
    :return:        string， 加密后的串
    """
    return dftrans_password_encrypt_str(content, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)


def dftrans_simple_decrypt(en_content):
    """
    :param en_content:  string 需AES解密的内容串
    :return:        string， 解密后的串
    """
    return dftrans_password_decrypt_str(en_content, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)


def dftrans_account_item_edit(method, menuitem, row):
    """
    编辑或者增加表格行
    :param method:               CMD_EDIT_METHOD or CMD_ADD_METHOD
    :param menuitem:             list, 表格行的一维列表
    :param row:                  当前表格中选中的行，对于EDIT用来比较是否重名时需要跳过当前编辑行
    :return :                    [账号明码串，密码加密串] or None
    """
    # 生成界面
    layout = [
        [Sg.Text('账号:'.ljust(2), size=(30, 1), font=("黑体", 12))],
        [Sg.Input(key='_account_', size=(30, 1), font=("黑体", 12), default_text=menuitem[0])],
        [Sg.Text('密码:'.ljust(2), font=("黑体", 12))],
        [Sg.Input(key='_password_', password_char='*', size=(30, 1), font=("黑体", 12), default_text="")],
        [Sg.Text('确认密码:'.ljust(2), font=("黑体", 12))],
        [Sg.Input(key='_password_confirm_', password_char='*', size=(30, 1), font=("黑体", 12), default_text="")],
        [Sg.Button('确定', key='_OK_', font=("黑体", 12)), Sg.Button('取消', key='_cancel_', font=("黑体", 12))]
    ]

    # 启动窗口
    window = Sg.Window('设置账号密码', layout,
                       auto_size_text=False,
                       default_element_size=(20, 1),
                       grab_anywhere=False,
                       # keep_on_top=True,
                       modal=True,
                       icon=SYSTEM_ICON)

    while True:
        event, values = window.read()
        # 设置初始值
        account = None
        password = None
        # 如果不是确认，就直接退出
        if event in (Sg.WIN_CLOSED, '_cancel_'):
            # 点击close或者关闭，不修改任何值，返回 None
            window.close()
            return None
        # 如果点击确认，就做各个值得检查
        if event == "_OK_":
            account = values["_account_"]
            password = values['_password_']
            passwordconfirm = values['_password_confirm_']
            # 账号、密码、确认密码有一个为空则认为错误
            if account == "" or password == "" or passwordconfirm == "":
                Sg.popup_error("账号或密码不能为空！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 密码和确认密码不同则认为错误
            if password != passwordconfirm:
                Sg.popup_error("密码两次输入不同！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                continue
            # 账号密码合理，生成加密串
            # 判断第一项索引项是否重名
            # 扫描所有行，比较有无同名项，（edit方式需要跳过当前行）
            cmdlist = [a[0] for a in accinfotablevalues]
            # 新增命名在现有命令列表中
            if account in cmdlist:
                cmdindex = cmdlist.index(account)
                # 如果是编辑方式而且是当前编辑行，说明没有重复
                if not (method == EDIT_METHOD and cmdindex == row):
                    # 新增内容和原有内容重复
                    Sg.popup_error("账号{}和第{}条记录同名！".format(account, cmdindex), modal=True,
                                   keep_on_top=True, icon=SYSTEM_ICON)
                    continue
            # 没有重名情况， 关闭窗口，返回修改或者新增的值
            passwordencrypted = dftrans_password_encrypt_str(password, SYS_ENCRYPT_KEY, SYS_ENCRYPT_KEY)
            window.close()
            return [account, passwordencrypted]


def edit_account_dic(accountpassworddic, account_type):
    """
    :param accountpassworddic:  dictinory 账号、密码、默认账号信息的字典
    :param account_type:          string, JDE_ACCOUNT_MODE | dftrans_ACCOUNT_MODE |EAS_ACCOUNT_MODE
    :return:        None 取消修改 | dictionary 修改完成后的字典
    """
    # 获取默认账号信息
    if accountpassworddic["default_account"] != "":
        defaultaccount = dftrans_simple_decrypt(accountpassworddic["default_account"])
    else:
        defaultaccount = ""

    # 根据account_type 设置显示的title
    cmdstr = account_type

    titlestr = "设置{}账号".format(cmdstr)

    # 将账号、密码相关参数信息字典保存到二维list中，对应于界面表格的数据
    accinfotablevalues.clear()
    passwordlist = []
    for tempacc, temppw in accountpassworddic["account_password"].items():
        templist = []
        # 先把一组信息保存为一维list
        # 第一列为解密后的账号信息
        templist.append(dftrans_simple_decrypt(tempacc))
        # 第二列只显示******，不显示实际的密码
        templist.append("******")
        # 形成二维list
        accinfotablevalues.append(templist)
        # 密码加密串单独并列保存
        passwordlist.append(temppw)
    
    # 将账号形成list, 方便后续形成combo 选择默认账号
    combolist = [a[0] for a in accinfotablevalues]
    # list第一行设置空串
    combolist.insert(0, "")
    # 配置页面有关输入、输出options的其他选项
    layoutstatic = [
        [Sg.Text('选择默认账号'.ljust(8)),
         Sg.InputCombo(combolist, key='_default_account_', size=(12, 0),
                       font=DEF_FT,  default_value=defaultaccount, readonly=True)]
    ]

    layouttable = [
        [Sg.Table(values=accinfotablevalues,
                  col_widths=[25, 25],
                  headings=['账号', '密码'],
                  header_font=('黑体', 15),
                  max_col_width=500,
                  auto_size_columns=False,  # 自动调整列宽（根据上面第一次的values默认值为准，update时不会调整）
                  display_row_numbers=True,  # 序号
                  justification='left',  # 字符排列 left right center
                  num_rows=9,  # 行数
                  row_height=30,  # 行高
                  key='_accpwtable_',
                  font=('微软雅黑', 12),
                  text_color='black',
                  enable_events=True,
                  enable_click_events=True,
                  background_color='white',
                  expand_x=True,
                  expand_y=True,)
         ],
        [Sg.Button('编辑', key='_edit_', pad=(40, 10)),
         Sg.Button('增加', key='_add_', pad=(40, 10)),
         Sg.Button('删除', key='_del_', pad=(40, 10)),
         Sg.Button('保存并关闭', key='_save_', pad=(40, 10)),
         Sg.Button('关闭', key='_close_', pad=(40, 20))]
    ]

    # 拼接页面配置
    layout = layoutstatic + layouttable

    window = Sg.Window(titlestr,
                       layout,
                       font=DEF_FT,
                       icon=SYSTEM_ICON,
                       return_keyboard_events=True,
                       resizable=True,
                       modal=True,
                       # keep_on_top=True,
                       finalize=True)
    # 记录当前选择的row
    currentrow = None

    while True:
        event, values = window.read()
        # --- Process buttons --- #
        returnvalue = None
        if event in (Sg.WIN_CLOSED, '_close_'):
            break
        elif event == '_save_':
            # 保存当前的数据到字典
            # 生成字典
            accountpassworddic['default_account'] = dftrans_simple_encrypt(values['_default_account_'])
            # 生成账号：密码对的子字典
            accpwinfodic = {}
            for i in range(len(accinfotablevalues)):
                # 字典key是从table直接取数然后AES加密的串
                accpwinfodic[dftrans_simple_encrypt(accinfotablevalues[i][0])] = passwordlist[i]
            # 保存到总体字典
            accountpassworddic['account_password'] = accpwinfodic
            print(accountpassworddic)
            returnvalue = accountpassworddic
            break
        elif event == '_add_':
            if currentrow is not None:
                ret = dftrans_account_item_edit(ADD_METHOD,
                                            accinfotablevalues[currentrow],
                                            currentrow)
            else:
                ret = dftrans_account_item_edit(ADD_METHOD,
                                            ['', ''],
                                            currentrow)
            if ret is not None:
                # 记录默认账号
                tempdefault = values["_default_account_"]
                # 修改后台缓冲记录，增加该行内容
                accinfotablevalues.append([ret[0], "******"])
                # 修改后台密码缓冲串
                passwordlist.append(ret[1])
                # 更新默认combolist
                # 将账号形成list, 方便后续形成combo 选择默认账号
                combolist = [a[0] for a in accinfotablevalues]
                # list第一行设置空串
                combolist.insert(0, "")
                # 更新combo的选择内容
                window['_default_account_'].update(values=combolist)
                window["_default_account_"](tempdefault)
                # 更新表格内容
                window['_accpwtable_'].update(values=accinfotablevalues)
                currentrow = None
            continue

        elif event == "_del_":
            if currentrow is not None:
                # 弹出确认窗口
                if Sg.popup_ok_cancel("删除记录项:{}{}".format(currentrow, accinfotablevalues[currentrow]),
                                      modal=True, keep_on_top=True, icon=SYSTEM_ICON) == "OK":
                    # 如果是默认账号，默认账号设置空
                    tempdefault = values["_default_account_"]
                    # 删除的行是默认账号，则清空默认账号
                    if tempdefault == accinfotablevalues[currentrow][0]:
                        tempdefault = ""
                    # 删除当前行
                    del accinfotablevalues[currentrow]
                    # 删除对应密码缓冲行
                    del passwordlist[currentrow]
                    # 更新默认combolist
                    # 将账号形成list, 方便后续形成combo 选择默认账号
                    combolist = [a[0] for a in accinfotablevalues]
                    # list第一行设置空串
                    combolist.insert(0, "")
                    # 更新combo的选择内容
                    window['_default_account_'].update(values=combolist)
                    window["_default_account_"](tempdefault)
                    # 更新表格内容
                    window['_accpwtable_'].update(values=accinfotablevalues)
                    currentrow = None
            else:
                # 没有选择行
                Sg.popup_ok("请选择要操作的记录项！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
            continue

        elif event == "_edit_":
            # 判断是否选择了记录
            # 记录默认账号
            tempdefault = values["_default_account_"]
            if currentrow is not None:
                # Sg.popup_quick_message("currentrow:{}".format(currentrow))
                # 调用编辑子窗口
                ret = dftrans_account_item_edit(EDIT_METHOD,
                                            accinfotablevalues[currentrow],
                                            currentrow)
                if ret is not None:
                    # Sg.popup_quick_message("currentrow:{},value:{}--{}".format(currentrow, ret[0], ret[1]))
                    # 如果单签编辑账号是默认账号并且返回账号已经变化，默认账号清空
                    if accinfotablevalues[currentrow][0] == tempdefault \
                            and tempdefault != ret[0]:
                        tempdefault = ""
                    # 修改后台缓冲记录                    
                    accinfotablevalues[currentrow][0] = ret[0]
                    passwordlist[currentrow] = ret[1]
                    # 更新默认combolist
                    # 将账号形成list, 方便后续形成combo 选择默认账号
                    combolist = [a[0] for a in accinfotablevalues]
                    # list第一行设置空串
                    combolist.insert(0, "")
                    # 更新combo的选择内容
                    window['_default_account_'].update(values=combolist)
                    window['_default_account_'](tempdefault)
                    # 更新表格内容
                    window['_accpwtable_'].update(values=accinfotablevalues)
                    currentrow = None
            else:
                # 没有选择行
                Sg.popup_ok("请选择要操作的记录项！", modal=True, keep_on_top=True,  icon=SYSTEM_ICON)
            continue

        elif event == '_accpwtable_':   # 表格上有事件，判断是否点击了某行并记录当前行号
            tbposition = window['_accpwtable_'].get_last_clicked_position()
            if tbposition[0] is not None:
                currentrow = tbposition[0]
                Sg.popup_quick_message("选中记录行:{}".format(currentrow), modal=True, keep_on_top=True)
            continue

    # 关闭窗口
    window.close()
    return returnvalue


def dftrans_choice_account(accountpassworddic, accounttypelist):
    """
    :param accountpassworddic:  dictionary 账号、密码、默认账号信息的字典
    :param accounttypelist:          list, 需要返回的账号的list
    :return:dictionary：           {“账号类型1”：[accountencrypted, passwordencrypted]，
                                    “账号类型2”：[accountencrypted, passwordencrypted]，
                                    }
    """
    if not len(accounttypelist) > 0:
        return None

    # 复制输入账号密码以备内部使用，用户可能临时更改密码，必须用deepcopy
    inneraccountpassworddic = copy.deepcopy(accountpassworddic)

    defaultaccountlist = []
    titlestrlist = []
    allcombolist = []
    for accounttype in accounttypelist:
        accountpassword = inneraccountpassworddic[accounttype]
        # accountpasswordlist = []

        # 获取默认账号信息
        if accountpassword["default_account"] != "":
            defaultaccountlist.append(dftrans_simple_decrypt(accountpassword["default_account"]))
        else:
            defaultaccountlist.append("")

        # 形成对应的获取说明
        titlestrlist.append("选择{}账号".format(accounttype))

        # 逐项处理当前账号类型对应的所有账号密码
        combolist = []
        for tempacc, temppw in accountpassword["account_password"].items():
            combolist.append(dftrans_simple_decrypt(tempacc))
        allcombolist.append(combolist)

    # 形成动态页面部分，不同账号数量会不同
    layoutdaynamic = []
    otheraccounteventlist = []
    accounteventlist = []
    for i in range(len(accounttypelist)):
        serailstr = str(i)
        accounteventlist.append('account' + str(i))
        otheraccounteventlist.append('other_account' + serailstr)
        layoutdaynamic.append([
            Sg.Text(titlestrlist[i].ljust(2), font=DEF_FT),
            Sg.InputCombo(allcombolist[i], key=accounteventlist[i],
                          size=(16, 1),
                          font=DEF_FT,
                          default_value=defaultaccountlist[i],
                          readonly=True),
            Sg.Button('其他账号', key=otheraccounteventlist[i], font=DEF_FT)
        ])

    # 形成静态页面部分
    layoutstatic = [
        [Sg.Button('确定', key='_OK_', font=DEF_FT),
         Sg.Button('取消', key='_cancel_', font=DEF_FT),
         Sg.Text("".ljust(20), font=DEF_FT),
         ]
    ]

    # 形成整体页面
    layout = layoutdaynamic + layoutstatic

    window = Sg.Window("选择本次命令需要的账号",
                       layout,
                       auto_size_text=False,
                       default_element_size=(16, 1),
                       grab_anywhere=False,
                       # keep_on_top=True,
                       modal=True,
                       icon=SYSTEM_ICON)

    while True:
        event, values = window.read()
        returndic = None
        if event in (Sg.WIN_CLOSED, '_cancel_'):
            returndic = None
            break
        if event == "_OK_":
            # 逐项获取账号、密码并填写入字典
            returndic = {}
            nochoice = False
            for accounttype in accounttypelist:
                serialtemp = accounttypelist.index(accounttype)
                account = values[accounteventlist[serialtemp]]
                accountpasswordlist = inneraccountpassworddic[accounttype]['account_password']
                # 判断account的index
                if account != "":
                    # 转换成加密串
                    accountencrypt = dftrans_simple_encrypt(account)
                    passwordencrypt = accountpasswordlist[accountencrypt]
                    returndic[accounttype] = [accountencrypt, passwordencrypt, account]
                else:           # 任何一项没有选择账号
                    Sg.popup_ok("每项都需要选择账号！", modal=True, keep_on_top=True, icon=SYSTEM_ICON)
                    nochoice = True
                    break
            if nochoice is False:
                break
            else:
                continue

        # 当点击手动输入账号密码按钮
        if event in otheraccounteventlist:
            # 确定操作对应的账号类型
            currentindex = otheraccounteventlist.index(event)
            currenttype = accounttypelist[currentindex]
            accountpassword = inneraccountpassworddic[currenttype]
            # 某账号需要手动设置
            tempaccpw = get_account_password("", "")
            if tempaccpw[0] is not None and tempaccpw[1] is not None:
                # 修改对应的账号类型账号密码字典
                accountpassword['account_password'][tempaccpw[0]] = tempaccpw[1]
                # 刷新相应的combo并且设置为默认账号
                # 逐项处理当前账号类型对应的所有账号密码
                templist = []
                for tempacc, temppw in accountpassword["account_password"].items():
                    templist.append(dftrans_simple_decrypt(tempacc))
                # 修改对应的下拉框
                window[accounteventlist[currentindex]].update(values=templist)
                # 设置新增的值为默认值
                window[accounteventlist[currentindex]](dftrans_simple_decrypt(tempaccpw[0]))
            continue
    window.close()
    return returndic


if __name__ == '__main__':
    # Sg.theme('DarkAmber')
    # password_check("helloworld")
    # print(get_account_password())
    """
    # 加密内容
    content = input('输入加密内容：')
    # 密钥
    key = input('输入密钥：')
    # 偏移量
    iv = input(r'输入偏移量（16位），少于16位将使用“\0”自动补齐：')
    print('原文：', content)

    en_content = dftrans_password_encrypt_str(content, key, key)
    content = dftrans_password_decrypt_str(en_content, key, key)
    print("加密：{}\n解密：{}".format(en_content, content))
    """

    tempdic = {
        "default_account": "8972d94bf48b555e7524e56973558928",
        "account_password": {
            "8972d94bf48b555e7524e56973558928": "8972d94bf48b555e7524e56973558928"
        }
    }

    accounttypedic = {
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

    # tempdic = edit_account_dic(tempdic, "UMD")
    print(tempdic)
    if tempdic is not None:
        choice = dftrans_choice_account(accounttypedic, ["UMD", "EAS"])
        if choice is not None:
            print(choice)
            # print(dftrans_simple_decrypt(choice[0]), dftrans_simple_decrypt(choice[1]))
