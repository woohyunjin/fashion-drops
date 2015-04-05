import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Identity, Compose

from fashion_crawler.items import FashionCrawlerItem

class Naning9_Spider(CrawlSpider):
	name = "naning9"
	allowed_domains = ["naning9.com"]
	start_urls = ["http://www.naning9.com"]
	rules = (
		Rule(LinkExtractor(allow=('shop\/shopdetail\.html', )), callback='parse_item'),
	)

	def parse_item(self, response):
		loader = ItemLoader(item=FashionCrawlerItem(), response=response);
		loader.add_value('url', response.url);
		loader.add_xpath('name', "//*[@id='lens_img']/@alt");
		loader.add_css('price', "font span span#mk_price_value::text");
		loader.add_value('mall_name', self.name);
		loader.add_css('p_code', "input[name='branduid']::attr(value)", TakeFirst());
		loader.add_xpath('image_url', "//*[@id='lens_img']/@src");
		return loader.load_item();
