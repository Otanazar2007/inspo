from sqlalchemy import Integer, Boolean, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship, validates
from database import get_db, Base
from datetime import datetime
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(30))
    password = Column(String)
    phone_number = Column(String, unique=True)
    email = Column(String, nullable=True, unique=True)
    address = Column(String, nullable=True)
    reg_date = Column(DateTime, default=datetime.now())
    cart_fk = relationship('Cart', back_populates='cart_fk')
    fav_fk = relationship('Favorite', back_populates='user_fk')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    descr = Column(String(2000))
    created_at = Column(DateTime, default=datetime.now())

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    descr = Column(String(2000))
    created_at = Column(DateTime, default=datetime.now())

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    descr = Column(String(2000), default='Описание товара')
    photo = Column(String, default='database/default_pics/istockphoto-1495088043-612x612.jpg')
    price = Column(String)
    count = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    created_at = Column(DateTime, default=datetime.now())
    category_fk = relationship(Category, lazy='subquery')
    brand_fk = relationship(Brand, lazy='subquery')

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    count  = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    cart_fk = relationship(User, lazy='subquery',back_populates='cart_fk')
    product_fk = relationship(Product, lazy='subquery', passive_deletes=True)

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    created_at = Column(DateTime, default=datetime.now())
    user_fk = relationship(User, lazy='subquery', back_populates='fav_fk', passive_deletes=True)
    product_fk = relationship(Product, lazy='subquery', passive_deletes=True)