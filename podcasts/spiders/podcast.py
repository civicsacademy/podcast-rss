# -*- coding: utf-8 -*-
import scrapy
import re
from podcasts.items import PodcastsItem
from HTMLParser import HTMLParser
import requests


class PodcastSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(PodcastSpider, self, *args, **kwargs).__init__()
        self.h = HTMLParser()

    name = "podcast"
    allowed_domains = ["www.civicsacademy.co.za"]
    start_urls = [
        'http://www.civicsacademy.co.za/podcasts/page/1',
        'http://www.civicsacademy.co.za/podcasts/page/2',
        'http://www.civicsacademy.co.za/podcasts/page/3',
        'http://www.civicsacademy.co.za/podcasts/?category=introduction-to-democracy',
        'http://www.civicsacademy.co.za/podcasts/?category=justice-human-rights',
        'http://www.civicsacademy.co.za/podcasts/?category=separation-of-powers',
        'http://www.civicsacademy.co.za/podcasts/?category=political-parties',
        'http://www.civicsacademy.co.za/podcasts/?category=elections',
        'http://www.civicsacademy.co.za/podcasts/?category=economics',
    ]

    def parse(self, response):
        for onclick in response.css('.popularinner').xpath('@onclick').extract():
            url = re.sub(r"^window.location='(.+)'$", r"\1", onclick)
            yield scrapy.Request(url, callback=self.parse_podcast)

    def parse_podcast(self, response):
        title = response.css('.podcasttitle::text').extract()[0]
        uri = response.xpath("//a[text()='Download file to listen later']/@href").extract()[0]
        description = response.css('.postcontent').xpath('string()').extract()[0]

        r = requests.get(uri, stream=True)
        local_filename = uri.split('/')[-1]
        with open('content/audio/' + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        item = PodcastsItem()
        item['title'] = title
        item['file'] = 'audio/' + local_filename
        item['description'] = self.h.unescape(description)
        return item
