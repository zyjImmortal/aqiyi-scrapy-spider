from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Float, Integer

Declarative = declarative_base()

class Base(Declarative):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class Movie(Base):
    __tablename__ = "movietable"
    id = Column(Integer)
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
    id = Column(Integer)
    director = Column(String(100))
    keyword = Column(String(500))
    category = Column(String(500))
    des = Column(String(3000))
    movie_id = Column(Integer)

class CategoryMovie(Base):
    __tablename__ = 'categoryMovieTable'
    numid = Column(Integer)
    category = Column(String(100))
    url = Column(String(100))
    title = Column(String(100))
    source = Column(String(100))

class MoviePerformer(Base):
    __tablename__ = 'movieperformertable'
    id = Column(Integer)
    performer = Column(String(100))
    role = Column(String(255))
    movie_id = Column(Integer)




class MovieUrl(Base):
    __tablename__ = 'movieurl'
    id = Column(Integer)
    movieurl = Column(String(255))


class PerformerDetail(Base):
    __tablename__ = 'performerdetailtable'
    id = Column(Integer)
    name = Column(String(100))
    e_name = Column(String(100))
    alias = Column(String(200))
    sex = Column(String(10))
    bloodtype = Column(String(5))
    height = Column(String(10))
    address = Column(String(500))
    birthday = Column(String(50))
    constellation = Column(String(500))
    location = Column(String(200))
    residentialAddress = Column(String(100))
    school = Column(String(200))
    brokerageAgency = Column(String(200))
    fameyear = Column(String(200))
    hobby = Column(String(1000))
    occupation = Column(String(500))
    weight = Column(String(500))
    image = Column(String(1000))
    des = Column(String(2000))


