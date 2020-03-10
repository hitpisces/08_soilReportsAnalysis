# -*- coding: utf-8 -*-
# @Time    : 19/10/15 12:01
# @Author  : Jay Lam
# @File    : pdf2txt.py
# @Software: PyCharm

# 批量版pdf转txt
# 命令行下使用“python pdf2txt -p pdfdir路径 -t txtdir路径” 运行程序

import getopt
import glob
import os
import sys
import time
from io import StringIO

from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser


# 方法一
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    # 创建一个PDF资源管理器对象来存储共赏资源
    with open(fname, 'rb') as f:
        praser = PDFParser(f)
        doc = PDFDocument(praser)
        if not doc.is_extractable:
            err = fname + "is not extractable"+"\n"
            return err
            raise

        elif doc.is_extractable:
            manager = PDFResourceManager()
            # 创建一个PDF设备对象
            converter = TextConverter(manager, output, laparams=LAParams())
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(manager, converter)

            # 对pdf每一页进行分析
            for page in PDFPage.get_pages(f, pagenums):
                interpreter.process_page(page)
            f.close()
            converter.close()

            # 得到每一页的txt文档
            text = output.getvalue()
            output.close()
            return text


# 方法二: 增加了对不可提取页面检测并报错，报错文件写入extraErr.txt
def convert2(path):
    output = StringIO()
    with open(path, 'rb') as f:
        praser = PDFParser(f)

        doc = PDFDocument(praser)

        if not doc.is_extractable:
            with open("extraErr.txt", "a", encoding="utf-8") as fi:
                fi.write(path)
                fi.close()
            raise PDFTextExtractionNotAllowed

        pdfrm = PDFResourceManager()

        laparams = LAParams()

        device = PDFPageAggregator(pdfrm, laparams=laparams)

        interpreter = PDFPageInterpreter(pdfrm, device)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if hasattr(x, "get_text"):
                    content = x.get_text()
                    output.write(content)

    content = output.getvalue()
    output.close()
    return content


# 将pdfdir下所有文件转为txt并存入txtdir目录
def convertMultiple(pdfDir, txtDir):
    # 判断是否有储存的文件夹，如果有则pass，没有则创建
    if os.path.exists(txtDir):
        pass
    else:
        os.makedirs(txtDir)
    # 判断读取pdf是否需要密码
    if pdfDir == "":
        pdfDir = os.getcwd() + "\\"  # 如果没有pdfDir则跳过

    # 遍历文件夹下每一个pdf文件
    totalNum = len(glob.glob(pdfDir + '/*.pdf'))
    for pdf in os.listdir(pdfDir):  # 遍历pdfDir下每个pdf文件
        fileExtension = pdf.split(".")[-1]
        # 判断是否该文件夹下的文件是否是pdf文件
        if fileExtension == "pdf" or fileExtension == "PDF":
            # 构建pdf的完全路径
            try:
                pdfFilename = pdfDir + "\\" + pdf
                text = convert(pdfFilename)  # 获得pdf文件字符串
                # 构建存储文件的目标路径
                textFilename = txtDir + '\\' + pdf[:-4] + ".txt"
                # 将解析得到的pdf文件写入对应的txt文件
                f = open(textFilename, 'a', encoding='utf-8')
                f.write(text)
                f.close()

                # 判断pdfdir和txtdir两个目录下文件数量，计算进度
                processedNum = len(glob.glob(txtDir + '/*.txt'))
                print(pdfDir + "处理进度:" + str(processedNum) + "/" + str(totalNum) + "完成时间:" + time.strftime(
                    '%m-%d %H:%M:%S', time.localtime(time.time())))

            except Exception as e:
                print(e.args)
                with open(pdfDir+"\\"+"log.txt", "a", encoding="utf-8") as fi:  # 异常写入日志
                    fi.write(pdfFilename+str(e.args)+"\n")
                    fi.close()


# i : info
# p : pdfDir
# t = txtDir
def pdf2txt(argv):
    try:
        # opts是指拿到argv中必须拿到的参数，args是argv中不需要的参数
        opts, args = getopt.getopt(argv, "ip:t:")
    except getopt.GetoptError:
        print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
        sys.exit(2)
    for opt, arg in opts:
        # 解析每一个参数，得到源文件路径和目标文件路径
        if opt == "-i":
            print("pdfToT.py -p <pdfdirectory> -t <textdirectory>")
            sys.exit()
        elif opt == "-p":
            pdfDir = arg
        elif opt == "-t":
            txtDir = arg
    # 调用pdf解析文件
    convertMultiple(pdfDir, txtDir)


if __name__ == "__main__":
    pdf2txt(sys.argv[1:])

"""
#camelot库提取pdf表格
tables = camelot.read_pdf("test2.pdf")
print(tables)
tables[0].df
tables.export('test.csv',f='csv',compress=True)
tables[0].to_csv('test.csv')
tables
tables[0]
tables[0].parsing_report
"""

"""
#tabula库提取pdf表格
df = tabula.read_pdf(pathDir+"\\test.pdf",pages='5')
print(df)
"""
