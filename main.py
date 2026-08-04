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


# ======================================
# Database Dependency
# ======================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================================
# Authentication APIs
# ======================================

@app.post("/register")
def register(
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
    return crud.login_user(
        user,
        db,
        response
    )


# ======================================
# Mobile CRUD APIs
# ======================================

@app.post(
    "/mobiles",
    response_model=schemas.MobileResponse
)
def create_mobile(
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    return crud.create_mobile(
        db,
        mobile
    )


@app.get(
    "/mobiles",
    response_model=list[schemas.MobileResponse]
)
def read_all_mobiles(
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):
    return crud.get_mobiles(db)


@app.get(
    "/mobiles/{mobile_id}",
    response_model=schemas.MobileResponse
)
def read_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):

    mobile = crud.get_mobile(
        db,
        mobile_id
    )

    if not mobile:
        raise HTTPException(
            status_code=404,
            detail="Mobile not found"
        )

    return mobile


@app.put(
    "/mobiles/{mobile_id}",
    response_model=schemas.MobileResponse
)
def update_mobile(
    mobile_id: int,
    mobile: schemas.MobileCreate,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
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


@app.delete("/mobiles/{mobile_id}")
def delete_mobile(
    mobile_id: int,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
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


# ======================================
# Search Mobile by Brand
# ======================================

@app.get(
    "/brand/{brand}",
    response_model=list[schemas.MobileResponse]
)
def search_mobile(
    brand: str,
    db: Session = Depends(get_db),
    admin=Depends(verify_admin)
):

    return crud.get_mobile_by_brand(
        db,
        brand
    )