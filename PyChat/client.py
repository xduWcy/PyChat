import ctypes
import re
import socket
import time
from threading import Thread

from PyQt5.QtGui import QTextCursor, QColor
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from login_Uidesign import Ui_Dialog_login
from register_Uidesign import Ui_Dialog_register
from main_window import Ui_MainWindow

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class Client:
    """创建客户端的模板类"""
    def __init__(self):
        print("初始化tcp多人聊天室客户端")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client_socket.connect(('192.168.31.142', 7890))
        self.client_socket.connect(('127.0.0.1', 7890))

    def send_login_info(self, username, password):
        """
        发送登录用户的用户名和密码给服务器验证，并return验证结果
        :param username: 待验证的用户名
        :param password: 待验证的密码
        :return: 验证结果
        """
        # 告诉服务器本次请求的类型，“1” 是验证登录
        self.client_socket.sendall("1".encode("utf-8"))

        # 将用户名和密码按照一定规律组合后一起发送给服务器
        username_psw = username + ">>>>" + password
        self.client_socket.sendall(username_psw.encode("utf-8"))

        # 获取服务器的返回值，"1"代表通过，“0”代表不通过，再放回True or False
        check_result = self.client_socket.recv(1024).decode("utf-8")
        return check_result

    def send_register_info(self, username, password):
        """
        发送用户注册的用户名和密码给服务器，并返回注册结果
        :param username: 待注册的用户名
        :param password: 待注册的密码
        :return: 注册结果
        """
        # 判断两次输入的密码是否一致
        #if not password == confirm:
            #return "密码不一致，请重新输入！"
        # 告诉服务器本次请求类型，“2” 是注册用户
        self.client_socket.sendall("2".encode("utf-8"))

        # 将用户名和密码按一定规律组装后发送给服务器
        username_psw = username + ">>>>" + password
        self.client_socket.sendall(username_psw.encode("utf-8"))

        # 获取服务器返回的结果
        check_result = self.client_socket.recv(1024).decode("utf-8")
        return check_result

    def send_msg(self, content):
        """
        向服务器发送数据
        :param content: 待发送的内容
        """
        # 告诉服务器本次请求类型，“3” 是发送消息
        self.client_socket.sendall("3".encode("utf-8"))
        self.client_socket.sendall(content.encode("utf-8"))

    def recv_data(self, size=1024):
        """
        客户端向服务器接收数据
        :return: 接收到的数据
        """
        return self.client_socket.recv(size).decode("utf-8")

    def close(self):
        """
        关闭客户端与服务器连接的套接字
        """
        self.client_socket.close()

class login_dialog(QDialog, Ui_Dialog_login):
    def __init__(self, parent=None):
        super(login_dialog, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

        self.pushButton.clicked.connect(self.login_func)
        self.pushButton_2.clicked.connect(self.reg_func)

    def get_input(self):
        """
        获得用户输入的账户和密码
        :return: 返回用户用户输入的账户和密码
        """
        return self.lineEdit.text(), self.lineEdit_2.text()

    def login_func(self):
        """
        封装到登陆界面中的登录按钮的功能。
        """
        username, password = self.get_input()
        client = Client()
        check_result = client.send_login_info(username, password)

        if check_result == "登陆成功":
            QMessageBox.information(self, "Success", "登陆成功！")
            self.close()

            main_panel = main_window(username, client)
            thread = Thread(target=main_panel.handle_msg)
            thread.start()
            print("线程创建成功...")
            main_panel.show()


        elif check_result == "用户名或密码错误，请重试":
            QMessageBox.warning(self, "Error", "用户名或密码错误！")

        elif check_result == "该用户尚未注册":
            QMessageBox.warning(self, "Error", "不存在该用户，请先注册！")

    def reg_func(self):
        """
        封装到登录界面的注册按钮中，实现从登录界面跳转到注册界面
        """
        self.close()
        register_window = register_dialog()
        register_window.show()
        register_window.exec_()



class register_dialog(QDialog, Ui_Dialog_register):
    def __init__(self, parent=None):
        super(register_dialog, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

        self.pushButton.clicked.connect(self.reg_func)
        self.pushButton_2.clicked.connect(self.cancel_func)

    def get_input(self):
        return self.lineEdit.text(), self.lineEdit_2.text()

    def cancel_func(self):
        """
        封装到取消按钮中
        :return:
        """
        self.close()
        login_window = login_dialog()
        login_window.show()
        login_window.exec_()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message',
    #                                  "你确定要取消注册吗?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         QApplication.quit()
    #     else:
    #         event.ignore()  # 忽略关闭事件，窗口保持打开


    def reg_func(self):
        """
        封装到注册界面的注册按钮中
        """
        username, password= self.get_input()
        client = Client()
        ret = client.send_register_info(username, password)
        print(ret)

        if ret == "用户名已经存在！":
            QMessageBox.warning(self, "Error", "用户名或密码错误！")
        elif ret == "注册成功！":
            # 注册成功后提示，然后跳回登录界面
            QMessageBox.information(self, "Success", "注册成功！")
            self.close()
            login_window = login_dialog()
            login_window.show()
            login_window.exec_()
        else:
            QMessageBox.warning(self, "Error", "发生未知错误！")


class main_window(QMainWindow, Ui_MainWindow):
    def __init__(self, username, client, parent=None):
        super(main_window, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.username = username
        self.client = client

        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.send_func)



    def handle_msg(self):
        """
        处理关于在线用户列表和消息框中内容的信息
        """
        #print("111111111111111")
        time.sleep(2)  # 暂停一下，等待主界面渲染完毕
        while True:
            try:
                # 获取数据类型：在线用户列表、消息内容
                recv_data = self.client.recv_data()
                if recv_data:
                    ret = re.match(r"(#![\w]{7}#!)([\s\S]+)", recv_data)
                    option = ret.group(1)
                    print("recieved type: " + option)
                    print(recv_data)
                    if option == "#!onlines#!":
                        print("获取在线用户列表数据")
                        # 将一次性获取得到的用户名以 “#!”为标记分隔成一个列表
                        online_usernames = ret.group(2).split("#!")
                        online_usernames.remove("")  # 去除列表中的空字符串
                        print(online_usernames)
                        self.update_online_list(online_usernames)
                        print(online_usernames)
                    elif option == "#!message#!":  # 正则区分用户名和消息内容
                        print("获取新消息")
                        username_content = ret.group(2)
                        ret = re.match(r"(.*)#!([\s\S]*)", username_content)
                        username = ret.group(1)
                        content = ret.group(2)
                        self.set_msg_show_format(username, content)
                    elif option == "#!notices#!":
                        print("获取用户上下线通知")
                        notice = ret.group(2)  # 将通知提取出来
                        self.show_notice(notice)
            except Exception as ret:
                print("接受服务器消息出错，消息接受子线程结束。" + str(ret))
                break

    def update_online_list(self, online_usernames):
        """刷新在线列表 -- 一遍又一遍地清空，再回填到列表中"""
        print("正在更新列表...")
        self.listWidget.clear()  # 全部清空
        print("**********")
        for username in online_usernames:
            self.listWidget.addItem(username)

    def show_notice(self, notice):
        self.textEdit.append(notice)


    def set_msg_show_format(self, username, content):
        title = f"{username} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
        message = title + content + "\n"

        self.textEdit.append(message)

        # 确保文本框的视图滚动到末尾
        scrollbar = self.textEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        # title = username + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        # self.textEdit.append(title)
        # 根据发送者是否是当前用户来决定标题的颜色


    def send_func(self):
        # 在这里实现发送消息的逻辑
        message = self.textEdit_2.toPlainText()
        # 假设将消息发送到client的某个方法（这里需要您自己实现）
        # self.client.send_message(message)

        self.client.send_msg(message)
        # 清空输入框
        self.textEdit_2.clear()
        # 在消息框中显示发送的消息（这里只是模拟，实际可能需要格式化）
        #self.msg_box.append(f"{self.username}: {message}")

    # def clear_input_box(self):
    #     # 清空输入框
    #     self.textEdit_2.clear()

    # def get_input_box_content(self):
    #     return self.textEdit_2.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = login_dialog()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序





