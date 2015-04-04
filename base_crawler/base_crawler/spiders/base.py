import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class base_spider(CrawlSpider):
	
	name = 'base';

	def __init__(self, **kw):
		super(base_spider, self).__init__(**kw);
		self.name = kw.get('name');
		self.allowed_domains = kw.get('allowed_domains');
		self.start_urls = kw.get('start_urls');
		self.rules = (
			Rule(LinkExtractor(allow=
	

