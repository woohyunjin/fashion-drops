import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader

from fashion_crawler.items import FashionCrawlerItem 

class StyleNanda_Spider(CrawlSpider):
	name = "stylenanda"
	allowed_domains = ["stylenanda.com"]
	start_urls = ["http://www.stylenanda.com/"]
	rules = (
				Rule(LinkExtractor(allow=('category\.php', ))),
				Rule(LinkExtractor(allow=('product\.php', )), callback='parse_item'),
			)

	def parse_item(self, response):
		loader = ItemLoader(item=FashionCrawlerItem(), response=response);
		loader.add_value('url', response.url);
		loader.add_css('name', "input#script_product_name::attr(value)");
		loader.add_css('price', "span#main_price::text");
		loader.add_value('mall_name', self.name);
		loader.add_css('p_code', "input[name='product_no']::attr(value)");
		loader.add_css('image_url', "img[name='big_img']::attr(src)");
		return loader.load_item()
	
		# create base spider class with all explanations
		# draw the basics on JustinMind
		# set up Flask
		
