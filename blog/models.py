from sqlalchemy.orm import backref, relationship
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="cascade"))
    
    creator = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    admin_acc = Column(Boolean, default=False)

    blogs = relationship("Blog", back_populates="creator")
