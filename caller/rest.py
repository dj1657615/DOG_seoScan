# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
import zipfile
main_server = 'http://43.201.119.167:23113/'
# main_server = 'http://127.0.0.1:23113/'

def login(**data):
    body = {
            'id': data['userId'], 
            'pw': data['userPw'],
    }
    # print(body)
    try :
        response = requests.post(main_server + 'user/login/free', data  = body,timeout= 300)
        loginObject = json.loads(response.text)
        return loginObject["status"]
    except Exception as e :            
        raise e.Except["None"]

def getVersion():
    response = requests.get(main_server + 'free/lately/?item=2')
    bodyObject = json.loads(response.text)
    return bodyObject.get("version")