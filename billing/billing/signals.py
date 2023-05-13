from datetime import datetime as dt


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from billing.models import Filmwork, FilmworkSubscribe


@receiver(post_delete, sender=FilmworkSubscribe)
def filmwork_subscribe_changed(sender, **kwargs):
    instance = kwargs.get('instance', None)
    raise ValueError('qqq')
    if instance:
        instance.filmwork.modified_subscribe_date = dt.now()
        instance.filmwork.save()


@receiver(post_save, sender=FilmworkSubscribe)
def filmwork_subscribe_changed(sender, **kwargs):
    instance = kwargs.get('instance', None)
    # raise ValueError('qqq')
    if instance:
        instance.filmwork.modified_subscribe_date = dt.now()
        instance.filmwork.save()
