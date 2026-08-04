from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class Mobile(Base):
    __tablename__ = "mobiles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    ram = Column(String(30), nullable=False)
    storage = Column(String(30), nullable=False)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)