"""Модуль содерижт API для сервиса user-preferences."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query


user_purchased_films_router = APIRouter()


@user_purchased_films_router.post(
    '/add',
)
async def add_purchased_film_to_user(
):
    """
    Ручка позволяет добавить купленный фильм в профиль пользователя.

    `Args`:
        body: тело запроса.
        user_profiles_service: сервис для работы с профилями польтзовтелей.

    `Returns`:
        Response
    """
    pass


@user_purchased_films_router.patch(
    '/del',
)
async def del_purchased_film_from_user(
):
    """
    Ручка позволяет удалить у пользователя фильм из списка купленных.

    `Args`:
        body: тело запроса.
        user_profiles_service: сервис для работы с профилями польтзовтелей.

    `Returns`:
        Response
    """
    pass


@user_purchased_films_router.get(
    '/list',
)
async def get_user_purchased_films(
) -> list:
    """
    Ручка позволяет получить писок купленных фильмов.

    `Args`:
        user_id: иденитификатор пользователя.
        only_with_events: показывать только тех пользователей, которые подписаны хотябы на одно уведомление.
        user_profiles_service: сервис для работы с профилями польтзовтелей.

    `Returns`:
        list[UserPurchasedFilms]
    """
    pass
