from http import HTTPStatus

from django.conf import settings
from rest_framework.generics import GenericAPIView
import jwt
from rest_framework.response import Response

from billing.models import Consumer, Subscribe, Payment
from billing.serializers import SubscribeSerializer, WebhookSerializer
from billing.stripe import create_subscribe, cancel_subscribe


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


class CancelSubscribe(GenericAPIView):
    serializer_class = SubscribeSerializer

    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # временно так авторизация
        user_id, email = try_get_token_payload(
            request.headers.get("Authorization").split(" ")[1]
        )
        subscribe_type = serializer.validated_data.get("subscribe_type")
        customer = Consumer.objects.filter(user_id=user_id, email=email).first()
        if (
            customer
            and customer.subscribe.filter(subscribe_type=subscribe_type).exists()
        ):
            cancel_subscribe(
                customer, Subscribe.objects.get(subscribe_type=subscribe_type)
            )
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(
            data="Invalid user or subscription", status=HTTPStatus.BAD_REQUEST
        )


class WebhookAPIView(GenericAPIView):
    serializer_class = WebhookSerializer

    def post(self, request):
        data = request.data["data"]
        event_type = request.data["type"]
        data_object = data["object"]
        if (
            event_type == "customer.subscription.created"
            or event_type == "customer.subscription.updated"
            or event_type == "customer.subscription.deleted"
        ):
            subscribe = Subscribe.objects.filter(
                payment_id=data_object["plan"]["id"]
            ).first()
            customer = Consumer.objects.filter(
                remote_consumer_id=data_object["customer"]
            ).first()
            if data_object["status"] == "active":
                customer.subscribe.add(subscribe)
            else:
                customer.subscribe.remove(subscribe)
            # TODO обращение к сервису Auth (тут асинхрон, можно без целери)
        if event_type == "invoice.paid":
            payment = Payment()
            payment.transaction_id = data_object["id"]
            payment.consumer = Consumer.objects.filter(
                remote_consumer_id=data_object["customer"]
            ).first()
            payment.subscription = Subscribe.objects.filter(
                payment_id=data_object["lines"]["data"][0]["plan"]["id"]
            ).first()
            payment.amount = data_object["lines"]["data"][0]["plan"]["amount"] / 100
            payment.save()
        return Response(status=HTTPStatus.OK)


# TODO куда нить вынести покрасивее
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
