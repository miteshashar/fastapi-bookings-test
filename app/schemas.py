from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    username: str

class UserCreateUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    name: str

class RoomCreateUpdate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    user_id: int

class BookingCreateUpdate(BookingBase):
    date: date
    room_id: int