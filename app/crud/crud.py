from datetime import date
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.schemas import BookingCreateUpdate, UserCreateUpdate, RoomCreateUpdate, UserCreateUpdate
from app.crud.base import CRUDBase
from app.models import Booking, User, Room

class CRUDUser(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

user = CRUDUser(User)
class CRUDRoom(CRUDBase[Room, RoomCreateUpdate, RoomCreateUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Room]:
        return db.query(Room).filter(Room.name == name).first()

room = CRUDRoom(Room)
class CRUDBooking(CRUDBase[Booking, BookingCreateUpdate, BookingCreateUpdate]):
    def check_room_availability(self, db: Session, *, room_id: int, date: date) -> bool:
        return db.query(Booking).filter(Booking.room_id == room_id, Booking.date == date).first() is None
    
    def get_by_room(self, db: Session, *, room_id: int, date: date):
        return db.query(Booking).filter(Booking.room_id == room_id, Booking.date == date).first()
    
    def remove_booking(self, db: Session, *, room_id: int, date: date) -> Booking:
        obj = self.get_by_room(db, room_id=room_id, date=date)
        db.delete(obj)
        db.commit()
        return obj

booking = CRUDBooking(Booking)