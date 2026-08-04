from sqlalchemy.orm import Session
from fastapi import Response

import models
import schemas

from security import (
    hash_password,
    verify_password,
    create_access_token
)


# ==========================
# Mobile CRUD Operations
# ==========================

def create_mobile(db: Session, mobile: schemas.MobileCreate):
    db_mobile = models.Mobile(**mobile.model_dump())

    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def get_mobiles(db: Session):
    return db.query(models.Mobile).all()


def get_mobile(db: Session, mobile_id: int):
    return db.query(models.Mobile).filter(
        models.Mobile.id == mobile_id
    ).first()


def update_mobile(
    db: Session,
    mobile_id: int,
    mobile: schemas.MobileCreate
):
    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db_mobile.brand = mobile.brand
    db_mobile.color = mobile.color
    db_mobile.price = mobile.price
    db_mobile.ram = mobile.ram
    db_mobile.storage = mobile.storage

    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def delete_mobile(db: Session, mobile_id: int):
    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db.delete(db_mobile)
    db.commit()

    return db_mobile


# ==========================
# Search Mobile By Brand
# ==========================

def get_mobile_by_brand(db: Session, brand: str):
    return db.query(models.Mobile).filter(
        models.Mobile.brand == brand
    ).all()


# ==========================
# User Registration
# ==========================

def create_user(user: schemas.UserCreate, db: Session):

    new_user = models.Users(**user.model_dump())

    # Change to False if you don't want every user to be an admin
    new_user.is_admin = True

    new_user.password = hash_password(
        new_user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==========================
# User Login
# ==========================

def login_user(
    user: schemas.UserLogin,
    db: Session,
    response: Response
):

    is_exists = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if not is_exists:
        return {
            "message": "User not found"
        }

    valid = verify_password(
        user.password,
        is_exists.password
    )

    if not valid:
        return {
            "message": "Invalid Password"
        }

    payload = {
        "name": is_exists.name,
        "email": is_exists.email,
        "is_admin": is_exists.is_admin,
        "is_loggedin": True
    }

    token = create_access_token(payload)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {
        "message": "Login Successful",
        "access_token": token
    }