from numbers import Number
from sqlalchemy import Sequence, Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from .database import Base, engine

class Demo_profile(Base):
    __tablename__ = "demo_profile"
    __table_args__ = {'schema': 'integrationplatform'}
    
    sisid           = Column(Integer, primary_key=True)
    firstname       = Column(String(length=100))
    surname        = Column(String(length=100))
    gender          = Column(String(20),nullable=False)
    birthdate       = Column(Date) 
    email           = Column(String(length=100))
    
      