# -*- coding: utf-8 -*-
# @Time    : 19/11/18 21:59
# @Author  : Jay Lam
# @File    : mergeFiles2Dir.py
# @Software: PyCharm

import os
import shutil

pathDir = os.path.abspath('.')

originDir = "D:\\详细调查报告\\"

desDir = "D:\\"

subdirList = os.listdir(originDir)

for subdir in subdirList:
    fileList = os.listdir(originDir + subdir)
    for file in fileList:
        shutil.move(originDir + subdir + "\\" + file, desDir)
print("完成移动文件到同一个目录！")
