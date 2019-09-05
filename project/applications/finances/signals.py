from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Transaction

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def on_new_transaction(sender, instance, **kwargs):
    if kwargs['created']:
        from_wallet = instance.from_wallet
        to_wallet = instance.to_wallet
        amount = instance.amount
        from_wallet.balance = from_wallet.balance - amount
        from_wallet.save()
        to_wallet.balance += amount
        to_wallet.save()