from functools import lru_cache
from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):
    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    class Config:
        case_sensitive = True
        env_file = ".env"

class TestSettings(Settings):
    class Config:
        case_sensitive = True
        env_file = "tests/.env"

@lru_cache
def get_settings():
    return Settings()

@lru_cache
def get_test_settings():
    return TestSettings()

settings = get_settings()