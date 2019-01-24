# -*- coding: utf-8 -*-
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

import re
import scrapy
from scrapy import signals
import os
import zipfile

from Statistics.items import StatisticsItem as Item
from Statistics import settings
from selenium import webdriver
import time
from scrapy.selector import Selector
# from tkinter import *
# from tkinter import messagebox
#
# import os
#
#
# def get_product_id():
#     base_url = get_base_url()
#     product_id = re.findall("productId=(\d+)", base_url)
#     while not product_id:
#         top = Tk()
#         top.attributes("-alpha", 0)
#         messagebox.showinfo(title="重新输入!", message="您输入了一个错误连接!")
#         top.destroy()
#
#         base_url = get_base_url()
#         product_id = re.findall("productId=(\d+)", base_url)
#     product_id = int(product_id[0])
#     return product_id
#
#
# def get_base_url():
#     def close_callback():
#         os._exit(0)
#     top = Tk()
#     top.geometry('650x230')
#
#     L1 = Label(top, text="输入网站")
#     L1.place(x=14, y=50)
#     e = StringVar()
#     text = Entry(top, textvariable=e, width=180)
#     text.place(x=14, y=80)
#     B = Button(top, text="确认", command=lambda: top.destroy())
#     B.place(x=14, y=150)
#     # text.bind('<Return>', get_text())
#     # text.pack()
#     text.focus_set()
#     top.protocol("WM_DELETE_WINDOW", close_callback)
#     top.mainloop()
#
#     base_url = e.get()
#
#     return base_url


class StatisticSpider(scrapy.Spider):
    name = 'statistic'
    allowed_domains = ['feedback.aliexpress.com']

    def __init__(self, url=None, *args, **kwargs):  #
        super(StatisticSpider, self).__init__(*args, **kwargs)
        # url = 'https://www.aliexpress.com/item/OUOH-2017-New-500ML-Creative-Collapsible-Foldable-Silicone-drink-Sports-Water-Bottle-Camping-Travel-bicycle-bottle/32792915807.html?spm=2114.10010108.1000014.3.e85f5795ASt5Gp&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.13338.110449.000000000000000&scm_id=1007.13338.110449.000000000000000&scm-url=1007.13338.110449.000000000000000&pvid=b19d41c1-fc7e-4371-8337-87075b7644a7'
        if re.findall("productId=(\d+)", url):
            self.product_id = re.findall("productId=(\d+)", url)[0]
        else:
            self.product_id = re.findall("(\d+).html", url)[0]

        self.start_urls = ['https://feedback.aliexpress.com/display/productEvaluation.htm?'
                           'productId=%s&ownerMemberId=235021169' % self.product_id]

        self.driver = webdriver.PhantomJS()
        self.driver.get(self.start_urls[0])


    def parse(self, response):
        totalpage = int(response.xpath('//label[@class="ui-label"]/text()').extract_first().split('/')[-1])
        for page in range(totalpage):
            # 容量
            capacities = response.xpath('//span[@class="first"]')

            # 颜色
            colors = response.xpath('//span[contains(string(.),"Color")]')

            # 物流
            Logistics = response.xpath('//span[contains(string(.),"Logistics")]')

            # 日期时间
            datetimes = response.xpath('//dl[@class="buyer-review"]/dd[@class="r-time"]/text()').extract()

            # 国家
            countries = response.xpath('//div[@class="user-country"]/b/text()').extract()

            # 图片
            image_urls = response.xpath('//ul[@class="util-clearfix"]/li/img/@src').extract()

            for i in range(len(countries)):
                item = Item()

                # 容量
                capacity = capacities[i].xpath('string(.)').extract_first()
                # capacity = re.search("\d+-\d+ml", capacity).group(0)

                # 颜色
                color = colors[i].xpath('string(.)').extract_first()
                color = color.split(":")[-1].strip()

                # 物流
                logistics = Logistics[i].xpath('string(.)').extract_first()
                logistics = logistics.split(":")[-1].strip()

                # 日期时间
                datetime = datetimes[i]

                # 国家
                country = countries[i]

                # 图片
                if i == 0:
                    item[Item.IMAGE_URLS] = image_urls
                else:
                    item[Item.IMAGE_URLS] = None

                item[Item.CAPACITY] = capacity
                item[Item.COLOR] = color
                item[Item.LOGISTICS] = logistics
                item[Item.DATETIME] = datetime
                item[Item.COUNTRY] = country
                item[Item.PRODUCT_ID] = self.product_id

                yield item
            if response.xpath('//a[contains(text(),"Next")]'):
                time.sleep(3)
                self.driver.find_element_by_xpath('//a[contains(text(),"Next")]').click()

                response = self.driver.page_source
                response = Selector(text=response)
            else:
                break

        self.driver.close()


# # 创建一个进程
# process = CrawlerProcess(get_project_settings())
# # 'followall' is the name of one of the spiders of the project.
# process.crawl(StatisticSpider)  # 避开命令行
# process.start()
