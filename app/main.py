import imp
from app.config import settings
from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(router)