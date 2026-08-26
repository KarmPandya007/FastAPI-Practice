from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    role: str = Field(default="user", example="user")
    is_active: bool = Field(default=True, example=True)

class UserCreate(UserBase):
    password: Optional[str] = Field(None, min_length=6, example="secret123")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="John Smith")
    email: Optional[EmailStr] = Field(None, example="john.smith@example.com")
    role: Optional[str] = Field(None, example="admin")
    is_active: Optional[bool] = Field(None, example=True)
    password: Optional[str] = Field(None, min_length=6, example="newsecret123")

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedUserResponse(BaseModel):
    total: int
    skip: int
    limit: int
    users: List[UserResponse]
