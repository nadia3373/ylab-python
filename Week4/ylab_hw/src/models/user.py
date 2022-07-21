from datetime import datetime

from sqlmodel import Field, SQLModel

__all__ = ("UserModel",)


class UserModel(SQLModel, table=True):
    username: str = Field(nullable=False)
    roles: list[str] = Field(nullable=False, default = [])
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    is_superuser: bool = Field(default=False)
    uuid: str = Field(primary_key=True)
    is_totp_enabled: bool = Field(default=False)
    is_active: bool = Field(default=True)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)