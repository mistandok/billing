"""Модуль описания БД."""

from django.db import models
from config.mixins import TimeStampedModel, UUIDMixin


class Consumer(TimeStampedModel):
    """Модель описывает сущность покупателя"""
    user_id = models.UUIDField(verbose_name="ID пользователя", null=True, blank=False)
    subscribe = models.ManyToManyField('Subscribe', through='ConsumerSubscribe')


#TODO: Consumer может иметь >1 подписки => связь М-to-М
# Мы реализовали через ConsumerSubscribe

# class Subscription(TimeStampedModel):
#     class SubscribeType(models.TextChoices):
#         OUR = "OU", "Наш кинотеатр"
#         AMEDIATEKA = "AM", "Амедиатека"
# 
#     subscribe_type = models.CharField(
#         verbose_name="Тип подписки",
#         max_length=2,
#         choices=SubscribeType.choices,
#         null=True,
#     )
#     consumer = models.ForeignKey(
#         Consumer,
#         verbose_name="Пользователь",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=False,
#     )
#     active = models.BooleanField(
#         verbose_name="Активная",
#         default=False,
#     )


#TODO: Payments - отслеживает платежи клиентов? Если так, то это похоже на историю
# платежей => можно хранить историю платежей из Stripe?
class Payment(UUIDMixin):
    """Модель описывает сущность платежа"""
    subscription = models.ForeignKey(
        'Subscribe',
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
    # TODO: change field to Decimal
    sum = models.FloatField(verbose_name="Сумма покупки", null=True, blank=False)
    transaction_id = models.CharField(max_length=300)

    class Meta:
        db_table = "billing\".\"payment"


class Subscribe(UUIDMixin):
    """Модель описывает сущность подписки"""
    class Type(models.TextChoices):
        SUBSCRIBER = "subscriber", "Наш кинотеатр"
        AMEDIATEKA = "amediateka", "Амедиатека"

    title = models.CharField(
        verbose_name="Тип подписки",
        max_length=10,
        choices=Type.choices,
        null=False,
        blank=True
    )
    description = models.CharField(max_length=2_000,)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "billing\".\"subscription"


class Filmwork(UUIDMixin):
    """Модель описывает сущность кинопроизведения"""
    title = models.CharField(
        max_length=200
    )
    modified_subscribe_date = models.DateTimeField(null=True, blank=True)

    subscribe = models.ManyToManyField(Subscribe, through='FilmworkSubscribe')

    class Meta:
        db_table = "billing\".\"filmwork"


class FilmworkSubscribe(UUIDMixin):
    """М2М модель кинопроизведения и подписки"""
    filmwork = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        null=False,
        blank=True
    )
    subscribe = models.ForeignKey(
        Subscribe,
        on_delete=models.CASCADE,
        null=False,
        blank=True
    )

    class Meta:
        db_table = "billing\".\"filmwork_subscribe"
        unique_together = [
            ['filmwork', 'subscribe'],
        ]


class ConsumerSubscribe(UUIDMixin, TimeStampedModel):
    """М2М модель покупателя и подписки"""
    subscribe = models.ForeignKey(
        Subscribe,
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )
    consumer = models.ForeignKey(
        Consumer,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=True,
    )

    class Meta:
        db_table = "billing\".\"consumer_subscribe"
        unique_together = [
            ['subscribe', 'consumer'],
        ]
