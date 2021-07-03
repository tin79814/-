# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 10:32:24 2020

@author: user
PyQt5 uic module convert ui file (XML code) into py file (Python code)"""

from PyQt5 import uic

fin = open ('UiMainApp.ui','r')

fout = open('UiMainApp.py', 'w') 
uic.compileUi (fin, fout, execute=True)
fin.close()
fout.close()

