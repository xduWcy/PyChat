import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QListWidget, \
    QTextEdit, QScrollBar, QPushButton
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt



class MainPanel(QMainWindow):
    def __init__(self, username, client):
        super().__init__()
        self.client = client
        self.username = username
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("MyChat: " + self.username)
        self.setGeometry(100, 100, 800, 500)

        # 创建中央窗口部件和布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 设置用户名标签
        username_label = QLabel("MyChat: " + self.username, self)
        font = QFont("Microsoft YaHei", 13)
        username_label.setFont(font)
        main_layout.addWidget(username_label)

        # 创建水平布局用于分隔在线列表和消息/输入区域
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        # 设置在线用户列表
        self.online_list_box = QListWidget(self)
        h_layout.addWidget(self.online_list_box)

        # 设置消息和输入区域的垂直布局
        v_layout = QVBoxLayout()
        h_layout.addLayout(v_layout)

        # 设置消息框
        self.msg_box = QTextEdit(self)
        self.msg_box.setReadOnly(True)
        self.msg_box.setFont(QFont("Microsoft YaHei", 12))

        self.msg_box.setTextColor(QColor("black"))
        v_layout.addWidget(self.msg_box)

        # 设置输入框和滚动条（虽然QTextEdit自带滚动条，但这里为了模拟您的Tkinter代码结构）
        input_box_container = QWidget(self)
        input_box_layout = QVBoxLayout(input_box_container)

        self.input_box = QTextEdit(self)
        self.input_box.setFont(QFont("Microsoft YaHei", 12))
        input_box_layout.addWidget(self.input_box)

        # 实际上QTextEdit自带垂直滚动条，这里不需要额外添加
        # 但为了模拟，我们仍然创建一个QScrollBar对象（虽然它不会被使用）
        # send_sr_bar = QScrollBar(Qt.Vertical, self)
        # input_box_layout.addWidget(send_sr_bar)

        v_layout.addWidget(input_box_container)

        # 设置发送和清空按钮
        btn_layout = QHBoxLayout()
        v_layout.addLayout(btn_layout)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_func)
        btn_layout.addWidget(self.send_button)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_input_box)
        btn_layout.addWidget(self.clear_button)

        # 设置窗口位置和大小（这里使用固定大小，但您可以添加代码来根据屏幕大小调整）
        # self.setGeometry(100, 100, 800, 500)

    def send_func(self):
        # 在这里实现发送消息的逻辑
        message = self.input_box.toPlainText()
        # 假设将消息发送到client的某个方法（这里需要您自己实现）
        # self.client.send_message(message)
        # 清空输入框
        self.input_box.clear()
        # 在消息框中显示发送的消息（这里只是模拟，实际可能需要格式化）
        self.msg_box.append(f"{self.username}: {message}")

    def clear_input_box(self):
        # 清空输入框
        self.input_box.clear()

        # 注意：这里没有直接等效于Tkinter的mainloop()的方法，因为PyQt5的事件循环是由QApplication管理的


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 假设client是一个已经实现的对象，这里需要您自己提供
    # client = YourClientClass()

    client = None  # 仅作为示例，实际应传递有效对象
    username = "example_user"
    main_panel = MainPanel(username, client)
    main_panel.show()
    sys.exit(app.exec_())