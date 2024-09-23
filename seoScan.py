# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import webbrowser
from datetime import datetime
import time
from view import login_Ui
from seoScanMain import MainWindow
import sys
from caller import rest
from controller import ui_controller
from caller import chromeAutoUpdate
import traceback

class Login(QMainWindow, login_Ui.Ui_LoginWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        login_Ui.Ui_LoginWindow.__init__(self)
        self.setWindowIcon(QIcon('resource/trayIcon.png'))
        
        chromeAutoUpdate.update()
        
        self.setupUi(self)
                    
        ui_controller.userLoadInfo(self)
        self.checkVersion()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.loginButton.clicked.connect(self._loginCheck)
        self.minimumButton.clicked.connect(self._minimumWindow)
        self.exitButton.clicked.connect(self._closeWindow)
        self.remoteButton.clicked.connect(self.openRemote)
        


    def checkVersion(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("LoginWindow", "Login-v"+self.version))


    def openRemote(self) :
        webbrowser.open("https://agczero.com/")
        
    def _minimumWindow(self):
        self.showMinimized()

    def _closeWindow(self):
        QCoreApplication.instance().quit()

    def _loginCheck(self):
        userVersion = '1.0.0.1'
        userId = self.idEdit.text()
        userPw = self.pwEdit.text()
        cbSaveInfo = self.idpw_checkbox.isChecked()
        version = rest.getVersion()
        ui_controller.userSaveInfo(self, cbSaveInfo, userId, userPw, version)

        data = {'userId':userId,'userPw':userPw}
        # print(rest)
        try :
            if(rest.login(**data)):
                self.close()
                self.main = MainWindow()
                self.main.setWindowIcon(QIcon('resource/trayIcon.png'))
                self.main.show()
            else :
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("올바른 계정정보를 입력해주세요     ")
                msgBox.exec_()
        except Exception as e : 
            # print(e)
            traceback.print_exc()

    def keyPressEvent(self, e): 
        if e.key() in [Qt.Key_Return, Qt.Key_Enter] :
            self._loginCheck()
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos != None :
                
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y()+ delta.y())
            self.oldPos = event.globalPos()
            
    def mouseReleaseEvent(self, event) :
        self.oldPos =None



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
    
    