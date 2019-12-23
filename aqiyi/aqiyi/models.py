from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column

Declarative = declarative_base()

class Base(Declarative):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class Movie(Base):
    __tablename__ = "movie"
    name = Column(String(length=100))


class MovieDetail(Base):
    pass


