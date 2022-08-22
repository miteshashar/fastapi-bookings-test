from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.schemas import UserCreateUpdate, RoomCreateUpdate, UserCreateUpdate
from app.crud.base import CRUDBase
from app.models import User, Room


class CRUDUser(CRUDBase[User, UserCreateUpdate, UserCreateUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

class CRUDRoom(CRUDBase[Room, RoomCreateUpdate, RoomCreateUpdate]):
    pass


user = CRUDUser(User)
room = CRUDRoom(Room)
