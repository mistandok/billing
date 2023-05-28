"""Модуль, дающий возможность работать с Redis."""

from redis.asyncio.client import Redis


redis: Redis | None = None


async def get_redis() -> Redis:
    """
    Метод-провайдер, дающий по заданному соединению объект класса Redis.

    Returns: Redis-объект.

    """
    return redis
