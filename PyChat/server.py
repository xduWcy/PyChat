import re
import socket
import hashlib
import logging
from threading import Thread
import  time



online_sockets = list()   # 套接字列表
sockets_users = dict()    # 套接字到用户名的映射字典

def encryption(input_string):
    """
    对用户账户的密码进行加密
    :param input_string:等待加密的密码字符串
    :return:加密后的密码字符串
    """
    #创建一个MD5 hash对象
    md5_hash = hashlib.md5()
    #更新哈希对象的内容
    md5_hash.update(input_string.encode('utf-8'))
    #获取十六进制的哈希值
    md5_result = md5_hash.hexdigest()
    return md5_result

def register_user(new_socket, username, password):
    """
    接受用户端传来的注册信息，并保存在本地
    :param new_socket: 与客户端通信的套接字
    :param username:用户注册的账户名称
    :param password:加密后的密码
    :return:
    """
    try:
        print("register>>>Username:" + username + "Key:" + password )

        # 读取存放于本地文件中的用户数据
        with open("./users.txt","r") as users_file:
            users_data = users_file.read()
        users_list = users_data.split("\n")

        #查询列表里是否存在已经存在的相同的用户名
        for user in users_list:
            if user == username:   #当用户名已经存在
                new_socket.sendall("用户名已经存在！".encode("utf-8"))
                return

        #将用户信息加入到TXT中
        with open("./users.txt", "a") as users_file:
            users_file.write(username + "\n" + password + "\n")
        new_socket.sendall("注册成功！".encode("utf-8"))

    except Exception as ret:
        print("添加用户数据出错：" + str(ret))
        new_socket.sendall("发生未知错误！".encode("utf-8"))

def login(user_name, pasword):
    print("检测账户密码是否正确")
    with open("./users.txt", "r") as user_file:
        user_data = user_file.read()
    users_list = user_data.split()

    for user in users_list:
        if user == user_name:
            index = users_list.index(user) + 1
            if users_list[index] == pasword:
                return "登陆成功"
            else:
                return "用户名或密码错误，请重试"

    return "该用户尚未注册"

def online_list():
    """
    发送在线用户名称
    :return:
    """
    # 组装所有在线用户名为一个字符串
    online_usernames = ""
    for sk in online_sockets:
        online_usernames += sockets_users[sk] + "#!"
    # 向所有在线用户发送在线列表用户名
    for socket in online_sockets:
        # 发送标识和在线用户列表用户名，前者为区分信息和在线用户列表
        socket.sendall(("#!onlines#!" + online_usernames).encode("utf-8"))

def online_notice(new_socket):
    """
    给所有在线客户端发送新客户端上线的通知
    :param new_socket: 新上线客户端的套接字
    """
    welcome_str = "******** Welcome "\
                  + sockets_users[new_socket] + \
                  " come to PyChat! ********"
    # 向所有在线用户发送新用户上线通知，#!notices#! 标志此类消息
    for socket in online_sockets:
        socket.sendall(("#!notices#!" + welcome_str).encode("utf-8"))


def offline_notice(offline_socket):
    """
    给所有在线用户发送用户离线通知
    :param offline_socket: 离线用户对应的套接字
    """
    left_str = "******** "\
               + sockets_users[offline_socket] + \
               " has left ********"
    for socket in online_sockets:
        socket.sendall(("#!notices#!" + left_str).encode("utf-8"))


def handle_reg(new_socket):
    """
    处理客户端的注册请求，接收客户端注册的用户信息，
    调用函数将用户名和加密后的密码存入本地文本
    :param new_socket: 本次连接过来的客户端套接字
    """
    username_psw = new_socket.recv(1024).decode("utf-8")
    # 组装后的用户格式为 username#!#!password
    ret = re.match(r"(.+)>>>>(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    encrypted_psw = encryption(password)
    register_user(new_socket, username, encrypted_psw)

def handle_login(new_socket):
    """
    处理登录请求
    :param new_socket: 用户连接时生成的套接字
    """
    username_psw = new_socket.recv(1024).decode("utf-8")
    # 组装后的用户信息格式为 username#!#!password
    ret = re.match(r"(.+)>>>>(.+)", username_psw)
    username = ret.group(1)
    password = ret.group(2)
    encrypted_psw = encryption(password)
    check_result = login(username, encrypted_psw)
    new_socket.sendall(check_result.encode("utf-8"))  # 将登陆结果发送给客户端

    # 只有登陆成功之后，才执行以下操作
    if check_result == "登陆成功":
        # 将对应的socket与用户名对应起来，并添加到字典中
        sockets_users[new_socket] = username
        # 将连接的socket添加到在线列表中
        online_sockets.append(new_socket)
        print(online_sockets)
        online_list()
        time.sleep(8)
        online_notice(new_socket)


def handle_msg(new_socket):
    """
    基于假设：发送的消息类型的内容总和不会超过1024Byte
    对客户端要发送的内容进行广播
    :param new_socket: 要发送信息的客户端的套接字
    """
    content = new_socket.recv(1024).decode("utf-8")
    # 发送给所有在线客户端
    for socket in online_sockets:
        socket.sendall(("#!message#!"\
                        + sockets_users[new_socket] + "#!"\
                        +content).encode("utf-8"))


def handle(new_socket, addr):
    """
    服务器运行的主框架
    :param new_socket: 本次连接的客户端套接字
    :param addr: 本次连接客户端的ip和port
    """
    try:
        while True:
            req_type = new_socket.recv(1).decode("utf-8")  # 获取请求类型
            print(req_type)
            if req_type:  # 如果不为真，则说明客户端已断开
                if req_type == "1":  # 登录请求
                    print("开始处理登录请求")
                    handle_login(new_socket)
                elif req_type == "2":  # 注册请求
                    print("开始处理注册请求")
                    handle_reg(new_socket)
                elif req_type == "3":  # 发送消息
                    print("开始处理发送消息请求")
                    handle_msg(new_socket)
            else:
                break
    except Exception as ret:
        print(str(addr) + " 连接异常，准备断开: " + str(ret))
    finally:
        try:
            # 客户端断开后执行的操作
            new_socket.close()
            online_sockets.remove(new_socket)
            offline_notice(new_socket)
            sockets_users.pop(new_socket)
            time.sleep(4)
            online_list()
        except Exception as ret:
            print(str(addr) + "连接关闭异常")



if __name__ == "__main__":
    try:
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #创建TCP套接字
        main_socket.bind(("127.0.0.1", 7890))  # 服务器绑定的ip和port，绑定本地信息
        main_socket.listen(128)  # 最大挂起数
        print("服务器启动成功，开始监听...")
        while True:
            new_socket, addr = main_socket.accept()
            Thread(target=handle, args=(new_socket, addr)).start()
    except Exception as ret:
        print("服务器出错: " + str(ret))
