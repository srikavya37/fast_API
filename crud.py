from sqlalchemy.orm import Session
from fastapi import Response, HTTPException
import models
import schemas
import bcrypt
import jwt

from datetime import datetime, timedelta

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"


# =====================================================
# Mobile CRUD
# =====================================================

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


# =====================================================
# Search by Brand
# =====================================================

def get_mobile_by_brand(db: Session, brand: str):

    return db.query(models.Mobile).filter(
        models.Mobile.brand == brand
    ).all()


# =====================================================
# User Registration
# =====================================================

def create_user(user: schemas.UserCreate, db: Session):

    existing_user = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.Users(**user.model_dump())

    hashed_password = bcrypt.hashpw(
        new_user.password.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode("utf-8")

    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "user": new_user
    }


# =====================================================
# User Login
# =====================================================

def login_user(
    user: schemas.UserLogin,
    db: Session,
    response: Response
):

    db_user = db.query(models.Users).filter(
        models.Users.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    valid_password = bcrypt.checkpw(
        user.password.encode(),
        db_user.password.encode()
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    payload = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "is_admin": db_user.is_admin,
        "is_loggedin": True,
        "exp": datetime.utcnow() + timedelta(hours=1)
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
        secure=False,
        samesite="lax"
    )

    return {
        "message": "Login Successful",
        "access_token": token,
        "is_admin": db_user.is_admin
    }


# =====================================================
# Get Admin Users
# =====================================================

def get_admin_users(db: Session):

    return db.query(models.Users).filter(
        models.Users.is_admin == True
    ).all()


# =====================================================
# Get Normal Users
# =====================================================

def get_normal_users(db: Session):

    return db.query(models.Users).filter(
        models.Users.is_admin == False
    ).all()