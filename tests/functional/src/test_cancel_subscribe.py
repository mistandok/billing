"""Модуль отвечает за тестирование обработки событий."""

import pytest

from tests.functional.utils.api import api_request
from tests.functional.settings import settings


@pytest.mark.asyncio
async def test_cancel_subscribe(
    api_session,
):
    """Тестирование доступоности ручки отмены подписки пользователя."""

    url = f'http://{settings.billing_host}/billing/api/v1/cancel-subscribe/'
    expected_body = {
        "name": "Cancel Subscribe",
        "description": "АПИ для отмены подписки пользователя.",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ]
    }

    body, headers, status = await api_request(api_session, 'OPTIONS', url)

    assert body == expected_body
