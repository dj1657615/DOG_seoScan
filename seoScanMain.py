# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from view import main_Ui
import clipboard

from controller import findFriend

class MainWindow(QMainWindow , main_Ui.Ui_MainWindow):
     def __init__(self):
        QMainWindow.__init__(self)
        main_Ui.Ui_MainWindow.__init__(self)
        
        self.th_findFriend = findFriend.Thread(self)
        self.noFriendList = []
        self.noFriendAllList = []
        self.deleteIndexList = []
        self.tempList = []
        self.process = 0
        self.processValue = 0
        self.allFriend = 0
        self.deltePercent = 0
        self.lastListSize = 0
        
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.connectClickEvent() 
        
     def connectClickEvent(self) :
        self.minimumButton.clicked.connect(self._minimumWindow)
        self.exitButton.clicked.connect(self._closeWindow)
        
        self.btnSearchFollower.clicked.connect(self.startFindFriend)
        self.table.cellDoubleClicked.connect(self.onCellDoubleClicked)        
        self.btnAllDelete.clicked.connect(lambda: self.showDeleteConfirm(None, None, "all"))
        self.btnAllDelete.clicked.connect(self.deleteFriendRowUpdate)
        self.btnStop.clicked.connect(self.stopFindFriend)
      
        self.th_findFriend.percent.connect(self.stopFindFriend) 

        
     def stopFindFriend(self, value) :
         self.btnStop.setDisabled(True)
         self.currentFriendName.setText("중지중입니다")
         self.th_findFriend.stopThread(True)
         if value == 100 :
            self.idEdit.setReadOnly(False)
            self.pwEdit.setReadOnly(False)
            self.btnSearchFollower.show()
            self.btnStop.hide()
            self.currentFriendName.setText("완료되었습니다") 
            self.progressBar.setValue(100)
        
     def startFindFriend(self) :
        self.th_findFriend = findFriend.Thread(self)
        self.th_findFriend.getAccount(self.idEdit.text(), self.pwEdit.text()) 
        self.currentFriendName.setText("이웃찾기를 시작합니다... 잠시만 기다려주세요....")
        
        self.idEdit.setReadOnly(True)
        self.pwEdit.setReadOnly(True)
        self.btnSearchFollower.hide()
        self.btnStop.show()
        self.progressBar.setValue(5)
        
        self.th_findFriend.loginError.connect(self.errorUi)
        self.th_findFriend.percent.connect(self.updateProcessPercent)
        self.th_findFriend.name.connect(self.updateCurrentFriendName)
        self.th_findFriend.start()
        self.th_findFriend.dataReady.connect(self.updateTable)
        self.th_findFriend.percent.connect(self.updateUi)
     
 
           
     def updateCurrentFriendName(self, name):  
        self.currentFriendName.setText(name)
        
     def updateTable(self, data):
        self.allFriend = len(data)
        self.table.setRowCount(len(data))
        self.noFriendList.clear()
        self.noFriendAllList.clear()
        self.deleteIndexList.clear()
        
        temp_list = []
        for i in range(len(data)):
           
            groupName_item = QtWidgets.QTableWidgetItem(str(data[i][0]))
            groupName_item.setTextAlignment(QtCore.Qt.AlignCenter)
            friendCheck_item = QtWidgets.QTableWidgetItem(str(data[i][1]))
            friendCheck_item.setTextAlignment(QtCore.Qt.AlignCenter)
            friendName_item = QtWidgets.QTableWidgetItem(str(data[i][2]))
            friendName_item.setTextAlignment(QtCore.Qt.AlignCenter)
            lastPostTime_item = QtWidgets.QTableWidgetItem(str(data[i][3]))
            lastPostTime_item.setTextAlignment(QtCore.Qt.AlignCenter)
            friendDay_item = QtWidgets.QTableWidgetItem(str(data[i][4]))
            friendDay_item.setTextAlignment(QtCore.Qt.AlignCenter)
            delete_item = QtWidgets.QTableWidgetItem("X")
            delete_item.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.table.setItem(i, 0, groupName_item)
            self.table.setItem(i, 1, friendCheck_item)
            self.table.setItem(i, 2, friendName_item)
            self.table.setItem(i, 3, lastPostTime_item)
            self.table.setItem(i, 4, friendDay_item) 
            self.table.setItem(i, 5, delete_item) 
            
            self.table.setColumnWidth(2, 380) 
            self.table.setColumnWidth(3, 92)
            self.table.setColumnWidth(4, 92)   
            self.table.setColumnWidth(5, 58)     
            if 99 > i > 15 :
                self.table.setColumnWidth(5, 50)
            elif i > 98 :
                self.table.setColumnWidth(2, 375)
                self.table.setColumnWidth(5, 50)
            
            if data[i][1] == "이웃":    
             temp_list.append((i, data[i][2]))    
            
        temp_list = list(set(temp_list))
        temp_list.sort(key=lambda x: x[0])
        
        self.noFriendAllList.extend(temp_list) 
        self.deleteIndexList.extend(temp_list)
        self.lastListSize = len(self.deleteIndexList)
        
     def errorUi(self, errorText) :
         if errorText == "error_account" :
            
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("\n" + "올바른 아이디/비밀번호를 입력해주세요  " + "\n")
            
         if errorText == "error_noText" :
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("\n" + "아이디/비밀번호를 입력해주세요  " + "\n")
            
         msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
         msgBox.exec_()       

         self.refreshiUi()
         
     def refreshiUi(self) :
         self.idEdit.setReadOnly(False)
         self.pwEdit.setReadOnly(False)
         self.btnSearchFollower.show()
         self.btnStop.hide()
         self.progressBar.setValue(0)    
         self.currentFriendName.setText("")
                
     def setKeyword(self) :
        self.process = 1
        
     def updateProcessPercent(self, value):
        self.progressBar.setValue(value)
        
     def updateUi(self, value):
        self.processValue = value
        if value == 100 :
           self.idEdit.setReadOnly(False)
           self.pwEdit.setReadOnly(False)
           self.btnSearchFollower.show()
           self.btnStop.hide()
           self.currentFriendName.setText("이웃찾기가 완료되었습니다")
           self.result_title.setText(f"이웃 : {len(self.noFriendAllList)} / 전체이웃 : {str(self.allFriend)}")
           
           if len(self.noFriendAllList) >0 :
               self.btnAllDelete.show()
     
     def onCellDoubleClicked(self, row, column):
        print("click")
        print(row)
        if self.processValue == 100 :
            if column == 5:  
                  print("0k")           
                  second_column_value = self.table.item(row, 2).text() 
                  self.showDeleteConfirm(row, second_column_value, "one")
               
     def showDeleteConfirm(self, row, name, type):
         msgBox = QtWidgets.QMessageBox()
         if type == "one":
            msgBox.setText("\n" + "이웃을 삭제하시겠습니까??  " + "\n")
         elif type == "all":
            msgBox.setText("\n" + "서로이웃이 아닌 이웃을 전부 삭제하시겠습니까??  " + "\n")
         elif type == "no":
            msgBox.setText("\n" + "삭제할 이웃이 없습니다  " + "\n")
         msgBox.setWindowTitle("이웃삭제")
         msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
         msgBox.buttonClicked.connect(lambda button: self.deleteFriend(button, row, name, type))
         msgBox.exec_() 
         
     def deleteFriend(self, button, row, name, type):
        
       if button.text() == "OK":
         if type == "one" and row is not None:
               self.noFriendList.append(name)
               self.deleteIndexList.append([row,name])
               print("-------------------------")
               print( self.deleteIndexList)
               self.th_findFriend.getDeleteList(self.noFriendList)
               self.th_findFriend.deletePercent.connect(self.deleteFriendRowUpdate)
               
               print(name)
         elif type == "all":
               if len(self.noFriendAllList) > 0 :
                  self.th_findFriend.getDeleteList(self.noFriendAllList)
                  self.th_findFriend.deletePercent.connect(self.deleteFriendRowUpdate)
               else :
                  self.showDeleteConfirm(0, "no")
                  
     def deleteFriendRowUpdate(self, value) :
        
      self.currentFriendName.setText("이웃을 삭제중입니다... 잠시만 기다려주세요....")
      self.idEdit.setReadOnly(True)
      self.pwEdit.setReadOnly(True)
      self.btnSearchFollower.setDisabled(True)
      self.progressBar.setValue(value) 
      
      count = 0
      
      print("-----------111111111111--------------")
      print( len(self.deleteIndexList))
      print(self.lastListSize)
      print( self.deleteIndexList)
      print( value)
      
      if value == 100 :   
         if len(self.deleteIndexList) > 0 :
            print("-----------33333333333333333--------------")
            
            print(len(self.deleteIndexList))
            print(self.lastListSize)
            
            print(self.deleteIndexList)
            
            if len(self.deleteIndexList) > self.lastListSize :
               lastData = self.deleteIndexList[-1]
               row = lastData[0]
               print (lastData)
               print (row)
               self.table.removeRow(int(row))
               self.deleteIndexList = self.deleteIndexList[:-1]
               print(self.deleteIndexList)
               self.lastListSize -1
               self.table.repaint()   
               
            else :   
               print("-----------22222--------------")
               for row in self.deleteIndexList:
                  
                  print("-----------333333--------------")
                  if count == len(self.deleteIndexList) :
                     break
                  for rowCount in range(self.table.rowCount()):
                     
                     if str(row[1]).strip() == self.table.item(rowCount, 2).text() :
                        print("innnnnnnnnnnn")
                        self.table.removeRow(rowCount)
                        self.btnAllDelete.hide() 
                        count+=1
                        break
                        
         self.table.repaint()   
         self.result_title.setText(f"이웃 : {len(self.noFriendAllList)} / 전체이웃 : {str(self.table.rowCount())}") 
         self.idEdit.setReadOnly(False)
         self.pwEdit.setReadOnly(False)
         self.btnSearchFollower.setDisabled(False)
         self.currentFriendName.setText("완료되었습니다")                
           
     def _minimumWindow(self):
         self.showMinimized()

     def _closeWindow(self):
        
         QCoreApplication.instance().quit()
         
     def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

     def mouseMoveEvent(self, event):
        if self.oldPos != None :
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y()+ delta.y())
            self.oldPos = event.globalPos()
            
     def mouseReleaseEvent(self, event) :
        self.oldPos =None
     
     def keyPressEvent(self, e): 
        if self.process == 0 : 
           
         if e.key() in [Qt.Key_Return, Qt.Key_Enter] :
            self.startFindFriend()  
            print("enter") 