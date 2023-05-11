from django.db import models
from config.mixins import TimeStampedModel


class Consumer(TimeStampedModel):
    user_id = models.UUIDField(verbose_name="ID пользователя", null=True, blank=False)


class Subscription(TimeStampedModel):
    class SubscribeType(models.TextChoices):
        OUR = "OU", "Наш кинотеатр"
        AMEDIATEKA = "AM", "Амедиатека"

    subscribe_type = models.CharField(
        verbose_name="Тип подписки",
        max_length=2,
        choices=SubscribeType.choices,
        null=True,
    )
    consumer = models.ForeignKey(
        Consumer,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    active = models.BooleanField(
        verbose_name="Активная",
        default=False,
    )


class Payments(TimeStampedModel):
    subscription = models.ForeignKey(
        Subscription,
        verbose_name="Подписка",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    consumer = models.ForeignKey(
        Consumer,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    sum = models.FloatField(verbose_name="Сумма покупки", null=True, blank=False)
