# -*- coding: utf-8 -*-
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

import re
import scrapy

from Statistics.items import StatisticsItem as Item
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

    def __init__(self):  # , url=None, *args, **kwargs
        # super(StatisticSpider, self).__init__(*args, **kwargs)
        url = 'https://www.aliexpress.com/item/iHaitun-L-Type-C-Cable-Adapter-For-Huawei-Mate-20-Pro-10-P20-Xiaomi-Splitter-Audio/32960853697.html?spm=a2g01.11146674.layer-iabdzn.13.608bcbb8SgZWdz&gps-id=6046422&scm=1007.16233.92932.0&scm_id=1007.16233.92932.0&scm-url=1007.16233.92932.0&pvid=ecbfc7b2-8313-47b2-bc0a-490c5586757f'
        if re.findall("productId=(\d+)", url):
            self.product_id = re.findall("productId=(\d+)", url)[0]
        else:
            self.product_id = re.findall("(\d+).html", url)[0]

        self.start_urls = ['https://feedback.aliexpress.com/display/productEvaluation.htm?'
                           'productId=%s&ownerMemberId=235021169' % self.product_id]

        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.get(self.start_urls[0])

    def parse(self, response):
        if not response.xpath('//div[@class="no-feedback wholesale-product-feedback"]'):
            yield scrapy.Request(url=response.url, callback=self.parse_detail)
        else:
            elem = response.xpath('//a[@class="fb-sort-list-href"]')
            if elem:
                self.driver.find_element_by_xpath('//a[@class="fb-sort-list-href"]').click()
                res = Selector(text=self.driver.page_source)
                if res.xpath('//div[@class="no-feedback wholesale-product-feedback"]'):
                    pass
                else:
                    yield scrapy.Request(url=response.url, callback=self.parse_detail, meta={'res': res})

    def parse_detail(self, response):
        if response.meta:
            response = response.meta['res']
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
                capacity = capacity.replace('\\t', '').replace('\\n', '')
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
