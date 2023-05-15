from django.urls import path

from billing.views import CreateSubscribe, CancelSubscribe, WebhookAPIView

urlpatterns = [
    path("create-subscribe/", CreateSubscribe.as_view()),
    path("cancel-subscribe/", CancelSubscribe.as_view()),
    path("webhook/", WebhookAPIView.as_view()),
]
