# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FashionCrawlerItem(scrapy.Item):
	url = scrapy.Field()
	name = scrapy.Field()
	price = scrapy.Field()
	mall_name = scrapy.Field()
	p_code = scrapy.Field()
	image_url = scrapy.Field()

