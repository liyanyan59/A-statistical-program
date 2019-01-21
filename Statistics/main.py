
from scrapy.cmdline import execute


execute(['scrapy', 'crawl', 'statistic'])

# totalpage = int(response.xpath('//label[@class="ui-label"]/text()').extract_first().split('/')[-1])
# for page in range(totalpage):
#     # 容量
#     capacities = response.xpath('//span[@class="first"]')
#
#     # 颜色
#     colors = response.xpath('//span[contains(string(.),"Color")]')
#
#     # 物流
#     logistics = response.xpath('//span[contains(string(.),"Logistics")]')
#
#     # 日期时间
#     datetimes = response.xpath('//dl[@class="buyer-review"]/dd[@class="r-time"]/text()').extract()
#
#     # 国家
#     countries = response.xpath('//div[@class="user-country"]/b/text()').extract()
#
#     # 图片
#     img = response.xpath('//ul[@class="util-clearfix"]')
#
#     for i in range(10):
#         item = Item()
#
#         # 容量
#         capacity = capacities[i].xpath('string(.)').extract_first()
#         capacity = re.search("\d{3}-\d{3}ml", capacity).group(0)
#
#         # 颜色
#         color = colors[i].xpath('string(.)').extract_first()
#         color = color.split(":")[-1].strip()
#
#         # 物流
#         logistics = logistics[i].xpath('string(.)').extract_first()
#         logistics = logistics.split(":")[-1].strip()
#
#         # 日期时间
#         datetime = datetimes[i]
#
#         # 国家
#         country = countries[i]
#
#         # 图片
#         image_urls = img[i].xpath('/li/img/@src')
#
#         item[Item.CAPACITY] = capacity
#         item[Item.COLOR] = color
#         item[Item.LOGISTICS] = logistics
#         item[Item.DATETIME] = datetime
#         item[Item.COUNTRY] = country
#         item[Item.IMAGE_URLS] = image_urls