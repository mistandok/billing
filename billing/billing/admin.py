from django.contrib import admin
from .models import Consumer, Subscription, Payments

# Register your models here.
@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass
