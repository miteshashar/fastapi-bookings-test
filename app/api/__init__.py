from fastapi import APIRouter

from app.api import users, rooms

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])