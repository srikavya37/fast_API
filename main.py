from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import schemas

from database import Base, engine, SessionLocal
from auth import verify_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mobile Management API"
)


# ==========================
# Database Dependency
# ==========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# User APIs
# ==========================

@app.post("/register_user")
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(user, db)


@app.post("/login")
def login(
    response: Response,
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    return crud.login_user(user, db, response)


# ==========================
# Mobile APIs
# ==========================

# Create Mobile
@app.post("/mobiles", response_model=schemas.MobileResponse)
def create_mobile(
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db)
):
    return crud.create_mobile(db, mobile)


# Get All Mobiles (Admin Only)
@app.get("/mobiles", response_model=list[schemas.MobileResponse])
def get_all_mobiles(
    db: Session = Depends(get_db),
    user=Depends(verify_admin)
):
    return crud.get_mobiles(db)


# Get Mobile By ID
@app.get("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def get_mobile(
    mobile_id: int,
    db: Session = Depends(get_db)
):
    mobile = crud.get_mobile(db, mobile_id)

    if not mobile:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return mobile


# Update Mobile
@app.put("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def update_mobile(
    mobile_id: int,
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db)
):
    updated = crud.update_mobile(
        db,
        mobile_id,
        mobile
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return updated


# Delete Mobile
@app.delete("/mobiles/{mobile_id}")
def delete_mobile(
    mobile_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_mobile(
        db,
        mobile_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return {
        "message": "Mobile deleted successfully"
    }


# Search Mobile By Brand
@app.get("/brand/{brand}")
def get_brand(
    brand: str,
    db: Session = Depends(get_db)
):
    return crud.get_mobile_by_brand(
        db,
        brand
    )