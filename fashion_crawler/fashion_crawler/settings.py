# -*- coding: utf-8 -*-

# Scrapy settings for fashion_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

PROJECT = 'fashion_crawler'
BOT_NAME = PROJECT

SPIDER_MODULES = ['fashion_crawler.spiders']
NEWSPIDER_MODULE = 'fashion_crawler.spiders'

DEFAULT_REQUEST_HEADERS = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'ko',
}

DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
	PROJECT + '.pipelines.FashionCrawlerPipeline': 300,
	PROJECT + '.pipelines.DuplicatesPipeline': 200,
}

FEED_URI = 'result/%(name)s/export_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORTERS = {
    'csv': PROJECT + '.exporter.FashionCrawlerCsvItemExporter',
}
CSV_DELIMITER = '\t'

FIELDS_TO_EXPORT = [
	'name',
	'price',
	'p_code',
	'mall_name',
	'image_url',
	'url',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fashion_crawler (+http://www.yourdomain.com)'
