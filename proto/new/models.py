from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from hashlib import sha512

class Links(Base):
    __tablename__ = 'links'

    id          =   Column(Integer, primary_key=True)
    link        =   Column(String(2048), unique=True, nullable=False)
    updated     =   Column(DateTime)
    title       =   Column(String(2048))
    uuid        =   Column(String(32), unique=True, nullable=False)
    #tags        =   relationship('Tag', secondary=tags, backref = backref('images', lazy='dynamic'))
    #comments    =   relationship('Comment', backref='image', lazy='dynamic')

	#def __init__(self, link):
	#	self.link = link
	#	self.uuid = sha512(self.link).digest()

#    def __repr__(self):
#        p = "<Link (link='" + self.link + "')"
#        return "%d" % (p)

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime, nullable=False)
    last_updated_after = Column(DateTime)
    last_updated_before = Column(DateTime)

    #def __repr__(self):
    #    return "<Config (last_updated='%s', link='%d')" % (datetime.strptime(self.last_updated, "%m/%d/%y"))
