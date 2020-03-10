# -*- coding: utf-8 -*-
# @Time    : 19/12/9 12:41
# @Author  : Jay Lam
# @File    : gensimChecker.py
# @Software: PyCharm

import jieba
from gensim import corpora, models, similarities
from collections import defaultdict
from pyhanlp import *
from dupChecker import openFile, nlpAnalyzer, checkFile

pathDir = os.path.abspath('.') + "//"


def genGensim(filepath):
    print("开始生成每个文件的稀疏向量……\n")
    res = checkFile(filepath)
    fileGensim = {}

    for files in res:
        content = nlpAnalyzer(openFile(filepath + "//" + files), 2)
        frequency = defaultdict(content)
        print(frequency)


if __name__ == "__main__":
    genGensim("C:\\Users\\linsj\\PycharmProjects\\08_soilReportsAnalysis\\data")
