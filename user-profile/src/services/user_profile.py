"""Модуль содержит сервис для работы с user_preferences."""

from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from src.core.config import DatabaseName, CollectionName
from src.db.mongodb import get_mongo_client
from src.db.redis import get_redis
from src.models.response_models import IdResponse
from src.models.user_profile import UserProfile
from src.services.crud.factories import get_crud_object_by_client
from src.services.types import TStorageClient, CacheClient


class UserProfileService:
    """
    Класс отвечает за доступные действия с пользовательским профилем

    Attributes:
        cache_client: клиент кэша.
        _storage_client: клиент для работы с хранилищем данных.
        _user_profile: объект для CRUD-операций с хранилищем данных.
    """

    __slots__ = ('cache_client', '_storage_client', '_user_profile')

    def __init__(self, storage_client: TStorageClient, cache_client: CacheClient):
        self.cache_client = cache_client
        self._storage_client = storage_client
        self._user_profile = get_crud_object_by_client(
            storage_client,
            db_name=DatabaseName.PROFILES.value,
            collection_name=CollectionName.USER_PROFILE.value,
            model=UserProfile,
        )

    async def upsert_user_purchased_films(self, user_id: str, purchased_films: list[str]) -> IdResponse:
        """
        Метод добавляет данные в профиль пользователя.

        Args:
            user_id: идентификатор пользователя.
            purchased_films: купленные фильмы.
        """
        user_profile = await self._user_profile.get(dict(user_id=user_id))

        if user_profile:
            current_purchased_films = user_profile.purchased_films

            is_need_update = False
            for new_purchased_films in purchased_films:
                if new_purchased_films not in current_purchased_films:
                    current_purchased_films.append(new_purchased_films)
                    is_need_update = True

            if is_need_update:
                await self._user_profile.update(dict(user_id=user_id), dict(purchased_films=current_purchased_films))

            result_id = str(user_profile.id)
        else:
            new_user_profile = UserProfile(user_id=user_id, purchased_films=purchased_films)
            result_id = await self._user_profile.insert(new_user_profile)

        return IdResponse(id=result_id)

    async def delete_purchased_film_from_user(self, user_id: str, preferences: list[Preferences]):
        """
        Метод удаляет данные из профиля пользователя.

        Args:
            user_id: идентификатор пользователя, для которого необходимо удалить пользовательские настройки.
            preferences: пользовательские настройки, которые нужно удалить.
        """
        user_preferences = await self._user_profile.get(dict(user_id=user_id))

        if not user_preferences:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Для пользователя настройки еще не заданы!')

        current_preferences = user_preferences.preferences

        is_need_update = False
        for preference_for_delete in preferences:
            try:
                current_preferences.remove(preference_for_delete)
                is_need_update = True
            except ValueError:
                continue

        if is_need_update:
            encoded_preferences = [jsonable_encoder(preference) for preference in current_preferences]
            await self._user_profile.update(dict(user_id=user_id), dict(preferences=encoded_preferences))

    async def get_user_profile(
        self,
        user_ids: list[str],
        only_with_events: bool = False
    ) -> list[UserPreferences]:
        return await self._user_preferences_searcher.get(user_ids, only_with_events)


@lru_cache()
def get_user_profiles_service(
        storage_client: TStorageClient = Depends(get_mongo_client),
        cache_client: CacheClient = Depends(get_redis),
) -> UserProfileService:
    """
    Функция возвращает сервис для работы с пользовательскими профилями.

    Args:
        storage_client: клиент для работы с хранилищем данных.
        cache_client: клиент кэша.

    Returns:
        UserProfileService
    """
    return UserProfileService(storage_client, cache_client)
