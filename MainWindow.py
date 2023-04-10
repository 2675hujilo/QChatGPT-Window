import atexit
import os
import shutil

import ast
import json
import re
import subprocess
import threading
import time

import markdown2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCursor, QBrush, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox, QApplication
import sys


log_colors_config = {
    'DEBUG': 'green',
    'INFO': 'black',
    'WARNING': 'purple',
    'ERROR': 'red',
    'CRITICAL': 'cyan',
}

doc_cfg = "override.json"
doc_cmds = "cmdpriv.json"
doc_tips = "tips-win.py"

if not os.path.exists('banlist.py'):
    shutil.copy('res/templates/banlist-template.py', 'banlist.py')

# 检查是否有sensitive.json
if not os.path.exists("sensitive.json"):
    shutil.copy("res/templates/sensitive-template.json", "sensitive.json")

# 检查是否有scenario/default.json
if not os.path.exists("scenario/default.json"):
    shutil.copy("scenario/default-template.json", "scenario/default.json")

# 检查cmdpriv.json
if not os.path.exists("cmdpriv.json"):
    shutil.copy("res/templates/cmdpriv-template.json", "cmdpriv.json")

# 检查tips_custom
if not os.path.exists("tips.py"):
    shutil.copy("tips-custom-template.py", "tips.py")

# 检查temp目录
if not os.path.exists("temp/"):
    os.mkdir("temp/")

# 检查并创建plugins、prompts目录
check_path = ["plugins", "prompts"]
for path in check_path:
    if not os.path.exists(path):
        os.mkdir(path)

# 配置文件存在性校验
if not os.path.exists('config.py'):
    shutil.copy('config-template.py', 'config.py')

if not os.path.exists(doc_cfg):
    with open('override-all.json', 'r', encoding="utf-8") as f1, open(doc_cfg, 'w', encoding="utf-8") as f2:
        for line in f1:
            # if "logging_level = logging.INFO" in line or "import logging" in line:
            #     continue
            f2.write(line)
       # f2.write("logging_level = logging.INFO")

with open('tips.py', 'r', encoding="utf-8") as f1, open(doc_tips, 'w', encoding="utf-8") as f2:
    for line in f1:
        f2.write(line)

if not os.path.exists(doc_cmds):
    with open('cmdpriv.json', 'r', encoding="utf-8") as f1, open(doc_cmds, 'w', encoding="utf-8") as f2:
        for line in f1:
            f2.write(line)
if not os.path.exists("main.pyw"):
    with open('main.py', 'r', encoding="utf-8") as f1,open ("main.pyw", 'w', encoding="utf-8") as f2:
        for line in f1:
            f2.write(line)
# 文本框对应字段的值
# doc_cfg = "config.py"的值
value_cfgs_mirai_http_api_config = "mirai_http_api_config"
value_cfgs_mirai_http_api_config_adapter = "adapter"
value_cfgs_mirai_http_api_config_host = "host"
value_cfgs_mirai_http_api_config_port = "port"
value_cfgs_mirai_http_api_config_verifyKey = "verifyKey"
value_cfgs_mirai_http_api_config_qq = "qq"

value_cfgs_openai_config = "openai_config"
value_cfgs_openai_config_api_key = "api_key"
value_cfgs_openai_config_api_key_default = "default"
value_cfgs_openai_config_http_proxy = "http_proxy"
value_cfgs_openai_config_reverse_proxy = "reverse_proxy"

value_cfgs_user_name = "user_name"
value_cfgs_bot_name = "bot_name"

value_cfgs_default_prompt = "default_prompt"

value_cfgs_preset_mode = "preset_mode"
value_cfgs_admin_qq = "admin_qq"

value_cfgs_response_rules = "response_rules"
value_cfgs_response_rules_at = "at"
value_cfgs_response_rules_prefix = "prefix"
value_cfgs_response_rules_regexp = "regexp"
value_cfgs_response_rules_random_rate = "random_rate"

value_cfgs_ignore_rules = "ignore_rules"
value_cfgs_ignore_rules_prefix = "prefix"
value_cfgs_ignore_rules_regexp = "regexp"

value_cfgs_prompt_submit_length = "prompt_submit_length"

value_cfgs_completion_api_params = "completion_api_params"
value_cfgs_completion_api_params_model = "model"
value_cfgs_completion_api_params_temperature = "temperature"
value_cfgs_completion_api_params_max_tokens = "max_tokens"
value_cfgs_completion_api_params_top_p = "top_p"
value_cfgs_completion_api_params_frequency_penalty = "frequency_penalty"
value_cfgs_completion_api_params_presence_penalty = "presence_penalty"

value_cfgs_image_api_params = "image_api_params"
value_cfgs_image_api_params_size = "size"

value_cfgs_include_image_description = "include_image_description"
value_cfgs_quote_origin = "quote_origin"
value_cfgs_process_message_timeout = "process_message_timeout"
value_cfgs_retry_times = "retry_times"
value_cfgs_show_prefix = "show_prefix"
value_cfgs_multi_subject = "multi_subject"
value_cfgs_waifu_voice = "waifu_voice"
value_cfgs_pool_num = "pool_num"
value_cfgs_sys_pool_num = "sys_pool_num"
value_cfgs_admin_pool_num = "admin_pool_num"
value_cfgs_user_pool_num = "user_pool_num"
value_cfgs_session_expire_time = "session_expire_time"
value_cfgs_rate_limitation = "rate_limitation"
value_cfgs_rate_limit_strategy = "rate_limit_strategy"
value_cfgs_blob_message_threshold = "blob_message_threshold"
value_cfgs_blob_message_strategy = "blob_message_strategy"
value_cfgs_font_path = "font_path"
value_cfgs_income_msg_check = "income_msg_check"
value_cfgs_sensitive_word_filter = "sensitive_word_filter"
value_cfgs_baidu_check = "baidu_check"
value_cfgs_baidu_api_key = "baidu_api_key"
value_cfgs_baidu_secret_key = "baidu_secret_key"
value_cfgs_api_key_fee_threshold = "api_key_fee_threshold"
value_cfgs_encourage_sponsor_at_start = "encourage_sponsor_at_start"
value_cfgs_auto_switch_api_key = "auto_switch_api_key="
value_cfgs_hide_exce_info_to_user = "hide_exce_info_to_user"
value_cfgs_upgrade_dependencies = "upgrade_dependencies"
value_cfgs_report_usage = "report_usage"
value_cfgs_inappropriate_message_tips = "inappropriate_message_tips"
value_cfgs_logging_level="logging_level"

# doc_cmds = "cmdpriv.json"的值
value_cmds_draw = "draw"
value_cmds_plugin = "plugin"
value_cmds_plugin_get = "plugin.get"
value_cmds_plugin_update = "plugin.update"
value_cmds_plugin_del = "plugin.del"
value_cmds_plugin_off = "plugin.off"
value_cmds_plugin_on = "plugin.on"
value_cmds_default = "default"
value_cmds_default_set = "default.set"
value_cmds_del = "del"
value_cmds_del_all = "del.all"
value_cmds_delhst = "delhst"
value_cmds_delhst_all = "delhst.all"
value_cmds_last = "last"
value_cmds_list = "list"
value_cmds_next = "next"
value_cmds_prompt = "prompt"
value_cmds_resend = "resend"
value_cmds_reset = "reset"
value_cmds_cfg = "cfg"
value_cmds_cmd = "cmd"
value_cmds_help = "help"
value_cmds_reload = "reload"
value_cmds_update = "update"
value_cmds_usage = "usage"
value_cmds_version = "version"

# doc_tips = "tips.py"的值
value_tips_alter_tip_message = "alter_tip_message"
value_tips_rate_limit_drop_tip = "rate_limit_drop_tip"
value_tips_help_message = "help_message"
value_tips_reply_message = "reply_message"
value_tips_replys_message = "replys_message"
value_tips_command_admin_message = "command_admin_message"
value_tips_command_err_message = "command_err_message"
value_tips_command_reset_message = "command_reset_message"
value_tips_command_reset_name_message = "command_reset_name_message"






class Bot(QObject):
    output_signal = pyqtSignal(str)

    def __init__(self, MainWindow):
        super().__init__(MainWindow)
        self.main_window = MainWindow
        self.process = None
        self.running = False
        self.check_running_timer = QTimer()
        self.check_running_timer.timeout.connect(self.check_running)
        self.check_running_timer.start(1000)
        # atexit.register(self.exit_handler)  # 注册退出函数
    #     self.hook = win32api.SetConsoleCtrlHandler(self.handle_exit, True)
    #
    # def handle_exit(self, event):
    #     if event == win32con.CTRL_CLOSE_EVENT:
    #         self.main_window.update_status_buttons()
    #         self.update_status_buttons()
    #         return True  # 返回True表示已处理该事件
    def check_running(self):
        if self.process is not None and self.process.poll() is None:
            if not self.running:
                self.running = True
                self.output_signal.emit("程序已经在运行中。\n")
        else:
            if self.running:
                self.running = False
                self.output_signal.emit("程序已经停止。\n")
                self.main_window.update_status_buttons()

    # def exit_handler(self):
    #     if self.running:
    #         self.running = False
    #         self.output_signal.emit(" 程序已经停止。\n")
    #         self.update_status_buttons()
    def start(self):
        if self.running:
            self.output_signal.emit("程序已经在运行中。\n")
            return
        self.running = True


        # 当从pycharm中无参数启动时，编码为utf-8
        # 当从pycharm中有--debug参数启动时，编码为gbk
        # 当从cmd中无参数启动时，编码为gbk
        # 当从cmd中有--debug参数启动时，编码为gbk
        try:
            cmd=self.main_window.page_main_edit_current_command.text()
            self.process = subprocess.Popen(
                cmd.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="gbk",
                universal_newlines=True,
                bufsize=1,
                errors="ignore",

            )
        except Exception as e:
            self.running = False
            rai_dia(e)

        def output_reader():
            while self.running:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.output_signal.emit(line)

        threading.Thread(target=output_reader, daemon=True).start()

    def stop(self):
        if not self.running:
            self.output_signal.emit("程序已经停止。\n")
            return
        # win32api.SetConsoleCtrlHandler(self.hook, False)
        self.running = False
        self.process.terminate()
        self.process.wait()

    def is_running(self):
        return self.running


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bot = Bot(self)
        self.bot.output_signal.connect(self.log_output)
        self.value_cfgs_default_prompt = "default_prompt"
        self.update_status_buttons()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         print("Left button clicked")
    #     elif event.button() == Qt.RightButton:
    #         print("Right button clicked")
    #     elif event.button() == Qt.MiddleButton:
    #         print("Middle button clicked")
    def log_output(self, line):
        self.page_log_text_appendText(line)

    def update_status_buttons(self):
        if self.bot.is_running():
            self.page_main_edit_bot_status_on.setHidden(False)
            self.page_main_edit_bot_status_off.setHidden(True)
        else:
            self.page_main_edit_bot_status_on.setHidden(True)
            self.page_main_edit_bot_status_off.setHidden(False)

    def bot_start_clicked(self):
        if len(str(self.dict_cfgs[value_cfgs_admin_qq]))<2:
            QtWidgets.QMessageBox.warning(self,"第一次启动","请在配置页面输入管理员QQ后，再启动！")

        else:
            self.bot.start()

            self.update_status_buttons()

    def bot_stop_clicked(self):
        self.bot.stop()

        self.bot.check_running_timer.stop()
        self.update_status_buttons()
    def closeEvent(self, event):
        self.bot.stop()
        while self.bot.is_running():
            time.sleep(0.1)
        super().closeEvent(event)

    def test1(self):

        self.page_log_text_appendText(
            "[2023-04-06 20:29: 0], group: [204785790, 691226829]")

    def switchEncoding(self):
        print("a")

    # def log_btn_send_clicked(self):
    #
    #     self.bot.process.stdin.write(self.page_main_edit_current_command.text() + '\n')
    #     print("a")
    def open_log_path(self):
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        try:
            os.startfile(log_path)
        except Exception as e:
            rai_dia(e)

    def open_scenario_path(self):
        scenario_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenario')
        try:
            os.startfile(scenario_path)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "我", "最少保留一个人格！")

    def page_log_text_appendText(self, text):
        # 获取当前的光标位置
        cursor = self.page_log_text.textCursor()
        # 移动光标到文档结尾
        cursor.movePosition(QTextCursor.End)

        # 过滤掉控制字符
        text = re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', text)

        # 匹配日志级别和日志信息
        log_pattern = r'\b(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)\b'
        match = re.search(log_pattern, text)

        # 如果匹配成功，设置颜色样式
        if match:
            level = match.group()
            message = text[len(level) + 2:]  # 去掉level和": "后的文本内容

            # 设置文本颜色
            color = log_colors_config.get(level, 'white')
            cursor.movePosition(QTextCursor.End)

            format = cursor.charFormat()
            format.setForeground(QBrush(QColor(color)))

            cursor.insertText(f'{text}', format)
        else:
            # 在文本尾部追加内容
            color = 'black'
            format = cursor.charFormat()
            format.setForeground(QBrush(QColor(color)))
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(f'{text}', format)

        # 更新光标位置
        self.page_log_text.setTextCursor(cursor)

        # 确保文档内容已经展示出来（如果需要滚动条自动跟随最新内容，则需要调用该函数）
        self.page_log_text.ensureCursorVisible()

    def add_api_key(self):
        api_key_name, ok = QtWidgets.QInputDialog.getText(self, "添加 API Key", "API 名称：")
        if ok and api_key_name:
            if api_key_name in self.dict_cfgs.get(value_cfgs_openai_config, {}).get(value_cfgs_openai_config_api_key,
                                                                                    {}).keys():
                QtWidgets.QMessageBox.warning(self, "添加 API Key", "API 名称已存在！")
            else:
                while True:
                    api_key_value, ok = QtWidgets.QInputDialog.getText(self, "添加 API Key", "API 值：")
                    if ok and api_key_value:
                        regex = QtCore.QRegExp("^sk-.+$")
                        validator = QtGui.QRegExpValidator(regex, self)
                        if validator.validate(api_key_value, 0)[0] == QtGui.QValidator.Acceptable:
                            if value_cfgs_openai_config not in self.dict_cfgs:
                                self.dict_cfgs[value_cfgs_openai_config] = {}
                            if value_cfgs_openai_config_api_key not in self.dict_cfgs[value_cfgs_openai_config]:
                                self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key] = {}

                            # 新增键值对并排序
                            self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key][
                                api_key_name] = api_key_value
                            sorted_dict = dict(sorted(
                                self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key].items()))
                            self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key] = sorted_dict

                            # 更新下拉框
                            self.page_set_edit_cfg_api.clear()
                            self.page_set_edit_cfg_api.addItems(sorted_dict.keys())
                            self.page_set_edit_cfg_api.setCurrentIndex(self.page_set_edit_cfg_api.count() - 1)

                            # 写回文件
                            with open(doc_cfg, "w", encoding='utf-8') as f:
                                for key, value in self.dict_cfgs.items():
                                    f.write(f"{key} = {repr(value)}\n")
                            break
                        else:
                            QtWidgets.QMessageBox.warning(self, "添加 API Key", "API 值格式不正确，请重新输入！")
                            continue
                    else:
                        break


    def del_api_key(self):
        self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key].pop(
            self.page_set_edit_cfg_api.currentText(), None)
        self.page_set_edit_cfg_api.removeItem(self.page_set_edit_cfg_api.currentIndex())

        # 写回文件
        try:
            with open(doc_cfg, "w", encoding='utf-8') as f:
                for key, value in self.dict_cfgs.items():
                    f.write(f"{key} = {repr(value)}\n")
        except Exception as e:
            rai_dia(e)
    def add_default_prompt(self):
        new_key, ok = QtWidgets.QInputDialog.getText(self, "添加普通人格", "请输入人格名:")
        if ok:
            if new_key in self.dict_cfgs.get(value_cfgs_default_prompt, {}).keys():
                QtWidgets.QMessageBox.warning(self, "添加普通人格", "人格名已存在！")
            else:
                # 使用QInputDialog获取新值
                new_value, ok = QtWidgets.QInputDialog.getText(self, "添加普通人格", "请输入人格内容:")
                if ok and new_value:
                    # 将新键值对插入字典
                    self.dict_cfgs[value_cfgs_default_prompt][new_key] = new_value
                    with open(doc_cfg, "w", encoding='utf-8') as f:
                        for key, value in self.dict_cfgs.items():
                            f.write(f"{key} = {repr(value)}\n")
                    # # 更新下拉框
                    self.page_set_edit_cfg_default_prompt_choose.clear()
                    self.page_set_edit_cfg_default_prompt_choose.addItems(
                        self.dict_cfgs[value_cfgs_default_prompt].keys())


    def del_default_prompt(self):
        if len(self.dict_cfgs[value_cfgs_default_prompt]) == 1:
            QtWidgets.QMessageBox.warning(self, "删除普通人格", "最少保留一个人格！")
        else:
            self.dict_cfgs[value_cfgs_default_prompt].pop(self.page_set_edit_cfg_default_prompt_choose.currentText(), None)
            self.page_set_edit_cfg_default_prompt_choose.removeItem(
                self.page_set_edit_cfg_default_prompt_choose.currentIndex())
            try:
                with open(doc_cfg, "w", encoding='utf-8') as f:
                    for key, value in self.dict_cfgs.items():
                        f.write(f"{key} = {repr(value)}\n")
            except Exception as e:
                rai_dia(e)

    def update_default_prompt(self):
        current_text = self.page_set_edit_cfg_default_prompt_choose.currentText()
        if current_text in self.dict_cfgs.get(value_cfgs_default_prompt, {}):
            self.page_set_edit_cfg_default_prompt.setPlainText(
                self.dict_cfgs[value_cfgs_default_prompt][self.page_set_edit_cfg_default_prompt_choose.currentText()])
        else:
            # 给出默认值或错误提示
            print("无法获取该键人格下拉框的值的值。")

    def setupUi(self, MainWIndow):
        MainWIndow.setObjectName("MainWIndow")
        MainWIndow.setWindowIcon( QtGui.QIcon("images/icon.ico"))
        MainWIndow.resize(1160, 840)
        MainWIndow.setMinimumSize(QtCore.QSize(1160, 840))
        MainWIndow.setMaximumSize(QtCore.QSize(1300, 840))
        MainWIndow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWIndow.setStyleSheet(" border:0px;\n"
                                 "/*background-color:  rgba(106, 160, 217, 0.5) \n"
                                 "background-image:   url(\'back.png\')*/\n"
                                 "QMainWindow::separator {\n"
                                 "    height: 0;\n"
                                 "}\n"
                                 "\n"
                                 "QWidget#centralWidget { \n"
                                 "    border: none;\n"
                                 "    margin-top: 1px;\n"
                                 "}\n"
                                 "\n"
                                 "QStatusBar {\n"
                                 "    height: 30px;\n"
                                 "}")
        with open(doc_tips, "r", encoding='utf-8') as f:
            tip_str = f.read()
        tip_ast = ast.parse(tip_str)
        tip_dict = {}
        for node in tip_ast.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                key = node.targets[0].id
                value = ast.literal_eval(node.value)
                tip_dict[key] = value

        # 在内存中保存配置字典
        self.dict_tips = tip_dict.copy()

        # 更新tips字段的值并写回到配置文件中
        def update_value_tips(name, new_value):
            self.dict_tips[name] = new_value
            self.update_doc_tips()

        # 读取cfg.py文件并将其解析为Python对象
        try:
            with open(doc_cfg, "r", encoding='utf-8') as f:
                cfg_dict = json.load(f)
        except Exception as e:
            rai_dia(e)
        # with open(doc_cfg, "r", encoding='utf-8') as f:
        #     cfg_str = f.read()
        # cfg_ast = ast.parse(cfg_str)
        # cfg_dict = {}
        # for node in cfg_ast.body:
        #     if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        #         key = node.targets[0].id
        #         value = ast.literal_eval(node.value)
        #         cfg_dict[key] = value

        # 在内存中保存配置字典
        self.dict_cfgs = cfg_dict.copy()

        def update_mirai_qq(value):
            if value:
                new_dict = {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
                            **{value_cfgs_mirai_http_api_config_qq: int(value)}}
                update_value_cfgs(value_cfgs_mirai_http_api_config, new_dict)
        def update_admin_qq(value):
            if value:
                update_value_cfgs(value_cfgs_admin_qq, int(value))
        def update_value_cfgs(name, new_value):
            try:
                self.dict_cfgs[name] = new_value
                self.update_doc_cfgs()
            except Exception as e:
                rai_dia(e)
        try:
            with open(doc_cmds, "r", encoding='utf-8') as f:
                cmd = json.load(f)
        except Exception as e:
            rai_dia(e)
        # 在内存中保存配置字典
        self.dict_cmds = cmd.copy()

        # 更新cmdpriv.json文件中的数据
        def update_value_cmds(name, new_value):
            self.dict_cmds[name] = new_value
            try:
                with open(doc_cmds, "w", encoding='utf-8') as f:
                    json.dump(self.dict_cmds, f)
            except Exception as e:
                rai_dia(e)
        self.centralwidget = QtWidgets.QWidget(MainWIndow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(1300, 840))
        self.centralwidget.setMaximumSize(QtCore.QSize(1300, 840))
        self.centralwidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.centralwidget.setStyleSheet(" ")
        self.centralwidget.setObjectName("centralwidget")
        self.back_all = QtWidgets.QLabel(self.centralwidget)
        self.back_all.setGeometry(QtCore.QRect(0, 0, 1300, 840))
        self.back_all.setMinimumSize(QtCore.QSize(1300, 840))
        self.back_all.setMaximumSize(QtCore.QSize(1300, 840))
        self.back_all.setAutoFillBackground(False)
        self.back_all.setStyleSheet("/*background-image: url(images/bg_all.png);*/\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center center;\n"
                                    "background-attachment: fixed;")
        self.back_all.setText("")
        self.back_all.setPixmap(QtGui.QPixmap("images/bg_all.png"))
        self.back_all.setObjectName("back_all")
        self.back_top = QtWidgets.QLabel(self.centralwidget)
        self.back_top.setGeometry(QtCore.QRect(0, 0, 1300, 100))
        self.back_top.setMinimumSize(QtCore.QSize(1300, 100))
        self.back_top.setMaximumSize(QtCore.QSize(1300, 100))
        self.back_top.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.back_top.setStyleSheet("background-repeat: no-repeat;")
        self.back_top.setText("")
        self.back_top.setPixmap(QtGui.QPixmap("images/bg_top.png"))
        self.back_top.setObjectName("back_top")
        self.back_left = QtWidgets.QLabel(self.centralwidget)
        self.back_left.setGeometry(QtCore.QRect(0, 100, 140, 740))
        self.back_left.setMinimumSize(QtCore.QSize(140, 740))
        self.back_left.setMaximumSize(QtCore.QSize(140, 740))
        self.back_left.setText("")
        self.back_left.setPixmap(QtGui.QPixmap("images/bg_left - 副本.png"))
        self.back_left.setObjectName("back_left")
        self.back_right = QtWidgets.QLabel(self.centralwidget)
        self.back_right.setEnabled(True)
        self.back_right.setGeometry(QtCore.QRect(1160, 100, 140, 740))
        self.back_right.setMinimumSize(QtCore.QSize(140, 740))
        self.back_right.setMaximumSize(QtCore.QSize(140, 740))
        self.back_right.setText("")
        self.back_right.setPixmap(QtGui.QPixmap("images/bg_right.png"))
        self.back_right.setObjectName("back_right")
        self.menu_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.menu_tab.setGeometry(QtCore.QRect(0, 100, 1160, 740))
        self.menu_tab.setMinimumSize(QtCore.QSize(1020, 740))
        self.menu_tab.setMaximumSize(QtCore.QSize(1160, 740))
        self.menu_tab.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.menu_tab.setStyleSheet("/* This is argv_debug comment in argv_debug CSS stylesheet */\n"
                                    "QTabBar::tab {background-color: rgba(255, 255, 255, 0.001); } \n"
                                    "QTabBar::tab {\n"
                                    "                \n"
                                    "                text-align: left;\n"
                                    "            }\n"
                                    "QTabBar::tab {\n"
                                    "                height: 80px;\n"
                                    "                width: 140px;\n"
                                    "                font-size: 20px;\n"
                                    "                padding-left: 0px;\n"
                                    "                padding-right: 0px; \n"
                                    "    padding: 0px 0px 0px 0px;   /* 分别指定上、右、下、左四个方向的内边距大小 */\n"
                                    "            }\n"
                                    "            QTabBar::tab:selected {     \n"
                                    "            background-color: rgba(255, 255, 255, 0.6);\n"
                                    "            }\n"
                                    "QTabBar::tab:hover {\n"
                                    " background-color: rgba(255, 255, 255, 0.4);\n"
                                    "                 \n"
                                    "            }\n"
                                    "\n"
                                    "QTabWidget::pane { border-image: url(images/back_center.png) 0 0 0 0 stretch stretch;"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center center;\n"
                                    "background-attachment: fixed;}\n"
                                    "background-color: rgba(255, 255, 255,0.25); ")
        self.menu_tab.setTabPosition(QtWidgets.QTabWidget.West)
        self.menu_tab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.menu_tab.setTabsClosable(False)
        self.menu_tab.setTabBarAutoHide(True)
        self.menu_tab.setObjectName("menu_tab")
        self.tab_main = QtWidgets.QWidget()
        self.tab_main.setMinimumSize(QtCore.QSize(1020, 740))
        self.tab_main.setMaximumSize(QtCore.QSize(1160, 740))
        self.tab_main.setStyleSheet(
            "background-color: rgba(255, 255, 255,0.025);QMenu {background-color:rgb(233, 190, 203);}\n"
            "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
            " } ")
        self.tab_main.setObjectName("tab_main")
        self.page_main_label_bot_start = QtWidgets.QCommandLinkButton(self.tab_main)
        self.page_main_label_bot_start.setGeometry(QtCore.QRect(270, 590, 149, 85))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_main_label_bot_start.sizePolicy().hasHeightForWidth())
        self.page_main_label_bot_start.setSizePolicy(sizePolicy)
        self.page_main_label_bot_start.setStyleSheet("QPushButton::CommandLinkButton {\"\n"
                                                     " \"    background-color: #f1f1f1; /* 背景颜色 */\"\n"
                                                     " \"    border: none; /* 去除边框 */\"\n"
                                                     " \"    padding-left: 16px; /* 左侧缩排 */\"\n"
                                                     " \"}\"\n"
                                                     " \"QPushButton::CommandLinkButton:hover {\"\n"
                                                     " \"    background-color: #e1e1e1; /* 鼠标悬浮背景颜色 */\"}")
        self.page_main_label_bot_start.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/bot_start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_main_label_bot_start.setIcon(icon)
        self.page_main_label_bot_start.setIconSize(QtCore.QSize(250, 75))
        self.page_main_label_bot_start.setProperty("label_bot_start", QtGui.QPixmap("images/bot_start.png"))
        self.page_main_label_bot_start.setObjectName("page_main_label_bot_start")
        # 启动bot
        self.page_main_label_bot_start.clicked.connect(self.bot_start_clicked)

        self.page_main_label_bot_stop = QtWidgets.QCommandLinkButton(self.tab_main)
        self.page_main_label_bot_stop.setGeometry(QtCore.QRect(560, 580, 149, 95))
        self.page_main_label_bot_stop.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/bot_stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_main_label_bot_stop.setIcon(icon1)
        self.page_main_label_bot_stop.setIconSize(QtCore.QSize(250, 75))
        self.page_main_label_bot_stop.setProperty("label_bot_stop", QtGui.QPixmap("images/bot_stop.png"))
        self.page_main_label_bot_stop.setObjectName("page_main_label_bot_stop")
        self.page_main_label_bot_stop.clicked.connect(self.bot_stop_clicked)

        self.page_main_label_current_command = QtWidgets.QLabel(self.tab_main)
        self.page_main_label_current_command.setGeometry(QtCore.QRect(0, 700,120, 30))
        self.page_main_label_current_command.setText("当前启动命令：")
        self.page_main_label_current_command.setObjectName("page_main_label_current_command")

        self.page_main_edit_current_command = QtWidgets.QLineEdit(self.tab_main)
        self.page_main_edit_current_command.setGeometry(QtCore.QRect(120, 700, 300, 30))
        self.page_main_edit_current_command.setText("pythonw main.pyw -r")
        self.page_main_edit_current_command.setObjectName("page_main_edit_current_command")


        self.page_main_label_bot_status_2 = QtWidgets.QCommandLinkButton(self.tab_main)
        self.page_main_label_bot_status_2.setGeometry(QtCore.QRect(210, 380, 361, 121))
        self.page_main_label_bot_status_2.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/bot_status.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_main_label_bot_status_2.setIcon(icon2)
        self.page_main_label_bot_status_2.setIconSize(QtCore.QSize(300, 175))
        self.page_main_label_bot_status_2.setObjectName("page_main_label_bot_status_2")
        self.page_main_edit_bot_status_on = QtWidgets.QCommandLinkButton(self.tab_main)
        self.page_main_edit_bot_status_on.setGeometry(QtCore.QRect(530, 390, 201, 91))
        self.page_main_edit_bot_status_on.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/bot_status_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_main_edit_bot_status_on.setIcon(icon3)
        self.page_main_edit_bot_status_on.setIconSize(QtCore.QSize(200, 175))
        self.page_main_edit_bot_status_on.setObjectName("page_main_edit_bot_status_on")
        self.page_main_edit_bot_status_off = QtWidgets.QCommandLinkButton(self.tab_main)
        self.page_main_edit_bot_status_off.setGeometry(QtCore.QRect(510, 380, 231, 101))
        self.page_main_edit_bot_status_off.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/bot_status_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page_main_edit_bot_status_off.setIcon(icon4)
        self.page_main_edit_bot_status_off.setIconSize(QtCore.QSize(225, 175))
        self.page_main_edit_bot_status_off.setObjectName("page_main_edit_bot_status_off")

        self.menu_tab.addTab(self.tab_main, "")
        self.tab_log = QtWidgets.QWidget()
        self.tab_log.setMinimumSize(QtCore.QSize(1020, 740))
        self.tab_log.setMaximumSize(QtCore.QSize(1160, 740))
        self.tab_log.setStyleSheet(
            "background-color: rgba(255, 255, 255,0.025);QMenu {background-color:rgb(233, 190, 203);}\n"
            "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
            " } ")
        self.tab_log.setObjectName("tab_log")
        self.page_log_text = QtWidgets.QPlainTextEdit(self.tab_log)
        self.page_log_text.setGeometry(QtCore.QRect(0, 0, 1020, 651))
        self.page_log_text.setMaximumSize(QtCore.QSize(1020, 740))
        self.page_log_text.setStyleSheet("background-color:rgba(255,255,255,0.025)")
        self.page_log_text.setReadOnly(True)
        self.page_log_text.setObjectName("page_log_text")
        self.page_log_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.page_log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.page_log_text.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.page_log_label_time = QtWidgets.QLabel(self.tab_log)
        self.page_log_label_time.setGeometry(QtCore.QRect(0, 0, 217, 25))
        self.page_log_label_time.setStyleSheet("background-color:rgba(255,255,255,0.5)")
        self.page_log_label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.page_log_label_time.setObjectName("page_log_label_time")
        self.page_log_label_jiluqi = QtWidgets.QLabel(self.tab_log)
        self.page_log_label_jiluqi.setGeometry(QtCore.QRect(220, 0, 120, 26))
        self.page_log_label_jiluqi.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.page_log_label_jiluqi.setAlignment(QtCore.Qt.AlignCenter)
        self.page_log_label_jiluqi.setObjectName("page_log_label_jiluqi")
        self.page_log_label_level = QtWidgets.QLabel(self.tab_log)
        self.page_log_label_level.setGeometry(QtCore.QRect(343, 0, 68, 25))
        self.page_log_label_level.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.page_log_label_level.setAlignment(QtCore.Qt.AlignCenter)
        self.page_log_label_level.setObjectName("page_log_label_level")
        self.page_log_label_message = QtWidgets.QLabel(self.tab_log)
        self.page_log_label_message.setGeometry(QtCore.QRect(415, 0, 471, 25))
        self.page_log_label_message.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.page_log_label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.page_log_label_message.setObjectName("page_log_label_message")
        self.page_log_btn_open_log_path = QtWidgets.QPushButton(self.tab_log)
        self.page_log_btn_open_log_path.setGeometry(QtCore.QRect(863, 0, 131, 25))
        self.page_log_btn_open_log_path.setStyleSheet("background-color:rgb(85, 255, 255)")
        self.page_log_btn_open_log_path.setObjectName("page_log_btn_open_log_path")
        self.page_log_btn_open_log_path.clicked.connect(self.open_log_path)
        self.page_log_btn_switch_unicode = QtWidgets.QPushButton(self.tab_log)
        self.page_log_btn_switch_unicode.setGeometry(QtCore.QRect(900, 660, 93, 28))
        self.page_log_btn_switch_unicode.setObjectName("page_log_btn_switch_unicode")
        self.page_log_btn_switch_unicode.clicked.connect(self.switchEncoding)
        self.page_log_btn_switch_unicode.setHidden(True)
        self.page_log_btn_cmd_send = QtWidgets.QPushButton(self.tab_log)
        self.page_log_btn_cmd_send.setGeometry(QtCore.QRect(900, 690, 93, 28))
        self.page_log_btn_cmd_send.setObjectName("page_log_btn_cmd_send")
        self.page_log_btn_cmd_send.setHidden(True)
       # self.page_log_btn_cmd_send.clicked.connect(self.log_btn_send_clicked)
        self.page_log_cmd_input = QtWidgets.QLineEdit(self.tab_log)
        self.page_log_cmd_input.setGeometry(QtCore.QRect(10, 680, 871, 35))
        self.page_log_cmd_input.setObjectName("page_log_cmd_input")
        self.page_log_cmd_input.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_log_cmd_input.setHidden(True)
        self.page_log_text.raise_()
        self.page_log_label_time.raise_()
        self.page_log_label_jiluqi.raise_()
        self.page_log_label_level.raise_()
        self.page_log_label_message.raise_()
        self.page_log_btn_switch_unicode.raise_()
        self.page_log_btn_cmd_send.raise_()
        self.page_log_cmd_input.raise_()
        self.page_log_btn_open_log_path.raise_()
        self.menu_tab.addTab(self.tab_log, "")
        self.tab_set = QtWidgets.QWidget()
        self.tab_set.setMinimumSize(QtCore.QSize(1020, 740))
        self.tab_set.setMaximumSize(QtCore.QSize(1160, 740))
        self.tab_set.setSizeIncrement(QtCore.QSize(1020, 740))
        self.tab_set.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tab_set.setStyleSheet(
            "background-color: rgba(255, 255, 255,0.025);QMenu {background-color:rgb(233, 190, 203);}\n"
            "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
            " } ")
        self.tab_set.setObjectName("tab_set")
        self.page_set_scroll_area = QtWidgets.QScrollArea(self.tab_set)
        self.page_set_scroll_area.setGeometry(QtCore.QRect(0, 0, 1020, 740))
        self.page_set_scroll_area.setMinimumSize(QtCore.QSize(1020, 740))
        self.page_set_scroll_area.setMaximumSize(QtCore.QSize(1020, 740))
        self.page_set_scroll_area.setTabletTracking(True)
        self.page_set_scroll_area.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.page_set_scroll_area.setStyleSheet(" ")
        self.page_set_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.page_set_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.page_set_scroll_area.setWidgetResizable(False)
        self.page_set_scroll_area.setObjectName("page_set_scroll_area")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 1020, 4000))
        self.scrollAreaWidgetContents_5.setMinimumSize(QtCore.QSize(1020, 0))
        self.scrollAreaWidgetContents_5.setMaximumSize(QtCore.QSize(1020, 4500))
        self.scrollAreaWidgetContents_5.setStyleSheet("QMenu {background-color:rgb(233, 190, 203);}\n"
                                                      "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
                                                      " } ")
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.page_set_title_api_proxy = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_api_proxy.setGeometry(QtCore.QRect(260, 330, 91, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.page_set_title_api_proxy.setFont(font)
        self.page_set_title_api_proxy.setObjectName("page_set_title_api_proxy")
        self.page_set_title_api = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_api.setGeometry(QtCore.QRect(60, 290, 131, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.page_set_title_api.setFont(font)
        self.page_set_title_api.setObjectName("page_set_title_api")
        self.page_set_title_main = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_main.setGeometry(QtCore.QRect(60, 40, 149, 37))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_main.setFont(font)
        self.page_set_title_main.setObjectName("page_set_title_main")
        self.label_122 = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.label_122.setGeometry(QtCore.QRect(90, 600, 72, 15))
        font = QtGui.QFont()
        font.setPointSize(1)
        self.label_122.setFont(font)
        self.label_122.setObjectName("label_122")
        self.page_set_title_response = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_response.setGeometry(QtCore.QRect(60, 420, 161, 61))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.page_set_title_response.setFont(font)
        self.page_set_title_response.setObjectName("page_set_title_response")
        self.page_set_title_pipeiguize = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_pipeiguize.setGeometry(QtCore.QRect(60, 920, 131, 61))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.page_set_title_pipeiguize.setFont(font)
        self.page_set_title_pipeiguize.setObjectName("page_set_title_pipeiguize")
        self.page_set_btn_cfg_open_path_full_scenario = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_btn_cfg_open_path_full_scenario.setGeometry(QtCore.QRect(530, 430, 181, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_btn_cfg_open_path_full_scenario.setFont(font)
        self.page_set_btn_cfg_open_path_full_scenario.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_btn_cfg_open_path_full_scenario.setObjectName("page_set_btn_cfg_open_path_full_scenario")
        self.page_set_btn_cfg_open_path_full_scenario.clicked.connect(self.open_scenario_path)
        self.page_set_title_moxingshezhi = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_moxingshezhi.setGeometry(QtCore.QRect(60, 1190, 131, 51))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_moxingshezhi.setFont(font)
        self.page_set_title_moxingshezhi.setObjectName("page_set_title_moxingshezhi")
        self.page_set_title_huihuashezhi = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_huihuashezhi.setGeometry(QtCore.QRect(60, 1520, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_huihuashezhi.setFont(font)
        self.page_set_title_huihuashezhi.setObjectName("page_set_title_huihuashezhi")
        self.page_set_title_kaifazheshezhi = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_kaifazheshezhi.setGeometry(QtCore.QRect(60, 1700, 161, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_kaifazheshezhi.setFont(font)
        self.page_set_title_kaifazheshezhi.setObjectName("page_set_title_kaifazheshezhi")
        self.page_set_title_zhilingquanxian = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_zhilingquanxian.setGeometry(QtCore.QRect(60, 2590, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_zhilingquanxian.setFont(font)
        self.page_set_title_zhilingquanxian.setObjectName("page_set_title_zhilingquanxian")
        self.page_set_title_xiaoxitishiyu = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_title_xiaoxitishiyu.setGeometry(QtCore.QRect(60, 3140, 161, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.page_set_title_xiaoxitishiyu.setFont(font)
        self.page_set_title_xiaoxitishiyu.setObjectName("page_set_title_xiaoxitishiyu")
        self.page_set_edit_cfg_response_at = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_response_at.setGeometry(QtCore.QRect(260, 940, 171, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_response_at.setFont(font)
        self.page_set_edit_cfg_response_at.setObjectName("page_set_edit_cfg_response_at")
        self.page_set_edit_cfg_response_at.setChecked(
            self.dict_cfgs[value_cfgs_response_rules][value_cfgs_response_rules_at])
        self.page_set_edit_cfg_response_at.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_response_rules, {**self.dict_cfgs[value_cfgs_response_rules],
                                                                        **{value_cfgs_response_rules_at: bool(state)}}))

        self.page_set_edit_cfg_font_path = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_font_path.setGeometry(QtCore.QRect(544, 2100, 142, 30))
        self.page_set_edit_cfg_font_path.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_font_path.setObjectName("page_set_edit_cfg_font_path")
        self.page_set_edit_cfg_font_path.setText(self.dict_cfgs[value_cfgs_font_path])
        self.page_set_edit_cfg_font_path.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_font_path, new_value))

        self.page_set_edit_cfg_user_pool_num = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_user_pool_num.setGeometry(QtCore.QRect(560, 1860, 61, 30))
        self.page_set_edit_cfg_user_pool_num.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_user_pool_num.setMinimum(1)
        self.page_set_edit_cfg_user_pool_num.setMaximum(30)
        self.page_set_edit_cfg_user_pool_num.setObjectName("page_set_edit_cfg_user_pool_num")
        self.page_set_edit_cfg_user_pool_num.setValue(self.dict_cfgs[value_cfgs_user_pool_num])
        self.page_set_edit_cfg_user_pool_num.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_user_pool_num, new_value))

        self.page_set_label_cfg_user_pool_num = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_user_pool_num.setGeometry(QtCore.QRect(260, 1860, 306, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_user_pool_num.setFont(font)
        self.page_set_label_cfg_user_pool_num.setObjectName("page_set_label_cfg_user_pool_num")

        self.page_set_edit_cfg_admin_pool_num = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_admin_pool_num.setGeometry(QtCore.QRect(560, 1820, 61, 30))
        self.page_set_edit_cfg_admin_pool_num.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_admin_pool_num.setMinimum(1)
        self.page_set_edit_cfg_admin_pool_num.setMaximum(30)
        self.page_set_edit_cfg_admin_pool_num.setObjectName("page_set_edit_cfg_admin_pool_num")
        self.page_set_edit_cfg_admin_pool_num.setValue(self.dict_cfgs[value_cfgs_admin_pool_num])
        self.page_set_edit_cfg_admin_pool_num.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_admin_pool_num, new_value))

        self.page_set_label_cfg_admin_pool_num = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_admin_pool_num.setGeometry(QtCore.QRect(260, 1820, 306, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_admin_pool_num.setFont(font)
        self.page_set_label_cfg_admin_pool_num.setObjectName("page_set_label_cfg_admin_pool_num")

        self.page_set_label_cfg_font_path = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_font_path.setGeometry(QtCore.QRect(260, 2100, 288, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_font_path.setFont(font)
        self.page_set_label_cfg_font_path.setObjectName("page_set_label_cfg_font_path")

        self.page_set_btn_save = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_btn_save.setGeometry(QtCore.QRect(870, 3510, 101, 41))
        self.page_set_btn_save.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_btn_save.setObjectName("page_set_btn_save")
        self.page_set_btn_save.setHidden(True)
        self.page_set_label_cfg_default_prompt = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_default_prompt.setGeometry(QtCore.QRect(260, 470, 151, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_default_prompt.setFont(font)
        self.page_set_label_cfg_default_prompt.setObjectName("page_set_label_cfg_default_prompt")

        self.page_set_label_cfg_inappropriate_message_tips = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_inappropriate_message_tips.setGeometry(QtCore.QRect(260, 2340, 198, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_inappropriate_message_tips.setFont(font)
        self.page_set_label_cfg_inappropriate_message_tips.setObjectName(
            "page_set_label_cfg_inappropriate_message_tips")

        self.page_set_edit_cfg_inappropriate_message_tips = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_inappropriate_message_tips.setGeometry(QtCore.QRect(460, 2340, 142, 30))
        self.page_set_edit_cfg_inappropriate_message_tips.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_inappropriate_message_tips.setObjectName("page_set_edit_cfg_inappropriate_message_tips")
        self.page_set_edit_cfg_inappropriate_message_tips.setText(self.dict_cfgs[value_cfgs_inappropriate_message_tips])
        self.page_set_edit_cfg_inappropriate_message_tips.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_inappropriate_message_tips, new_value))

        self.page_set_label_cfg_prompt_submit_length = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_prompt_submit_length.setGeometry(QtCore.QRect(260, 1300, 288, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_prompt_submit_length.setFont(font)
        self.page_set_label_cfg_prompt_submit_length.setObjectName("page_set_label_cfg_prompt_submit_length")

        self.page_set_label_cfg_random_rate = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_random_rate.setGeometry(QtCore.QRect(260, 980, 112, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_random_rate.setFont(font)
        self.page_set_label_cfg_random_rate.setObjectName("page_set_label_cfg_random_rate")

        self.page_set_edit_cfg_random_rate = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_random_rate.setGeometry(QtCore.QRect(390, 980, 60, 30))
        self.page_set_edit_cfg_random_rate.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_random_rate.setMaximum(1.0)
        self.page_set_edit_cfg_random_rate.setSingleStep(0.1)
        self.page_set_edit_cfg_random_rate.setObjectName("page_set_edit_cfg_random_rate")
        self.page_set_edit_cfg_random_rate.setValue(
            self.dict_cfgs[value_cfgs_response_rules][value_cfgs_response_rules_random_rate])
        self.page_set_edit_cfg_random_rate.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_response_rules, {**self.dict_cfgs[value_cfgs_response_rules],
                                                                            **{
                                                                                value_cfgs_response_rules_random_rate: new_value}}))

        self.page_set_edit_cmd_draw = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_draw.setGeometry(QtCore.QRect(350, 2600, 36, 30))
        self.page_set_edit_cmd_draw.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_draw.setMinimum(1)
        self.page_set_edit_cmd_draw.setMaximum(2)
        self.page_set_edit_cmd_draw.setObjectName("page_set_edit_cmd_draw")
        self.page_set_edit_cmd_draw.setValue(self.dict_cmds[value_cmds_draw])
        self.page_set_edit_cmd_draw.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_draw, new_value))

        self.page_set_edit_cmd_default = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_default.setGeometry(QtCore.QRect(350, 2640, 36, 30))
        self.page_set_edit_cmd_default.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_default.setMinimum(1)
        self.page_set_edit_cmd_default.setMaximum(2)
        self.page_set_edit_cmd_default.setObjectName("page_set_edit_cmd_default")
        self.page_set_edit_cmd_default.setValue(self.dict_cmds[value_cmds_default])
        self.page_set_edit_cmd_default.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_default, new_value))

        self.page_set_edit_cmd_default_set = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_default_set.setGeometry(QtCore.QRect(350, 2680, 36, 30))
        self.page_set_edit_cmd_default_set.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_default_set.setMinimum(1)
        self.page_set_edit_cmd_default_set.setMaximum(2)
        self.page_set_edit_cmd_default_set.setObjectName("page_set_edit_cmd_default_set")
        self.page_set_edit_cmd_default_set.setValue(self.dict_cmds[value_cmds_default])
        self.page_set_edit_cmd_default_set.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_default_set, new_value))

        self.page_set_edit_cmd_del = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_del.setGeometry(QtCore.QRect(350, 2720, 36, 30))
        self.page_set_edit_cmd_del.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_del.setMinimum(1)
        self.page_set_edit_cmd_del.setMaximum(2)
        self.page_set_edit_cmd_del.setObjectName("page_set_edit_cmd_del")
        self.page_set_edit_cmd_del.setValue(self.dict_cmds[value_cmds_del])
        self.page_set_edit_cmd_del.valueChanged.connect(lambda new_value: update_value_cmds(value_cmds_del, new_value))

        self.page_set_edit_cmd_del_all = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_del_all.setGeometry(QtCore.QRect(350, 2760, 36, 30))
        self.page_set_edit_cmd_del_all.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_del_all.setMinimum(1)
        self.page_set_edit_cmd_del_all.setMaximum(2)
        self.page_set_edit_cmd_del_all.setObjectName("page_set_edit_cmd_del_all")
        self.page_set_edit_cmd_del_all.setValue(self.dict_cmds[value_cmds_del_all])
        self.page_set_edit_cmd_del_all.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_del_all, new_value))

        self.page_set_edit_cmd_delhst = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_delhst.setGeometry(QtCore.QRect(350, 2800, 36, 30))
        self.page_set_edit_cmd_delhst.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_delhst.setMinimum(1)
        self.page_set_edit_cmd_delhst.setMaximum(2)
        self.page_set_edit_cmd_delhst.setObjectName("page_set_edit_cmd_delhst")
        self.page_set_edit_cmd_delhst.setValue(self.dict_cmds[value_cmds_delhst])
        self.page_set_edit_cmd_delhst.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_delhst, new_value))

        self.page_set_edit_cmd_delhst_all = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_delhst_all.setGeometry(QtCore.QRect(350, 2840, 36, 30))
        self.page_set_edit_cmd_delhst_all.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_delhst_all.setMinimum(1)
        self.page_set_edit_cmd_delhst_all.setMaximum(2)
        self.page_set_edit_cmd_delhst_all.setObjectName("page_set_edit_cmd_delhst_all")
        self.page_set_edit_cmd_delhst_all.setValue(self.dict_cmds[value_cmds_delhst_all])
        self.page_set_edit_cmd_delhst_all.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_delhst_all, new_value))

        self.page_set_edit_cmd_last = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_last.setGeometry(QtCore.QRect(350, 2880, 36, 30))
        self.page_set_edit_cmd_last.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_last.setMinimum(1)
        self.page_set_edit_cmd_last.setMaximum(2)
        self.page_set_edit_cmd_last.setObjectName("page_set_edit_cmd_last")
        self.page_set_edit_cmd_last.setValue(self.dict_cmds[value_cmds_last])
        self.page_set_edit_cmd_last.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_last, new_value))

        self.page_set_edit_cmd_prompt = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_prompt.setGeometry(QtCore.QRect(350, 2920, 36, 30))
        self.page_set_edit_cmd_prompt.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_prompt.setMinimum(1)
        self.page_set_edit_cmd_prompt.setMaximum(2)
        self.page_set_edit_cmd_prompt.setObjectName("page_set_edit_cmd_prompt")
        self.page_set_edit_cmd_prompt.setValue(self.dict_cmds[value_cmds_prompt])
        self.page_set_edit_cmd_prompt.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_prompt, new_value))

        self.page_set_edit_cmd_reset = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_reset.setGeometry(QtCore.QRect(350, 2960, 36, 30))
        self.page_set_edit_cmd_reset.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_reset.setMinimum(1)
        self.page_set_edit_cmd_reset.setMaximum(2)
        self.page_set_edit_cmd_reset.setObjectName("page_set_edit_cmd_reset")
        self.page_set_edit_cmd_reset.setValue(self.dict_cmds[value_cmds_reset])
        self.page_set_edit_cmd_reset.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_reset, new_value))

        self.page_set_edit_cmd_reload = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_reload.setGeometry(QtCore.QRect(350, 3000, 36, 30))
        self.page_set_edit_cmd_reload.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_reload.setMinimum(1)
        self.page_set_edit_cmd_reload.setMaximum(2)
        self.page_set_edit_cmd_reload.setObjectName("page_set_edit_cmd_reload")
        self.page_set_edit_cmd_reload.setValue(self.dict_cmds[value_cmds_reload])
        self.page_set_edit_cmd_reload.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_reload, new_value))

        self.page_set_edit_cmd_usage = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_usage.setGeometry(QtCore.QRect(350, 3040, 36, 30))
        self.page_set_edit_cmd_usage.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_usage.setMinimum(1)
        self.page_set_edit_cmd_usage.setMaximum(2)
        self.page_set_edit_cmd_usage.setObjectName("page_set_edit_cmd_usage")
        self.page_set_edit_cmd_usage.setValue(self.dict_cmds[value_cmds_usage])
        self.page_set_edit_cmd_usage.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_usage, new_value))

        self.page_set_edit_cmd_version = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_version.setGeometry(QtCore.QRect(629, 3040, 36, 30))
        self.page_set_edit_cmd_version.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_version.setMinimum(1)
        self.page_set_edit_cmd_version.setMaximum(2)
        self.page_set_edit_cmd_version.setObjectName("page_set_edit_cmd_version")
        self.page_set_edit_cmd_version.setValue(self.dict_cmds[value_cmds_version])
        self.page_set_edit_cmd_version.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_version, new_value))

        self.page_set_edit_cmd_cmd = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_cmd.setGeometry(QtCore.QRect(629, 3080, 36, 30))
        self.page_set_edit_cmd_cmd.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_cmd.setMinimum(1)
        self.page_set_edit_cmd_cmd.setMaximum(2)
        self.page_set_edit_cmd_cmd.setObjectName("page_set_edit_cmd_cmd")
        self.page_set_edit_cmd_cmd.setValue(self.dict_cmds[value_cmds_cmd])
        self.page_set_edit_cmd_cmd.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_cmd, new_value))

        self.page_set_edit_cmd_cfg = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_cfg.setGeometry(QtCore.QRect(350, 3080, 36, 30))
        self.page_set_edit_cmd_cfg.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_cfg.setMinimum(1)
        self.page_set_edit_cmd_cfg.setMaximum(2)
        self.page_set_edit_cmd_cfg.setObjectName("page_set_edit_cmd_cfg")
        self.page_set_edit_cmd_cfg.setValue(self.dict_cmds[value_cmds_cfg])
        self.page_set_edit_cmd_cfg.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_cfg, new_value))

        self.page_set_edit_cmd_update = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_update.setGeometry(QtCore.QRect(629, 3000, 36, 30))
        self.page_set_edit_cmd_update.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_update.setMinimum(1)
        self.page_set_edit_cmd_update.setMaximum(2)
        self.page_set_edit_cmd_update.setObjectName("page_set_edit_cmd_update")
        self.page_set_edit_cmd_update.setValue(self.dict_cmds[value_cmds_update])
        self.page_set_edit_cmd_update.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_update, new_value))

        self.page_set_edit_cmd_help = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_help.setGeometry(QtCore.QRect(629, 2960, 36, 30))
        self.page_set_edit_cmd_help.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_help.setMinimum(1)
        self.page_set_edit_cmd_help.setMaximum(2)
        self.page_set_edit_cmd_help.setObjectName("page_set_edit_cmd_help")
        self.page_set_edit_cmd_help.setValue(self.dict_cmds[value_cmds_help])
        self.page_set_edit_cmd_help.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_help, new_value))

        self.page_set_edit_cmd_resend = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_resend.setGeometry(QtCore.QRect(629, 2920, 36, 30))
        self.page_set_edit_cmd_resend.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_resend.setMinimum(1)
        self.page_set_edit_cmd_resend.setMaximum(2)
        self.page_set_edit_cmd_resend.setObjectName("page_set_edit_cmd_resend")
        self.page_set_edit_cmd_resend.setValue(self.dict_cmds[value_cmds_resend])
        self.page_set_edit_cmd_resend.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_resend, new_value))

        self.page_set_edit_cmd_next = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_next.setGeometry(QtCore.QRect(629, 2880, 36, 30))
        self.page_set_edit_cmd_next.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_next.setMinimum(1)
        self.page_set_edit_cmd_next.setMaximum(2)
        self.page_set_edit_cmd_next.setObjectName("page_set_edit_cmd_next")
        self.page_set_edit_cmd_next.setValue(self.dict_cmds[value_cmds_next])
        self.page_set_edit_cmd_next.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_next, new_value))

        self.page_set_edit_cmd_list = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_list.setGeometry(QtCore.QRect(629, 2840, 36, 30))
        self.page_set_edit_cmd_list.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_list.setMinimum(1)
        self.page_set_edit_cmd_list.setMaximum(2)
        self.page_set_edit_cmd_list.setObjectName("page_set_edit_cmd_list")
        self.page_set_edit_cmd_list.setValue(self.dict_cmds[value_cmds_list])
        self.page_set_edit_cmd_list.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_list, new_value))

        self.page_set_edit_cmd_plugin_on = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin_on.setGeometry(QtCore.QRect(629, 2800, 36, 30))
        self.page_set_edit_cmd_plugin_on.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin_on.setMinimum(1)
        self.page_set_edit_cmd_plugin_on.setMaximum(2)
        self.page_set_edit_cmd_plugin_on.setObjectName("page_set_edit_cmd_plugin_on")
        self.page_set_edit_cmd_plugin_on.setValue(self.dict_cmds[value_cmds_plugin_on])
        self.page_set_edit_cmd_plugin_on.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin_on, new_value))

        self.page_set_edit_cmd_plugin_off = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin_off.setGeometry(QtCore.QRect(629, 2760, 36, 30))
        self.page_set_edit_cmd_plugin_off.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin_off.setMinimum(1)
        self.page_set_edit_cmd_plugin_off.setMaximum(2)
        self.page_set_edit_cmd_plugin_off.setObjectName("page_set_edit_cmd_plugin_off")
        self.page_set_edit_cmd_plugin_off.setValue(self.dict_cmds[value_cmds_plugin_off])
        self.page_set_edit_cmd_plugin_off.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin_off, new_value))

        self.page_set_edit_cmd_plugin_del = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin_del.setGeometry(QtCore.QRect(629, 2720, 36, 30))
        self.page_set_edit_cmd_plugin_del.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin_del.setMinimum(1)
        self.page_set_edit_cmd_plugin_del.setMaximum(2)
        self.page_set_edit_cmd_plugin_del.setObjectName("page_set_edit_cmd_plugin_del")
        self.page_set_edit_cmd_plugin_del.setValue(self.dict_cmds[value_cmds_plugin_del])
        self.page_set_edit_cmd_plugin_del.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin_del, new_value))

        self.page_set_edit_cmd_plugin_update = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin_update.setGeometry(QtCore.QRect(629, 2680, 36, 30))
        self.page_set_edit_cmd_plugin_update.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin_update.setMinimum(1)
        self.page_set_edit_cmd_plugin_update.setMaximum(2)
        self.page_set_edit_cmd_plugin_update.setObjectName("page_set_edit_cmd_plugin_update")
        self.page_set_edit_cmd_plugin_update.setValue(self.dict_cmds[value_cmds_plugin_update])
        self.page_set_edit_cmd_plugin_update.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin_update, new_value))

        self.page_set_edit_cmd_plugin_get = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin_get.setGeometry(QtCore.QRect(629, 2640, 36, 30))
        self.page_set_edit_cmd_plugin_get.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin_get.setMinimum(1)
        self.page_set_edit_cmd_plugin_get.setMaximum(2)
        self.page_set_edit_cmd_plugin_get.setObjectName("page_set_edit_cmd_plugin_get")
        self.page_set_edit_cmd_plugin_get.setValue(self.dict_cmds[value_cmds_plugin_get])
        self.page_set_edit_cmd_plugin_get.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin_get, new_value))

        self.page_set_edit_cmd_plugin = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cmd_plugin.setGeometry(QtCore.QRect(629, 2600, 36, 30))
        self.page_set_edit_cmd_plugin.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cmd_plugin.setMinimum(1)
        self.page_set_edit_cmd_plugin.setMaximum(2)
        self.page_set_edit_cmd_plugin.setObjectName("page_set_edit_cmd_plugin")
        self.page_set_edit_cmd_plugin.setValue(self.dict_cmds[value_cmds_plugin])
        self.page_set_edit_cmd_plugin.valueChanged.connect(
            lambda new_value: update_value_cmds(value_cmds_plugin, new_value))

        self.page_set_label_cfg_api = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api.setGeometry(QtCore.QRect(260, 290, 91, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api.setFont(font)
        self.page_set_label_cfg_api.setObjectName("page_set_label_cfg_api")

        self.page_set_edit_cfg_api = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api.setGeometry(QtCore.QRect(370, 290, 230, 30))
        self.page_set_edit_cfg_api.setTabletTracking(True)
        self.page_set_edit_cfg_api.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.page_set_edit_cfg_api.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_api.setEditable(True)
        self.page_set_edit_cfg_api.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.page_set_edit_cfg_api.setObjectName("page_set_edit_cfg_api")
        self.page_set_edit_cfg_api.setCurrentIndex(0)
        self.page_set_edit_cfg_api.addItems(
            self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key].keys())

        # self.page_set_edit_cfg_api.currentText(lambda text:":".join(str(self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key].keys())) + ":" + str(self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_api_key].values()))
        self.page_set_edit_cfg_api_add = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_add.setGeometry(QtCore.QRect(620, 290, 50, 30))
        self.page_set_edit_cfg_api_add.setText("添加")
        self.page_set_edit_cfg_api_add.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_api_add.clicked.connect(self.add_api_key)

        self.page_set_edit_cfg_api_del = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_del.setGeometry(QtCore.QRect(690, 290, 50, 30))
        self.page_set_edit_cfg_api_del.setText("删除")
        self.page_set_edit_cfg_api_del.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_api_del.clicked.connect(self.del_api_key)

        self.page_set_edit_cfg_default_prompt = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_default_prompt.setGeometry(QtCore.QRect(260, 510, 711, 400))
        self.page_set_edit_cfg_default_prompt.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.page_set_edit_cfg_default_prompt.setDisabled(True)
        self.page_set_edit_cfg_default_prompt.setStyleSheet("background-color:rgba(255,255,255,0.5);")
        self.page_set_edit_cfg_default_prompt.setObjectName("page_set_edit_cfg_default_prompt")
        self.page_set_edit_cfg_default_prompt.setPlainText(
            next(iter(self.dict_cfgs[value_cfgs_default_prompt].values())))

        self.page_set_edit_cfg_default_prompt_choose = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_default_prompt_choose.setGeometry(QtCore.QRect(400, 472, 170, 30))
        self.page_set_edit_cfg_default_prompt_choose.setTabletTracking(True)
        self.page_set_edit_cfg_default_prompt_choose.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.page_set_edit_cfg_default_prompt_choose.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_default_prompt_choose.setEditable(False)
        self.page_set_edit_cfg_default_prompt_choose.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.page_set_edit_cfg_default_prompt_choose.setObjectName("page_set_edit_cfg_default_prompt_choose")
        # 添加选项到下拉框中
        self.page_set_edit_cfg_default_prompt_choose.addItems(self.dict_cfgs[value_cfgs_default_prompt].keys())
        self.page_set_edit_cfg_default_prompt_choose.setCurrentIndex(0)
        # 显示对应值
        self.page_set_edit_cfg_default_prompt_choose.currentTextChanged.connect(self.update_default_prompt)

        self.page_set_edit_cfg_prompt_add = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_prompt_add.setGeometry(QtCore.QRect(620, 472, 50, 30))
        self.page_set_edit_cfg_prompt_add.setText("添加")
        self.page_set_edit_cfg_prompt_add.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_prompt_add.clicked.connect(self.add_default_prompt)

        self.page_set_edit_cfg_prompt_del = QtWidgets.QPushButton(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_prompt_del.setGeometry(QtCore.QRect(690, 472, 50, 30))
        self.page_set_edit_cfg_prompt_del.setText("删除")
        self.page_set_edit_cfg_prompt_del.setStyleSheet("border: 1px solid rgba(0,0,0,0.5);")
        self.page_set_edit_cfg_prompt_del.clicked.connect(self.del_default_prompt)

        self.page_set_edit_cfg_blob_message_strategy = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_blob_message_strategy.setGeometry(QtCore.QRect(410, 2060, 91, 30))
        self.page_set_edit_cfg_blob_message_strategy.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_blob_message_strategy.setObjectName("page_set_edit_cfg_blob_message_strategy")
        self.page_set_edit_cfg_blob_message_strategy.addItem("")
        self.page_set_edit_cfg_blob_message_strategy.addItem("")
        self.page_set_edit_cfg_blob_message_strategy.setItemText(0, "image")
        self.page_set_edit_cfg_blob_message_strategy.setItemText(1, "forward")
        self.page_set_edit_cfg_blob_message_strategy.setCurrentText(self.dict_cfgs[value_cfgs_blob_message_strategy])
        self.page_set_edit_cfg_blob_message_strategy.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_blob_message_strategy, new_value))

        self.page_set_edit_cfg_rate_limit_strategy = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_rate_limit_strategy.setGeometry(QtCore.QRect(380, 1980, 71, 30))
        self.page_set_edit_cfg_rate_limit_strategy.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_rate_limit_strategy.setObjectName("page_set_edit_cfg_rate_limit_strategy")
        self.page_set_edit_cfg_rate_limit_strategy.addItem("")
        self.page_set_edit_cfg_rate_limit_strategy.addItem("")
        self.page_set_edit_cfg_rate_limit_strategy.setItemText(0, "wait")
        self.page_set_edit_cfg_rate_limit_strategy.setItemText(1, "drop")
        self.page_set_edit_cfg_rate_limit_strategy.setCurrentText(self.dict_cfgs[value_cfgs_rate_limit_strategy])
        self.page_set_edit_cfg_rate_limit_strategy.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_rate_limit_strategy, new_value))

        self.page_set_edit_cfg_baidu_secret_key = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_baidu_secret_key.setGeometry(QtCore.QRect(440, 2300, 326, 30))
        self.page_set_edit_cfg_baidu_secret_key.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_baidu_secret_key.setObjectName("page_set_edit_cfg_baidu_secret_key")
        self.page_set_edit_cfg_baidu_secret_key.setText(self.dict_cfgs[value_cfgs_baidu_secret_key])
        self.page_set_edit_cfg_baidu_secret_key.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_baidu_secret_key, new_value))

        self.page_set_edit_cfg_session_expire_time = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_session_expire_time.setGeometry(QtCore.QRect(430, 1900, 60, 30))
        self.page_set_edit_cfg_session_expire_time.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_session_expire_time.setMinimum(1)
        self.page_set_edit_cfg_session_expire_time.setMaximum(86400)
        self.page_set_edit_cfg_session_expire_time.setSingleStep(60)
        self.page_set_edit_cfg_session_expire_time.setObjectName("page_set_edit_cfg_session_expire_time")
        self.page_set_edit_cfg_session_expire_time.setValue(self.dict_cfgs[value_cfgs_session_expire_time])
        self.page_set_edit_cfg_session_expire_time.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_session_expire_time, new_value))

        self.page_set_label_cfg_blob_message_threshold = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_blob_message_threshold.setGeometry(QtCore.QRect(260, 2020, 234, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_blob_message_threshold.setFont(font)
        self.page_set_label_cfg_blob_message_threshold.setObjectName("page_set_label_cfg_blob_message_threshold")

        self.page_set_edit_cfg_blob_message_threshold = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_blob_message_threshold.setGeometry(QtCore.QRect(500, 2020, 81, 30))
        self.page_set_edit_cfg_blob_message_threshold.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_blob_message_threshold.setMaximum(4096)
        self.page_set_edit_cfg_blob_message_threshold.setSingleStep(128)
        self.page_set_edit_cfg_blob_message_threshold.setObjectName("page_set_edit_cfg_blob_message_threshold")
        self.page_set_edit_cfg_blob_message_threshold.setValue(self.dict_cfgs[value_cfgs_blob_message_threshold])
        self.page_set_edit_cfg_blob_message_threshold.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_blob_message_threshold, new_value))

        self.page_set_edit_cfg_baidu_check = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_baidu_check.setGeometry(QtCore.QRect(260, 2220, 329, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_baidu_check.setFont(font)
        self.page_set_edit_cfg_baidu_check.setObjectName("page_set_edit_cfg_baidu_check")
        self.page_set_edit_cfg_baidu_check.setChecked(self.dict_cfgs[value_cfgs_baidu_check])
        self.page_set_edit_cfg_baidu_check.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_baidu_check, bool(state)))

        self.page_set_label_cfg_baidu_secret_key = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_baidu_secret_key.setGeometry(QtCore.QRect(260, 2300, 176, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_baidu_secret_key.setFont(font)
        self.page_set_label_cfg_baidu_secret_key.setObjectName("page_set_label_cfg_baidu_secret_key")

        self.page_set_edit_cfg_income_msg_check = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_income_msg_check.setGeometry(QtCore.QRect(260, 2140, 329, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_income_msg_check.setFont(font)
        self.page_set_edit_cfg_income_msg_check.setObjectName("page_set_edit_cfg_income_msg_check")
        self.page_set_edit_cfg_income_msg_check.setChecked(self.dict_cfgs[value_cfgs_income_msg_check])
        self.page_set_edit_cfg_income_msg_check.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_income_msg_check, bool(state)))

        self.page_set_label_cfg_rate_limitation_danwei = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_rate_limitation_danwei.setGeometry(QtCore.QRect(470, 1940, 48, 30))
        self.page_set_label_cfg_rate_limitation_danwei.setObjectName("page_set_label_cfg_rate_limitation_danwei")

        self.page_set_edit_cfg_sensitive_word_filter = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_sensitive_word_filter.setGeometry(QtCore.QRect(260, 2180, 329, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_sensitive_word_filter.setFont(font)
        self.page_set_edit_cfg_sensitive_word_filter.setObjectName("page_set_edit_cfg_sensitive_word_filter")
        self.page_set_edit_cfg_sensitive_word_filter.setChecked(self.dict_cfgs[value_cfgs_sensitive_word_filter])
        self.page_set_edit_cfg_sensitive_word_filter.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_sensitive_word_filter, bool(state)))

        self.page_set_edit_cfg_rate_limitation = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_rate_limitation.setGeometry(QtCore.QRect(410, 1940, 51, 30))
        self.page_set_edit_cfg_rate_limitation.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_rate_limitation.setMinimum(1)
        self.page_set_edit_cfg_rate_limitation.setMaximum(60)
        self.page_set_edit_cfg_rate_limitation.setObjectName("page_set_edit_cfg_rate_limitation")
        self.page_set_edit_cfg_rate_limitation.setValue(self.dict_cfgs[value_cfgs_rate_limitation])
        self.page_set_edit_cfg_rate_limitation.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_rate_limitation, new_value))

        self.page_set_label_cfg_rate_limit_strategy = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_rate_limit_strategy.setGeometry(QtCore.QRect(260, 1980, 126, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_rate_limit_strategy.setFont(font)
        self.page_set_label_cfg_rate_limit_strategy.setObjectName("page_set_label_cfg_rate_limit_strategy")

        self.page_set_label_cfg_session_expire_time = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_session_expire_time.setGeometry(QtCore.QRect(260, 1900, 180, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_session_expire_time.setFont(font)
        self.page_set_label_cfg_session_expire_time.setObjectName("page_set_label_cfg_session_expire_time")

        self.page_set_label_cfg_blob_message_strategy = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_blob_message_strategy.setGeometry(QtCore.QRect(260, 2060, 144, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_blob_message_strategy.setFont(font)
        self.page_set_label_cfg_blob_message_strategy.setObjectName("page_set_label_cfg_blob_message_strategy")

        self.page_set_label_cfg_rate_limitation = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_rate_limitation.setGeometry(QtCore.QRect(260, 1940, 144, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_rate_limitation.setFont(font)
        self.page_set_label_cfg_rate_limitation.setObjectName("page_set_label_cfg_rate_limitation")

        self.page_set_label_cfg_session_expire_time_danwei = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_session_expire_time_danwei.setGeometry(QtCore.QRect(500, 1900, 48, 30))
        self.page_set_label_cfg_session_expire_time_danwei.setObjectName(
            "page_set_label_cfg_session_expire_time_danwei")

        self.page_set_label_cfg_image_size = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_image_size.setGeometry(QtCore.QRect(260, 1460, 93, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_image_size.setFont(font)
        self.page_set_label_cfg_image_size.setObjectName("page_set_label_cfg_image_size")

        self.page_set_edit_cfg_quote_origin = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_quote_origin.setGeometry(QtCore.QRect(260, 1560, 354, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_quote_origin.setFont(font)
        self.page_set_edit_cfg_quote_origin.setObjectName("page_set_edit_cfg_quote_origin")
        self.page_set_edit_cfg_quote_origin.setChecked(self.dict_cfgs[value_cfgs_quote_origin])
        self.page_set_edit_cfg_quote_origin.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_quote_origin, bool(state)))

        self.page_set_label_cfg_include_image_description = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_include_image_description.setGeometry(QtCore.QRect(260, 1520, 354, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_include_image_description.setFont(font)
        self.page_set_label_cfg_include_image_description.setObjectName("page_set_label_cfg_include_image_description")

        self.page_set_label_cfg_sys_pool_num = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_sys_pool_num.setGeometry(QtCore.QRect(260, 1780, 180, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_sys_pool_num.setFont(font)
        self.page_set_label_cfg_sys_pool_num.setObjectName("page_set_label_cfg_sys_pool_num")

        self.page_set_edit_cfg_process_message_timeout = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_process_message_timeout.setGeometry(QtCore.QRect(430, 1700, 60, 30))
        self.page_set_edit_cfg_process_message_timeout.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_process_message_timeout.setMinimum(1)
        self.page_set_edit_cfg_process_message_timeout.setMaximum(500)
        self.page_set_edit_cfg_process_message_timeout.setSingleStep(5)
        self.page_set_edit_cfg_process_message_timeout.setObjectName("page_set_edit_cfg_process_message_timeout")
        self.page_set_edit_cfg_process_message_timeout.setValue(self.dict_cfgs[value_cfgs_process_message_timeout])
        self.page_set_edit_cfg_process_message_timeout.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_process_message_timeout, new_value))

        self.page_set_edit_cfg_qiyongduoduixiangmingcheng = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setEnabled(False)
        self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setGeometry(QtCore.QRect(260, 1640, 354, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setFont(font)
        self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setObjectName("page_set_edit_cfg_qiyongduoduixiangmingcheng")
        # self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setChecked(self.dict_cfgs[x])
        # self.page_set_edit_cfg_qiyongduoduixiangmingcheng.stateChanged.connect(lambda state: update_value_cfgs(x, bool(state)))
        # 暂未实现

        self.page_set_label_cfg_process_message_timeout_danwei = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_process_message_timeout_danwei.setGeometry(QtCore.QRect(490, 1700, 48, 30))
        self.page_set_label_cfg_process_message_timeout_danwei.setObjectName(
            "page_set_label_cfg_process_message_timeout_danwei")

        self.page_set_label_cfg_retry_times = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_retry_times.setGeometry(QtCore.QRect(260, 1740, 198, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_retry_times.setFont(font)
        self.page_set_label_cfg_retry_times.setObjectName("page_set_label_cfg_retry_times")

        self.page_set_edit_cfg_sys_pool_num = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_sys_pool_num.setGeometry(QtCore.QRect(440, 1780, 61, 30))
        self.page_set_edit_cfg_sys_pool_num.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_sys_pool_num.setMinimum(1)
        self.page_set_edit_cfg_sys_pool_num.setMaximum(30)
        self.page_set_edit_cfg_sys_pool_num.setObjectName("page_set_edit_cfg_sys_pool_num")
        self.page_set_edit_cfg_sys_pool_num.setValue(self.dict_cfgs[value_cfgs_sys_pool_num])
        self.page_set_edit_cfg_sys_pool_num.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_sys_pool_num, new_value))

        self.page_set_edit_cfg_show_prefix = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_show_prefix.setGeometry(QtCore.QRect(260, 1600, 354, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_show_prefix.setFont(font)
        self.page_set_edit_cfg_show_prefix.setObjectName("page_set_edit_cfg_show_prefix")
        self.page_set_edit_cfg_show_prefix.setChecked(self.dict_cfgs[value_cfgs_show_prefix])
        self.page_set_edit_cfg_show_prefix.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_show_prefix, bool(state)))

        self.page_set_edit_cfg_retry_times = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_retry_times.setGeometry(QtCore.QRect(450, 1740, 79, 30))
        self.page_set_edit_cfg_retry_times.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_retry_times.setMinimum(1)
        self.page_set_edit_cfg_retry_times.setMaximum(10)
        self.page_set_edit_cfg_retry_times.setObjectName("page_set_edit_cfg_retry_times")
        self.page_set_edit_cfg_retry_times.setValue(self.dict_cfgs[value_cfgs_retry_times])
        self.page_set_edit_cfg_retry_times.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_retry_times, new_value))

        self.page_set_label_cfg_process_message_timeout_left = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_process_message_timeout_left.setGeometry(QtCore.QRect(260, 1700, 166, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_process_message_timeout_left.setFont(font)
        self.page_set_label_cfg_process_message_timeout_left.setObjectName(
            "page_set_label_cfg_process_message_timeout_left")

        self.page_set_edit_cfg_image_size = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_image_size.setGeometry(QtCore.QRect(350, 1460, 110, 30))
        self.page_set_edit_cfg_image_size.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_image_size.setObjectName("page_set_edit_cfg_image_size")
        self.page_set_edit_cfg_image_size.addItem("")
        self.page_set_edit_cfg_image_size.addItem("")
        self.page_set_edit_cfg_image_size.addItem("")
        self.page_set_edit_cfg_image_size.setItemText(0, "256x256")
        self.page_set_edit_cfg_image_size.setItemText(1, "512x512")
        self.page_set_edit_cfg_image_size.setItemText(2, "1024x1024")
        self.page_set_edit_cfg_image_size.setCurrentText(
            self.dict_cfgs[value_cfgs_image_api_params][value_cfgs_image_api_params_size])
        self.page_set_edit_cfg_image_size.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_image_api_params,
                                                {**self.dict_cfgs[value_cfgs_image_api_params],
                                                 **{value_cfgs_image_api_params_size: new_value}}))

        self.page_set_label_cfg_ignore_prefix = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_ignore_prefix.setGeometry(QtCore.QRect(260, 1100, 160, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_ignore_prefix.setFont(font)
        self.page_set_label_cfg_ignore_prefix.setObjectName("page_set_label_cfg_ignore_prefix")

        self.page_set_label_cfg_ignore_regexp = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_ignore_regexp.setGeometry(QtCore.QRect(260, 1140, 161, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_ignore_regexp.setFont(font)
        self.page_set_label_cfg_ignore_regexp.setObjectName("page_set_label_cfg_ignore_regexp")

        self.page_set_edit_cfg_ignore_prefix = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_ignore_prefix.setGeometry(QtCore.QRect(430, 1100, 321, 30))
        self.page_set_edit_cfg_ignore_prefix.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_ignore_prefix.setObjectName("page_set_edit_cfg_ignore_prefix")
        self.page_set_edit_cfg_ignore_prefix.setStyleSheet("QLineEdit {border: 1px solid rgba(0,0,0, 0.5);}QToolTip { border: none; background-color: white; color: black; } QToolTip QLabel { color: red; }")
        self.page_set_edit_cfg_ignore_prefix.setToolTip("输入内容以<span style='color:red'>【英文逗号】</span>分隔。比如:关键词1,关键词2,关键词3")

        # self.page_set_edit_cfg_ignore_prefix.setValue(self.dict_cfgs[w])
        # self.page_set_edit_cfg_ignore_prefix.valueChanged.connect(lambda new_value: update_value_cfgs(w, new_value))
        self.page_set_edit_cfg_ignore_prefix.setText(
            ','.join(self.dict_cfgs[value_cfgs_ignore_rules][value_cfgs_ignore_rules_prefix]))
        self.page_set_edit_cfg_ignore_prefix.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_ignore_rules,
                                                {**self.dict_cfgs[value_cfgs_ignore_rules],
                                                 **{value_cfgs_ignore_rules_prefix: new_value.split(',')}}))

        self.page_set_edit_cfg_ignore_regexp = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_ignore_regexp.setGeometry(QtCore.QRect(430, 1140, 321, 30))
        self.page_set_edit_cfg_ignore_regexp.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_ignore_regexp.setObjectName("page_set_edit_cfg_ignore_regexp")
        self.page_set_edit_cfg_ignore_regexp.setStyleSheet("QLineEdit {border: 1px solid rgba(0,0,0, 0.5);}QToolTip { border: none; background-color: white; color: black; } QToolTip QLabel { color: red; }")
        self.page_set_edit_cfg_ignore_regexp.setToolTip("输入内容以<span style='color:red'>【英文逗号】</span>分隔。比如:关键词1,关键词2,关键词3")

        self.page_set_edit_cfg_ignore_regexp.setText(
            ','.join(self.dict_cfgs[value_cfgs_ignore_rules][value_cfgs_ignore_rules_regexp]))
        self.page_set_edit_cfg_ignore_regexp.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_ignore_rules,
                                                {**self.dict_cfgs[value_cfgs_ignore_rules],
                                                 **{value_cfgs_ignore_rules_regexp: new_value.split(',')}}))

        self.page_set_edit_cfg_api_presence_penalty = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_presence_penalty.setGeometry(QtCore.QRect(450, 1420, 105, 30))
        self.page_set_edit_cfg_api_presence_penalty.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_presence_penalty.setMaximum(1.0)
        self.page_set_edit_cfg_api_presence_penalty.setSingleStep(0.1)
        self.page_set_edit_cfg_api_presence_penalty.setObjectName("page_set_edit_cfg_api_presence_penalty")
        self.page_set_edit_cfg_api_presence_penalty.setValue(
            self.dict_cfgs[value_cfgs_completion_api_params][value_cfgs_completion_api_params_presence_penalty])
        self.page_set_edit_cfg_api_presence_penalty.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_completion_api_params,
                                                {**self.dict_cfgs[value_cfgs_completion_api_params],
                                                 **{value_cfgs_completion_api_params_presence_penalty: new_value}}))

        self.page_set_edit_cfg_api_frequency_penalty = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_frequency_penalty.setGeometry(QtCore.QRect(450, 1380, 105, 30))
        self.page_set_edit_cfg_api_frequency_penalty.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_frequency_penalty.setMaximum(1.0)
        self.page_set_edit_cfg_api_frequency_penalty.setSingleStep(0.1)
        self.page_set_edit_cfg_api_frequency_penalty.setObjectName("page_set_edit_cfg_api_frequency_penalty")
        self.page_set_edit_cfg_api_frequency_penalty.setValue(
            self.dict_cfgs[value_cfgs_completion_api_params][value_cfgs_completion_api_params_frequency_penalty])
        self.page_set_edit_cfg_api_frequency_penalty.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_completion_api_params,
                                                {**self.dict_cfgs[value_cfgs_completion_api_params],
                                                 **{value_cfgs_completion_api_params_frequency_penalty: new_value}}))

        self.page_set_label_cfg_api_model = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_model.setGeometry(QtCore.QRect(260, 1200, 54, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_model.setFont(font)
        self.page_set_label_cfg_api_model.setObjectName("page_set_label_cfg_api_model")

        self.page_set_label_cfg_api_frequency_penalty = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_frequency_penalty.setGeometry(QtCore.QRect(260, 1380, 177, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_frequency_penalty.setFont(font)
        self.page_set_label_cfg_api_frequency_penalty.setObjectName("page_set_label_cfg_api_frequency_penalty")

        self.page_set_edit_cfg_api_top_p = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_top_p.setGeometry(QtCore.QRect(550, 1340, 84, 30))
        self.page_set_edit_cfg_api_top_p.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_top_p.setMaximum(1.0)
        self.page_set_edit_cfg_api_top_p.setSingleStep(0.1)
        self.page_set_edit_cfg_api_top_p.setObjectName("page_set_edit_cfg_api_top_p")
        self.page_set_edit_cfg_api_top_p.setValue(
            self.dict_cfgs[value_cfgs_completion_api_params][value_cfgs_completion_api_params_top_p])
        self.page_set_edit_cfg_api_top_p.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_completion_api_params,
                                                {**self.dict_cfgs[value_cfgs_completion_api_params],
                                                 **{value_cfgs_completion_api_params_top_p: new_value}}))

        self.page_set_label_cfg_api_presence_penalty = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_presence_penalty.setGeometry(QtCore.QRect(260, 1420, 177, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_presence_penalty.setFont(font)
        self.page_set_label_cfg_api_presence_penalty.setObjectName("page_set_label_cfg_api_presence_penalty")

        self.page_set_label_cfg_api_top_p = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_top_p.setGeometry(QtCore.QRect(260, 1340, 288, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_top_p.setFont(font)
        self.page_set_label_cfg_api_top_p.setObjectName("page_set_label_cfg_api_top_p")

        self.page_set_edit_cfg_prompt_submit_length = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_prompt_submit_length.setGeometry(QtCore.QRect(510, 1300, 91, 30))
        self.page_set_edit_cfg_prompt_submit_length.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_prompt_submit_length.setMaximum(4096)
        self.page_set_edit_cfg_prompt_submit_length.setSingleStep(128)
        self.page_set_edit_cfg_prompt_submit_length.setObjectName("page_set_edit_cfg_prompt_submit_length")
        self.page_set_edit_cfg_prompt_submit_length.setValue(self.dict_cfgs[value_cfgs_prompt_submit_length])
        self.page_set_edit_cfg_prompt_submit_length.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_prompt_submit_length, new_value))

        self.page_set_label_cfg_api_temperature = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_temperature.setGeometry(QtCore.QRect(260, 1240, 54, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_temperature.setFont(font)
        self.page_set_label_cfg_api_temperature.setObjectName("page_set_label_cfg_api_temperature")
        self.page_set_label_cfg_api_temperature.setToolTip("数值越低得到的回答越理性，取值范围[0, 1]")
        self.page_set_label_cfg_api_temperature.setStyleSheet(
            "QLineEdit {border: 1px solid rgba(0,0,0, 0.5);}QToolTip { border: none; background-color: white; color: black; } QToolTip QLabel { color: red; }")


        self.page_set_edit_cfg_response_regexp = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_response_regexp.setGeometry(QtCore.QRect(430, 1061, 321, 30))
        self.page_set_edit_cfg_response_regexp.setObjectName("page_set_edit_cfg_response_regexp")
        self.page_set_edit_cfg_response_regexp.setStyleSheet("QLineEdit {border: 1px solid rgba(0,0,0, 0.5);}QToolTip { border: none; background-color: white; color: black; } QToolTip QLabel { color: red; }")
        self.page_set_edit_cfg_response_regexp.setToolTip("输入内容以<span style='color:red'>【英文逗号】</span>分隔。比如:关键词1,关键词2,关键词3")
        self.page_set_edit_cfg_response_regexp.setText(
            ','.join(self.dict_cfgs[value_cfgs_response_rules][value_cfgs_response_rules_regexp]))
        self.page_set_edit_cfg_response_regexp.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_response_rules,
                                                {**self.dict_cfgs[value_cfgs_response_rules],
                                                 **{value_cfgs_response_rules_regexp: new_value.split(',')}}))
        self.page_set_edit_cfg_response_prefix = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_response_prefix.setGeometry(QtCore.QRect(430, 1020, 321, 30))
        self.page_set_edit_cfg_response_prefix.setObjectName("page_set_edit_cfg_response_prefix")
        self.page_set_edit_cfg_response_prefix.setStyleSheet("QLineEdit {border: 1px solid rgba(0,0,0, 0.5);}QToolTip { border: none; background-color: white; color: black; } QToolTip QLabel { color: red; }")
        self.page_set_edit_cfg_response_prefix.setToolTip("输入内容以<span style='color:red'>【英文】逗号</span>分隔。比如关键词1,关键词2,关键词3")

        self.page_set_edit_cfg_response_prefix.setText(
            ','.join(self.dict_cfgs[value_cfgs_response_rules][value_cfgs_response_rules_prefix]))
        self.page_set_edit_cfg_response_prefix.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_response_rules,
                                                {**self.dict_cfgs[value_cfgs_response_rules],
                                                 **{value_cfgs_response_rules_prefix: new_value.split(',')}}))

        self.page_set_edit_cfg_api_temperature = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_temperature.setGeometry(QtCore.QRect(330, 1240, 60, 30))
        self.page_set_edit_cfg_api_temperature.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_temperature.setMaximum(1.0)
        self.page_set_edit_cfg_api_temperature.setSingleStep(0.1)
        self.page_set_edit_cfg_api_temperature.setObjectName("page_set_edit_cfg_api_temperature")
        self.page_set_edit_cfg_api_temperature.setValue(
            self.dict_cfgs[value_cfgs_completion_api_params][value_cfgs_completion_api_params_temperature])
        self.page_set_edit_cfg_api_temperature.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_completion_api_params,
                                                {**self.dict_cfgs[value_cfgs_completion_api_params],
                                                 **{value_cfgs_completion_api_params_temperature: new_value}}))

        self.page_set_edit_cfg_api_model = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_model.setEnabled(True)
        self.page_set_edit_cfg_api_model.setGeometry(QtCore.QRect(330, 1200, 201, 30))
        self.page_set_edit_cfg_api_model.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);"
                                                       "QComboBox {"
                                                       "    background-color: (255,255,255, 0.1);"
                                                       "    color: white;  /* 定义文本的颜色 */"
                                                       "}"
                                                       "QComboBox QAbstractItemView {"
                                                       "    background-color: white;"
                                                       "    selection-background-color:   /* 定义选择项后背景色 */"
                                                       "    color: rgb(255, 170, 255);"
                                                       "    selection-color: white;  /* 定义选择区文本的颜色 */"
                                                       "}")
        self.page_set_edit_cfg_api_model.setEditable(False)
        self.page_set_edit_cfg_api_model.setModelColumn(0)
        self.page_set_edit_cfg_api_model.setObjectName("page_set_edit_cfg_api_model")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.addItem("")
        self.page_set_edit_cfg_api_model.setItemText(0, "gpt-4")
        self.page_set_edit_cfg_api_model.setItemText(1, "gpt-4-0314")
        self.page_set_edit_cfg_api_model.setItemText(2, "gpt-4-32k")
        self.page_set_edit_cfg_api_model.setItemText(3, "gpt-4-32k-0314")
        self.page_set_edit_cfg_api_model.setItemText(4, "gpt-3.5-turbo")
        self.page_set_edit_cfg_api_model.setItemText(5, "gpt-3.5-turbo-0301")
        self.page_set_edit_cfg_api_model.setItemText(6, "text-davinci-003")
        self.page_set_edit_cfg_api_model.setItemText(7, "text-davinci-002")
        self.page_set_edit_cfg_api_model.setItemText(8, "code-davinci-002")
        self.page_set_edit_cfg_api_model.setItemText(9, "code-cushman-001")
        self.page_set_edit_cfg_api_model.setItemText(10, "text-curie-001")
        self.page_set_edit_cfg_api_model.setItemText(11, "text-babbage-001")
        self.page_set_edit_cfg_api_model.setItemText(12, "text-ada-001")
        self.page_set_edit_cfg_api_model.setCurrentText(
            self.dict_cfgs[value_cfgs_completion_api_params][value_cfgs_completion_api_params_model])
        self.page_set_edit_cfg_api_model.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_completion_api_params,
                                                {**self.dict_cfgs[value_cfgs_completion_api_params],
                                                 **{value_cfgs_completion_api_params_model: new_value}}))

        self.page_set_label_cfg_mirai_qq = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_mirai_qq.setGeometry(QtCore.QRect(260, 190, 102, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_mirai_qq.setFont(font)
        self.page_set_label_cfg_mirai_qq.setObjectName("page_set_label_cfg_mirai_qq")
        self.page_set_label_cfg_admin_qq = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_admin_qq.setGeometry(QtCore.QRect(260, 225, 102, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_admin_qq.setFont(font)
        self.page_set_label_cfg_admin_qq.setObjectName("page_set_label_cfg_admin_qq")
        self.page_set_label_cfg_mirai_verifyKey = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_mirai_verifyKey.setGeometry(QtCore.QRect(260, 155, 96, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_mirai_verifyKey.setFont(font)
        self.page_set_label_cfg_mirai_verifyKey.setObjectName("page_set_label_cfg_mirai_verifyKey")
        self.page_set_label_cfg_mirai_host = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_mirai_host.setGeometry(QtCore.QRect(260, 85, 90, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_mirai_host.setFont(font)
        self.page_set_label_cfg_mirai_host.setIndent(-1)
        self.page_set_label_cfg_mirai_host.setObjectName("page_set_label_cfg_mirai_host")
        self.page_set_label_cfg_mirai_port = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_mirai_port.setGeometry(QtCore.QRect(260, 120, 54, 25))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_mirai_port.setFont(font)
        self.page_set_label_cfg_mirai_port.setObjectName("page_set_label_cfg_mirai_port")
        self.page_set_label_cfg_mirai_adapter = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_mirai_adapter.setGeometry(QtCore.QRect(260, 50, 90, 24))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_mirai_adapter.setFont(font)
        self.page_set_label_cfg_mirai_adapter.setObjectName("page_set_label_cfg_mirai_adapter")
        self.page_set_edit_cfg_mirai_host = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_mirai_host.setGeometry(QtCore.QRect(370, 85, 142, 25))
        self.page_set_edit_cfg_mirai_host.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_mirai_host.setObjectName("page_set_edit_cfg_mirai_host")
        self.page_set_edit_cfg_mirai_host.setText(
            self.dict_cfgs[value_cfgs_mirai_http_api_config][value_cfgs_mirai_http_api_config_host])
        self.page_set_edit_cfg_mirai_host.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_mirai_http_api_config,
                                                {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
                                                 **{value_cfgs_mirai_http_api_config_host: new_value}}))

        self.page_set_edit_cfg_mirai_port = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_mirai_port.setGeometry(QtCore.QRect(370, 120, 142, 25))
        self.page_set_edit_cfg_mirai_port.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_mirai_port.setObjectName("page_set_edit_cfg_mirai_port")
        self.page_set_edit_cfg_mirai_port.setMaximum(65535)
        self.page_set_edit_cfg_mirai_port.setMinimum(0)
        self.page_set_edit_cfg_mirai_port.setValue(
            self.dict_cfgs[value_cfgs_mirai_http_api_config][value_cfgs_mirai_http_api_config_port])
        self.page_set_edit_cfg_mirai_port.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_mirai_http_api_config,
                                                {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
                                                 **{value_cfgs_mirai_http_api_config_port: new_value}}))

        self.page_set_edit_cfg_mirai_verifyKey = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_mirai_verifyKey.setGeometry(QtCore.QRect(370, 155, 140, 25))
        self.page_set_edit_cfg_mirai_verifyKey.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_mirai_verifyKey.setObjectName("page_set_edit_cfg_mirai_verifyKey")
        self.page_set_edit_cfg_mirai_verifyKey.setText(
            self.dict_cfgs[value_cfgs_mirai_http_api_config][value_cfgs_mirai_http_api_config_verifyKey])
        self.page_set_edit_cfg_mirai_verifyKey.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_mirai_http_api_config,
                                                {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
                                                 **{value_cfgs_mirai_http_api_config_verifyKey: new_value}}))

        self.page_set_edit_cfg_mirai_qq = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_mirai_qq.setGeometry(QtCore.QRect(370, 190, 142, 25))
        self.page_set_edit_cfg_mirai_qq.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_mirai_qq.setObjectName("page_set_edit_cfg_mirai_qq")
        self.page_set_edit_cfg_mirai_qq.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,13}"), self))
        self.page_set_edit_cfg_mirai_qq.setText(str(
            self.dict_cfgs[value_cfgs_mirai_http_api_config][value_cfgs_mirai_http_api_config_qq]))
        self.page_set_edit_cfg_mirai_qq.textChanged.connect(lambda new_value: update_mirai_qq(new_value))
        # self.page_set_edit_cfg_mirai_qq.textChanged.connect(
        #     lambda new_value: update_value_cfgs(value_cfgs_mirai_http_api_config,
        #                                         {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
        #                                          **{value_cfgs_mirai_http_api_config_qq: int(new_value)}}))

        self.page_set_edit_cfg_admin_qq = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_admin_qq.setGeometry(QtCore.QRect(370, 225, 142, 25))
        self.page_set_edit_cfg_admin_qq.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_admin_qq.setObjectName("page_set_edit_cfg_admin_qq")
        self.page_set_edit_cfg_admin_qq.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,13}"), self))
        self.page_set_edit_cfg_admin_qq.setText(str(
            self.dict_cfgs[value_cfgs_admin_qq]))
        self.page_set_edit_cfg_admin_qq.textChanged.connect(lambda new_value: update_admin_qq(new_value))
        # self.page_set_edit_cfg_admin_qq.textChanged.connect(
        #     lambda new_value: update_value_cfgs(value_cfgs_admin_qq, int(new_value)))



        self.page_set_edit_cfg_mirai_adapter = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_mirai_adapter.setGeometry(QtCore.QRect(370, 50, 200, 25))
        self.page_set_edit_cfg_mirai_adapter.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_mirai_adapter.setObjectName("page_set_edit_cfg_mirai_adapter")
        self.page_set_edit_cfg_mirai_adapter.addItem("")
        self.page_set_edit_cfg_mirai_adapter.addItem("")
        self.page_set_edit_cfg_mirai_adapter.setItemText(0, "HTTPAdapter")
        self.page_set_edit_cfg_mirai_adapter.setItemText(1, "WebSocketAdapter")
        self.page_set_edit_cfg_mirai_adapter.setCurrentText(self.dict_cfgs[value_cfgs_mirai_http_api_config][value_cfgs_mirai_http_api_config_adapter])
        self.page_set_edit_cfg_mirai_adapter.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_mirai_http_api_config,
                                                  {**self.dict_cfgs[value_cfgs_mirai_http_api_config],
                                                 **{value_cfgs_mirai_http_api_config_adapter: new_value}}))

        self.page_set_edit_cfg_api_http_proxy = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_http_proxy.setGeometry(QtCore.QRect(450, 335, 142, 22))
        self.page_set_edit_cfg_api_http_proxy.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_http_proxy.setObjectName("page_set_edit_cfg_api_http_proxy")
        self.page_set_edit_cfg_api_http_proxy.setText(
            self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_http_proxy])
        self.page_set_edit_cfg_api_http_proxy.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_openai_config,
                                                {**self.dict_cfgs[value_cfgs_openai_config],
                                                 **{value_cfgs_openai_config_http_proxy: new_value}}))

        self.page_set_edit_cfg_api_reverse_proxy = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_api_reverse_proxy.setGeometry(QtCore.QRect(450, 370, 142, 22))
        self.page_set_edit_cfg_api_reverse_proxy.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_api_reverse_proxy.setObjectName("page_set_edit_cfg_api_reverse_proxy")
        self.page_set_edit_cfg_api_reverse_proxy.setText(
            self.dict_cfgs[value_cfgs_openai_config][value_cfgs_openai_config_reverse_proxy])
        self.page_set_edit_cfg_api_reverse_proxy.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_openai_config,
                                                {**self.dict_cfgs[value_cfgs_openai_config],
                                                 **{value_cfgs_openai_config_reverse_proxy: new_value}}))

        self.page_set_label_cfg_api_reverse_proxy = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_reverse_proxy.setGeometry(QtCore.QRect(370, 370, 65, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_reverse_proxy.setFont(font)
        self.page_set_label_cfg_api_reverse_proxy.setObjectName("page_set_label_cfg_api_reverse_proxy")

        self.page_set_label_cfg_api_http_proxy = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_api_http_proxy.setGeometry(QtCore.QRect(370, 330, 41, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_api_http_proxy.setFont(font)
        self.page_set_label_cfg_api_http_proxy.setObjectName("page_set_label_cfg_api_http_proxy")

        self.page_set_label_cfg_preset_mode = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_preset_mode.setGeometry(QtCore.QRect(260, 430, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_preset_mode.setFont(font)
        self.page_set_label_cfg_preset_mode.setObjectName("page_set_label_cfg_preset_mode")

        self.page_set_edit_cfg_preset_mode = QtWidgets.QComboBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_preset_mode.setGeometry(QtCore.QRect(370, 430, 141, 31))
        self.page_set_edit_cfg_preset_mode.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_preset_mode.setObjectName("page_set_edit_cfg_preset_mode")
        self.page_set_edit_cfg_preset_mode.addItem("")
        self.page_set_edit_cfg_preset_mode.addItem("")
        self.page_set_edit_cfg_preset_mode.setItemText(0, "normal")
        self.page_set_edit_cfg_preset_mode.setItemText(1, "full_scenario")
        self.page_set_edit_cfg_preset_mode.setCurrentText(self.dict_cfgs[value_cfgs_preset_mode])
        self.page_set_edit_cfg_preset_mode.currentTextChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_preset_mode, new_value))

        self.page_set_label_cfg_response_prefix = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_response_prefix.setGeometry(QtCore.QRect(260, 1020, 90, 29))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_response_prefix.setFont(font)
        self.page_set_label_cfg_response_prefix.setObjectName("page_set_label_cfg_response_prefix")

        self.page_set_label_cfg_response_regexp = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_response_regexp.setGeometry(QtCore.QRect(260, 1060, 161, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_response_regexp.setFont(font)
        self.page_set_label_cfg_response_regexp.setObjectName("page_set_label_cfg_response_regexp")

        self.page_set_label_cfg_baidu_api_key = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_baidu_api_key.setGeometry(QtCore.QRect(260, 2260, 141, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_baidu_api_key.setFont(font)
        self.page_set_label_cfg_baidu_api_key.setObjectName("page_set_label_cfg_baidu_api_key")

        self.page_set_edit_cfg_baidu_api_key = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_baidu_api_key.setGeometry(QtCore.QRect(400, 2260, 142, 30))
        self.page_set_edit_cfg_baidu_api_key.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_baidu_api_key.setObjectName("page_set_edit_cfg_baidu_api_key")
        self.page_set_edit_cfg_baidu_api_key.setText(self.dict_cfgs[value_cfgs_baidu_api_key])
        self.page_set_edit_cfg_baidu_api_key.textChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_baidu_api_key, new_value))

        self.page_set_edit_cfg_encourage_sponsor_at_start = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_encourage_sponsor_at_start.setGeometry(QtCore.QRect(260, 2380, 167, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_encourage_sponsor_at_start.setFont(font)
        self.page_set_edit_cfg_encourage_sponsor_at_start.setObjectName("page_set_edit_cfg_encourage_sponsor_at_start")
        self.page_set_edit_cfg_encourage_sponsor_at_start.setChecked(
            self.dict_cfgs[value_cfgs_encourage_sponsor_at_start])
        self.page_set_edit_cfg_encourage_sponsor_at_start.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_encourage_sponsor_at_start, bool(state)))

        self.page_set_edit_cfg_hide_exce_info_to_user = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_hide_exce_info_to_user.setGeometry(QtCore.QRect(260, 2420, 347, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_hide_exce_info_to_user.setFont(font)
        self.page_set_edit_cfg_hide_exce_info_to_user.setObjectName("page_set_edit_cfg_hide_exce_info_to_user")
        self.page_set_edit_cfg_hide_exce_info_to_user.setChecked(self.dict_cfgs[value_cfgs_hide_exce_info_to_user])
        self.page_set_edit_cfg_hide_exce_info_to_user.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_hide_exce_info_to_user, bool(state)))

        self.page_set_edit_cfg_upgrade_dependencies = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_upgrade_dependencies.setGeometry(QtCore.QRect(260, 2460, 203, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_upgrade_dependencies.setFont(font)
        self.page_set_edit_cfg_upgrade_dependencies.setObjectName("page_set_edit_cfg_upgrade_dependencies")
        self.page_set_edit_cfg_upgrade_dependencies.setChecked(self.dict_cfgs[value_cfgs_upgrade_dependencies])
        self.page_set_edit_cfg_upgrade_dependencies.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_upgrade_dependencies, bool(state)))

        self.page_set_edit_cfg_report_usage = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_report_usage.setGeometry(QtCore.QRect(260, 2500, 131, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_edit_cfg_report_usage.setFont(font)
        self.page_set_edit_cfg_report_usage.setObjectName("page_set_edit_cfg_report_usage")
        self.page_set_edit_cfg_report_usage.setChecked(self.dict_cfgs[value_cfgs_report_usage])
        self.page_set_edit_cfg_report_usage.stateChanged.connect(
            lambda state: update_value_cfgs(value_cfgs_report_usage, bool(state)))

        self.page_set_edit_cfg_logging_level = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_5)
        self.page_set_edit_cfg_logging_level.setGeometry(QtCore.QRect(360, 2540, 142, 30))
        self.page_set_edit_cfg_logging_level.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_cfg_logging_level.setObjectName("page_set_edit_cfg_logging_level")
        self.page_set_edit_cfg_logging_level.setValue(self.dict_cfgs[value_cfgs_logging_level])
        self.page_set_edit_cfg_logging_level.valueChanged.connect(
            lambda new_value: update_value_cfgs(value_cfgs_logging_level, new_value))

        self.page_set_label_cfg_logging_level = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cfg_logging_level.setGeometry(QtCore.QRect(260, 2540, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_cfg_logging_level.setFont(font)
        self.page_set_label_cfg_logging_level.setObjectName("page_set_label_cfg_logging_level")

        self.page_set_label_cmd_plugin_off = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin_off.setGeometry(QtCore.QRect(510, 2760, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin_off.setFont(font)
        self.page_set_label_cmd_plugin_off.setObjectName("page_set_label_cmd_plugin_off")

        self.page_set_label_cmd_plugin = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin.setGeometry(QtCore.QRect(510, 2600, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin.setFont(font)
        self.page_set_label_cmd_plugin.setObjectName("page_set_label_cmd_plugin")

        self.page_set_label_cmd_plugin_get = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin_get.setGeometry(QtCore.QRect(510, 2640, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin_get.setFont(font)
        self.page_set_label_cmd_plugin_get.setObjectName("page_set_label_cmd_plugin_get")

        self.page_set_label_cmd_plugin_update = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin_update.setGeometry(QtCore.QRect(510, 2680, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin_update.setFont(font)
        self.page_set_label_cmd_plugin_update.setObjectName("page_set_label_cmd_plugin_update")

        self.page_set_label_cmd_plugin_del = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin_del.setGeometry(QtCore.QRect(510, 2720, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin_del.setFont(font)
        self.page_set_label_cmd_plugin_del.setObjectName("page_set_label_cmd_plugin_del")

        self.page_set_label_cmd_plugin_on = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_plugin_on.setGeometry(QtCore.QRect(510, 2800, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_plugin_on.setFont(font)
        self.page_set_label_cmd_plugin_on.setObjectName("page_set_label_cmd_plugin_on")

        self.page_set_label_cmd_list = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_list.setGeometry(QtCore.QRect(510, 2840, 120, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_list.setFont(font)
        self.page_set_label_cmd_list.setObjectName("page_set_label_cmd_list")

        self.page_set_label_cmd_next = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_next.setGeometry(QtCore.QRect(510, 2880, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_next.setFont(font)
        self.page_set_label_cmd_next.setObjectName("page_set_label_cmd_next")

        self.page_set_label_cmd_resend = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_resend.setGeometry(QtCore.QRect(510, 2920, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_resend.setFont(font)
        self.page_set_label_cmd_resend.setObjectName("page_set_label_cmd_resend")

        self.page_set_label_cmd_help = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_help.setGeometry(QtCore.QRect(510, 2960, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_help.setFont(font)
        self.page_set_label_cmd_help.setObjectName("page_set_label_cmd_help")

        self.page_set_label_cmd_update = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_update.setGeometry(QtCore.QRect(510, 3000, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_update.setFont(font)
        self.page_set_label_cmd_update.setObjectName("page_set_label_cmd_update")

        self.page_set_label_cmd_version = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_version.setGeometry(QtCore.QRect(510, 3040, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_version.setFont(font)
        self.page_set_label_cmd_version.setObjectName("page_set_label_cmd_version")

        self.page_set_label_tips_command_reset_name_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_command_reset_name_message.setGeometry(QtCore.QRect(260, 3460, 162, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_command_reset_name_message.setFont(font)
        self.page_set_label_tips_command_reset_name_message.setObjectName(
            "page_set_label_tips_command_reset_name_message")

        self.page_set_label_tips_alter_tip_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_alter_tip_message.setGeometry(QtCore.QRect(260, 3140, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_alter_tip_message.setFont(font)
        self.page_set_label_tips_alter_tip_message.setObjectName("page_set_label_tips_alter_tip_message")

        self.page_set_label_tips_rate_limit_drop_tip = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_rate_limit_drop_tip.setGeometry(QtCore.QRect(260, 3180, 180, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_rate_limit_drop_tip.setFont(font)
        self.page_set_label_tips_rate_limit_drop_tip.setObjectName("page_set_label_tips_rate_limit_drop_tip")

        self.page_set_label_tips_help_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_help_message.setGeometry(QtCore.QRect(260, 3220, 182, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_help_message.setFont(font)
        self.page_set_label_tips_help_message.setObjectName("page_set_label_tips_help_message")

        self.page_set_label_tips_reply_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_reply_message.setGeometry(QtCore.QRect(260, 3260, 162, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_reply_message.setFont(font)
        self.page_set_label_tips_reply_message.setObjectName("page_set_label_tips_reply_message")

        self.page_set_label_tips_replys_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_replys_message.setGeometry(QtCore.QRect(260, 3300, 162, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_replys_message.setFont(font)
        self.page_set_label_tips_replys_message.setObjectName("page_set_label_tips_replys_message")

        self.page_set_label_tips_command_admin_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_command_admin_message.setGeometry(QtCore.QRect(260, 3340, 162, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_command_admin_message.setFont(font)
        self.page_set_label_tips_command_admin_message.setObjectName("page_set_label_tips_command_admin_message")

        self.page_set_label_tips_command_err_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_command_err_message.setGeometry(QtCore.QRect(260, 3380, 162, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_command_err_message.setFont(font)
        self.page_set_label_tips_command_err_message.setObjectName("page_set_label_tips_command_err_message")

        self.page_set_label_tips_command_reset_message = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_tips_command_reset_message.setGeometry(QtCore.QRect(260, 3420, 126, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.page_set_label_tips_command_reset_message.setFont(font)
        self.page_set_label_tips_command_reset_message.setObjectName("page_set_label_tips_command_reset_message")

        self.page_set_label_cmd_draw = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_draw.setGeometry(QtCore.QRect(260, 2600, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_draw.setFont(font)
        self.page_set_label_cmd_draw.setObjectName("page_set_label_cmd_draw")

        self.page_set_label_cmd_default = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_default.setGeometry(QtCore.QRect(260, 2640,90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_default.setFont(font)
        self.page_set_label_cmd_default.setObjectName("page_set_label_cmd_default")

        self.page_set_label_cmd_default_set = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_default_set.setGeometry(QtCore.QRect(260, 2680, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_default_set.setFont(font)
        self.page_set_label_cmd_default_set.setObjectName("page_set_label_cmd_default_set")

        self.page_set_label_cmd_del = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_del.setGeometry(QtCore.QRect(260, 2720, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_del.setFont(font)
        self.page_set_label_cmd_del.setObjectName("page_set_label_cmd_del")

        self.page_set_label_cmd_del_all = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_del_all.setGeometry(QtCore.QRect(260, 2760, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_del_all.setFont(font)
        self.page_set_label_cmd_del_all.setObjectName("page_set_label_cmd_del_all")

        self.page_set_label_cmd_delhst = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_delhst.setGeometry(QtCore.QRect(260, 2800, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_delhst.setFont(font)
        self.page_set_label_cmd_delhst.setObjectName("page_set_label_cmd_delhst")

        self.page_set_label_cmd_delhs_tall = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_delhs_tall.setGeometry(QtCore.QRect(260, 2840, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_delhs_tall.setFont(font)
        self.page_set_label_cmd_delhs_tall.setObjectName("page_set_label_cmd_delhs_tall")

        self.page_set_label_cmd_last = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_last.setGeometry(QtCore.QRect(260, 2880, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_last.setFont(font)
        self.page_set_label_cmd_last.setObjectName("page_set_label_cmd_last")

        self.page_set_label_cmd_prompt = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_prompt.setGeometry(QtCore.QRect(260, 2920, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_prompt.setFont(font)
        self.page_set_label_cmd_prompt.setObjectName("page_set_label_cmd_prompt")

        self.page_set_label_cmd_reset = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_reset.setGeometry(QtCore.QRect(260, 2960, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_reset.setFont(font)
        self.page_set_label_cmd_reset.setObjectName("page_set_label_cmd_reset")

        self.page_set_label_cmd_reload = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_reload.setGeometry(QtCore.QRect(260, 3000, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_reload.setFont(font)
        self.page_set_label_cmd_reload.setObjectName("page_set_label_cmd_reload")

        self.page_set_label_cmd_usage = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_usage.setGeometry(QtCore.QRect(260, 3040, 90, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_usage.setFont(font)
        self.page_set_label_cmd_usage.setObjectName("page_set_label_cmd_usage")

        self.page_set_label_cmd_cmd = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_cmd.setGeometry(QtCore.QRect(510, 3080, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_cmd.setFont(font)
        self.page_set_label_cmd_cmd.setObjectName("page_set_label_cmd_cmd")

        self.page_set_label_cmd_cfg = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.page_set_label_cmd_cfg.setGeometry(QtCore.QRect(260, 3080, 120, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.page_set_label_cmd_cfg.setFont(font)
        self.page_set_label_cmd_cfg.setObjectName("page_set_label_cmd_cfg")

        self.page_set_edit_tips_alter_tip_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_alter_tip_message.setGeometry(QtCore.QRect(442, 3140, 527, 30))
        self.page_set_edit_tips_alter_tip_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_alter_tip_message.setObjectName("page_set_edit_tips_alter_tip_message")
        self.page_set_edit_tips_alter_tip_message.setText(str(self.dict_tips[value_tips_alter_tip_message]))
        self.page_set_edit_tips_alter_tip_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_alter_tip_message, new_value))

        self.page_set_edit_tips_rate_limit_drop_tip = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_rate_limit_drop_tip.setGeometry(QtCore.QRect(442, 3180, 527, 30))
        self.page_set_edit_tips_rate_limit_drop_tip.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_rate_limit_drop_tip.setObjectName("page_set_edit_tips_rate_limit_drop_tip")
        self.page_set_edit_tips_rate_limit_drop_tip.setText(str(self.dict_tips[value_tips_rate_limit_drop_tip]))
        self.page_set_edit_tips_rate_limit_drop_tip.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_rate_limit_drop_tip, new_value))

        self.page_set_edit_tips_help_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_help_message.setGeometry(QtCore.QRect(442, 3220, 527, 30))
        self.page_set_edit_tips_help_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_help_message.setObjectName("page_set_edit_tips_help_message")
        self.page_set_edit_tips_help_message.setText(str(self.dict_tips[value_tips_help_message]))
        self.page_set_edit_tips_help_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_help_message, new_value))

        self.page_set_edit_tips_reply_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_reply_message.setGeometry(QtCore.QRect(442, 3260, 527, 30))
        self.page_set_edit_tips_reply_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_reply_message.setObjectName("page_set_edit_tips_reply_message")
        self.page_set_edit_tips_reply_message.setText(str(self.dict_tips[value_tips_reply_message]))
        self.page_set_edit_tips_reply_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_reply_message, new_value))

        self.page_set_edit_tips_replys_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_replys_message.setGeometry(QtCore.QRect(442, 3300, 527, 30))
        self.page_set_edit_tips_replys_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_replys_message.setObjectName("page_set_edit_tips_replys_message")
        self.page_set_edit_tips_replys_message.setText(str(self.dict_tips[value_tips_replys_message]))
        self.page_set_edit_tips_replys_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_replys_message, new_value))

        self.page_set_edit_tips_command_admin_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_command_admin_message.setGeometry(QtCore.QRect(442, 3340, 527, 30))
        self.page_set_edit_tips_command_admin_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_command_admin_message.setObjectName("page_set_edit_tips_command_admin_message")
        self.page_set_edit_tips_command_admin_message.setText(str(self.dict_tips[value_tips_command_admin_message]))
        self.page_set_edit_tips_command_admin_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_command_admin_message, new_value))

        self.page_set_edit_tips_command_err_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_command_err_message.setGeometry(QtCore.QRect(442, 3380, 527, 30))
        self.page_set_edit_tips_command_err_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_command_err_message.setObjectName("page_set_edit_tips_command_err_message")
        self.page_set_edit_tips_command_err_message.setText(str(self.dict_tips[value_tips_command_err_message]))
        self.page_set_edit_tips_command_err_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_command_err_message, new_value))

        self.page_set_edit_tips_command_reset_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_command_reset_message.setGeometry(QtCore.QRect(442, 3420, 527, 30))
        self.page_set_edit_tips_command_reset_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_command_reset_message.setObjectName("page_set_edit_tips_command_reset_message")
        self.page_set_edit_tips_command_reset_message.setText(str(self.dict_tips[value_tips_command_reset_message]))
        self.page_set_edit_tips_command_reset_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_command_reset_message, new_value))

        self.page_set_edit_tips_command_reset_name_message = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_5)
        self.page_set_edit_tips_command_reset_name_message.setGeometry(QtCore.QRect(442, 3460, 527, 30))
        self.page_set_edit_tips_command_reset_name_message.setStyleSheet("border: 1px solid rgba(0,0,0, 0.5);")
        self.page_set_edit_tips_command_reset_name_message.setObjectName(
            "page_set_edit_tips_command_reset_name_message")
        self.page_set_edit_tips_command_reset_name_message.setText(
            str(self.dict_tips[value_tips_command_reset_name_message]))
        self.page_set_edit_tips_command_reset_name_message.textChanged.connect(
            lambda new_value: update_value_tips(value_tips_command_reset_name_message, new_value))

        self.page_set_scroll_area.setWidget(self.scrollAreaWidgetContents_5)
        self.menu_tab.addTab(self.tab_set, "")
        self.tab_help = QtWidgets.QWidget()
        self.tab_help.setMinimumSize(QtCore.QSize(1020, 740))
        self.tab_help.setMaximumSize(QtCore.QSize(1160, 740))
        self.tab_help.setStyleSheet(
            "background-color: rgba(255, 255, 255,0.025);QMenu {background-color:rgb(233, 190, 203);}\n"
            "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
            " } ")
        self.tab_help.setObjectName("tab_help")

        self.page_help_text = QtWidgets.QTextBrowser(self.tab_help)
        self.page_help_text.setGeometry(QtCore.QRect(0, 0, 1020, 740))
        self.page_help_text.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.page_help_text.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.page_help_text.setStyleSheet(" ")
        self.page_help_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.page_help_text.setAcceptRichText(True)
        self.page_help_text.setObjectName("page_help_text")
        with open("README.md","r",encoding="utf8") as f:
            content=f.read()
        html = markdown2.markdown(content)
        self.page_help_text.setHtml(html)

        self.menu_tab.addTab(self.tab_help, "")
        self.tab_cbout = QtWidgets.QWidget()
        self.tab_cbout.setMinimumSize(QtCore.QSize(1020, 740))
        self.tab_cbout.setMaximumSize(QtCore.QSize(1160, 740))
        self.tab_cbout.setStyleSheet(
            "background-color: rgba(255, 255, 255,0.025);QMenu {background-color:rgb(233, 190, 203);}\n"
            "QComboBox QAbstractItemView {background-color:  rgb(185, 208, 230);\n"
            " } ")
        self.tab_cbout.setObjectName("tab_cbout")
        self.page_about_text = QtWidgets.QTextBrowser(self.tab_cbout)
        self.page_about_text.setGeometry(QtCore.QRect(0, 0, 1021, 741))
        self.page_about_text.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.page_about_text.setObjectName("page_about_text")

        self.menu_tab.addTab(self.tab_cbout, "")
        self.back_center = QtWidgets.QLabel(self.centralwidget)
        self.back_center.setEnabled(True)
        self.back_center.setGeometry(QtCore.QRect(140, 100, 1020, 740))
        self.back_center.setMinimumSize(QtCore.QSize(1020, 740))
        self.back_center.setMaximumSize(QtCore.QSize(1020, 740))
        self.back_center.setStyleSheet("background-repeat: no-repeat;\n"
                                       "background-position: center center;\n"
                                       "background-attachment: fixed;")
        self.back_center.setText("")
        self.back_center.setPixmap(QtGui.QPixmap("images/bg_center.png"))
        self.back_center.setObjectName("back_center")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(300, 10, 661, 91))
        self.textBrowser.setStyleSheet("   font-family: \"华文琥珀\";\n"
                                       " \n"
                                       "  \n"
                                       "color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255));\n"
                                       "background-color:rgba(255,255,255,0)")
        self.textBrowser.setObjectName("textBrowser")

        self.btn_caidan_youshangjiao = QtWidgets.QPushButton(self.centralwidget)
        self.btn_caidan_youshangjiao.setGeometry(QtCore.QRect(1280, 10, 21, 61))
        self.btn_caidan_youshangjiao.setText("")
        self.btn_caidan_youshangjiao.setObjectName("btn_caidan_youshangjiao")
        self.back_all.raise_()
        self.back_top.raise_()
        self.back_center.raise_()
        self.back_left.raise_()
        self.menu_tab.raise_()
        self.back_right.raise_()
        self.textBrowser.raise_()
        self.btn_caidan_youshangjiao.raise_()

        MainWIndow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWIndow)
        self.statusbar.setMaximumSize(QtCore.QSize(1160, 0))
        self.statusbar.setObjectName("statusbar")
        MainWIndow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWIndow)
        self.menu_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWIndow)

    def update_doc_tips(self):
        # 将更改后的配置写回到配置文件中
        try:
            with open(doc_tips, "w", encoding='utf-8') as f:
                for key, value in self.dict_tips.items():
                    f.write(f"{key} = {repr(value)}\n")
            with open('tips.py', 'w', encoding="utf-8") as f1, open(doc_tips, 'r', encoding="utf-8") as f2:

                for line in f2:
                    f1.write(line)
        except Exception as e:
            rai_dia(e)
    def update_doc_cfgs(self):
        try:
            with open(doc_cfg, "w", encoding='utf-8') as f:
                json.dump(self.dict_cfgs, f)
        except Exception as e:
            rai_dia(e)
        # with open('cmdpriv.json', 'w', encoding="utf-8") as f1, open(doc_cmds, 'r', encoding="utf-8") as f2:
        #     for line in f2:
        #         f1.write(line)
        # 将更改后的配置写回到配置文件中
        # with open(doc_cfg, "w", encoding='utf-8') as f:
        #     for key, value in self.dict_cfgs.items():
        #         f.write(f"{key} = {repr(value)}\n")
        # with open('config.py', 'w', encoding="utf-8") as f1, open(doc_cfg, 'r', encoding="utf-8") as f2:
        #      f1.write("import logging\n")
        #      for line in f2:
        #         f1.write(line)
        #      f1.write("logging_level = logging.INFO")
    def update_doc_cmds(self):
        # 将更改后的配置写回到配置文件中
        try:
            with open(doc_cmds, "w", encoding='utf-8') as f:
                json.dump(self.dict_cmds, f)
        except Exception as e:
            rai_dia(e)
        # with open('cmdpriv.json', 'w', encoding="utf-8") as f1, open(doc_cmds, 'r', encoding="utf-8") as f2:
        #     for line in f2:
        #         f1.write(line)
    def retranslateUi(self, MainWIndow):
        _translate = QtCore.QCoreApplication.translate
        MainWIndow.setWindowTitle(_translate("MainWIndow", "QChatGPT beta 1.0"))
        self.page_log_label_time.setText(_translate("MainWIndow", "时间"))
        self.page_log_label_jiluqi.setText(_translate("MainWIndow", "记录器"))
        self.page_log_label_level.setText(_translate("MainWIndow", "级别"))
        self.page_log_label_message.setText(_translate("MainWIndow", "信息"))
        self.page_log_btn_open_log_path.setText(_translate("MainWIndow", "打开日志目录"))
        self.page_log_btn_switch_unicode.setText(_translate("MainWIndow", "编码"))
        self.page_log_btn_cmd_send.setText(_translate("MainWIndow", "发送"))
        self.page_set_title_api_proxy.setText(_translate("MainWIndow", "API代理："))
        self.page_set_title_api.setText(_translate("MainWIndow", "API设置："))
        self.page_set_title_main.setText(_translate("MainWIndow", "基本设置:"))
        self.label_122.setText(_translate("MainWIndow", "响应参数："))
        self.page_set_title_response.setText(_translate("MainWIndow", "人格设置："))
        self.page_set_title_pipeiguize.setText(_translate("MainWIndow", "匹配规则："))
        self.page_set_btn_cfg_open_path_full_scenario.setText(_translate("MainWIndow", "打开情景预设目录"))
        self.page_set_title_moxingshezhi.setText(_translate("MainWIndow", "模型设置："))
        self.page_set_title_huihuashezhi.setText(_translate("MainWIndow", "会话设置："))
        self.page_set_title_kaifazheshezhi.setText(_translate("MainWIndow", "开发者设置："))
        self.page_set_title_zhilingquanxian.setText(_translate("MainWIndow", "指令权限："))
        self.page_set_title_xiaoxitishiyu.setText(_translate("MainWIndow", "消息提示语："))
        self.page_set_edit_cfg_response_at.setText(_translate("MainWIndow", "响应“at”消息"))
        self.page_set_label_cfg_user_pool_num.setText(_translate("MainWIndow", "执行用户请求和指令的并行线程数量："))
        self.page_set_label_cfg_admin_pool_num.setText(_translate("MainWIndow", "执行管理员请求和指令并行线程数量："))
        self.page_set_label_cfg_font_path.setText(_translate("MainWIndow", "文字转图片时使用的字体文件路径："))
        self.page_set_btn_save.setText(_translate("MainWIndow", "保存设置"))
        self.page_set_label_cfg_default_prompt.setText(_translate("MainWIndow", "普通模式人格："))
        self.page_set_label_cfg_inappropriate_message_tips.setText(_translate("MainWIndow", "不合规消息自定义返回："))
        self.page_set_label_cfg_prompt_submit_length.setText(_translate("MainWIndow", "发送对话记录上下文的字符数："))
        self.page_set_label_cfg_random_rate.setText(_translate("MainWIndow", "随机响应概率:"))
        self.page_set_label_cfg_api.setText(_translate("MainWIndow", "API_KEY："))
        self.page_set_label_cfg_blob_message_threshold.setText(_translate("MainWIndow", "应用长消息处理策略的阈值："))
        self.page_set_edit_cfg_baidu_check.setText(_translate("MainWIndow", "启用百度云内容安全审核"))
        self.page_set_label_cfg_baidu_secret_key.setText(_translate("MainWIndow", "百度云SECRET_KEY："))
        self.page_set_edit_cfg_income_msg_check.setText(_translate("MainWIndow", "检查收到的消息中是否包含敏感词"))
        self.page_set_label_cfg_rate_limitation_danwei.setText(_translate("MainWIndow", "次"))
        self.page_set_edit_cfg_sensitive_word_filter.setText(_translate("MainWIndow", "以同样数量的*代替敏感词回复"))
        self.page_set_label_cfg_rate_limit_strategy.setText(_translate("MainWIndow", "会话限速策略："))
        self.page_set_label_cfg_session_expire_time.setText(_translate("MainWIndow", "每个会话的过期时间："))
        self.page_set_label_cfg_blob_message_strategy.setText(_translate("MainWIndow", "长消息处理策略："))
        self.page_set_label_cfg_rate_limitation.setText(_translate("MainWIndow", "会话限速：每分钟"))
        self.page_set_label_cfg_session_expire_time_danwei.setText(_translate("MainWIndow", "秒"))
        self.page_set_label_cfg_image_size.setText(_translate("MainWIndow", "图片尺寸："))
        self.page_set_edit_cfg_quote_origin.setText(_translate("MainWIndow", "群内回复消息时引用原消息"))
        self.page_set_label_cfg_include_image_description.setText(_translate("MainWIndow", "回复绘图时包含图片描述"))
        self.page_set_label_cfg_sys_pool_num.setText(_translate("MainWIndow", "程序运行本身线程池："))
        self.page_set_edit_cfg_qiyongduoduixiangmingcheng.setText(_translate("MainWIndow", "群内会话启用多对象名称(暂未实现)"))
        self.page_set_label_cfg_process_message_timeout_danwei.setText(_translate("MainWIndow", "秒"))
        self.page_set_label_cfg_retry_times.setText(_translate("MainWIndow", "消息处理超时重试次数："))
        self.page_set_edit_cfg_show_prefix.setText(_translate("MainWIndow", "回复消息时显示[GPT]前缀"))
        self.page_set_label_cfg_process_message_timeout_left.setText(_translate("MainWIndow", "消息处理的超时时间:"))
        self.page_set_label_cfg_ignore_prefix.setText(_translate("MainWIndow", "忽略前缀："))
        self.page_set_label_cfg_ignore_regexp.setText(_translate("MainWIndow", "忽略正则表达式："))
        self.page_set_label_cfg_api_model.setText(_translate("MainWIndow", "模型："))
        self.page_set_label_cfg_api_frequency_penalty.setText(_translate("MainWIndow", "frequency_penalty："))
        self.page_set_label_cfg_api_presence_penalty.setText(_translate("MainWIndow", "presence_penalty："))
        self.page_set_label_cfg_api_top_p.setText(_translate("MainWIndow", "生成的文本的文本与要求的符合度："))
        self.page_set_label_cfg_api_temperature.setText(_translate("MainWIndow", "理性："))
        self.page_set_label_cfg_mirai_qq.setText(_translate("MainWIndow", "机器人QQ："))
        self.page_set_label_cfg_admin_qq.setText(_translate("MainWIndow", "管理员QQ："))
        self.page_set_label_cfg_mirai_verifyKey.setText(_translate("MainWIndow", "verifyKey："))
        self.page_set_label_cfg_mirai_host.setText(_translate("MainWIndow", "主机地址："))
        self.page_set_label_cfg_mirai_port.setText(_translate("MainWIndow", "端口："))
        self.page_set_label_cfg_mirai_adapter.setText(_translate("MainWIndow", "接入方式："))
        self.page_set_label_cfg_api_reverse_proxy.setText(_translate("MainWIndow", "reverse:"))
        self.page_set_label_cfg_api_http_proxy.setText(_translate("MainWIndow", "http:"))
        self.page_set_label_cfg_preset_mode.setText(_translate("MainWIndow", "人格模式："))
        self.page_set_label_cfg_response_prefix.setText(_translate("MainWIndow", "响应前缀："))
        self.page_set_label_cfg_response_regexp.setText(_translate("MainWIndow", "响应正则表达式："))
        self.page_set_label_cfg_baidu_api_key.setText(_translate("MainWIndow", "百度云API_KEY："))
        self.page_set_edit_cfg_encourage_sponsor_at_start.setText(_translate("MainWIndow", "启动时发送赞赏码"))
        self.page_set_edit_cfg_hide_exce_info_to_user.setText(_translate("MainWIndow", "消息处理出错时向用户隐藏错误详细信息"))
        self.page_set_edit_cfg_upgrade_dependencies.setText(_translate("MainWIndow", "启动时进行依赖库更新"))
        self.page_set_edit_cfg_report_usage.setText(_translate("MainWIndow", "上报统计信息"))
        self.page_set_label_cfg_logging_level.setText(_translate("MainWIndow", "日志级别："))
        self.page_set_label_cmd_plugin_off.setText(_translate("MainWIndow", "plugin.off"))
        self.page_set_label_cmd_plugin.setText(_translate("MainWIndow", "plugin"))
        self.page_set_label_cmd_plugin_get.setText(_translate("MainWIndow", "plugin.get"))
        self.page_set_label_cmd_plugin_update.setText(_translate("MainWIndow", "plugin.update"))
        self.page_set_label_cmd_plugin_del.setText(_translate("MainWIndow", "plugin.del"))
        self.page_set_label_cmd_plugin_on.setText(_translate("MainWIndow", "plugin.on"))
        self.page_set_label_cmd_list.setText(_translate("MainWIndow", "list"))
        self.page_set_label_cmd_next.setText(_translate("MainWIndow", "next"))
        self.page_set_label_cmd_resend.setText(_translate("MainWIndow", "resend"))
        self.page_set_label_cmd_help.setText(_translate("MainWIndow", "help"))
        self.page_set_label_cmd_update.setText(_translate("MainWIndow", "update"))
        self.page_set_label_cmd_version.setText(_translate("MainWIndow", "version"))
        self.page_set_label_tips_command_reset_name_message.setText(_translate("MainWIndow", "修改预设成功提示："))
        self.page_set_label_tips_alter_tip_message.setText(_translate("MainWIndow", "出错提示："))
        self.page_set_label_tips_rate_limit_drop_tip.setText(_translate("MainWIndow", "对话丢弃的提示信息："))
        self.page_set_label_tips_help_message.setText(_translate("MainWIndow", "指令！help帮助信息："))
        self.page_set_label_tips_reply_message.setText(_translate("MainWIndow", "私聊消息超时提示："))
        self.page_set_label_tips_replys_message.setText(_translate("MainWIndow", "群聊消息超时提示："))
        self.page_set_label_tips_command_admin_message.setText(_translate("MainWIndow", "指令权限不足提示："))
        self.page_set_label_tips_command_err_message.setText(_translate("MainWIndow", "指令无效提示提示："))
        self.page_set_label_tips_command_reset_message.setText(_translate("MainWIndow", "会话重置提示："))
        self.page_set_label_cmd_draw.setText(_translate("MainWIndow", "draw"))
        self.page_set_label_cmd_default.setText(_translate("MainWIndow", "default"))
        self.page_set_label_cmd_default_set.setText(_translate("MainWIndow", "default.set"))
        self.page_set_label_cmd_del.setText(_translate("MainWIndow", "del"))
        self.page_set_label_cmd_del_all.setText(_translate("MainWIndow", "del.all"))
        self.page_set_label_cmd_delhst.setText(_translate("MainWIndow", "delhst"))
        self.page_set_label_cmd_delhs_tall.setText(_translate("MainWIndow", "delhst.all"))
        self.page_set_label_cmd_last.setText(_translate("MainWIndow", "last"))
        self.page_set_label_cmd_prompt.setText(_translate("MainWIndow", "prompt"))
        self.page_set_label_cmd_reset.setText(_translate("MainWIndow", "reset"))
        self.page_set_label_cmd_reload.setText(_translate("MainWIndow", "reload"))
        self.page_set_label_cmd_usage.setText(_translate("MainWIndow", "usage"))
        self.page_set_label_cmd_cfg.setText(_translate("MainWIndow", "cfg"))
        self.page_set_label_cmd_cmd.setText(_translate("MainWIndow", "cmd"))
        self.page_about_text.setHtml(_translate("MainWIndow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">[关于页面]项目仓库：</span><img src=\"file:///C:\\Users\\26751\\AppData\\Roaming\\Tencent\\QQTempSys\\[5UQ[BL(6~BS2JV6W}N6[%S.png\" /><span style=\" font-size:16pt;\">https://github.com/2675hujilo/QChatGPT-win.git</span></p></body></html>"))
        self.textBrowser.setHtml(_translate("MainWIndow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'华文琥珀\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:131073;\"><span style=\" font-size:36pt; color:#00ff7f;\">欢</span><span style=\" font-size:36pt; color:#aaffff;\">迎</span><span style=\" font-size:36pt; color:#ff5500;\">使</span><span style=\" font-size:36pt; color:#5555ff;\">用</span><span style=\" font-size:36pt; color:#00ff00;\">Q</span><span style=\" font-size:36pt; color:#55ffff;\">C</span><span style=\" font-size:36pt; color:#0055ff;\">h</span><span style=\" font-size:36pt; color:#ff00ff;\">a</span><span style=\" font-size:36pt; color:#5500ff;\">t</span><span style=\" font-size:36pt; color:#00aa00;\">G</span><span style=\" font-size:36pt; color:#55ffff;\">P</span><span style=\" font-size:36pt; color:#5500ff;\">T</span><span style=\" font-size:36pt; color:#55ffff;\"> </span></p></body></html>"))


def rai_dia(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(str(message))
    msg_box.exec_()


if __name__ == "__main__":
    if "--debug" in sys.argv:
        # 设置Qt属性
        from PyQt5.QtCore import QCoreApplication, Qt

        QCoreApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

    app = QApplication(sys.argv)
    app.setFont(QFont("微软雅黑",10))
    try:
        window = MainWindow()
        window.show()

        if "--debug" in sys.argv:
            print("using debug mode")
            app.processEvents(QEventLoop.AllEvents)  # 等待窗口事件
            window.setAttribute(Qt.WA_TranslucentBackground)  # 使窗口背景透明
            app.exec_()

            # 输出窗口事件
            # for event in app.allWidgets():
            #     print(event.objectName(), event.metaObject().className())
            #     for child in event.children():
            #         print(" ", child.objectName(), child.metaObject().className())
            #         for grandchild in child.children():
            #             print("   ", grandchild.objectName(), grandchild.metaObject().className())
        else:
            app.exec_()

    except Exception as e:
        raise e
