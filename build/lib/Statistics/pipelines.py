# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import zipfile

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
        self.zipName = settings.IMAGES_STORE + '/%s.zip' % self.product_id
        # 创建文件
        path = settings.IMAGES_STORE + '/%s/%s.xlsx' % (self.product_id, self.product_id)

        if not os.path.exists(path):
            os.mkdir(settings.IMAGES_STORE + '/%s' % self.product_id)
        file = open(path, 'w')
        file.close()

    # spider关闭时的逻辑
    def spider_closed(self, spider):
        # 打包
        self.adddirfile()

        os.system("rm -rf "+settings.IMAGES_STORE+"/%s.t" % self.product_id)  # 删除状态文件
        # os.system("rm -rf "+settings.IMAGES_STORE+"/%s/" % self.product_id)   # 删除文件夹
        os.system("killall -9 chrome")
        os.system("killall -9 chromedriver")  # 回收内存

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
        file_news = startdir + '.zip'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()


class ExcelPipeline(object):
    def __init__(self):
        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active

    def process_item(self, item, spider):

        # 设置表头
        head = []

        if list(self.ws.rows):
            for cell in list(self.ws.rows)[0]:  # 原有表头
                head.append(cell.value)   # 为了防止一些数据span数量不同的问题的出现

        for key in item[item.INFOS]:
            if key.upper() not in head:
                head.append(key.upper())
        if ('DATETIME' and 'COUNTRY') not in head:
            head.append('DATETIME')
            head.append('COUNTRY')
        for i in range(len(head)):
            self.ws.cell(row=1, column=i+1).value = head[i]
        # self.ws.append(head)

        self.product_id = item[item.PRODUCT_ID]
        path = settings.IMAGES_STORE + '/%s/%s.xlsx' % (self.product_id, self.product_id)
        # 整理每一项（行）数据
        line = [''] * len(head)
        for key in item[item.INFOS]:
            line[head.index(key.upper())] = item[item.INFOS][key]
        line[head.index('DATETIME')] = item[item.DATETIME]
        line[head.index('COUNTRY')] = item[item.COUNTRY]

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
