from datetime import datetime
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Request
from src.services.user import get_user_service
from src.api.v1.schemas.tokens import RefreshToken, Tokens, AccessToken
from src.api.v1.schemas.users import UModel, User, UserUpdate
import uuid as uuid_pkg


router = APIRouter()


@router.post(
    path="/login",
    response_model=dict,
    status_code=200,
    summary="Войти на сайт",
    tags=["login"],
)
def log_user_in(user: User, user_service=Depends(get_user_service)) -> Tokens:
    """Функция для входа зарегистрироанных пользователей."""
    if user:
        if user_service.authenticate(user):
            access_uuid = str(uuid_pkg.uuid4())
            refresh_uuid = str(uuid_pkg.uuid4())
            current_time = int(datetime.utcnow().timestamp())
            acc_token: str = user_service.create_access_token(user, access_uuid, refresh_uuid, current_time)
            refr_token: str = user_service.create_refresh_token(user, refresh_uuid, current_time)
            tokens = Tokens(access_token=acc_token, refresh_token=refr_token)
            return tokens
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                        detail="Incorrect login data")


@router.post(
    path="/refresh",
    response_model=Tokens,
    status_code=200,
    summary="Обновить токен",
    tags=["refresh"],
)
def refresh(request: Request, user_service=Depends(get_user_service)):
    """Функция обновления токенов."""
    token: str = user_service.decode_request_header(request)
    token: RefreshToken = user_service.decode_refresh_token(token)
    if token:
        if user_service.check_if_refresh_token_valid(token):
            user_service.remove_refresh_token(token["jti"], token["user_uuid"])
            user: UModel = user_service.create_response(user_uuid=token["user_uuid"])
            access_uuid = str(uuid_pkg.uuid4())
            refresh_uuid = str(uuid_pkg.uuid4())
            current_time = int(datetime.utcnow().timestamp())
            acc_token: str = user_service.create_access_token(user, access_uuid, refresh_uuid, current_time)
            refr_token: str = user_service.create_refresh_token(user, refresh_uuid, current_time)
            tokens = Tokens(access_token=acc_token, refresh_token=refr_token)
            return tokens
    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                        detail="User is not logged in or refresh token has expired.Please log in again.")


@router.get(
    path="/users/me",
    response_model=dict,
    status_code=200,
    summary="Просмотр информации о себе",
    tags=["profile"],
)
def show_user_info(request: Request, user_service=Depends(get_user_service)) -> dict:
    """Функция просмотра своего профиля."""
    token: str = user_service.decode_request_header(request)
    token: AccessToken = user_service.decode_token(token)
    if token:
        if user_service.check_if_refresh_token_valid(token) and user_service.check_if_access_token_valid(token):
            user: UModel = user_service.create_response(user=token["username"])
            delattr(user, "is_totp_enabled")
            delattr(user, "password")
            delattr(user, "is_active")
            resp = {}
            resp["user"] = user
            return resp
        elif user_service.check_if_access_token_valid(token) is False and user_service.check_if_refresh_token_valid(token) is False:
            return {"msg": "Log in to see this page."}
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True:
            return {"msg": "Access token has expired. Please refresh."}
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="User is not logged in or access token has expired. Please log in or refresh.")


@router.patch(
    path="/users/me",
    response_model=dict,
    status_code=200,
    summary="Обновление информации о себе",
    tags=["profile"],
)
def update_user_info(request: Request, data: UserUpdate, user_service=Depends(get_user_service)) -> dict:
    """Функция обновления информации о себе."""
    token: str = user_service.decode_request_header(request)
    token: AccessToken = user_service.decode_token(token)
    if token:
        access_uuid = str(uuid_pkg.uuid4())
        refresh_uuid = token["refresh_uuid"]
        current_time = int(datetime.utcnow().timestamp())
        if user_service.check_if_access_token_valid(token) and user_service.check_if_access_token_valid(token):
            user: UModel = user_service.update_user_info(token["username"], data)
            if not user:
                    return {"msg: User data not valid."}
            delattr(user, "is_totp_enabled")
            delattr(user, "password")
            delattr(user, "is_active")
            user_service.block_access_token(token["jti"])
            resp = {}
            resp["msg"] = "Update is successful. Please use new access_token."
            resp["user"] = user.dict()
            resp["access_token"] = user_service.create_access_token(user, access_uuid, refresh_uuid, current_time)
            return resp
        elif user_service.check_if_access_token_valid(token) is False and user_service.check_if_refresh_token_valid(token) is False:
            return {"msg": "Log in to see this page."}
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True:
            return {"msg": "Access token has expired. Please refresh."}
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="User is not logged in or access token has expired. Please log in or refresh.")



@router.post(
    path="/logout",
    status_code=200,
    response_model=dict,
    summary="Выйти",
    tags=["logout"],
)
def logout(request: Request, user_service=Depends(get_user_service)):
    """Функция выхода из профиля."""
    token: str = user_service.decode_request_header(request)
    token: AccessToken = user_service.decode_token(token)
    if token:
        if user_service.check_if_access_token_valid(token) and user_service.check_if_refresh_token_valid(token):
            user_service.block_access_token(token["jti"])
            refresh_uuid = token["refresh_uuid"]
            user_uuid = token["user_uuid"]
            if user_service.remove_refresh_token(token=refresh_uuid, user_id=user_uuid):
                return {"msg": "You have been logged out."}
        elif user_service.check_if_access_token_valid(token) is False and user_service.check_if_refresh_token_valid(token) is False:
            return {"msg": "User is not logged in."}
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True:
            return {"msg": "Access token has expired. Please refresh."}
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="User is not logged in or access token has expired. Please log in or refresh.")


@router.post(
    path="/logout_all",
    response_model=dict,
    status_code=200,
    summary="Выйти со всех устройств",
    tags=["logout_all"],
)
def logout_all(request: Request, user_service=Depends(get_user_service)):
    """Функция выхода со всех устройств."""
    token: str = user_service.decode_request_header(request)
    token: AccessToken = user_service.decode_token(token)
    if token:
        if user_service.check_if_access_token_valid(token) and user_service.check_if_refresh_token_valid(token):
            user_service.block_access_token(token["jti"])
            user_uuid = token["user_uuid"]
            if user_service.remove_refresh_token(token=None, user_id=user_uuid):
                return {"msg": "You have been logged out from all devices."}
        elif user_service.check_if_access_token_valid(token) is False and user_service.check_if_refresh_token_valid(token) is False:
            return {"msg": "User is not logged in."}
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True:
            return {"msg": "Access token has expired. Please refresh."}
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="User is not logged in or access token has expired. Please log in or refresh.")
