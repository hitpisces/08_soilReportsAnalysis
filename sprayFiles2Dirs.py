# -*- coding: utf-8 -*-
# @Time    : 19/11/12 11:51
# @Author  : Jay Lam
# @File    : sprayFiles2Dirs.py
# @Software: PyCharm

"""
程序功能说明：
在folderPath处新建peopleNumber个文件夹，
原始文件存储在path处
给每个文件夹分配总文件数÷peopleNumber个文件

Tips:
1: os.path.join(path1,path2...)
this function is used to combine the path,it returns a path which is 'path1/path2...'

2: os.makedirs(path)
this function is used to make a directory(new folder) in the path param

3: shutil.move(oldPath,newPath)
this function is used to move file from param1 to param 2

4: os.path.exists(path)
this function is used to check the filePath(param1) whether exists
"""

import os
import shutil
import random # 如果文件随机分配则使用此库

# 待处理文件所在路径
path = 'E:\\fxpg\\'

# 拟生成的多个文件夹所在路径
folderPath = 'E:\\'

peopleNumber = 11

# 获取待处理文件列表
file_list = os.listdir(path)

# 根据文件数÷拟分配数，计算最终需要新生成多少个新的子文件夹
folderNumber = 0
if len(file_list) % peopleNumber == 0:
    folderNumber = len(file_list) / peopleNumber
elif len(file_list) % peopleNumber != 0:
    folderNumber = len(file_list) // peopleNumber + 1

# 生成新的子文件夹
sort_folder_number = [x for x in range(0, folderNumber)]
for number in sort_folder_number:
    new_folder_path = os.path.join(folderPath, '%s' % number)  # 新文件夹形如 ‘folderPath\number'
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print("new a floder named " + str(number) + 'at the path of ' + new_folder_path)

print('there are ' + str(len(file_list)) + ' files at the path of ' + path)
for i in range(0, len(file_list)):
    old_file_path = os.path.join(path, file_list[i])
    if os.path.isdir(old_file_path):
        '''if the path is a folder,program will pass it'''
        print('files does not exist ,path=' + old_file_path + ' it is a dir')
        pass
    elif not os.path.exists(old_file_path):
        '''if the path does not exist,program will pass it'''
        print('files does not exist ,path=' + old_file_path)
        pass
    else:
        '''define the number,it decides how many files each people process'''
        new_file_path = os.path.join(folderPath, '%s' % (i % folderNumber)) # 平均放文件，如果随机放则用random函数
        if not os.path.exists(new_file_path):
            print('not exist path:' + new_file_path)
            break
        shutil.copy(old_file_path, new_file_path)
        print('success move file from ' + old_file_path + ' to ' + new_file_path)
print("完成分类输出！")
