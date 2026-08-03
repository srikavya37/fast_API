#models
from sqlalchemy import Column, Integer, String, Float  # type: ignore
from database import Base

class Mobile(Base):
    __tablename__ = "mobiles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    ram = Column(String(20), nullable=False)
    storage = Column(String(20), nullable=False)
    color = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")