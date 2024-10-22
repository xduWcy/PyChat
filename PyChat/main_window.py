# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 591)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/chat.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color:rgb(0, 0, 0)")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(0, 0, 0);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_2.addWidget(self.textEdit_2, 0, QtCore.Qt.AlignBottom)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(1920, 1080))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/send.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton, 0, QtCore.Qt.AlignRight)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyChat"))
        self.pushButton.setText(_translate("MainWindow", "发送"))
import resource_rc
