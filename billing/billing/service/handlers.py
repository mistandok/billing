from datetime import datetime as dt


from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from billing.models import Filmwork


@receiver(m2m_changed, sender=Filmwork.subscribe.through)
def filmwork_subscribe_changed(sender, **kwargs):
    instance = kwargs.get('instance', None)
    print('q')
    if instance:
        print('1')
        instance.update(modified_subscribe_date=dt.now())
