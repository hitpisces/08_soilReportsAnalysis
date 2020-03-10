import re
import os
import openpyxl
import time

dataPath = 'E:\\治理与修复txt\\'
pathDir = os.path.abspath('.') + "//"
dateStamp = time.strftime("%H%M",time.localtime(time.time()))

wb = openpyxl.Workbook(pathDir+'提交单位result.xlsx')
ws = wb.create_sheet('Sheet1')

filenames = os.listdir(dataPath)

for filename in filenames:
    try:
        f = open(dataPath+filename,'r',encoding='utf-8')
        txtContents = f.readlines()
        dicresult = {}
        for line in txtContents:
            line = line.strip()
            if re.match('提.*交.*单.*位.*', line):
                splitlint = line.split('：')
                dicresult['提交单位']=splitlint[1]
            if re.match('编.*制.*单.*位.*',line):
                splitlint = line.split('：')
                dicresult['编制单位'] = splitlint[1]
        if '提交单位' not in dicresult.keys():
            dicresult['提交单位'] = ''
        if '编制单位' not in dicresult.keys():
            dicresult['编制单位'] = ''

        ws.append([filename,dicresult['提交单位'],dicresult['编制单位']])
    except Exception as e:
        dicresult['错误原因']=str(e)
        dicresult['提交单位'] = ''
        dicresult['编制单位'] = ''
        ws.append([filename, dicresult['提交单位'], dicresult['编制单位'],dicresult['错误原因']])
        print(filename,e)

wb.save(pathDir+dateStamp+'提交单位result.xlsx')
wb.close()
print("完成处理！")


