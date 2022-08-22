from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)

class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

# class Booking(Base):
#     room_id = Column(ForeignKey("room.id"), primary_key=True, backref="bookings")
#     date = Column(Date, primary_key=True)
#     user_id = Column(ForeignKey("user.id"), backref="bookings", nullable=False)