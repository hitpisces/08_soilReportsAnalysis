# -*- coding: utf-8 -*-
# @Time    : 19/11/19 12:19
# @Author  : Jay Lam
# @File    : delBlankline.py
# @Software: PyCharm

def clearBlankline(fileName):
    originFile = open(fileName, 'r', encoding='utf-8')
    desFile = open(fileName + "cln.txt", 'a', encoding='utf-8')
    try:
        for line in originFile.readlines():
            if line == '\n':
                line = line.strip("\n")
                desFile.write(line)
    finally:
        originFile.close()
        desFile.close()


if __name__ == '__main__':
    clearBlankline("C:\\Users\\linsj\\PycharmProjects\\08_soilReportsAnalysis\\东方化工厂DF-01地块初步调查报告.txt")
