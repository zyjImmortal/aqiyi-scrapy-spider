# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['iqiyi.com']
    start_urls = ['https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html']

    def parse(self, response):

        li_list = response.xpath("//ul[@class='qy-mod-ul']/li")
        for li in li_list:
            item = {}
            item['img_url'] = "https:" + li.xpath('./div/div[1]/a/@href').extract_first()
            # a标签下面有span标签，这里xpath无需加span。a/text()可直接获取span里的文本
            item['movie_name'] = li.xpath("./div/div[2]/p[1]/a/text()").extract_first()
            print(item)
