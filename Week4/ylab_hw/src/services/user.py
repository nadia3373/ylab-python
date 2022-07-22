from datetime import datetime
from fastapi import Depends, Request
from passlib.context import CryptContext
from typing import Optional, Union
from sqlmodel import Session
from src.core import config
from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES
from src.db import get_session
from src.models.user import UserModel
from src.api.v1.schemas.users import UModel, User, UserCreate, UserUpdate
from src.api.v1.schemas.tokens import AccessToken, RefreshToken
from src.services.mixins import UserMixin
import jwt
import re
import redis
import uuid as uuid_pkg

"""Для шифрования паролей."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Подключение к базам данных Redis."""
blocked_access_tokens = redis.Redis(
    host=config.REDIS_HOST, port=config.REDIS_PORT,
    db=1, decode_responses=True,
)

active_refresh_tokens = redis.Redis(
    host=config.REDIS_HOST, port=config.REDIS_PORT,
    db=2, decode_responses=True,
)


class UserService(UserMixin):
    def authenticate(self, user: User) -> bool:
        """Аутентификация пользователя."""
        user_name = self.session.query(UserModel).filter(UserModel.username == user.username).first()
        if user_name:
            user_password = pwd_context.verify(user.password,
                                               user_name.password)
        if user_name and user_password:
            return True

    def validate(self, user: UserCreate) -> bool:
        """Валидация данных пользователя."""
        username_result = re.search("^\w+([\.-]?\w+)*@?\w+([\.-]?\w+)*((\.\w{2,3})+)?$", user.username)
        email_result = re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", user.email)
        password_result = re.search("^(?=.*\d)?(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", user.password)
        if username_result and email_result and password_result:
            return True
        else:
            return False

    def check_if_exists(self, user: UserCreate) -> bool:
        """Проверка на существование пользователя."""
        user_by_name = self.session.query(UserModel).filter(UserModel.username == user.username).first()
        user_by_email = self.session.query(UserModel).filter(UserModel.email == user.email).first()
        if user_by_name or user_by_email:
            return True
        else:
            return False

    def create_user(self, user: UserCreate) -> dict:
        """Создание пользователя."""
        new_uuid = uuid_pkg.uuid4()
        hashed_password = pwd_context.hash(user.password)
        new_user = UserModel(username=user.username, email=user.email,
                             password=hashed_password, uuid=str(new_uuid))
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.username

    def create_response(self, user: Optional[str]=None,
                        user_uuid: Optional[str]=None):
        """Поиск пользователя в базе данных."""
        if user is not None:
            user_model = self.session.query(UserModel).filter(UserModel.username == user).first()
        elif user_uuid is not None:
            user_model = self.session.query(UserModel).filter(UserModel.uuid == user_uuid).first()
        if user_model:
            return user_model
        else:
            return None

    def create_access_token(self, data: Union[User, UModel], access_uuid: str,
                            refresh_uuid: str, current_time: int) -> AccessToken:
        """Создание access_token."""
        if type(data) is User:
            user: UModel = self.session.query(UserModel).filter(UserModel.username == data.username).first()
        else:
            user: UModel = data
        user_id = user.uuid
        access_payload = AccessToken(
            fresh=True,
            iat=current_time,
            jti=access_uuid,
            type="access",
            user_uuid=user_id,
            nbf=current_time,
            exp=current_time + int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
            refresh_uuid=refresh_uuid,
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
            created_at=str(user.created_at),
            roles=user.roles,
        )
        acc_token = jwt.encode(access_payload.dict(), JWT_SECRET_KEY,
                               algorithm=JWT_ALGORITHM)
        return acc_token

    def create_refresh_token(self, user: User, refresh_uuid: str,
                             current_time: int) -> RefreshToken:
        """Создание refresh_token."""
        user: UModel = self.session.query(UserModel).filter(UserModel.username == user.username).first()
        user_id = user.uuid
        refresh_payload = RefreshToken(
            fresh=True,
            iat=current_time,
            jti=refresh_uuid,
            type="refresh",
            user_uuid=user_id,
            nbf=current_time,
            exp=current_time + int(REFRESH_TOKEN_EXPIRE_MINUTES) * 60,
        )
        refr_token = jwt.encode(refresh_payload.dict(), JWT_SECRET_KEY,
                                algorithm=JWT_ALGORITHM)
        active_refresh_tokens.lpush(user_id, refresh_uuid)
        return refr_token

    def decode_token(self, token: str) -> AccessToken:
        """Расшифровка access_token."""
        decoded_token: AccessToken = jwt.decode(token, JWT_SECRET_KEY,
                                                algorithms=[JWT_ALGORITHM])
        return decoded_token

    def decode_refresh_token(self, token: str) -> RefreshToken:
        """Расшифровка refresh_token."""
        decoded_token: RefreshToken = jwt.decode(token, JWT_SECRET_KEY,
                                                 algorithms=[JWT_ALGORITHM])
        return decoded_token

    def decode_request_header(self, request: Request) -> str:
        """Расшифровка заголовка авторизации."""
        try:
            token = request.headers.get('Authorization')
            token = token.split(" ")
            token = token[1]
            return token
        except:
            return None

    def update_user_info(self, username: str, data: UserUpdate) -> UModel:
        """Обновление информации о пользователе."""
        user: UModel = self.session.query(UserModel).filter(UserModel.username == username).first()
        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.password:
            hashed_password = pwd_context.hash(data.password)
            user.password = hashed_password
        self.session.commit()
        self.session.refresh(user)
        return user

    def check_if_token_blocked(self, token: str) -> bool:
        """Проверка токена на блокировку."""
        return True if token in blocked_access_tokens else False

    def block_access_token(self, token: str):
        """Блокировка токена."""
        blocked_access_tokens.set(token, "")

    def check_if_access_token_valid(self, token: AccessToken) -> bool:
        """Валидация access_token."""
        current_time = int(datetime.utcnow().timestamp())
        if((current_time < int(token["exp"])) and (self.check_if_token_blocked(token["jti"]) is False)):
            if token["user_uuid"] in active_refresh_tokens:
                refresh_tokens: list = active_refresh_tokens.lrange(token["user_uuid"], 0, -1)
                match = False
                for i in refresh_tokens:
                    if i == token["refresh_uuid"]:
                        match = True
                if match is True:
                    return True
        return False

    def remove_refresh_token(self, token: Union[str, None], user_id: str) -> bool:
        """Удаление refresh_token."""
        if type(token) is str:
            if user_id in active_refresh_tokens:
                for i in active_refresh_tokens.lrange(user_id, 0, -1):
                    if i == token:
                        active_refresh_tokens.lrem(user_id, 1, i)
                        return True
                    else:
                        return False
        else:
            if user_id in active_refresh_tokens:
                active_refresh_tokens.delete(user_id)
                return True
            return False

    def check_if_refresh_token_valid(self, token: Union[AccessToken, RefreshToken]) -> bool:
        """Валидация refresh_token."""
        if token["type"] == "access":
            refresh_uuid = token["refresh_uuid"]
        elif token["type"] == "refresh":
            refresh_uuid = token["jti"]
        user_uuid = token["user_uuid"]
        if user_uuid in active_refresh_tokens:
            match = False
            for i in active_refresh_tokens.lrange(user_uuid, 0, -1):
                if i == refresh_uuid:
                    match = True
            if match is True:
                current_time = int(datetime.utcnow().timestamp())
                if current_time <= int(token["exp"]):
                    return True
        return False


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session=session)
