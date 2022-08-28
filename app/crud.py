from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_property(db: Session, property_id: int):
    return db.query(models.Property).filter(models.Property.id == property_id).first()

def get_property_by_name(db: Session, name: str):
    return db.query(models.Property).filter(models.Property.name == name).first()

def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Property).offset(skip).limit(limit).all()

def create_property(db: Session, property: schemas.PropertyCreate):
    db_property = models.Property(name=property.name)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property