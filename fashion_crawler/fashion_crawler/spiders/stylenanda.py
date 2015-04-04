import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader

from fashion-crawler.items import FashionCrawlerItem 

class StyleNanda_Spider(CrawlSpider):
		name = "stylenanda"
		allowed_domains = ["stylenanda.com"]
		start_urls = ["http://www.stylenanda.com"]
		rules = (
					Rule(LinkExtractor(allow=('category\.php', ))),
					Rule(LinkExtractor(allow=('product\.php', )), callback='parse_item'),
		)
		
		def parse_item(self, response):
			self.log("[%s:%s] A response has arrived!" % (self.name, response.url);
			loader = ItemLoader(item=FashionCrawlerItem, response=response);
			loader.item['url'] = response.url;
			#for each field in the items, add extractor, take first, unicode

			return loader.load_item()
			
			#fill in the parse_item function
			#work on tab auto indentation 
			#create base spider class with all explanations
			#create spider class for naning9
			#start crawling (mind language settings and crawl speed)
			#check validity of crawled data
			#send it off to donghyun
			#clean up directory and commit + push
			#check github
			#draw the basics on JustinMind
			#set up Flask
		
