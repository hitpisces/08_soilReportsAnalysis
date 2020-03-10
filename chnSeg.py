#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import jieba 
def savefile(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)
        
def readfile(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content   
fullname = 'XXX.txt'  # 拼出文件名全路径
content = readfile(fullname)  # 读取文件内容

content = content.replace('\r\n'.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除换行
content = content.replace(' '.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除空行、多余的空格
content_seg = jieba.cut(content)  # 为文件内容分词
savefile('F:/work/聚类1234类分词.txt',' '.join(content_seg).encode('utf-8'))  # 将处理后的文件保存到分词后语料目录

print("中文语料分词结束！！！")

