# -*- coding: utf-8 -*-
import scrapy


class GkSpider(scrapy.Spider):
    name = 'gk'
    allowed_domains = ['guokr.com']
    start_urls = ['https://www.guokr.com/science/category/science']

    def parse(self, response):
        div_list = response.xpath("//*[@id='app']/div[2]/section/div/div[1]/div")
        for div in div_list:
            item = {}
            item['title'] = div.xpath("./div[2]/div[1]/text()").extract_first()
