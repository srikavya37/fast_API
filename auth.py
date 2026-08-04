from fastapi import Depends, HTTPException
from dependencies import get_current_user


def verify_admin(user=Depends(get_current_user)):

    if not user.get("is_admin"):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user