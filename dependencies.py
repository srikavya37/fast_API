from fastapi import Request, HTTPException
from security import verify_token


def get_current_user(request: Request):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = verify_token(token)
        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )