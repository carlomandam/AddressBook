from sqlalchemy import Column, Integer, String, Float
from database import Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)