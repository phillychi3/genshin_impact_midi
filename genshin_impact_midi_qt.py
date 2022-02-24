# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\genshin.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import threading
from time import time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets  import QFileDialog

idk = {"48":"z","49":"z","50":"x","51":"x","52":"c","53":"v","54":"v","55":"b","56":"b","57":"n","58":"n","59":"m","60":"a","61":"a","62":"s","63":"s","64":"d","65":"f","66":"f","67":"g","68":"g","69":"h","70":"h","71":"j","72":"q","73":"q","74":"w","75":"w","76":"e","77":"r","78":"r","79":"t","80":"t","81":"y","82":"y","83":"u"}
exit_flag = False
prM=100
prm=0

class Ui_MainWindow(threading.Thread,object):
    def __init__(self):
        threading.Thread.__init__(self)
        self.file_name = ""

    def play(self):
        thread_play = play(self.file_name,self.progressBar)
        thread_play.start()

    def stop(self):
        global exit_flag
        exit_flag=True

    def openfile(self):
        self.file_namefile , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()","", "midi Files (*.mid)")
        if check:
            self.file_name = self.file_namefile
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(468, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 140, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 140, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        #self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        #self.openGLWidget.setGeometry(QtCore.QRect(30, 50, 41, 41))
        #self.openGLWidget.setObjectName("openGLWidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(100, 60, 321, 23))
        self.progressBar.setProperty("value", prm)
        self.progressBar.setMaximum(prM)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 468, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "開始"))
        self.pushButton_2.setText(_translate("MainWindow", "暫停"))
        self.pushButton_3.setText(_translate("MainWindow", "開啟檔案"))
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_3.clicked.connect(self.openfile)
        self.pushButton.clicked.connect(self.play)

class keytip(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)
        self.msg = msg
    def run(self):
        import pyautogui as pg
        try:              
                if self.msg.type == 'note_on':
                    pg.keyDown(idk[str(self.msg.note)])
                    #print(f"keydown{idk[str(self.msg.note)]}")
                elif self.msg.type == 'note_off':
                    pg.keyUp(idk[str(self.msg.note)])
                    #print(f"keyUp{idk[str(self.msg.note)]}")
        except:
                pass

class play(threading.Thread):
    def __init__(self,file_name,progressBar):
        threading.Thread.__init__(self)
        self.file_name = file_name
        self.progressBar = progressBar
    
    def run(self):
        import time,mido
        global exit_flag,prM,prm
        prm=prM=0
        time.sleep(3)
        mid = mido.MidiFile(self.file_name, clip=True)
        for i in mid:
            prM+=i.time
            self.progressBar.setMaximum(int(prM))
        for msg in mid:
                time.sleep(msg.time)
                prm+=msg.time
                self.progressBar.setValue(int(prm))
                if not msg.is_meta: 
                    thread_keytip = keytip(msg)
                    thread_keytip.start()
                if exit_flag:
                    break
        exit_flag = False

def is_admin():
    from ctypes import windll
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False   

if __name__ == "__main__":
    if is_admin():
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    else:
        print("%15s" % "沒有權限")
        print('%20s'%'*** 需要以管理員身份執行 ***')