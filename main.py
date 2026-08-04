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


# ====================================================
#                 USER APIs
# ====================================================

@app.post("/register", tags=["Authentication"])
def register(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):

    return crud.create_user(user, db)


@app.post("/login", tags=["Authentication"])
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


# ====================================================
#               MOBILE CRUD APIs
# ====================================================

@app.post(
    "/mobiles",
    response_model=schemas.MobileResponse,
    tags=["Mobiles"]
)
def create_mobile(
        mobile: schemas.MobileCreate,
        db: Session = Depends(get_db)
):

    return crud.create_mobile(db, mobile)


@app.get(
    "/mobiles",
    response_model=list[schemas.MobileResponse],
    tags=["Mobiles"]
)
def get_all_mobiles(
        db: Session = Depends(get_db),
        admin=Depends(verify_admin)
):

    return crud.get_mobiles(db)


@app.get(
    "/mobiles/{mobile_id}",
    response_model=schemas.MobileResponse,
    tags=["Mobiles"]
)
def get_mobile(
        mobile_id: int,
        db: Session = Depends(get_db)
):

    mobile = crud.get_mobile(db, mobile_id)

    if not mobile:
        raise HTTPException(
            status_code=404,
            detail="Mobile Not Found"
        )

    return mobile


@app.put(
    "/mobiles/{mobile_id}",
    response_model=schemas.MobileResponse,
    tags=["Mobiles"]
)
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
            detail="Mobile Not Found"
        )

    return updated


@app.delete(
    "/mobiles/{mobile_id}",
    tags=["Mobiles"]
)
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
            detail="Mobile Not Found"
        )

    return {
        "message": "Mobile Deleted Successfully"
    }


@app.get(
    "/brand/{brand}",
    response_model=list[schemas.MobileResponse],
    tags=["Mobiles"]
)
def search_brand(
        brand: str,
        db: Session = Depends(get_db)
):

    return crud.search_brand(
        db,
        brand
    )