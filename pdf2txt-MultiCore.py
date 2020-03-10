# -*- coding: utf-8 -*-
# @Time    : 19/11/11 14:14
# @Author  : Jay Lam
# @File    : pdf2txt-MultiCore.py
# @Software: PyCharm

import multiprocessing as mp
from multiprocessing import Pool, freeze_support, Process
from pdf2txt import convert2, convertMultiple
import os


def convertMulticore(n):
    pathDirInput = "E:\\" + str(n)
    pathDirOutput = "D:\\" + str(n)
    convertMultiple(pathDirInput, pathDirOutput)


if __name__ == '__main__':
    """
    freeze_support()
    pool = mp.Pool(processes=8)  # 指定所用CPU核心数

    pool.apply_async(pdf2txt.convertMultiple(pathDirInput1, pathDirOutput1), (1,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput2, pathDirOutput2), (2,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput3, pathDirOutput3), (3,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput4, pathDirOutput4), (4,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput5, pathDirOutput5), (5,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput6, pathDirOutput6), (6,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput7, pathDirOutput7), (7,))
    pool.apply_async(pdf2txt.convertMultiple(pathDirInput8, pathDirOutput8), (8,))

    pool.close()
    pool.join()
    """

    """
    q = mp.Queue()
    p1 = mp.Process(target=pdf2txt.convertMultiple(pathDirInput1, pathDirOutput1), args=(q,))
    p2 = mp.Process(target=pdf2txt.convertMultiple(pathDirInput2, pathDirOutput2), args=(q,))
    p3 = mp.Process(target=pdf2txt.convertMultiple(pathDirInput3, pathDirOutput3), args=(q,))
    p4 = mp.Process(target=pdf2txt.convertMultiple(pathDirInput4, pathDirOutput4), args=(q,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    res1 = q.get()
    res2 = q.get()
    res3 = q.get()
    res4 = q.get()

    print(str(res1+res2+res3+res4))
    """

    with Pool(processes=56) as pool: # 指定核心数
        freeze_support()
        pool.map(convertMulticore, range(0, 56)) # range范围要和核心数一致
    pool.close()
    pool.join()
    print("完成处理！")
