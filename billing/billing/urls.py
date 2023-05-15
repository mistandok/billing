from django.urls import path

from billing.views import CreateSubscribe, WebhookAPIView

urlpatterns = [
    path("subscribe/", CreateSubscribe.as_view()),
    path("webhook/", WebhookAPIView.as_view())
]