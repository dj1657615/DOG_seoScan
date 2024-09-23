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



groupName = []
friendCheck = []
friendName = []
lastPostTime = []
friendDay = []
page_num = 0

# id = self.naverId.strip()
# pw = self.naverPW.strip()
id = "sechinam"
pw = "agc1991!1"

    
options = webdriver.ChromeOptions()

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-allow-origins=*")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=2000,1000")
options.add_argument("--disable-gpu")
options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.set_window_position(-100,100) 

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
    driver.find_element(By.CLASS_NAME,"btn_login_wrap").click()
    
except NoSuchElementException:
    pass

driver.implicitly_wait(3)


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

deleteList =  ["대구 북구청|대구 북구청 공식 블로그"]
page = 0
while True :
    
    
    if len(deleteList) > 0 :
                # print("===============================")
                # print(deleteList)
                
                driver.refresh() 
                content = driver.find_element(By.ID, "papermain")
                driver.switch_to.frame(content)
                
                driver.find_elements(By.CLASS_NAME, "selectbox-box")[2].click()
                
                # print(page)
                if page > 0 :
                    driver.find_element(By.CLASS_NAME,"paginate_re").find_elements(By.TAG_NAME, "a")[page -1].click()
                
                items = driver.find_element(By.CLASS_NAME, "tbl_buddymanage")
                tbody  = items.find_element(By.TAG_NAME, "tbody")
                index  = tbody.find_elements(By.TAG_NAME, "tr")
                 
                if len(deleteList) == 1 :
                        
                        # print("11111")
                        for item in index :
                            
                            # print("2222")
                            item_name = item.find_element(By.CLASS_NAME, "ellipsis2").text
                            
                            # print(item_name)
                            
                            # print(item_name.strip())
                            # print(str(deleteList[0]).strip())
                            # print(item_name.strip()== str(deleteList[0]).strip())
                            # print(item_name.strip()== (deleteList[0]).strip())
                            if item_name.strip() == str(deleteList[0]).strip() :
                                
                                # print("3333")
                                item.find_element(By.CLASS_NAME, "checkwrap").find_element(By.TAG_NAME, "input").click()
                                driver.find_element(By.CLASS_NAME, "btn_del").click()
                                driver.find_elements(By.CLASS_NAME, "btn_2")[1].find_element(By.TAG_NAME, "input").click() 
                                time.sleep(0.5)
                                deleteList.clear()
                                # print("4444")
                                break
                        page+=1    
                        
                    
                elif len(deleteList) > 1 :
                    
                    checkDrop = driver.find_elements(By.CLASS_NAME, "selectbox-layer")[2].find_element(By.CLASS_NAME, "selectbox-list").find_elements(By.TAG_NAME, "li")[1]
                    checkDrop.click()
                    time.sleep(0.5)
                
                    driver.find_elements(By.CLASS_NAME, "checkAll")[0].click()
                    driver.find_element(By.CLASS_NAME, "btn_del").click()
                    driver.find_elements(By.CLASS_NAME, "btn_2")[1].find_element(By.TAG_NAME, "input").click() 
   