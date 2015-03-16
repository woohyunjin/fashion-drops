# -*- coding: utf-8 -*-

# Scrapy settings for stylenanda project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stylenanda'

SPIDER_MODULES = ['stylenanda.spiders']
NEWSPIDER_MODULE = 'stylenanda.spiders'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ko',
}

DOWNLOAD_DELAY = 1.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stylenanda (+http://www.yourdomain.com)'

