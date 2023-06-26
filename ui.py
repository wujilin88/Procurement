import sys,json,time,crawler, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置主界面标题
        self.setWindowTitle("浙江政府采购网爬取")
        # 设置固定尺寸
        self.width = 380
        self.height = 450
        self.setFixedSize(self.width, self.height)
        self.webui()
        pass

    def webui(self):
        self.pathLab = QLabel(self)
        self.pathLab.setText("*文件保存路径")
        self.pathLab.move(5,0)
        self.pathEdit = QLineEdit(self)
        # self.pathEdit.setEnabled(False)
        self.pathEdit.move(90,5)
        self.pathEdit.resize(180,20)
        self.filePathButton = QPushButton("请选择路径",self)
        self.filePathButton.move(280,3)
        self.filePathButton.resize(70,25)
        self.filePathButton.clicked.connect(self.clickbut)


        # 设置软件图标（可省略）
        # self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.pathdate = QLabel(self)
        self.pathdate.setText("发布时间：")
        self.pathdate.move(5,35)
        self.dateEditleft = QDateEdit(QDate.currentDate(), self)
        self.dateEditleft.setDisplayFormat("yyyy-MM-dd")
        self.dateEditleft.move(60,35)
        self.dateEditleft.setCalendarPopup(True)
        self.dateEditright = QDateEdit(QDate.currentDate(), self)
        self.dateEditright.setDisplayFormat("yyyy-MM-dd")
        self.dateEditright.move(185,35)
        self.dateEditright.setCalendarPopup(True)
        self.pathstartbtn = QPushButton("开始爬取",self)
        self.pathstartbtn.resize(70,25)
        self.pathstartbtn.move(290,40)
        self.pathstartbtn.clicked.connect(self.startpath)
        self.lable1 = QLabel(self)
        self.lable1.setText("-")
        self.lable1.move(170,35)

        pass


    def startpath(self):
        pass


    def clickbut(self):
        path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if path == '':
            return
        times = round(time.time() * 1000)
        fileName = '浙江政府采购网_数据爬取结果_' + str(times) + '.xls'
        self.pathEdit.setText(path + '/' + fileName)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindows()
    w.show()
    sys.exit(app.exec_())