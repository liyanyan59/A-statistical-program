# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 16:23
# @Author  : LY
# @FileName: tools
# @Software: PyCharm
# @Official Accounts：大数据学习废话集
from tkinter import *


def get_product_id():
    top = Tk()
    L1 = Label(top, text="网站名")
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    B = Button(top, text="确认",)
    top.mainloop()

    productId = E1.get()
    return productId