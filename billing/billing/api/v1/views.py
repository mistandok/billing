from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from billing.models import Consumer, Subscribe, Payment
from billing.serializers import SubscribeSerializer, WebhookSerializer

from billing.service.bearer_auth import generic_bearer_auth, BearerTokenMixin

from billing.service.errors import PaymentError
from billing.service.payments import create_customer_subscribe_payment_link, cancel_subscribe_for_user


class CreateSubscribe(GenericAPIView, BearerTokenMixin):
    """АПИ для создания подписки пользователя."""

    serializer_class = SubscribeSerializer

    @generic_bearer_auth
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email
        subscribe_type = serializer.validated_data.get("subscribe_type")

        try:
            url = create_customer_subscribe_payment_link(user_id, email, subscribe_type)
        except PaymentError as e:
            return Response(data=str(e), status=HTTPStatus.BAD_REQUEST)
        except Exception:
            return Response(data='Что-то пошло не так, мы уже решаем проблему', status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(url)


class CancelSubscribe(GenericAPIView, BearerTokenMixin):
    """АПИ для отмены подписки пользователя."""

    serializer_class = SubscribeSerializer

    @generic_bearer_auth
    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = self.token_payload.sub.user_id
        email = self.token_payload.sub.email
        subscribe_type = serializer.validated_data.get("subscribe_type")

        try:
            is_sub_canceled = cancel_subscribe_for_user(user_id, email, subscribe_type)

            if is_sub_canceled:
                return Response(status=HTTPStatus.NO_CONTENT)

            return Response(data="Пользователя с такой подпиской не существует.", status=HTTPStatus.BAD_REQUEST)
        except Exception:
            return Response(data='Что-то пошло не так, мы уже решаем проблему', status=HTTPStatus.INTERNAL_SERVER_ERROR)


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
