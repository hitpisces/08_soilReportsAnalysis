# -*- coding: utf-8 -*-
# @Time    : 19/10/15 12:44
# @Author  : Jay Lam
# @File    : dupChecker.py
# @Software: PyCharm

import json
import re
import pandas as pd
import pandas_profiling as pp
from pyhanlp import *

import sim_hash_multiple

pathDir = os.path.abspath('.') + "//"


def checkFile(filepath):
    if not os.path.exists(filepath):
        print('没有检测到待对比文件集所在文件夹！')
        exit()
    if not os.listdir(filepath):
        print('没有检测到待对比文件集！')
        exit()
    return os.listdir(filepath)


def openFile(filename):
    if filename.endswith(".txt"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.read()
                line.strip('\n')
                line.replace('\r', '')
                line.replace('\b', '')
                line.replace('\f', '')
                return line
        except Exception as e:
            print(e)


def genSimhash(filepath):
    print("开始生成所有文件指纹...\n")
    res = checkFile(filepath)
    fileshash = {}
    for item in res:
        content = nlpAnalyzer(openFile(filepath + "//" + item), 2)
        # content = openFile(filepath + "//" + item).split()
        if content:
            itemhash = sim_hash_multiple.simhash(content).hash
        else:
            continue
        fileshash[item] = itemhash
    with open("hashdata.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(fileshash))
        f.close()
    print("已生成所有文件指纹！\n")


def nlpAnalyzer(strContent, modelType):
    treatedContent = []
    HanLP.Config.ShowTermNature = False  # 关闭词性标注

    if modelType == 0:
        PercpLexAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')  # 感知机分词
        analyzer = PercpLexAnalyzer()
        results = analyzer.analyze(strContent)
    elif modelType == 1:
        BasicTokenizer = JClass('com.hankcs.hanlp.tokenizer.BasicTokenizer')  # 默认分词，使用维特比分词
        results = BasicTokenizer.segment(strContent)
    elif modelType == 2:
        NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')  # NLP自然语言分词
        results = NLPTokenizer.segment(strContent)
    elif modelType == 3:
        results = HanLP.segment(strContent)  # 维特比分词

    # 返回关键词
    # keywordList = HanLP.extractKeyword(strContent, 5)

    # 返回摘要
    # sentenceList = HanLP.extractSummary(strContent, 30)

    # 去停用词
    coreStopwordDic = JClass('com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary')
    coreStopwordDic.apply(results)

    # 人名实体识别
    # peopleName = HanLP.newSegment().enableNameRecognize(True)
    # peopleName.seg(strContent)

    for i in range(len(results)):
        treatedContent.append(str(results[i]).replace('\n', ''))

    return treatedContent


def startCheck(filepath):
    print("开始进行检测……")
    res = []
    filehash = {}

    # 导入已生成的hash指纹
    with open("hashdata.json", "r", encoding="utf-8") as f:
        filehash = json.load(f)

    # newhash = sim_hash_multiple.simhash(openFile(filepath).split()) # 不使用分词，直接按单词拆分文本

    newhash = sim_hash_multiple.simhash(nlpAnalyzer(openFile(filepath), 2))
    print(newhash)
    for k, v in filehash.items():
        hamming = newhash.hamming_distance(v)
        similarity = newhash.similarity(v)
        print("该文件和" + k + "的汉明距离为：" + str(hamming) + " 相似度为：" + str(round(similarity * 100.0, 4)) + "%\n")
    print("完成检测！")


def dataOverview(path, sheetName):
    reader = pd.read_excel(path, sheetName)
    report = pp.ProfileReport(reader)
    filename = re.sub(r'[A-Za-z0-9\\.\\_\\/\\:]',"",str(path))
    print(filename)
    report.to_file(pathDir + filename+"result.html")


if __name__ == "__main__":
    # startCheck("C://Users//linsj//PycharmProjects//08_soilReportsAnalysis//东方化工厂DF-01地块初步调查报告.txt")
    # nlpAnalyzer(openFile("C://Users//linsj//PycharmProjects//08_soilReportsAnalysis//东方化工厂DF-01地块初步调查报告.txt"), 2)
    # genSimhash('C:\\Users\\linsj\\PycharmProjects\\08_soilReportsAnalysis\\data')
    #dataOverview("C://Users//linsj//PycharmProjects//08_soilReportsAnalysis//不同单位_高相似度筛选.xlsx",sheetName="Sheet1")
    dataOverview("C:\\Users\\linsj\\Downloads\\titanic\\train.csv",sheetName="train")
