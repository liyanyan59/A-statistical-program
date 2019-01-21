# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 16:23
# @Author  : LY
# @FileName: tools
# @Software: PyCharm
# @Official Accounts：大数据学习废话集
from tkinter import *
from tkinter import messagebox

import os


def get_product_id():
    base_url = get_base_url()
    product_id = re.findall("productId=(\d+)", base_url)
    while not product_id:
        top = Tk()
        top.attributes("-alpha", 0)
        messagebox.showinfo(title="重新输入!", message="您输入了一个错误连接!")
        top.destroy()

        base_url = get_base_url()
        product_id = re.findall("productId=(\d+)", base_url)
    product_id = int(product_id[0])
    return product_id


def get_base_url():
    def close_callback():
        os._exit(0)
    top = Tk()
    top.geometry('650x230')

    L1 = Label(top, text="输入网站")
    L1.place(x=14, y=50)
    e = StringVar()
    text = Entry(top, textvariable=e, width=180)
    text.place(x=14, y=80)
    B = Button(top, text="确认", command=lambda: top.destroy())
    B.place(x=14, y=150)
    # text.bind('<Return>', get_text())
    # text.pack()
    text.focus_set()
    top.protocol("WM_DELETE_WINDOW", close_callback)
    top.mainloop()

    base_url = e.get()

    return base_url
