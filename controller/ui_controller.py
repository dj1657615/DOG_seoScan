# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import configparser
from datetime import datetime

def userLoadInfo(self):
    config = configparser.ConfigParser()
    config.read('./info.on')

    self.version = str(config['Config']['version'])
    saveConfig = config['User']['save']
    if saveConfig == 't':
        saveid = str(config['User']['id'])
        savepw = str(config['User']['pw'])
        self.idpw_checkbox.toggle()
        self.idEdit.setText(saveid)
        self.pwEdit.setText(savepw)


def userSaveInfo(self, checkState, loginid, loginpw, version):
    if checkState == True:
        saveCheck = 't'
        config = configparser.ConfigParser()
        config.read('./info.on')
        config['User']['id'] = loginid
        config['User']['pw'] = loginpw
        config['User']['save'] = saveCheck
        config['Config']['version'] = version
        with open('./info.on', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    
    elif checkState == False:
        saveCheck = 'f'
        config = configparser.ConfigParser()
        config.read('./info.on')
        config['User']['id'] = ""
        config['User']['pw'] = ""
        config['User']['save'] = saveCheck
        config['Config']['version'] = version
        with open('./info.on', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    return loginid, loginpw