import sys, json, time, crawler, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from interface import start


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置主界面标题
        self.setWindowTitle("浙江政府采购网爬取")
        # 设置固定尺寸
        self.width = 380
        self.height = 450
        self.setFixedSize(self.width, self.height)
        self.initUi()
        pass

    def initUi(self):
        _ICON_PATH = 'D:\pyObject\Procurement\serch.ico'
        icon = QIcon()
        icon.addPixmap(QPixmap(_ICON_PATH), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.pathLab = QLabel(self)
        self.pathLab.setText("*文件保存路径:")
        self.pathLab.move(5, 5)

        self.pathEdit = QLineEdit(self)
        self.pathEdit.move(110, 10)
        self.pathEdit.resize(170, 20)

        self.filePathButton = QPushButton("选择路径", self)
        self.filePathButton.move(290, 8)
        self.filePathButton.resize(80, 25)
        self.filePathButton.clicked.connect(self.clickBut)

        self.pathDate = QLabel(self)
        self.pathDate.setText("发布时间：")
        self.pathDate.move(5, 40)

        self.dateEditleft = QDateEdit(QDate.currentDate(), self)
        self.dateEditleft.setDisplayFormat("yyyy-MM-dd")
        self.dateEditleft.resize(130, 25)
        self.dateEditleft.move(70, 40)
        self.dateEditleft.setCalendarPopup(True)

        self.dateEditright = QDateEdit(QDate.currentDate(), self)
        self.dateEditright.setDisplayFormat("yyyy-MM-dd")
        # self.dateEditright.dateChanged.connect(self.onDateChanged)
        self.dateEditright.resize(130, 25)
        self.dateEditright.move(230, 40)
        self.dateEditright.setCalendarPopup(True)

        self.lable1 = QLabel(self)
        self.lable1.setText("-")
        self.lable1.resize(10, 10)
        self.lable1.move(215, 50)

        self.page = QLabel(self)
        self.page.setText("页面范围：")
        self.page.move(5, 75)

        self.minPage = QLineEdit(self)
        self.minPage.resize(130, 25)
        self.minPage.move(70, 75)

        self.maxPage = QLineEdit(self)
        self.maxPage.resize(130, 25)
        self.maxPage.move(230, 75)

        self.lable2 = QLabel(self)
        self.lable2.setText("-")
        self.lable2.resize(10, 10)
        self.lable2.move(215, 85)

        # 展示区域
        self.textShow = QPlainTextEdit(self)
        self.textShow.setReadOnly(True)
        self.textShow.resize(360, 260)
        self.textShow.move(10, 120)

        self.pathStartbtn = QPushButton("开始爬取", self)
        self.pathStartbtn.resize(80, 26)
        self.pathStartbtn.move(300, 400)
        self.pathStartbtn.clicked.connect(self.startPath)
        pass

    def clickBut(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if path == '':
            return
        times = round(time.time() * 1000)
        fileName = '浙江政府采购网中标（成交）结果公告_' + str(times) + '.xls'
        self.pathEdit.setText(path + '/' + fileName)
        pass

    # 开始爬取按钮触发内容
    def startPath(self):
        path = self.pathEdit.text()
        mindate = self.dateEditleft.text()
        maxdate = self.dateEditright.text()
        minpage = self.minPage.text()
        maxpage = self.maxPage.text()
        # 路径非空判断
        if path == '':
            msg_box = QMessageBox(QMessageBox.Question, '【警告】', '请选择正确的路径！！！')
            msg_box.exec_()
        elif mindate > maxdate:
            msg_box = QMessageBox(QMessageBox.Question, '【警告】', '最小发布时间不能大于最大发布时间！！！')
            msg_box.exec_()
        elif minpage > maxpage:
            msg_box = QMessageBox(QMessageBox.Question, '【警告】', '最小爬取页不能大于最大爬取页！！！')
            msg_box.exec_()
        else:
            print(path, mindate, maxdate, minpage, maxpage)
            try:
                start(path, mindate, maxdate, int(minpage), int(maxpage))
            except BaseException as e:
                # print(e.args)
                msg_box = QMessageBox(QMessageBox.Question, '【警告】', str(e.args))
                msg_box.exec_()

            self.shoInf("文件爬取成功，保存路径为：" + str(path))
            pass

    def shoInf(self, strInfo: str):
        self.textShow.appendPlainText(strInfo)


# 程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 调用窗体方法
    w = MainWindows()
    w.show()
    sys.exit(app.exec_())
