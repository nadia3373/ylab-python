from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from src.api.v1.schemas import PostCreate, PostListResponse, PostModel
from src.api.v1.schemas.tokens import AccessToken
from src.services import PostService, get_post_service
from src.services.user import get_user_service

router = APIRouter()


@router.get(
    path="/",
    response_model=PostListResponse,
    summary="Список постов",
    tags=["posts"],
)
def post_list(
    post_service: PostService = Depends(get_post_service),
) -> PostListResponse:
    """Отображение списка всех постов."""
    posts: dict = post_service.get_post_list()
    if not posts:
        # Если посты не найдены, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="posts not found")
    return PostListResponse(**posts)


@router.get(
    path="/{post_id}",
    response_model=PostModel,
    summary="Получить определенный пост",
    tags=["posts"],
)
def post_detail(
    post_id: int, post_service: PostService = Depends(get_post_service),
) -> PostModel:
    """Детальное отображение поста."""
    post: Optional[dict] = post_service.get_post_detail(item_id=post_id)
    if not post:
        # Если пост не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="post not found")
    return PostModel(**post)


@router.post(
    path="/",
    summary="Создать пост",
    tags=["posts"],
)
def post_create(
    request: Request, post: PostCreate, post_service: PostService = Depends(get_post_service), user_service = Depends(get_user_service)
) -> PostModel:
    """Функция создания поста."""
    if not post:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="Incorrect data.")
    token: str = user_service.decode_request_header(request)
    token: AccessToken = user_service.decode_token(token)
    if token:
        if user_service.check_if_access_token_valid(token) and user_service.check_if_refresh_token_valid(token):
            user_id = token["user_uuid"]
            post: dict = post_service.create_post(post=post, user_uuid=user_id)
            return PostModel(**post)
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is False:
            return {"msg": "Log in to create a post."}
        elif user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True:
            return {"msg": "Access token has expired. Please refresh."}
        print(user_service.check_if_access_token_valid(token)is False and user_service.check_if_refresh_token_valid(token) is True)
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="User is not logged in or access token has expired. Please log in or refresh.")
 
