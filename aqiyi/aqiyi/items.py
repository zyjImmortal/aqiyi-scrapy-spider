# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ActorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
    character = scrapy.Field()
    actor_id = scrapy.Field()
    timestamp = scrapy.Field()
    save_image_url = scrapy.Field()


class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    category_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    sub_ype = scrapy.Field()
    sub_name = scrapy.Field()
    level = scrapy.Field()
    qipu_id = scrapy.Field()
    parent_id = scrapy.Field()
    timestamp = scrapy.Field()


class DirectorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
    director_id = scrapy.Field()
    timestamp = scrapy.Field()
    save_image_url = scrapy.Field()


class MainCharactorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    image_url = scrapy.Field()
    character = scrapy.Field()
    main_charactor_id = scrapy.Field()
    timestamp = scrapy.Field()
    save_image_url = scrapy.Field()


class MovieTableItem(scrapy.Item):
    id = scrapy.Field()
    movie_id = scrapy.Field()
    channel_id = scrapy.Field()
    description = scrapy.Field()
    name = scrapy.Field()
    play_url = scrapy.Field()
    duration = scrapy.Field()
    focus = scrapy.Field()
    score = scrapy.Field()
    second_info = scrapy.Field()
    format_period = scrapy.Field()
    site_id = scrapy.Field()
    issue_time = scrapy.Field()
    image_url = scrapy.Field()
    timestamp = scrapy.Field()
    save_image_url = scrapy.Field()


class PerformerDetailTableItem(scrapy.Item):
    name = scrapy.Field()
    job_title = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    blood = scrapy.Field()
    address = scrapy.Field()
    image_url = scrapy.Field()
    des = scrapy.Field()
    save_image_url = scrapy.Field()
    timestamp = scrapy.Field()
    performer_id = scrapy.Field()
