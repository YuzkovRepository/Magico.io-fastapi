import re

from pydantic import BaseModel, Field, EmailStr, ConfigDict, validator


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=8, max_length=20, example="NewUser123")
    email: EmailStr
    password: str = Field(min_length=8, max_length=20, example="Passwod123")

    @validator('password')
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long (max 72 bytes)')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserCreateResponse(BaseModel):
    success: bool
    message: str
    username: str
    email: EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="Passwod123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str