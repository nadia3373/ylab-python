from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from src.api.v1.schemas.users import UserCreate, UModel
from src.services.user import UserService, get_user_service

router = APIRouter()


@router.post(
    path="/",
    response_model=dict,
    status_code=201,
    summary="Создать пользователя",
    tags=["signup"],
)
def user_create(user: UserCreate,
                user_service: UserService = Depends(get_user_service)) -> dict:
    """Функция создания пользователя."""
    if not user_service.check_if_exists(user):
        if user_service.validate(user):
            response = {}
            user_name: str = user_service.create_user(user=user)
            user: UModel = user_service.create_response(user=user_name)
            delattr(user, "password")
            if user:
                response["msg"] = "User created."
                response["user"] = user
                return response
            else:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail="User not created")
        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="User data not valid")
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="User already exists")
