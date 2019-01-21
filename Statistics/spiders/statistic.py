# -*- coding: utf-8 -*-
import re

import scrapy
from Statistics.items import StatisticsItem as Item
from selenium import webdriver
import time
from scrapy.selector import Selector


class StatisticSpider(scrapy.Spider):
    name = 'statistic'
    allowed_domains = ['feedback.aliexpress.com']
    start_urls = ['https://feedback.aliexpress.com/display/productEvaluation.htm?productId=32956338726'
                  '&ownerMemberId=235021169&companyId=244265688&memberType=seller&startValidDate=&i18n=true']

    driver = webdriver.PhantomJS()
    driver.get(start_urls[0])

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
                capacity = re.search("\d{3}-\d{3}ml", capacity).group(0)

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


                yield item

            self.driver.find_element_by_xpath('//a[contains(text(),"Next")]').click()

            time.sleep(3)
            response = self.driver.page_source
            response = Selector(text=response)

        self.driver.close()






