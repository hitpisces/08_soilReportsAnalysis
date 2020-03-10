import json
import time
import pandas as pd
import openpyxl

t1 = time.time()
filename = '治理与修复hashdata'
filepath = 'C:/Users/linsj/PycharmProjects/08_soilReportsAnalysis/hashdata64/'
resultpath = 'C:/Users/linsj/Desktop/result/'
resultbook = openpyxl.Workbook(resultpath + filename + '.xlsx')
ws = resultbook.create_sheet('Sheet1')
ws.append(['file1', 'file2', 'hamming_distance', 'similarity(%)'])
with open(filepath + filename + '.json', "r", encoding="utf-8") as f:
    filehash = json.load(f)


listk = []
listv = []
for k, v in filehash.items():
    listk.append(k)
    listv.append(v)


def hammingDistance(x, y):
    hamming_distance = 0
    s = str(bin(x ^ y))
    for i in range(2, len(s)):
        if int(s[i]) is 1:
            hamming_distance += 1
    return hamming_distance


def similarity(x, y):
    a = float(x)
    b = float(y)
    if a > b:
        return b / a
    else:
        return a / b


def compare_json(key, value, wb, i=0):
    r = len(key)
    for x in range(i, r):
        for j in range(x + 1, r):
            distance = hammingDistance(value[i], value[j])
            similarity_ = round(similarity(value[i], value[j]) * 100, 4)
            wb.append([key[i], key[j], distance, similarity_])
        i += 1


compare_json(listk, listv, wb=ws)
resultbook.save(resultpath + filename + '.xlsx')
resultbook.close()
print("程序运行时间：", round(time.time() - t1, 3), 's')
