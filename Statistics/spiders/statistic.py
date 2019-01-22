# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import re
import scrapy
from Statistics.items import StatisticsItem as Item
from selenium import webdriver
import time
from scrapy.selector import Selector
from Statistics.util.tools import get_product_id


class StatisticSpider(scrapy.Spider):
    name = 'statistic'
    allowed_domains = ['feedback.aliexpress.com']

    def __init__(self):

        self.product_id = get_product_id()
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

            for i in range(10):
                item = Item()

                # 容量
                capacity = capacities[i].xpath('string(.)').extract_first()
                capacity = re.search("\d+-\d+ml", capacity).group(0)

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

            self.driver.find_element_by_xpath('//a[contains(text(),"Next")]').click()

            time.sleep(3)
            response = self.driver.page_source
            response = Selector(text=response)

        self.driver.close()

#
# # 创建一个进程
# process = CrawlerProcess(get_project_settings())
# # 'followall' is the name of one of the spiders of the project.
# process.crawl(StatisticSpider)  # 避开命令行
# process.start()
