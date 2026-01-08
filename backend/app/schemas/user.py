"""
User schemas.

- UserCreate: input for registration
- UserOut: safe response (never returns password hash)
"""

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, max_length=72, description="The user's password")

class UserOut(BaseModel):
    id:int
    email: EmailStr

    class config:
        from_attributes = True