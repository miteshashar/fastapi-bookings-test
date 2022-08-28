from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[schemas.Room])
def read_rooms(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    """
    Retrieve rooms.
    """
    rooms = crud.room.get_multi(db, skip=skip, limit=limit)
    return rooms


@router.post("/", response_model=schemas.Room, status_code=201)
def create_room(
    *,
    db: Session = Depends(get_db),
    room_in: schemas.RoomCreateUpdate,
) -> Any:
    """
    Create new room.
    """
    room = crud.room.get_by_name(db, name=room_in.name)
    if room:
        raise HTTPException(
            status_code=400,
            detail="Room name %s already exists." % room_in.username,
        )
    return crud.room.create(db, obj_in=room_in)


@router.get("/{room_id}", response_model=schemas.Room)
def read_room_by_id(
    room_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific room by id.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found.",
        )
    return room


@router.put("/{room_id}", response_model=schemas.Room, status_code=201)
def update_room(
    *,
    db: Session = Depends(get_db),
    room_id: int,
    room_in: schemas.RoomCreateUpdate,
) -> Any:
    """
    Update a room.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found.",
        )
    room_name = crud.room.get_by_name(db, name=room_in.name)
    if room_name:
        raise HTTPException(
            status_code=400,
            detail="Room name %s already exists." % room_in.name,
        )
    return crud.room.update(db, db_obj=room, obj_in=room_in)

@router.delete("/{room_id}", status_code=204)
def delete_room(
    *,
    db: Session = Depends(get_db),
    room_id: int,
    room_in: schemas.BaseModel
) -> Any:
    """
    Delete a room.
    """
    room = crud.room.get(db, id=room_id)
    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found.",
        )
    crud.room.remove(db, id=room_id)