from django.utils import timezone


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from billing.models import FilmworkSubscribe, Subscribe, Consumer
from billing.stripe import create_customer

from .service.payment_systems.factories import get_payment_system_by_name
from .service.payment_systems.interfaces import PaymentSystemName


@receiver(post_delete, sender=FilmworkSubscribe, weak=False)
def filmwork_subscribe_changed(sender, instance, **kwargs):
    """
    Сигнал при удалении связи многие ко многим для фильмов и их подписок.

    Args:
        sender: отправитель.
        kwargs: именнованые параметры.
    """
    if instance:
        instance.filmwork.modified_subscribe_date = timezone.now()
        instance.filmwork.save()


@receiver(post_save, sender=FilmworkSubscribe, weak=False)
def filmwork_subscribe_changed(sender, instance, **kwargs):
    """
    Сигнал при удалении связи многие ко многим для фильмов и их подписок.

    Args:
        sender: отправитель.
        kwargs: именнованые параметры.
    """
    if instance:
        instance.filmwork.modified_subscribe_date = timezone.now()
        instance.filmwork.save()


@receiver(post_save, sender=Subscribe)
def create_product_signal(sender, created, instance: Subscribe, *args, **kwargs):
    """Сигнал при записи продукта."""
    if created:
        payment_system = get_payment_system_by_name(PaymentSystemName.STRIPE)
        remote_product_id, remote_price_id = payment_system.create_product_and_price(instance)
        instance.product_id = remote_product_id
        instance.payment_id = remote_price_id
        instance.save()


@receiver(post_save, sender=Consumer)
def create_customer_signal(sender, created, instance: Consumer, *args, **kwargs):
    """Сигнал при записи покупателя."""
    if created:
        payment_system = get_payment_system_by_name(PaymentSystemName.STRIPE)
        remote_customer_id = payment_system.create_customer(consumer=instance)
        instance.remote_consumer_id = remote_customer_id
        instance.save()
