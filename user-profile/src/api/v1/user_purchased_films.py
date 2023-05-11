"""Модуль содерижт API для сервиса user-preferences."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.models.auth_models import HTTPTokenAuthorizationCredentials
from src.models.requests_body_models import PurchasedFilmRequest
from src.models.response_models import IdResponse, Response
from src.models.user_profile import UserProfile
from src.services.auth_validation.bearer_tokens import JWTBearer
from src.services.user_profile import get_user_profiles_service, UserProfileService

user_purchased_films_router = APIRouter()

admin_jwt_bearer = JWTBearer(admin_required=True)


@user_purchased_films_router.post(
    '/upsert',
)
async def upsert_user_purchased_films(
    body: PurchasedFilmRequest,
    user_profile_service: UserProfileService = Depends(get_user_profiles_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(admin_jwt_bearer),
) -> IdResponse:
    """
    Ручка позволяет добавить купленный фильм в профиль пользователя.

    `Args`:
        body: тело запроса.
        user_profile_service: сервис для работы с профилями польтзовтелей.
        credentials: данные входа.

    `Returns`:
        IdResponse
    """

    return await user_profile_service.upsert_user_purchased_films(
        user_id=body.user_id,
        purchased_films=body.film_ids
    )


@user_purchased_films_router.patch(
    '/del',
)
async def delete_purchased_film_from_user(
    body: PurchasedFilmRequest,
    user_profile_service: UserProfileService = Depends(get_user_profiles_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(admin_jwt_bearer),
) -> Response:
    """
    Ручка позволяет удалить у пользователя фильм из списка купленных.

    `Args`:
        body: тело запроса.
        user_profile_service: сервис для работы с профилями польтзовтелей.
        credentials: данные входа.

    `Returns`:
        Response
    """

    await user_profile_service.delete_purchased_film_from_user(
        user_id=body.user_id,
        films_for_delete=body.film_ids
    )
    return Response(detail='Один или несколько фильмов успешно удалёны!')


@user_purchased_films_router.get(
    '/list',
)
async def get_user_profile(
    user_id: str = Query(),
    user_profile_service: UserProfileService = Depends(get_user_profiles_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(admin_jwt_bearer),
) -> UserProfile:
    """
    Ручка позволяет получить список купленных пользователем фильмов.

    `Args`:
        user_id: идентификатор пользователя.
        user_profile_service: сервис для работы с профилями польтзовтелей.
        credentials: данные входа.

    `Returns`:
        UserProfile
    """
    return await user_profile_service.get_user_profile(user_id=user_id)
