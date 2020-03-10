# -*- coding: utf-8 -*-
import tkinter.messagebox
from word import getContent

def openfile(filename):
    if filename.split('.')[-1]=="txt":
        try:
            with open(filename,'r', encoding='UTF-8') as f:
                line = f.read()
                line.replace('\n','')
                return line
        except Exception as e:
            print(e)
            tkinter.messagebox.showwarning("警告","文件编码不是UTF-8！")
    else:
        return getContent(filename)
            

