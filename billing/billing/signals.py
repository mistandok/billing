from django.utils import timezone


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from billing.models import FilmworkSubscribe, Subscribe, Consumer
from billing.stripe import create_product, create_customer


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
    if created:
        create_product(instance)


# @receiver(post_save, sender=Consumer)
# def create_product_signal(sender, created, instance: Consumer, *args, **kwargs):
#     if created:
#         create_customer(instance)
