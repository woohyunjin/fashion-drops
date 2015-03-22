import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class StyleNandaSpider(CrawlSpider):
	name = "stylenanda";
	allowed_domains = ["stylenanda.com"];
	start_urls = ["http://www.stylenanda.com/"];
	file_name = "stylenanda_data.txt";
	output_file = open(file_name, 'w');
	output_file.write("");
	output_file.close();

	rules = (
		Rule(LinkExtractor(allow=('category\.php', ))),
		Rule(LinkExtractor(allow=('product\.php', )), callback='parse_item'),
	)

	def parse_item(self, response):
		self.log("A response from %s just arrived!" % response.url);
		with open("stylenanda_data.txt", 'a') as file:
			file.write(response.url + "\n");
			file.write(response.css("meta[name='Description']::attr(content)").extract().pop().encode('utf-8') + "\n");
			file.write(response.css("span#main_price::text").extract().pop().encode('utf-8') + "\n");
			file.write(response.css("meta[property='og:image']::attr(content)").extract().pop().encode('utf-8') + "\n");
			file.write(response.css("input#product_code::attr(value)").extract().pop().encode('utf-8') + "\n");
			file.write("\n");		
	
