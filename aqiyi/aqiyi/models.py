from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Float, Integer

Declarative = declarative_base()

class Base(Declarative):
    __abstract__ = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class Movie(Base):
    __tablename__ = "movietable"
    id = Column(Integer, primary_key=True)
    moviename = Column(String(length=100))
    time = Column(String(128))
    url = Column(String(500))
    imagepath = Column(String(2000))
    saveimagepath = Column(String(500))
    score = Column(Float)
    status = Column(Integer)
    source = Column(String(64))


class MovieDetail(Base):
    __tablename__ = 'moviedetailtable'
    director = Column(String(100))
    director_id = Column(Integer)
    keyword = Column(String(500))
    category = Column(String(500))
    des = Column(String(3000))
    movie_id = Column(Integer, primary_key=True)

class CategoryMovie(Base):
    __tablename__ = 'categoryMovieTable'
    num_id = Column(Integer, primary_key=True)
    category = Column(String(100))
    url = Column(String(100))
    title = Column(String(100))
    source = Column(String(100))

class MoviePerformer(Base):
    __tablename__ = 'movieperformertable'
    id = Column(Integer, primary_key=True)
    performer = Column(String(100))
    image_url = Column(String(300))
    save_image_url = Column(String(500))
    role = Column(String(255))
    movie_id = Column(Integer)


class PerformerDetail(Base):
    __tablename__ = 'performerdetailtable'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    height = Column(String(10))
    weight = Column(String(500))
    bloodtype = Column(String(5))
    address = Column(String(500))
    imageurl = Column(String(1000))
    saveimageurl = Column(String(1000))
    des = Column(String(2000))
    birthday = Column(String(50))

    e_name = Column(String(100)) # 外文名
    alias = Column(String(200))  #别名
    sex = Column(String(10))
    constellation = Column(String(500))  # 星座
    location = Column(String(200))
    residentialAddress = Column(String(100)) # 居住地址
    school = Column(String(200))
    brokerageAgency = Column(String(200)) # 经纪公司
    fameyear = Column(String(200))  # 成名年代
    hobby = Column(String(1000))
    occupation = Column(String(500))  # 职业



