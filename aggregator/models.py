from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime
from hashlib import md5

class Links(Base):
    __tablename__ = 'links'

    id          =   Column(Integer, primary_key=True)
    link        =   Column(String(2048), unique=True, nullable=False)
    updated     =   Column(DateTime)
    title       =   Column(String(2048))
    uuid        =   Column(String(32), unique=True, nullable=False)

    def __init__(self, link, title, updated):
        self.link = link.strip()
        self.uuid = md5(link).digest().encode('hex')
        title = title.strip()
        if title:
            self.title = title
        else:
            self.title = link
        self.updated = updated

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime)
    last_updated_after = Column(DateTime, nullable=False)
    last_updated_before = Column(DateTime, nullable=False)
