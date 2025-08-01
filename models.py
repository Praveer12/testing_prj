from sqlalchemy import String, Integer, Column, Float, ForeignKey, text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category= Column(String, nullable=False)

    products = relationship("Ecomm", back_populates="category")



class Ecomm(Base):
    __tablename__ = "material"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), index=True)
    product= Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="products")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String,nullable=False)
    created = Column(TIMESTAMP,nullable=False,server_default = text('now()'))
