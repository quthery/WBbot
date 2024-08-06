from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Model(DeclarativeBase):
    pass

class Users(Model):
    __tablename__ = "users"
    

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    username = Column(String)
    password = Column(String)
    apis = relationship("Api", back_populates="user")

class Api(Model):
    __tablename__ = "apis"
    

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_key = Column(String)
    user = relationship("Users", back_populates="apis")


class Article(Model):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    api_key = Column(String, ForeignKey("apis.api_key"))
    art = Column(String)
    quantity = Column(Integer)
    days = Column(Integer)


class OrderUID(Model):
    __tablename__ = "orderuids"
    uid = Column(String, primary_key=True)
