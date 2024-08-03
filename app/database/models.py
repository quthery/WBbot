from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase

class Model(DeclarativeBase):
    pass

class Users(Model):
    __tablename__ = "users"
    

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    username = Column(String)
    apis = relationship("Api", back_populates="user")

class Api(Model):
    __tablename__ = "apis"
    

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_key = Column(String)
    user = relationship("Users", back_populates="apis")


class Items(Model):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    art = Column(String)
    quantity = Column(Integer)
    days = Column(Integer)
