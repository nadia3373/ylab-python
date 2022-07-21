from pydantic import BaseModel


class Token(BaseModel):
    fresh: bool
    iat: int
    jti: str
    type: str
    user_uuid: str
    nbf: int
    exp: int


class AccessToken(Token):
    refresh_uuid: str
    username: str
    email: str
    is_superuser: bool
    created_at: str
    roles: list[str]


class RefreshToken(Token):
    pass


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
