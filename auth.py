#auth
from sqlalchemy.orm import Session
import models
import schemas
import security


def register(db: Session, user: schemas.UserCreate):

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

    token = security.create_access_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return token