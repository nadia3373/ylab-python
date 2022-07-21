from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserCreate(User):
    email: str


class UserShow(BaseModel):
    username: str
    email: str


class UModel(User, UserShow):
    uuid: str
    created_at: datetime
    roles: list[str]
    is_superuser: bool
    is_totp_enabled: bool
    is_active: bool


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
