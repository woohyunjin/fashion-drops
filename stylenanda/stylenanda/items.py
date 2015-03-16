# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StylenandaItem(scrapy.Item):
	product_name = scrapy.Field();
	price = scrapy.Field();
	reward_points = scrapy.Field();
	product_code = scrapy.Field();
    
