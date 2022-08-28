from http.client import UNSUPPORTED_MEDIA_TYPE
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app import crud, models, schemas
from app.db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreateUpdate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username %s already exists." % user_in.username,
        )
    return crud.user.create(db, obj_in=user_in)


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User, status_code=201)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserCreateUpdate,
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    user_username = crud.user.get_by_username(db, username=user_in.username)
    if user_username:
        raise HTTPException(
            status_code=400,
            detail="Username %s already exists." % user_in.username,
        )
    return crud.user.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{user_id}", status_code=204)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.BaseModel
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    crud.user.remove(db, id=user_id)