# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy.contrib.loader.processor import TakeFirst, Identity, Compose

from fashion.items import FashionItem

class Naning9Spider(CrawlSpider):
	name = "naning9"
	allowed_domains = ["naning9.com"]
	start_urls = (
		'http://www.naning9.com/',
	)

	rules = (
		# and follow links from them (since no callback means follow=True by default).
		#Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
		# Extract links matching 'item.php' and parse them with the spider's method parse_item
		Rule(LinkExtractor(allow=('shop\/shopdetail\.html', )), callback='parse_item_with_loader'),
		#Rule(LinkExtractor(allow=('shop\/shopdetail\.html', )), callback='parse_item'),
	)

	def parse_item_with_loader(self, response):
		root = 'http://www.naning9.com/'
		sel_map = {
			'pic' : '//*[@id="lens_img"]/@src',
			'name' : '//*[@id="contents"]/div[2]/div[2]/p/text()[3]',
			'maker' : '//*[@id="contents"]/div[2]/div[2]/div[1]/table//tr[1]/td/text()',
			'price' : '//*[@id="mk_price_value"]/text()'
		}

		loader = ItemLoader(item=FashionItem(), response=response)
		loader.item['url'] = response.url

		for (key, s) in sel_map.iteritems():
			loader.add_xpath(key, s, TakeFirst(), unicode.strip)

		return loader.load_item()


	def parse_item(self, response):
		root = 'http://www.naning9.com/'
		sel_map = {
			'pic' : '//*[@id="lens_img"]/@src',
			'name' : '//*[@id="contents"]/div[2]/div[2]/p/text()[3]',
			'maker' : '//*[@id="contents"]/div[2]/div[2]/div[1]/table//tr[1]/td/text()',
			'price' : '//*[@id="mk_price_value"]/text()'
		}

		invalid = False

		item = FashionItem()
		item['url'] = response.url

		for (key, s) in sel_map.iteritems():
			nlist = response.xpath(s).extract()
			if nlist:# and len(nlist) == 1:
				item[key] = nlist[0].strip()
			else:
				invalid = True
				break

		return item
