# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import tarfile

import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request, signals
# from twisted.enterprise import adbapi
from Statistics import settings
from openpyxl import Workbook


#
class StatisticsPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.product_id = spider.product_id
        self.zipName = settings.FILES_STORE + '/%s.zip' % self.product_id
        path = settings.IMAGES_STORE + '/%s/%s.xlsx' % (self.product_id, self.product_id)

        if not os.path.exists(path):
            os.mkdir(settings.IMAGES_STORE + '/%s' % self.product_id)
        file = open(path, 'w')
        file.close()

    # spider关闭时的逻辑
    def spider_closed(self, spider):
        self.adddirfile()

    def process_item(self, item, spider):
        return item

    # 把整个文件夹内的文件打包
    def adddirfile(self):
        # f = zipfile.ZipFile(settings.IMAGES_STORE + '/%s.zip' % self.product_id, 'w', zipfile.ZIP_DEFLATED)
        #
        startdir = settings.IMAGES_STORE + "/%s" % self.product_id  # image folder
        # files = os.listdir(startdir)  # 得到文件夹下的所有文件名称
        # for file in files:
        #     print(os.path.abspath(file))
        #     self.f.write(os.path.abspath(file))
        #
        # f.close()
        tf = tarfile.open(self.zipName, 'w:gz')
        tf.add(startdir)
        tf.close()


class ExcelPipeline(object):
    def __init__(self):
        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        # 设置表头
        self.ws.append(['CAPACITY', 'COLOR', 'LOGISTICS', 'DATETIME', 'COUNTRY'])

    def process_item(self, item, spider):
        self.product_id = item[item.PRODUCT_ID]
        path = settings.IMAGES_STORE + '/%s/%s.xlsx' % (self.product_id, self.product_id)
        if not os.path.exists(path):
            file = open(path, 'w')
            file.close()
        # 整理每一项（行）数据
        line = [item[item.CAPACITY], item[item.COLOR], item[item.LOGISTICS], item[item.DATETIME], item[item.COUNTRY]]
        # 将数据添加到xlsx中
        self.ws.append(line)
        # 保存xlsx文件
        self.wb.save(path)
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
