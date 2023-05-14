from http import HTTPStatus

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.generics import GenericAPIView
import jwt
from rest_framework.response import Response

from billing.models import Consumer, Subscribe
from billing.serializers import SubscribeSerializer
from billing.stripe import create_subscribe


class CreateSubscribe(GenericAPIView):
    serializer_class = SubscribeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # временно так авторизация
        user_id, email = try_get_token_payload(
            request.headers.get("Authorization").split(" ")[1]
        )
        subscribe_type = serializer.validated_data.get("subscribe_type")
        customer, created = Consumer.objects.get_or_create(user_id=user_id, email=email)
        if customer.subscribe.filter(subscribe_type=subscribe_type).exists():
            return Response(data="Already exists", status=HTTPStatus.BAD_REQUEST)
        subscribe = Subscribe.objects.get(subscribe_type=subscribe_type)
        return Response(create_subscribe(consumer=customer, subscribe=subscribe))


def try_get_token_payload(encoded_token: str):
    """
    Функция пытается расшифровать токени получить из него информацию.

    Args:
        encoded_token: зашифрованный токен.

    Returns:
        email и user_id
    """
    try:
        payload = jwt.decode(
            encoded_token,
            settings.JWT_SECRET_KEY.encode("utf-8"),
            algorithms=[settings.JWT_ALGORITHM],
            options=dict(verify_exp=False),
        ).get("sub")
        if "email" not in payload:
            return Response(data="No email in token", status=HTTPStatus.UNAUTHORIZED)
        return payload.get("user_id"), payload.get("email")
    except jwt.PyJWTError:
        return Response(
            data="Invalid or expired token.", status=HTTPStatus.UNAUTHORIZED
        )
