# -*- coding: utf-8 -*-
import json
import time

import redis
import scrapy
from scrapy import  Request
from scrapy.utils.project import get_project_settings

client = redis.Redis(host=get_project_settings().get('REDIS_HOST'), port=get_project_settings().get('REDIS_PORT'),db=get_project_settings().get('REDIS_DB'))
client.set("error", 0)
#12小时过期
client.expire("error", 60*60*12)

from aqiyi.items import PerformerDetailTableItem, ActorItem, MainCharactorItem, DirectorItem, \
    CategoryItem, MovieTableItem


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
                movie = MovieTableItem()
                movie['id'] = id
                movie['movie_id'] = item['tvId']
                movie['channel_id'] = item['channelId']
                movie['description'] = description
                movie['name'] = item['name']
                movie['play_url'] = item['playUrl']
                movie['duration'] = item['duration']
                movie['focus'] = focus
                movie['score'] = item.get('score') or 0
                movie['second_info'] = item['secondInfo']
                movie['format_period'] = item['formatPeriod']
                movie['site_id'] = 'iqiyi'
                try:
                    movie['issue_time'] = item['issueTime']
                except:
                    movie['issue_time'] = 0
                movie['image_url'] = item['imageUrl']
                movie['timestamp'] = int(time.time())
                yield movie
            else:
                error = client.get('error')
                error_num = int(error) + 1
                if error_num > 1000:
                    return
                else:
                    client.set('error', int(error) + 1)
                    client.expire("error", 60 * 60 * 12)
                continue
            # 类型
            categories = item.get('categories')
            if categories is None:
                continue
            for category in categories:
                category_item = CategoryItem()
                category_item['id'] = id
                category_item['category_id'] = category['id']
                category_item['name'] = category['name']
                category_item['url'] = category['url']
                category_item['sub_ype'] = category['subType']
                category_item['sub_name'] = category['subName']
                category_item['level'] = category['level']
                category_item['qipu_id'] = category['qipuId']
                category_item['parent_id'] = category['parentId']
                category_item['timestamp'] = int(time.time())
                yield category_item
            if item.get('cast') is not None:
                directors = item['cast'].get('director')
                if directors is not None:
                    for director in directors:
                        # director组装模型
                        director_item = DirectorItem()
                        director_item['id'] = id
                        director_item['name'] = director['name']
                        director_item['image_url'] = director.get('image_url')
                        director_item['director_id'] = director['id']
                        director_item['timestamp'] = int(time.time())

                        res = client.sadd('performerid', director['id'])
                        if res == 1:
                            director_detail_url = 'https://www.iqiyi.com/lib/s_' + str(director['id']) + '.html'
                            yield scrapy.Request(director_detail_url, callback=self.performer_detail, meta={'id': director['id']})
                        yield director_item

                main_charactors = item['cast'].get('main_charactor') or None
                if main_charactors != None:
                    for main_charactor in main_charactors:
                        main_charactor_item = MainCharactorItem()
                        main_charactor_item['id'] = id
                        main_charactor_item['name'] = main_charactor['name']
                        main_charactor_item['image_url'] = main_charactor.get('image_url')
                        main_charactor_item['character'] = ",".join(main_charactor['character']).replace('"', '\\"')
                        main_charactor_item['main_charactor_id'] = main_charactor['id']
                        main_charactor_item['timestamp'] = int(time.time())
                        res = client.sadd('performer_id', main_charactor['id'])
                        if res == 1:
                            main_charactor_url = 'https://www.iqiyi.com/lib/s_' + str(main_charactor['id']) + '.html'
                            print(main_charactor_url)
                            yield scrapy.Request(main_charactor_url, callback=self.performer_detail, meta={'id': main_charactor['id']})
                        yield main_charactor_item

                actors = item['cast'].get('actor')
                if actors is not None:
                    for actor in actors:
                        actor_item = ActorItem()
                        actor_item['id'] = id
                        actor_item['name'] = actor['name']
                        actor_item['image_url'] = actor.get('image_url')
                        actor_item['character'] = ','.join(actor['character'])
                        actor_item['actor_id'] = actor['id']
                        actor_item['timestamp'] = int(time.time())
                        res = client.sadd('performer_id', actor['id'])
                        if res == 1:

                            actor_detail_url = 'https://www.iqiyi.com/lib/s_' + str(actor['id']) + '.html'
                            yield scrapy.Request(actor_detail_url, callback=self.performer_detail, meta={'id': actor['id']})
                        yield actor_item

    def performer_detail(self, response):
        id = response.meta['id']
        detail = PerformerDetailTableItem()
        detail['name'] = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        detail['job_title'] = response.xpath("normalize-space(//li[@itemprop='jobTitle']/text())").extract_first()
        detail['width'] = response.xpath("normalize-space(//li[@itemprop='weight']/text())").extract_first()
        detail['height'] = response.xpath("normalize-space(//li[@itemprop='height']/text())").extract_first()
        detail['blood'] = response.xpath(
            "normalize-space(//div[@class='mx_topic-item']/ul/li[last()]/text())").extract_first()
        detail['address'] = response.xpath("normalize-space(//li[@itemprop='birthplace']/text())").extract_first()
        detail['image_url'] = "http:" + response.xpath("//img[@itemprop='image']/@src").extract_first()
        detail['timestamp'] = int(time.time())
        detail['performer_id'] = id
        try:
            # 描述
            detail['des'] = response.xpath("//p[@class='mx_detail']/text()").extract()[-2].replace(' ', '').strip()
        except:
            detail['des'] = None
        yield detail
