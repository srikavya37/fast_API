#schemas
from pydantic import BaseModel

class MobileCreate(BaseModel):
    brand: str
    model: str
    ram: str
    storage: str
    color: str
    price: float


class MobileResponse(MobileCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str