from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String)
    service_id = Column(String)
    date = Column(DateTime)
    time_slot = Column(String)
    price = Column(Float)
    status = Column(String, default='confirmed')  # confirmed, cancelled, completed
    created_at = Column(DateTime) 