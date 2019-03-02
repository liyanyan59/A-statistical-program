# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 20:48
# @Author  : LY
# @FileName: test
# @Software: PyCharm
# @Official Accounts：大数据学习废话集
import zipfile

import os

import settings


class OPO:
    def main(self):
        self.adddirfile()



    # 把整个文件夹内的文件打包

    def adddirfile(self):
        startdir = "E:\\Statistics\\32956338726"  # 要压缩的文件夹路径
        file_news = startdir + '.zip'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()

    def a(self):
        path = 'G:\\迅雷下载\\1969635228\\1969635228.xlsx'

        file = open(path, 'w')
        file.close()


if __name__=="__main__":
    OPO().a()
