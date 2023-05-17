from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from billing.models import Consumer, Subscribe, Payment
from billing.serializers import SubscribeSerializer, WebhookSerializer
from billing.stripe import create_subscribe, cancel_subscribe

from .service.bearer_auth import generic_bearer_auth, BearerTokenMixin


class CreateSubscribe(GenericAPIView, BearerTokenMixin):
    serializer_class = SubscribeSerializer

    @generic_bearer_auth
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email

        subscribe_type = serializer.validated_data.get("subscribe_type")
        customer, created = Consumer.objects.get_or_create(user_id=user_id, email=email)
        if customer.subscribe.filter(subscribe_type=subscribe_type).exists():
            return Response(data="Already exists", status=HTTPStatus.BAD_REQUEST)
        # TODO: сделать проверку на существование объекта
        subscribe = Subscribe.objects.get(subscribe_type=subscribe_type)
        return Response(create_subscribe(consumer=customer, subscribe=subscribe))


class CancelSubscribe(GenericAPIView, BearerTokenMixin):
    serializer_class = SubscribeSerializer

    # TODO: переделать запрос, чтобы получать значение подписки из параметров, а не из тела.
    @generic_bearer_auth
    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email

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
