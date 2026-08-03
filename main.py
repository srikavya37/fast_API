from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud
import schemas
import auth

from database import Base, engine, SessionLocal
from dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Authentication APIs
# -------------------------

@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return auth.register(db, user)


@app.post("/login")
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    token = auth.login(
        db,
        user.username,
        user.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    response = JSONResponse(
        content={
            "message": "Login Successful"
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        secure=False,      # Change to True when using HTTPS in production
        samesite="Lax"
    )

    return response


# -------------------------
# Mobile APIs (Protected)
# -------------------------

@app.post("/mobiles", response_model=schemas.MobileResponse)
def create(
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.create_mobile(db, mobile)


@app.get("/mobiles", response_model=list[schemas.MobileResponse])
def read_all(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.get_mobiles(db)


@app.get("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def read_one(
    mobile_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    mobile = crud.get_mobile(db, mobile_id)

    if not mobile:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return mobile


@app.put("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def update(
    mobile_id: int,
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    updated = crud.update_mobile(db, mobile_id, mobile)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return updated


@app.delete("/mobiles/{mobile_id}")
def delete(
    mobile_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete mobiles"
        )

    deleted = crud.delete_mobile(db, mobile_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return {
        "message": "Mobile deleted successfully"
    }


@app.get("/brand/{brand}")
def get_brand_mobiles(
    brand: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.get_mobile_by_brand(db, brand)