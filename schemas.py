from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class EcommBase(BaseModel):
    product: str
    price: float
    description: str
    category_id: int


class EcommCreate(EcommBase):
    pass

class EcommUpdate(BaseModel):
    product: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class EcommResponse(EcommBase):
    id: int
    class Config:
        from_attributes = True



class CategoryBase(BaseModel):
    category: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    category: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    products: List[EcommResponse] = []

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str


# For user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

