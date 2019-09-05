from django.contrib import admin
from .models import Wallet, Transaction

# Register your models here.

class FromTransactionInline(admin.StackedInline):
    model = Transaction
    fk_name = 'from_wallet'


class ToTransactionInline(admin.StackedInline):
    model = Transaction
    fk_name = 'to_wallet'


class WalletAdmin(admin.ModelAdmin):
    model = Wallet

    inlines = [FromTransactionInline, ToTransactionInline, ]


admin.site.register(Wallet, WalletAdmin)
