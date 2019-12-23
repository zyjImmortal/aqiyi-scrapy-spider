# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aqiyi.aqiyi.exceptions import TableNotFoundException
from aqiyi.aqiyi.models import Movie


class MysqlPipeline:

    def __init__(self, db_url, db_name, db_user, db_password):
        self.db_url = db_url
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.setting.get("DB_URL"),
            db_name=crawler.setting.get("DB_NAME"),
            db_user=crawler.setting.get("DB_USER"),
            db_password=crawler.setting.get("DB_PASSWORD")
        )

    def open_spider(self, spider):
        self.engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}?charset=utf8"
                               .format(self.db_user, self.db_password, self.db_url, self.db_name),
                               encoding='utf-8', echo=True)
        self.session = Session(bind=self.engine)

    def close_spider(self, spider):
        self.session.close()


class MoviePipeline(MysqlPipeline):
    def process_item(self, item, spider):
        movie = Movie(**item)
        self.session.add(movie)
        self.session.commit()
        return item


class MovieDetailPipeline(MysqlPipeline):
    def process_item(self, item, spider):
        pass
