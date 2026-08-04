from pydantic import BaseModel


# ==================================
# Mobile Schemas
# ==================================

class MobileCreate(BaseModel):
    brand: str
    model: str
    price: float
    ram: str
    storage: str


class MobileResponse(MobileCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


# ==================================
# User Schemas
# ==================================

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: str
    password: str