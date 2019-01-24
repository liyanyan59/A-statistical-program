# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import zipfile

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
# from twisted.enterprise import adbapi
from Statistics import settings
from openpyxl import Workbook


class StatisticsPipeline(object):

    def process_item(self, item, spider):

        return item

    def open_spider(self, spider):
        # 创建zip文件
        pass

    def close_spider(self, item, spider):
        self.product_id = item[item.PRODUCT_ID]
        self.adddirfile()
        # self.addzip()
        pass

    def addzip(self):
        f = zipfile.ZipFile(settings.FILES_STORE+'%s.zip' % self.product_id, 'w', zipfile.ZIP_DEFLATED)
        f.write(settings.FILES_STORE+'%s.xlsx' % self.product_id)
        f.close()
    pass

    # 把整个文件夹内的文件打包

    def adddirfile(self):
        f = zipfile.ZipFile(settings.FILES_STORE+'%s.zip' % self.product_id, 'w', zipfile.ZIP_DEFLATED)
        startdir = settings.FILES_STORE+"%s" % self.product_id  # image folder
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                f.write(os.path.join(dirpath, filename))
        f.close()


class ExcelPipeline(object):
    def __init__(self):
        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        # 设置表头
        self.ws.append(['CAPACITY', 'COLOR', 'LOGISTICS', 'DATETIME', 'COUNTRY'])

    def process_item(self, item, spider):
        # 整理每一项（行）数据
        line = [item[item.CAPACITY], item[item.COLOR], item[item.LOGISTICS], item[item.DATETIME], item[item.COUNTRY]]
        # 将数据添加到xlsx中
        self.ws.append(line)
        # desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
        # 保存xlsx文件
        self.wb.save(settings.FILES_STORE+'/%s.xlsx' % (item[item.PRODUCT_ID]))
        return item


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.product_id = item[item.PRODUCT_ID]
        if item[item.IMAGE_URLS]:
            for url in item[item.IMAGE_URLS]:
                yield Request(url)

    def file_path(self, request, response=None, info=None):
        # desktop = os.path.join(os.path.expanduser("~"), 'Desktop')
        return '/%s/%s' % (self.product_id, request.url.split('/')[-1])


# class StatisticsPipeline:
#     def __init__(self):
#         db = settings.MYSQL_DB_NAME
#         host = settings.MYSQL_HOST
#         port = settings.MYSQL_PORT
#         user = settings.MYSQL_USER
#         passwd = settings.MYSQL_PASSWORD
#
#         self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, db=db, user=user,
#                                             passwd=passwd, charset='utf8')
#
#     def close_spider(self, spider):
#         self.dbpool.close()
#
#     def process_item(self, item, spider):
#         self.dbpool.runInteraction(self.insert_db, item)
#         return item
#
#     def insert_db(self, tx, item):
#         values = (
#             item[item.CAPACITY],
#             item[item.COLOR],
#             item[item.LOGISTICS],
#             item[item.DATETIME],
#             item[item.COUNTRY],
#         )
#
#         sql = 'INSERT INTO statistic VALUES(%s, %s, %s, %s, %s)'
#         tx.execute(sql, values)
