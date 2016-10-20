from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import db

class Links(db.Model):
    __tablename__ = 'links'

    id          =   Column(Integer, primary_key=True)
    link        =   Column(String(2048), unique=True, nullable=False)
    updated     =   Column(DateTime)
    title        =   Column(String(2048))
    uuid        =   Column(String(32), unique=True, nullable=False)

    def __init__(self, link, updated, title, uuid):
        self.link = link
        self.updated = updated
        self.title = title
        self.uuid = uuid


    def __repr__(self):
        return "<Links %s %s %s>" % (self.uuid, self.link, self.title)

class Config(db.Model):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime, nullable=False)
    last_updated_after = Column(DateTime)
    last_updated_before = Column(DateTime)

    def __init__(self, last_updated, last_updated_before, last_updated_after):
        self.last_updated = last_updated
        self.last_updated_before = last_updated_before
        self.last_updated_after = last_updated_after

def create_session(db='sqlite:///proto.db'):
    engine = create_engine(db, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
