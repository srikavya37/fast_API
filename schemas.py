from pydantic import BaseModel


# -------------------------
# Mobile Schemas
# -------------------------

class MobileCreate(BaseModel):
    brand: str
    color: str
    price: float
    ram: str
    storage: str


class MobileResponse(MobileCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(UserCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: str
    password: str