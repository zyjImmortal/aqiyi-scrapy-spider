# -*- coding: utf-8 -*-
import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.iqiyi.com/']
    start_urls = ['http://www.iqiyi.com//']

    def parse(self, response):
        pass
