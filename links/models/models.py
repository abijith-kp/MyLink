from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Links(Base):
    __tablename__ = 'links'

    id          =   Column(Integer, primary_key=True)
    link        =   Column(String(2048), unique=True, nullable=False)
    updated     =   Column(DateTime)
    title        =   Column(String(2048))
    uuid        =   Column(String(32), unique=True, nullable=False)

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime, nullable=False)
    last_updated_after = Column(DateTime)
    last_updated_before = Column(DateTime)

def create_session(db='sqlite:///proto.db'):
    engine = create_engine(db, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
