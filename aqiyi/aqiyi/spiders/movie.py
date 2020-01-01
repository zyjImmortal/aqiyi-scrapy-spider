# -*- coding: utf-8 -*-
import json
import time

import redis
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings

client = redis.Redis(host=get_project_settings().get('REDIS_HOST'), port=get_project_settings().get('REDIS_PORT'),
                     db=get_project_settings().get('REDIS_DB'))
client.set("error", 0)
# 12小时过期
client.expire("error", 60 * 60 * 12)

from aqiyi.items import PerformerDetailTableItem, MovieItem, MovieDetailItem, MoviePerformerItem, CategoryMovieItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['iqiyi.com']

    def start_requests(self):
        pages = []
        for i in range(1, 3):
            url = 'http://pcw-api.iqiyi.com/search/video/videolists?channel_id=%d&data_type=1&pageSize=48&site=iqiyi&pageNum=1' % i
            page = scrapy.Request(url, dont_filter=True)
            pages.append(page)
        return pages

    def parse(self, response):

        data = json.loads(response.text)
        movie_items = data['data']['list']
        if len(movie_items) == 0:
            return
        else:
            url = response.url
            next_url = url[:url.index('pageNum=') + 8] + str(int(url[url.index('pageNum=') + 8:]) + 1)
            yield Request(next_url, callback=self.parse)

        for item in movie_items:
            site_id = item['siteId']
            if site_id != 'iqiyi':
                continue
            id = int(time.time() * 1000 - 1558524422580)
            res = client.sadd('movie_id', item['tvId'])
            if res == 1:
                description = item.get('description')
                if description is not None:
                    description = description.replace('"', '\\"')
                focus = item.get('focus')
                if focus is not None:
                    focus = focus.replace('"', '\\"')
                # 组装模型存入数据库
                movie = MovieItem()
                movie['id'] = item['tvId']
                movie['moviename'] = item['name']
                movie['url'] = item['playUrl']
                movie['score'] = item.get('score') or 0
                movie['source'] = 'iqiyi'
                movie['status'] = item['payMark']
                try:
                    movie['time'] = item['duration']
                except:
                    movie['time'] = 0
                movie['imagepath'] = item['imageUrl']
                yield movie

                movie_detail = MovieDetailItem()
                movie_detail['director'] = item['cast'].get('director')
                movie_detail['director_id'] = item['cast'].get('id')
                movie_detail['des'] = item['description']
                movie_detail['category'] = ','.join([category['name'] for category in item['categories']])
                movie_detail['movie_id'] = item['tvId']
                movie_detail['keyword'] = item['focus']
                yield movie_detail
            else:
                error = client.get('error')
                error_num = int(error) + 1
                if error_num > 1000:
                    return
                else:
                    client.set('error', int(error) + 1)
                    client.expire("error", 60 * 60 * 12)
                continue
            categories = item.get('categories')
            if categories == None:
                continue
            for citem in categories:
                category = CategoryMovieItem()
                category['num_id'] = citem['id']
                category['title'] = citem['name']
                category['url'] = citem['url']
                category['category'] = citem['subName']
                category['source'] = "iqiyi"
                yield category
            if item.get('cast') is not None:
                directors = item['cast'].get('director')
                if directors is not None:
                    for director in directors:
                        # director组装模型
                        director_item = {}
                        director_item['director_id'] = director['id']

                        res = client.sadd('performerid', director_item['director_id'])
                        if res == 1:
                            director_detail_url = 'https://www.iqiyi.com/lib/s_' + str(
                                director_item['director_id']) + '.html'
                            yield scrapy.Request(director_detail_url, callback=self.performer_detail,
                                                 meta={'id': director_item['director_id']})

                main_charactors = item['cast'].get('main_charactor') or None
                if main_charactors != None:
                    for main_charactor in main_charactors:
                        main_charactor_item = MoviePerformerItem()
                        main_charactor_item['id'] = main_charactor['id']
                        main_charactor_item['performer'] = main_charactor['name']
                        main_charactor_item['image_url'] = main_charactor.get('image_url')
                        main_charactor_item['role'] = ",".join(main_charactor['character']).replace('"', '\\"')
                        main_charactor_item['movie_id'] = item['tvId']
                        res = client.sadd('performer_id', main_charactor_item['id'])
                        if res == 1:
                            main_charactor_url = 'https://www.iqiyi.com/lib/s_' + str(
                                main_charactor_item['id']) + '.html'
                            print(main_charactor_url)
                            yield scrapy.Request(main_charactor_url, callback=self.performer_detail,
                                                 meta={'id': main_charactor_item['id']})
                        yield main_charactor_item

    def performer_detail(self, response):
        id = response.meta['id']
        detail = PerformerDetailTableItem()
        detail['id'] = id
        detail['name'] = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        detail['occupation'] = response.xpath("normalize-space(//li[@itemprop='jobTitle']/text())").extract_first()
        detail['width'] = response.xpath("normalize-space(//li[@itemprop='weight']/text())").extract_first()
        detail['height'] = response.xpath("normalize-space(//li[@itemprop='height']/text())").extract_first()
        detail['bloodtype'] = response.xpath(
            "normalize-space(//div[@class='mx_topic-item']/ul/li[last()]/text())").extract_first()
        detail['address'] = response.xpath("normalize-space(//li[@itemprop='birthplace']/text())").extract_first()
        detail['imageurl'] = "http:" + response.xpath("//img[@itemprop='image']/@src").extract_first()
        detail['birthday'] = response.xpath("//li[@class='birthdate']/text()").extract_first()
        # detail['id'] = id
        # detail['e_name'] = response.xpath("//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[1]/text()").extract_first()
        detail['e_name'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[1]/text())").extract_first()
        detail['sex'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[2]/text())").extract_first()
        detail['location'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[5]/text())").extract_first()
        detail['school'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[6]/text())").extract_first()
        detail['fameyear'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[1]/dd[7]/text())").extract_first()

        detail['alias'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[1]/text())").extract_first()
        detail['constellation'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[4]/text())").extract_first()
        detail['residentialAddress'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[5]/text())").extract_first()
        detail['brokerageAgency'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[6]/text())").extract_first()
        detail['hobby'] = response.xpath(
            "normalize-space(//div[contains(@class, 'basic-info') and contains(@class, 'clearfix')]/dl[2]/dd[7]/text())").extract_first()
        try:
            # 描述
            detail['des'] = response.xpath("//p[@class='mx_detail']/text()").extract()[-2].replace(' ', '').strip()
        except:
            detail['des'] = None
        yield detail
