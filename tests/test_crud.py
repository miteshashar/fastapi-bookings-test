from this import d
import trace
from typing import Dict, List
import pytest
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.crud import user, room, booking
from app.db import get_db
from app.models import Booking, Room, User


@pytest.fixture(scope="session")
def john(db:Session) -> User:
    yield user.create(db, obj_in=dict(username="john_lennon"))

@pytest.fixture(scope="session")
def paul(db: Session) -> User:
    return user.create(db, obj_in=dict(username="mc_cartney"))

@pytest.fixture(scope="session")
def ashram(db: Session) -> Room:
    return room.create(db, obj_in=dict(name="Chaurasi Kutia"))

@pytest.fixture(scope="session")
def studio(db: Session) -> Room:
    return room.create(db, obj_in=dict(name="Abbey Road Studios"))

TOMORROW = date.today() + timedelta(days=1)
DAY_AFTER = TOMORROW + timedelta(days=1)

@pytest.fixture
def ashram_avl(db: Session, ashram) -> Dict[str, bool]:
    return {
        'tomorrow': booking.check_room_availability(db, room_id=ashram.id, date=TOMORROW),
        'day_after': booking.check_room_availability(db, room_id=ashram.id, date=DAY_AFTER),
    }

@pytest.fixture
def studio_avl(db: Session, studio) -> Dict[str, bool]:
    return {
        'tomorrow': booking.check_room_availability(db, room_id=studio.id, date=TOMORROW),
        'day_after': booking.check_room_availability(db, room_id=studio.id, date=DAY_AFTER),
    }

def test_availability_init(db: Session, ashram_avl: Dict[str, bool], studio_avl: Dict[str, bool]) -> None:
    assert ashram_avl['tomorrow'] == True
    assert ashram_avl['day_after'] == True
    assert studio_avl['tomorrow'] == True
    assert studio_avl['day_after'] == True
    
def test_bookings_stage_1(db:Session, ashram: Room, studio: Room, john: User, paul: User) -> None:
    b = booking.create(db, obj_in=dict(
        room_id=ashram.id,
        date=TOMORROW,
        user_id=john.id
        )
    )
    assert b is not None and b.room == ashram and b.date == TOMORROW and b.user == john
    b = booking.create(db, obj_in=dict(
        room_id=studio.id,
        date=DAY_AFTER,
        user_id=john.id
        )
    )
    assert b is not None and b.room == studio and b.date == DAY_AFTER and b.user == john

def test_availability_stage_1(db: Session, ashram_avl: Dict[str, bool], studio_avl: Dict[str, bool]) -> None:
    assert ashram_avl['tomorrow'] == False
    assert ashram_avl['day_after'] == True
    assert studio_avl['tomorrow'] == True
    assert studio_avl['day_after'] == False

def test_bookings_stage_2(db:Session, ashram: Room, studio: Room, john: User, paul: User) -> None:
    try:
        # Same room, date, user
        b = booking.create(db, obj_in=dict(
            room_id=ashram.id,
            date=TOMORROW,
            user_id=john.id
            )
        )
        pytest.fail("The same booking could be repeated. That should not be possible.")
    except IntegrityError:
        db.rollback()
    
    try:
        # Same room, date. Different user
        b = booking.create(db, obj_in=dict(
            room_id=studio.id,
            date=DAY_AFTER,
            user_id=paul.id
            )
        )
        pytest.fail("The same booking could be repeated. That should not be possible.")
    except IntegrityError:
        db.rollback()
    
def test_availability_stage_2(db: Session, ashram_avl: Dict[str, bool], studio_avl: Dict[str, bool]) -> None:
    assert ashram_avl['tomorrow'] == False
    assert ashram_avl['day_after'] == True
    assert studio_avl['tomorrow'] == True
    assert studio_avl['day_after'] == False

def test_bookings_stage_3(db:Session, ashram: Room, studio: Room, john: User, paul: User) -> None:
    # Same date, user. Try different room
    b = booking.create(db, obj_in=dict(
        room_id=studio.id,
        date=TOMORROW,
        user_id=john.id
        )
    )
    assert b is not None and b.room == studio and b.date == TOMORROW and b.user == john
    
    # Same date, user. Try different room
    b = booking.create(db, obj_in=dict(
        room_id=ashram.id,
        date=DAY_AFTER,
        user_id=paul.id
        )
    )
    assert b is not None and b.room == ashram and b.date == DAY_AFTER and b.user == paul

def test_availability_stage_3(db: Session, ashram_avl: Dict[str, bool], studio_avl: Dict[str, bool]) -> None:
    assert ashram_avl['tomorrow'] == False
    assert ashram_avl['day_after'] == False
    assert studio_avl['tomorrow'] == False
    assert studio_avl['day_after'] == False

def test_bookings_cancel(db: Session, ashram: Room, studio: Room, john: User, paul: User) -> None:
    try:
        b = booking.remove_booking(db, room_id=ashram.id, date=DAY_AFTER)
    except Exception as e:
        pytest.fail(e.args[0], pytrace=False)

def test_availability_cancel(db: Session, ashram_avl: Dict[str, bool], studio_avl: Dict[str, bool]) -> None:
    assert ashram_avl['tomorrow'] == False
    assert ashram_avl['day_after'] == True
    assert studio_avl['tomorrow'] == False
    assert studio_avl['day_after'] == False


def test_rebook_cancelled(db: Session, ashram: Room, john: User) -> None:
    # Rebook cancelled room. Different user.
    b = booking.create(db, obj_in=dict(
        room_id=ashram.id,
        date=DAY_AFTER,
        user_id=john.id
        )
    )
    assert b is not None and b.room == ashram and b.date == DAY_AFTER and b.user == john