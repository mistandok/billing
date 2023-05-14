from django.urls import path

from billing.views import CreateSubscribe

urlpatterns = [
    path("subscribe/", CreateSubscribe.as_view())
]