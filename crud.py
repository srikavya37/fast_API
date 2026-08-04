from sqlalchemy.orm import Session
from fastapi import Response, HTTPException
import models
import schemas
import bcrypt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


# ==========================
# Mobile CRUD
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


def update_mobile(db: Session, mobile_id: int, mobile: schemas.MobileCreate):

    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db_mobile.brand = mobile.brand
    db_mobile.model = mobile.model
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


def get_mobile_by_brand(db: Session, brand: str):

    return db.query(models.Mobile).filter(
        models.Mobile.brand == brand
    ).all()


# ==========================
# User Registration
# ==========================

def create_user(user: schemas.UserCreate, db: Session):

    # Check if email already exists
    existing_user = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.Users(**user.model_dump())

    hashed = bcrypt.hashpw(
        new_user.password.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode("utf-8")

    new_user.password = hashed

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
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid = bcrypt.checkpw(
        user.password.encode(),
        is_exists.password.encode()
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    payload = {
        "name": is_exists.name,
        "email": is_exists.email,
        "is_admin": is_exists.is_admin,
        "is_loggedin": True,
        "exp": datetime.utcnow() + timedelta(seconds=1000)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

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