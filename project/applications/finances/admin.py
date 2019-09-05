from django.contrib import admin
from .models import Wallet, Transaction

# Register your models here.

class TransactionInline(admin.StackedInline):
    model = Transaction


class WalletAdmin(admin.ModelAdmin):
    model = Wallet

    inlines = [TransactionInline,]


admin.site.register(Wallet, WalletAdmin)
