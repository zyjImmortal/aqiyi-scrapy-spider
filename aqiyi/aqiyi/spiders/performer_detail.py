# -*- coding: utf-8 -*-
import time

import scrapy



class PerformerDetailSpider(scrapy.Spider):
    name = 'performer_detail'
    allowed_domains = ['iqiyi.com']
    start_urls = ['https://www.iqiyi.com/lib/s_214783005.html']

    def parse(self, response):
        print(response.text)
        detail = {}
        detail['name'] = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        detail['occupation'] = response.xpath("normalize-space(//li[@itemprop='jobTitle']/text())").extract_first()
        detail['width'] = response.xpath("normalize-space(//li[@itemprop='weight']/text())").extract_first()
        detail['height'] = response.xpath("normalize-space(//li[@itemprop='height']/text())").extract_first()
        detail['blood_type'] = response.xpath(
            "normalize-space(//div[@class='mx_topic-item']/ul/li[last()]/text())").extract_first()
        detail['address'] = response.xpath("normalize-space(//li[@itemprop='birthplace']/text())").extract_first()
        detail['image_url'] = "http:" + response.xpath("//img[@itemprop='image']/@src").extract_first()
        detail['birthday'] = response.xpath("//li[@class='birthdate']/text()").extract_first()
        # detail['id'] = id
        # detail['e_name'] = response.xpath("//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[1]/text()").extract_first()
        detail['e_name'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[1]/text())").extract_first()
        detail['sex'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[2]/text())").extract_first()
        detail['location'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[5]/text())").extract_first()
        detail['school'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[6]/text())").extract_first()
        detail['fameyear'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[7]/text())").extract_first()

        detail['alias'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[1]/text())").extract_first()
        detail['constellation'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[4]/text())").extract_first()
        detail['residentialAddress'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[5]/text())").extract_first()
        detail['brokerageAgency'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[6]/text())").extract_first()
        detail['hobby'] = response.xpath("normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[7]/text())").extract_first()
        try:
            # 描述
            detail['des'] = response.xpath("//p[@class='mx_detail']/text()").extract()[-2].replace(' ', '').strip()
        except:
            detail['des'] = None
        print(detail)
