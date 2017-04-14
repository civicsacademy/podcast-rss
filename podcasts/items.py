# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PodcastsItem(scrapy.Item):
    file = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
