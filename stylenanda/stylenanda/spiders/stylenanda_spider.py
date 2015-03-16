import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class StyleNandaSpider(CrawlSpider):
	name = "stylenanda";
	allowed_domains = ["stylenanda.com"];
	start_urls = ["http://www.stylenanda.com/"];

	rules = (
		Rule(LinkExtractor(allow=('category\.php', ))),
		Rule(LinkExtractor(allow=('product\.php', )), callback='parse_item'),
	)

	def parse_item(self, response):
		self.log("A response from %s just arrived!" % response.url);
		
	
