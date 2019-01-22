
from scrapy.cmdline import execute
from tkinter import *
from tkinter import messagebox

execute(['scrapy', 'crawl', 'statistic'])

top = Tk()
top.attributes("-alpha", 0)
messagebox.showinfo(title="警告", message="不要关闭此窗口,否则关闭程序!程序结束后自动关闭!")


