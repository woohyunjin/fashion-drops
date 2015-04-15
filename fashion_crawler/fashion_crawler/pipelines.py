# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FashionCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):
	def __init__(self):
		self.p_code_seen = set()
	
	def process_item(self, item, spider):		
		if item['p_code'][0] in self.p_code_seen:
			raise DropItem("Duplicate item found: [%s]" % item['p_code'][0])
		else: 
			self.p_code_seen.add(item['p_code'][0])
			return item
