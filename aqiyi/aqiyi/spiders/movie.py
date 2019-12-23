# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['iqiyi.com']
    start_urls = ['https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='qy-mod-ul']/li")
        print(li_list)
        for li in li_list:
            item = {}
            item['movie_name'] = li.xpath("./div/div[2]/p[1]/a/span/text()").extract_first()
            print(item)
