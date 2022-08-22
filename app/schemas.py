from pydantic import BaseModel

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

