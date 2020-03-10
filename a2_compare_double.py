import time
import json
import openpyxl

t1 = time.time()

filename1 = '风险管控hashdata'
filename2 = '风险评估hashdata'
filepath = 'C:/Users/linsj/PycharmProjects/08_soilReportsAnalysis/hashdata64/'
resultpath = 'C:/Users/linsj/Desktop/result/'
resultbook = openpyxl.Workbook(resultpath + filename1 + '_' + filename2 + '.xlsx')
ws = resultbook.create_sheet("Sheet1")
ws.append(['file1', 'file2', 'hamming_distance', 'similarity(%)'])
# 打开第一个json文件
with open(filepath + filename1 + '.json', "r", encoding="utf-8") as f:
    dict1 = json.load(f)
# 打开第二个json文件
with open(filepath + filename2 + '.json', "r", encoding="utf-8") as f:
    dict2 = json.load(f)

k1 = []
k2 = []
v1 = []
v2 = []


def listappend(dic, klist, vlist):
    for k, v in dic.items():
        klist.append(k)
        vlist.append(v)


listappend(dict1, k1, v1)
listappend(dict2, k2, v2)


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


def comparejson(key1, key2, value1, value2, booksheet):
    len1 = len(key1)
    len2 = len(key2)
    for i in range(len1):
        for j in range(len2):
            distance = hammingDistance(value1[i], value2[j])
            similarity_ = round(similarity(value1[i], value2[j]) * 100, 4)
            booksheet.append([key1[i], key2[j], distance, similarity_])


comparejson(k1, k2, v1, v2, ws)

resultbook.save(resultpath + filename1 + '_' + filename2 + '.xlsx')
resultbook.close()

print("程序运行时间：", round(time.time() - t1, 3), 's')
