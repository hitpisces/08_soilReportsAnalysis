# -*- coding: utf-8 -*-
# @Time    : 19/10/15 12:44
# @Author  : Jay Lam
# @File    : dupChecker.py
# @Software: PyCharm

import json
import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

import dupChecker
import file
import sim_hash


class MY_GUI():

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.init_path = None
        self.check_path = []
        self.res = None

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("全国土壤污染状况详查调查报告查重工具")
        self.init_window_name.geometry('1200x700')  # 窗口名
        # 创建菜单对象，锁定到窗口（固定菜单）
        menubar = Menu(self.init_window_name)
        self.init_window_name.config(menu=menubar)
        menuOpen = Menu(menubar, tearoff=0)
        menuOpen.add_command(
            label="打开文件",
            command=self.get_path  # 响应函数
        )
        menuOpen.add_command(
            label="打开文件夹",
            command=self.get_dir  # 响应函数
        )

        menubar.add_cascade(label="1.导入源文件", command=self.get_file)
        menubar.add_cascade(label="2.导入待检测文件", menu=menuOpen)
        menubar.add_cascade(label="3.开始检测", command=self.startCheck)
        menubar.add_cascade(label="4.生成报告", command=self.genReport)
        menubar.add_cascade(label="5.使用指纹库检测", command=self.get_hash)

        # self.init_window_name.geometry('320x160+10+10')          #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"                      #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",1.0)            #虚化，值越小虚化程度越高

        # 标签
        self.init_data_label = Label(self.init_window_name, text="待比较文件列表")
        self.init_data_label.grid(row=1, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=1, column=13)
        # self.log_label = Label(self.init_window_name, text="结果显示")
        # self.log_label.grid(row=12, column=0)

        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=80, height=50)  # 原始数据录入框
        self.init_data_Text.grid(row=3, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=80, height=50)  # 处理结果展示
        self.result_data_Text.grid(row=3, column=13, rowspan=10, columnspan=10)
        self.text = Entry(self.init_window_name, text='')

        # self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        # self.log_data_Text.grid(row=13, column=0, columnspan=10)

        # 按钮
        # self.file_button = Button(self.init_window_name, text="打开文件", bg="lightblue", width=10, command=self.get_path)  # 调用内部方法  加()为直接调用
        # self.file_button.grid(row=1, column=1)

        # self.dir_button = Button(self.init_window_name, text="打开文件夹", bg="lightblue", width=10, command=self.get_dir)  # 调用内部方法  加()为直接调用
        # self.dir_button.grid(row=1, column=3)

        # self.result_button = Button(self.init_window_name, text="显示比较结果", bg="lightblue", width=10, command=self.get_text)  # 调用内部方法  加()为直接调用
        # self.result_button.grid(row=1, column=13)

        # 滚动条
        self.result_data_scrollbar_x = Scrollbar(self.init_window_name)  # 创建纵向滚动条
        self.result_data_scrollbar_x.config(command=self.result_data_Text.yview)  # 将创建的滚动条通过command参数绑定到需要拖动的Text上
        self.result_data_Text.config(yscrollcommand=self.result_data_scrollbar_x.set)  # Text反向绑定滚动条
        self.result_data_scrollbar_x.grid(row=3, column=10, rowspan=15, sticky='NS')
        self.result_data_scrollbar_y = Scrollbar(self.init_window_name)  # 创建纵向滚动条
        self.result_data_scrollbar_y.config(command=self.result_data_Text.yview)  # 将创建的滚动条通过command参数绑定到需要拖动的Text上
        self.result_data_Text.config(yscrollcommand=self.result_data_scrollbar_y.set)  # Text反向绑定滚动条
        self.result_data_scrollbar_y.grid(row=3, column=33, rowspan=15, sticky='NS')

        self.init_data_Text.insert(INSERT, "\n提示：尚未导入源文件！\n")

    def startCheck(self):
        self.result_data_Text.insert(INSERT, "========开始检测========\n")
        self.res = []
        init_hash = sim_hash.simhash(file.openfile(self.init_path).split())
        for item in self.check_path:
            s = file.openfile(item)
            item_hash = sim_hash.simhash(s.split())
            name = item.split('/')[-1]
            hamming = init_hash.hamming_distance(item_hash)
            similarity = init_hash.similarity(item_hash)
            self.res.append((item, hamming, similarity))
            self.result_data_Text.insert(INSERT,
                                         "\n" + name + "和源文件的汉明距离为：" + str(hamming) + " 相似度为：" + str(similarity) + "\n")

        self.result_data_Text.insert(INSERT, "\n========所有文件检测完毕========\n")

    def genReport(self):
        if not self.res:
            tkinter.messagebox.showinfo("提示", "\n提示：尚未检测任何文件！\n")
            return
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("原始对照文件:" + self.init_path + "\n")
            for i in self.res:
                f.write("文件:" + i[0] + "与原始对照文件的汉明距离为：" + str(i[1]) + "\t相似度为：" + str(i[2]) + "\n")
        self.result_data_Text.insert(INSERT, "\n已生成报告文件 report.txt")

    def get_file(self):
        filenames = filedialog.askopenfilename(filetypes=[("文本文件", ".txt"), ("Word", ".docx")])
        if len(filenames) != 0:
            self.init_data_Text.delete(1.0, 'end')
            self.init_data_Text.insert(INSERT, "\n已导入源文件：\n" + filenames)
            self.init_path = filenames
        else:
            self.init_data_Text.delete(1.0, 'end')
            self.init_data_Text.insert(INSERT, "\n提示：您没有选择任何文件！\n")
            tkinter.messagebox.showinfo("提示", "\n提示：您没有选择任何文件！\n")

    # 返回文件路径名
    def get_path(self):
        filenames = filedialog.askopenfilenames(filetypes=[("文本文件", ".txt"), ("Word", ".docx")])
        if len(filenames) != 0:
            string_filename = "\n==========================================\n检测文件列表：\n"
            self.check_path = []
            for i in range(0, len(filenames)):
                self.check_path.append(filenames[i])
                string_filename += str(filenames[i]) + "\n"
            self.init_data_Text.insert(INSERT, string_filename)
        else:
            self.init_data_Text.insert(INSERT, "您没有选择任何文件")

    # 打开文件夹
    def get_dir(self):
        dirname = filedialog.askdirectory(initialdir="D:/")
        self.check_path = []
        self.init_data_Text.insert(INSERT, "\n==========================================\n拟对比文件列表：\n")
        for filename in os.listdir(dirname):
            if filename.split('.')[-1] == "txt" or filename.split('.')[-1] == "docx":
                self.check_path.append(dirname + '/' + filename)
                self.init_data_Text.insert(INSERT, "\n" + filename)
        if not self.check_path:
            tkinter.messagebox.showinfo("提示", "没有发现可识别的文件类型！")
        else:
            print(self.check_path)

    # 使用指纹库文件
    def get_hash(self):
        self.result_data_Text.insert(INSERT, "========开始检测========\n")
        self.res = []
        self.filehash = {}

        # 导入已生成的hash指纹
        with open("hashdata.json", "r", encoding="utf-8") as f:
            self.filehash = json.load(f)

        # newhash = sim_hash_multiple.simhash(openFile(filepath).split()) # 不使用分词，直接按单词拆分文本

        newhash = dupChecker.sim_hash_multiple.simhash(dupChecker.nlpAnalyzer(dupChecker.openFile(self.init_path), 2))

        for k, v in self.filehash.items():
            hamming = newhash.hamming_distance(v)
            similarity = newhash.similarity(v)
            self.res.append((k, hamming, similarity))
            self.result_data_Text.insert(INSERT,
                                         "\n" + k + "和源文件的汉明距离为：" + str(hamming) + " 相似度为：" + str(similarity) + "\n")

        self.result_data_Text.insert(INSERT, "\n========所有文件检测完毕========\n")


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == "__main__":
    gui_start()
