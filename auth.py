#auth
from sqlalchemy.orm import Session
import models
import schemas
import security


from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import security


def register(db: Session, user: schemas.UserCreate):

    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed = security.hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login(db: Session, username: str, password: str):

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:
        return None

    if not security.verify_password(password, user.password):
        return None

    print("USERNAME:", user.username)
    print("EMAIL:", user.email)
    print("ROLE:", user.role)

    token = security.create_access_token(
        {
            "sub": user.username,
            "email": user.email,
            "role": user.role
        }
    )

    print("TOKEN:", token)

    return token