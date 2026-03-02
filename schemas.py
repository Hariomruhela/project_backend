from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Form, File, UploadFile

from typing import List, Optional
import re


# ------------------------
# Password Validation Regex
# ------------------------
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,14}$"


# ------------------------
# User Register Schema
# ------------------------
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "Password must be 8-14 characters long, contain one uppercase letter, one number, and one special character."
            )
        return value


# ------------------------
# User Login Schema
# ------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# Token Response Schema
# ------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool


# ------------------------
# Project Create Schema
# ------------------------
class ProjectCreate(BaseModel):
    id: int
    title: str
    description: str
    techstack: List[str]
    image_url: Optional[str]
    live_link: Optional[str]
    is_visible: bool

    class Config:
        form_mode = True
# ------------------------
# Project Update Schema
# ------------------------
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    techstack: Optional[List[str]] = None
    live_link: Optional[str] = None
    is_visible: Optional[bool] = None


# ------------------------
# Project Response Schema
# ------------------------
class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: str
    techstack: List[str]
    live_link: Optional[str]
    is_visible: bool

    class Config:
        from_attributes = True