"""Модуль описания БД."""

from django.db import models
from config.mixins import TimeStampedModel, UUIDMixin


class Consumer(UUIDMixin, TimeStampedModel):
    """Модель описывает сущность покупателя"""

    user_id = models.UUIDField(verbose_name="ID пользователя", null=True, blank=False)
    email = models.EmailField(verbose_name="Email", null=True, blank=False)
    remote_consumer_id = models.CharField(
        verbose_name="ID в платежной системе", max_length=200, null=True, blank=True
    )
    subscribe = models.ManyToManyField(
        "Subscribe", verbose_name="Подписки пользователя", blank=True
    )

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return self.email


class Payment(UUIDMixin, TimeStampedModel):
    """Модель описывает сущность платежа"""

    subscription = models.ForeignKey(
        "Subscribe",
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
    amount = models.DecimalField(
        verbose_name="Сумма покупки",
        null=True,
        blank=False,
        max_digits=10,
        decimal_places=2,
    )
    transaction_id = models.CharField(max_length=300, null=False, blank=False)

    class Meta:
        db_table = 'billing"."payment'
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.transaction_id


class Subscribe(UUIDMixin):
    """Модель описывает сущность подписки"""

    class SubscribeType(models.TextChoices):
        SUBSCRIBER = "SU", "Наш кинотеатр"
        AMEDIATEKA = "AM", "Амедиатека"

    subscribe_type = models.CharField(
        verbose_name="Тип подписки",
        max_length=2,
        choices=SubscribeType.choices,
        null=True,
        unique=True,
    )
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    price = models.DecimalField(
        verbose_name="Цена подписки USD", max_digits=10, decimal_places=2, null=True
    )
    payment_id = models.CharField(
        verbose_name="ID продукта в платежной системе",
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'billing"."subscribe'
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.get_subscribe_type_display()}"


class Filmwork(UUIDMixin):
    """Модель описывает сущность кинопроизведения"""

    title = models.CharField(max_length=200)
    modified_subscribe_date = models.DateTimeField(null=True, blank=True)
    subscribe = models.ManyToManyField(Subscribe, through="FilmworkSubscribe")

    class Meta:
        db_table = 'billing"."filmwork'
        indexes = [
            models.Index(
                fields=["modified_subscribe_date"], name="filmwork_subscribe_date_idx"
            ),
        ]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return f"{self.title}"


class FilmworkSubscribe(UUIDMixin):
    """М2М модель кинопроизведения и подписки"""

    filmwork = models.ForeignKey(
        Filmwork, on_delete=models.CASCADE, null=False, blank=False
    )
    subscribe = models.ForeignKey(
        Subscribe, on_delete=models.CASCADE, null=False, blank=False
    )

    class Meta:
        db_table = 'billing"."filmwork_subscribe'
        unique_together = [
            ["filmwork", "subscribe"],
        ]
        verbose_name = "Фильм в подписке"
        verbose_name_plural = "Фильмы в подписке"
