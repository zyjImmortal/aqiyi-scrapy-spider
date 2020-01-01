# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aqiyi.exceptions import TableNotFoundException
from aqiyi.models import Movie
from aqiyi.items import PerformerDetailTableItem, MovieItem, MovieDetailItem, MoviePerformerItem, CategoryMovieItem
from scrapy.utils.project import get_project_settings

class MysqlPipeline:

    def __init__(self, db_url, db_name, db_user, db_password):
        self.db_url = db_url
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=get_project_settings().get("DB_URL"),
            db_name=get_project_settings().get("DB_NAME"),
            db_user=get_project_settings().get("DB_USER"),
            db_password=get_project_settings().get("DB_PASSWORD")
        )

    def open_spider(self, spider):
        self.engine = create_engine("mysql+cymysql://{}:{}@{}:3306/{}?charset=utf8"
                               .format(self.db_user, self.db_password, self.db_url, self.db_name),
                               encoding='utf-8', echo=True)
        self.session = Session(bind=self.engine)

    def close_spider(self, spider):
        self.session.close()


class MoviePipeline(MysqlPipeline):
    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            movie = Movie(**item)
            self.session.add(movie)
            self.session.commit()
        if isinstance(item, PerformerDetailTableItem):
            detail = PerformerDetailTableItem(**item)
            self.session.add(detail)
            self.session.commit()
        if isinstance(item, MovieDetailItem):
            movie_detail = MovieDetailItem(**item)
            self.session.add(movie_detail)
            self.session.commit()
        if isinstance(item,CategoryMovieItem):
            category = CategoryMovieItem(**item)
            self.session.add(category)
            self.session.commit()
        if isinstance(item, MoviePerformerItem):
            performer = MoviePerformerItem(**item)
            self.session.add(performer)
            self.session.commit()
        return item


