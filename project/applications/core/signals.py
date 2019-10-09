from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from finances.models import Wallet


@receiver(post_save, sender=User)
def on_new_user(sender, instance, **kwargs):
    if kwargs['created']:
        wallet = Wallet.objects.create(
            user=instance,
            balance=5000,
        )
        wallet.save()