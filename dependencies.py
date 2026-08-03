from fastapi import Cookie, HTTPException
from jose import JWTError, jwt

from security import SECRET_KEY, ALGORITHM


def get_current_user(access_token: str = Cookie(default=None)):

    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Not Authenticated"
        )

    print("COOKIE TOKEN:", access_token)

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("PAYLOAD:", payload)

        username = payload.get("sub")
        role = payload.get("role")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return {
            "username": username,
            "role": role
        }

    except JWTError as e:
        print("JWT ERROR:", str(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )