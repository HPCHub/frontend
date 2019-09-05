from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        User, models.PROTECT,
        null=True, blank=True,
        verbose_name='User'
    )
    balance = models.DecimalField(
        null=True, blank=True,
        decimal_places=2,
        max_digits=12,
        verbose_name='Wallet balance'
    )

    def __str__(self):
        return '{} - {}'.format(self.user.email, self.balance)


class Transaction(models.Model):
    REASON_DEPOSITED = 'DEPOSITED'
    REASON_WITHDRAWN = 'WITHDRAWN'
    REASON_PURCHASE = 'PURCHASE'
    REASON_PURCHASE_REFUND = 'PURCHASE_REFUND'
    REASON_OTHER = 'OTHER'
    REASON_CHOICES = (
        (REASON_DEPOSITED, 'Deposited'),
        (REASON_WITHDRAWN, 'Withdrawn'),
        (REASON_PURCHASE, 'Purchase'),
        (REASON_PURCHASE_REFUND, 'Purchase refund'),
        (REASON_OTHER, 'Other'),
    )

    from_wallet = models.ForeignKey(
        Wallet, models.PROTECT,
        verbose_name='From wallet'
    )
    to_wallet = models.ForeignKey(
        Wallet, models.PROTECT,
        verbose_name='To wallet'
    )
    reason = models.CharField(
        choices=REASON_CHOICES,
        max_length=255
    )
    amount = models.DecimalField(
        null=True, blank=True,
        decimal_places=2,
        max_digits=12,
    )
    created_at = models.DateTimeField(
        auto_created=True
    )

    def __str__(self):
        return '{} - {} - {}'.format(self.from_wallet, self.to_wallet, self.amount)