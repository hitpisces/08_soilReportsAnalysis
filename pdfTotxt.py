# -*- coding: utf-8 -*-
# @Time    : 19/11/5 14:20
# @Author  : Jay Lam
# @File    : pdfTotxt.py
# @Software: PyCharm

# 单文件版pdf转txt

import os
from io import StringIO

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

pathDir = os.path.abspath('.')


class PDFUtils:

    def __init__(self):
        pass

    def pdf2txt(self, path):
        output = StringIO()
        with open(path, 'rb') as f:
            praser = PDFParser(f)

            doc = PDFDocument(praser)

            if not doc.is_extractable:
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


if __name__ == '__main__':
    path = pathDir + "\\" + "test3.pdf"
    pdf_utils = PDFUtils()
    print(pdf_utils.pdf2txt(path))
