# -*- coding: utf-8 -*-

from xmlrpc.client import Boolean
from PyQt5 import  QtCore
from PyQt5.QtCore import *
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
import re
import json
import clipboard
import pandas as pd
import math
from subprocess import CREATE_NO_WINDOW



class Thread(QtCore.QThread) :
    
    naverId = ""
    naverPW = ""
    
    deleteList = []
    stop = False
    
    _StopSignal = QtCore.pyqtSignal()
    
    loginError = QtCore.pyqtSignal(str)
    
    percent = QtCore.pyqtSignal(int)
    deletePercent = QtCore.pyqtSignal(int)
    
    name = QtCore.pyqtSignal(str)
    
    dataReady = QtCore.pyqtSignal(list) 
    
    def run(self):
            self.findFriend()
            self._StopSignal.emit()
            
    def getAccount(self, id, pw) :
            self.naverId = id
            self.naverPW = pw
            
    def getDeleteList(self, list) :
        self.deleteList = list      
    
    def stopThread(self, sign) :
        self.stop = sign           

    def findFriend(self) :

        groupName = []
        friendCheck = []
        friendName = []
        lastPostTime = []
        friendDay = []
        page_num = 0
        
        id = self.naverId.strip()
        pw = self.naverPW.strip()
        
        if not id :
            return self.loginError.emit("error_noText")  
            
            
        elif not pw :
            return self.loginError.emit("error_noText")  
            
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=2000,1000")
        options.add_argument("--disable-gpu")
        options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        service = Service()
        service.creation_flags = CREATE_NO_WINDOW

        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {'browser': 'ALL'} 

        chrome_path =  "chromedriver.exe"

        try :
            driver = webdriver.Chrome(service=service, executable_path=chrome_path, options=options, desired_capabilities=capabilities)
            driver.set_window_position(0,0)
            # driver.set_window_position(-10000,10000) 
        except NoSuchElementException:
            print("error")       
        
        
        url = "https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsection.blog.naver.com%2FBlogHome.naver"
        driver.get(url)
       
        clipboard.copy(id)
        time.sleep(0.5)
        id_field = driver.find_element(By.ID,"id")
        id_field.send_keys(Keys.CONTROL + "v")
        time.sleep(0.5)

        clipboard.copy(pw)
        time.sleep(0.5)
        pw_field = driver.find_element(By.ID,"pw")
        pw_field.send_keys(Keys.CONTROL + "v")
        time.sleep(0.5)
        
        errorElement = driver.find_element(By.CLASS_NAME,"login_error_wrap").get_attribute("style")
        try:
             if errorElement == "display: block" :
        
                self.loginError.emit("error_account")  
                driver.quit()
        except NoSuchElementException:
            pass    
        
        try:
            driver.find_element(By.CLASS_NAME,"btn_login_wrap").click()
        except NoSuchElementException:
            pass
        
        try:
            driver.find_element(By.CLASS_NAME,"btn_upload").find_element(By.TAG_NAME, "a").click()
        except NoSuchElementException:
            pass
        
        try:
            while True:
                driver.find_element(By.CLASS_NAME,"login_check").find_element(By.CLASS_NAME, "check_row").click()
                time.sleep(5)
                if driver.find_element(By.CLASS_NAME,"_buddy_dropdown_container") :
                    break
        except NoSuchElementException:
            pass

        driver.implicitly_wait(3)
        driver.set_window_position(-10000,10000) 
        
        
        driver.find_element(By.CLASS_NAME,"menu_my_article").find_elements(By.TAG_NAME, "a")[2].click()
        driver.find_element(By.CLASS_NAME,"link_manage_buddy").click()
        
        driver.switch_to.window(driver.window_handles[-1])
        
        
        beforeScrollY = driver.execute_script("return window.scrollY")
        while True:
            driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
            time.sleep(0.5)
            afterScrollY = driver.execute_script("return window.scrollY")
            if beforeScrollY == afterScrollY:
                break
            beforeScrollY = afterScrollY
        time.sleep(0.5)
        
        content = driver.find_element(By.ID, "papermain")
        driver.switch_to.frame(content)      
          
        while True:
            
            if self.stop == True :
                driver.quit()
                self.percent.emit(int(100))
                break
                
            pageSize = len(driver.find_element(By.CLASS_NAME,"paginate_re").find_elements(By.TAG_NAME, "a"))

            if page_num > 0 :
                try :  
                    if pageSize < page_num :
                        driver.refresh()
                        break
                    driver.find_element(By.CLASS_NAME,"paginate_re").find_elements(By.TAG_NAME, "a")[page_num -1].click()
                    
                except NoSuchElementException:
                    pass

            items = driver.find_element(By.CLASS_NAME, "tbl_buddymanage")

            tbody  = items.find_element(By.TAG_NAME, "tbody")
            itemList  = tbody.find_elements(By.TAG_NAME, "tr")
            
            totalFriend = driver.find_element(By.CLASS_NAME, "action2_r").find_element(By.TAG_NAME, "strong").text
            
            print(f"--------------{page_num+1}페이지 이웃찾기 시작-------------")
            
            friend_num = 0
            
            if(len(itemList)==0) :
                driver.quit()
                break
            
            for element in itemList:
                if self.stop == True :
                    driver.quit()
                    self.percent.emit(int(100))
                    break
                
                friend_num += 1
                
                tempGroupName = ""
                try :
                    tempGroupName = element.find_element(By.CLASS_NAME, "ellipsis1").text
                except:
                    pass
                groupName.append(tempGroupName)

                tempFriendCheck = ""
                try :
                    tempFriendCheck = "이웃"
                    if element.find_element(By.CLASS_NAME, "type").find_element(By.CLASS_NAME, "both").text :
                        tempFriendCheck = "서로이웃"
                        
                except:
                    pass
                friendCheck.append(tempFriendCheck)
                
                tempFriendName = ""
                try :
                    tempFriendName = element.find_element(By.CLASS_NAME, "ellipsis2").text
                except:
                    pass
                friendName.append(tempFriendName)
                
                tempLastPostTime = ""
                try :
                    tempLastPostTime = element.find_elements(By.TAG_NAME, "td")[5].text
                except:
                    pass
                lastPostTime.append(tempLastPostTime)
                
                tempFriendDay = ""
                try :
                    tempFriendDay = element.find_elements(By.TAG_NAME, "td")[6].text
                except:
                    pass
                friendDay.append(tempFriendDay)
                
                # data = tempGroupName + " / " + tempFriendCheck + " / " + tempFriendName + " / " +  tempLastPostTime + " / " + tempFriendDay
                # print(f"{friend_num} 번째 이웃 : {data}")
                
                self.name.emit(f"{page_num+1}페이지 {friend_num}번째 이웃 : {tempFriendName}")   

                currentNum = int(page_num*50) + int(friend_num)
                
                self.percent.emit(int(5+(currentNum*95)/int(totalFriend)))
                
                time.sleep(0.01)
                
                raw_data = {'그룹명' : groupName,
                        '상태' : friendCheck,
                        '이웃명' : friendName,
                        '최근글' : lastPostTime,
                        '이웃추가일' : friendDay,
                        }

                data_list = list(zip(raw_data['그룹명'], 
                        raw_data['상태'], 
                        raw_data['이웃명'], 
                        raw_data['최근글'], 
                        raw_data['이웃추가일']))
                    
                self.dataReady.emit(data_list) 

            page_num += 1
            time.sleep(1)
        
        page = 0
        while True :
            if len(self.deleteList) > 0 :
                if self.stop == True :
                    driver.quit()
                    self.percent.emit(int(100))
                    break
                print("===============================")
                print(self.deleteList)
                
                driver.refresh() 
                content = driver.find_element(By.ID, "papermain")
                driver.switch_to.frame(content)
                
                self.deletePercent.emit(int(10))
                driver.find_elements(By.CLASS_NAME, "selectbox-box")[2].click()
                
                self.deletePercent.emit(int(20))
                
                print(page)
                if page > 0 :
                    driver.find_element(By.CLASS_NAME,"paginate_re").find_elements(By.TAG_NAME, "a")[page -1].click()
                
                self.deletePercent.emit(int(30))    
                items = driver.find_element(By.CLASS_NAME, "tbl_buddymanage")
                tbody  = items.find_element(By.TAG_NAME, "tbody")
                index  = tbody.find_elements(By.TAG_NAME, "tr")
                
                self.deletePercent.emit(int(50))    
                if len(self.deleteList) == 1 :
                        
                        print("11111")
                        self.deletePercent.emit(int(65))    
                        for item in index :
                            
                            print("2222")
                            item_name = item.find_element(By.CLASS_NAME, "ellipsis2").text
                            
                            # print(item_name)
                            
                            if item_name.strip() == str(self.deleteList[0]).strip() :
                                
                                print("3333")
                                self.deletePercent.emit(int(80)) 
                                item.find_element(By.CLASS_NAME, "checkwrap").find_element(By.TAG_NAME, "input").click()
                                driver.find_element(By.CLASS_NAME, "btn_del").click()
                                driver.find_elements(By.CLASS_NAME, "btn_2")[1].find_element(By.TAG_NAME, "input").click() 
                                time.sleep(0.5)
                                self.deleteList.clear()
                                self.deletePercent.emit(int(100))
                                print("4444")
                                break
                        page+=1    
                        
                    
                elif len(self.deleteList) > 1 :
                    
                    while True :
                        if len (driver.find_elements(By.CLASS_NAME, "selectbox-layer")[2].find_element(By.CLASS_NAME, "selectbox-list").find_elements(By.TAG_NAME, "li")) > 0 :
                            break
                        time.sleep(0.005)
                        
                    checkDrop = driver.find_elements(By.CLASS_NAME, "selectbox-layer")[2].find_element(By.CLASS_NAME, "selectbox-list").find_elements(By.TAG_NAME, "li")[3]
                    checkDrop.click()
                    time.sleep(1)
                    self.deletePercent.emit(int(65))  
                    
                    while True:
                        neigborCount = driver.find_element(By.CLASS_NAME , "action2_r").find_element(By.CLASS_NAME , "fl").text
                        neigborCount = neigborCount.replace("정렬된 이웃","").replace("명","").replace(" ","").strip()
                        if int(neigborCount) == 0 :
                            print("nonono")
                            break
                        
                        driver.find_elements(By.CLASS_NAME, "checkAll")[0].click()
                        time.sleep(1)
                        driver.find_element(By.CLASS_NAME, "btn_del").click()
                        time.sleep(1)
                        driver.find_elements(By.CLASS_NAME, "btn_2")[1].find_element(By.TAG_NAME, "input").click() 
                        self.deletePercent.emit(int(80)) 
                    
                    self.deleteList.clear()
                    self.deletePercent.emit(int(100))
                    
                 
                    
            
                