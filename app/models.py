from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

# class Booking(Base):
#     __tablename__ = "bookings"
#     property_id = Column(ForeignKey("property.id"), primary_key=True, backref="bookings")
#     date = Column(Date, primary_key=True)
#     user_id = Column(ForeignKey("user.id"), backref="bookings", nullable=False)