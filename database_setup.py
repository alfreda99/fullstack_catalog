import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Represents the User object.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Book(Base):
    """Represents the Book object.
    """
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(500))
    picture = Column(String(250))
    price = Column(Float(precision=10, scale=2))
    inventoryCount = Column(Integer)
    rating = Column(String(100))
    dateUpdated = Column(DateTime(6))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


@property
def serialize(self):
    """Return object data in easily serializeable format"""
    return {
        'id': self.id,
        'user_id': self.user_id,
        'title': self.title,
        'author': self.author,
        'price': self.price,
        'category': self.category,
        'inventoryCount': self.inventoryCount,
        'rating': self.rating,
        'dateUpdated': str(self.dateUpdated),
        'description': self.description
    }


engine = create_engine('sqlite:///bookstore.db')


Base.metadata.create_all(engine)
