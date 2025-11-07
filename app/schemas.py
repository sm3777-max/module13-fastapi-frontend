# in app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a user (includes password)."""
    password: str

class UserRead(UserBase):
    """Schema for reading user data (excludes password_hash)."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # This tells Pydantic to read data from ORM models