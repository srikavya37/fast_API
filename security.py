from datetime import datetime, timedelta
import jwt
import bcrypt

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100


def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode()


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload