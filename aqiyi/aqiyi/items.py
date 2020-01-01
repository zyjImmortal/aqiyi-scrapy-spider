# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    id = scrapy.Field()
    moviename = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    imagepath = scrapy.Field()
    saveimagepath = scrapy.Field()
    score = scrapy.Field()
    status =  scrapy.Field()
    source = scrapy.Field()

class MovieDetailItem(scrapy.Item):
    id = scrapy.Field()
    director = scrapy.Field()
    director_id = scrapy.Field()
    keyword = scrapy.Field()
    category = scrapy.Field()
    des = scrapy.Field()
    movie_id = scrapy.Field()


class CategoryMovieItem(scrapy.Item):
    num_id = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()

class MoviePerformerItem(scrapy.Item):
    id = scrapy.Field()
    performer = scrapy.Field()
    image_url = scrapy.Field()
    role = scrapy.Field()
    movie_id =scrapy.Field()


class PerformerDetailTableItem(scrapy.Item):
    name = scrapy.Field()
    occupation = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    bloodtype = scrapy.Field()
    address = scrapy.Field()
    imageurl = scrapy.Field()
    des = scrapy.Field()
    saveimageurl = scrapy.Field()
    birthday = scrapy.Field()
    id = scrapy.Field()

    e_name = scrapy.Field()  # 外文名
    alias = scrapy.Field()  # 别名
    sex = scrapy.Field()
    constellation = scrapy.Field()  # 星座
    location = scrapy.Field()
    residentialAddress = scrapy.Field()  # 居住地址
    school = scrapy.Field()
    brokerageAgency = scrapy.Field()  # 经纪公司
    fameyear = scrapy.Field()  # 成名年代
    hobby = scrapy.Field()


class MovieUrlItem(scrapy.Item):
    movieurl = scrapy.Field()



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
