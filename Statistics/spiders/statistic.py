# -*- coding: utf-8 -*-
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

import re
from urllib.parse import urljoin

import os

import requests
import scrapy

from Statistics.items import StatisticsItem as Item
from selenium import webdriver
import time
from scrapy.selector import Selector

from Statistics.settings import IMAGES_STORE


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

        #
        # self.start_urls = ['https://feedback.aliexpress.com/display/productEvaluation.htm?'
        #                    'productId=%s&ownerMemberId=235021169' % self.product_id]

        os.system("touch "+IMAGES_STORE+"/%s.t" % self.product_id)   # 创建状态文件

        # option = webdriver.ChromeOptions()
        # option.add_argument("--headless")
        # option.add_argument('--no-sandbox')
        # option.add_argument('--disable-gpu')
        # self.driver = webdriver.Chrome(chrome_options=option)
        # self.driver.get(url)
        self.s = requests.Session()
        res = self.s.get(url)
        sel = Selector(response=res)
        url = sel.xpath('//iframe[contains(@thesrc,"feedback.aliexpress.com")]/@thesrc').extract_first()
        url = urljoin('https://feedback.aliexpress.com', url)

        self.start_urls = []
        self.start_urls.append(url)

    def parse(self, response):
        data = {'evaSortValue': 'sortlarest@feedback'}

        if not response.xpath('//div[@class="no-feedback wholesale-product-feedback"]'):
            yield scrapy.Request(url=response.url, callback=self.parse_detail, meta={'res': response, 'data': {}})
        else:
            elem = response.xpath('//a[@class="fb-sort-list-href"]')
            if elem:
                res = self.s.post(response.url, data=data)
                # self.driver.find_element_by_xpath('//a[@class="fb-sort-list-href"]').click()
                sel = Selector(response=res)
                if sel.xpath('//div[@class="no-feedback wholesale-product-feedback"]'):
                    pass
                else:
                    yield scrapy.Request(url=response.url, callback=self.parse_detail, meta={'res': sel, 'data': data})

    def parse_detail(self, response):
        res_url = response.url
        if response.meta:
            meta = response.meta
            response = meta['res']
            data = meta['data']
        totalpage = int(response.xpath('//label[@class="ui-label"]/text()').extract_first().split('/')[-1])
        for page in range(totalpage):

            infos = response.xpath('//div[@class="user-order-info"]')

            # 日期时间
            datetimes = response.xpath('//dl[@class="buyer-review"]/dd[@class="r-time"]/text()').extract()

            # 国家
            countries = response.xpath('//div[@class="user-country"]/b/text()').extract()

            # 图片
            image_urls = response.xpath('//ul[@class="util-clearfix"]/li/img/@src').extract()

            for i in range(len(countries)):
                item = Item()

                spans = infos[i].xpath('span')
                item[Item.INFOS] = {}

                for span in spans:
                    key = span.xpath('strong/text()').extract_first().replace(':', '')
                    value = span.xpath('string(.)').extract_first()
                    value = value.split(":")[-1].replace('\t', '').replace('\n', '').replace(' ', '')
                    item[Item.INFOS][key] = value

                    # 日期时间
                datetime = datetimes[i]

                # 国家
                country = countries[i]

                # 图片
                if i == 0:
                    item[Item.IMAGE_URLS] = image_urls
                else:
                    item[Item.IMAGE_URLS] = None

                # item[Item.CAPACITY] = capacity
                # item[Item.COLOR] = color
                # item[Item.LOGISTICS] = logistics
                item[Item.DATETIME] = datetime
                item[Item.COUNTRY] = country
                item[Item.PRODUCT_ID] = self.product_id

                yield item
            if response.xpath('//a[contains(text(),"Next")]'):
                # time.sleep(3)
                data['page'] = page+2
                res = self.s.post(res_url, data=data)
                response = Selector(response=res)

                # self.driver.find_element_by_xpath('//div[@class="ui-pagination ui-pagination-front ui-pagination-pager util-right"]/a[contains(text(),"Next")]').click()
                # response = self.driver.page_source
                # response = Selector(text=response)
            else:
                break

        # self.driver.close()
        # self.driver.quit()

# # 创建一个进程
# process = CrawlerProcess(get_project_settings())
# # 'followall' is the name of one of the spiders of the project.
# process.crawl(StatisticSpider)  # 避开命令行
# process.start()
