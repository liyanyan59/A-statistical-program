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
        self.product_id = 11111
        file = open(settings.FILES_STORE + '/%s.xlsx' % self.product_id, 'w')
        file.close()
        self.f = zipfile.ZipFile(settings.FILES_STORE + '/%s.zip' % self.product_id, 'w', zipfile.ZIP_DEFLATED)
        self.adddirfile()
        self.addzip()
        self.f.close()



    def addzip(self):
        f = zipfile.ZipFile(settings.FILES_STORE + '%s.zip' % self.product_id, 'w', zipfile.ZIP_DEFLATED)
        f.write(settings.FILES_STORE + '/%s.xlsx' % self.product_id)
        f.close()


    # 把整个文件夹内的文件打包

    def adddirfile(self):
        startdir = settings.FILES_STORE + "%s" % self.product_id  # image folder
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                self.f.write(os.path.join(dirpath, filename))

if __name__=="__main__":
    OPO().main()