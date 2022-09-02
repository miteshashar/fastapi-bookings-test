from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import Base

class Booking(Base):
    room_id = Column(ForeignKey("room.id"), primary_key=True)
    room = relationship("Room", back_populates="bookings")
    date = Column(Date, primary_key=True)
    user_id = Column(ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="bookings")
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    bookings = relationship("Booking", back_populates="user")

class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    bookings = relationship("Booking", back_populates="room")
