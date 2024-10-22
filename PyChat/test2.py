import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget


class ChatWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.msg_box = QTextEdit(self)
        self.msg_box.setReadOnly(True)  # 设置文本框为只读

        layout = QVBoxLayout()
        layout.addWidget(self.msg_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def set_msg_show_format(self, username, content):
        # 构建消息标题，包括用户名和时间戳
        title = f"{username} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
        message = title + content + "\n"

        # 直接追加到文本框中
        self.msg_box.append(message)

        # 确保文本框的视图滚动到末尾
        scrollbar = self.msg_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # 示例使用


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow("CurrentUser")
    window.setWindowTitle("Chat Window")
    window.resize(400, 300)
    window.show()

    # 模拟接收消息
    window.set_msg_show_format("CurrentUser", "Hello, this is a test message from myself!")
    window.set_msg_show_format("OtherUser", "Hello, this is a test message from someone else.")

    sys.exit(app.exec_())