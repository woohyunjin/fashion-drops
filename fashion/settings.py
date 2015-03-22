# -*- coding: utf-8 -*-

# Scrapy settings for naning9 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

PROJECT = 'fashion'
BOT_NAME = PROJECT

#DOMAINS = ['naning9, stylenanda']

SPIDER_MODULES = [PROJECT + '.spiders']
NEWSPIDER_MODULE = PROJECT + '.spiders'

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
	PROJECT + '.pipelines.DuplicatesPipeline': 900,
}

FEED_URI = 'result/%(name)s/export_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORTERS = {
    'csv': PROJECT + '.exporter.MyCsvItemExporter',
}
CSV_DELIMITER = '\t'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'naning9 (+http://www.yourdomain.com)'
