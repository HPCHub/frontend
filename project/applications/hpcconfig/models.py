from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class HPCProvider(models.Model):
    pass


class Formula(models.Model):
    pass


class ConfigRequest(models.Model):
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True
    )
    data = models.TextField(
        verbose_name='request_data'
    )
    created_at = models.DateTimeField(
        auto_created=True
    )


class ConfigRequestResult(models.Model):
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True
    )
    data = models.TextField(
        verbose_name='request_data'
    )
    request = models.ForeignKey(
        ConfigRequest, models.CASCADE, null=True, blank=True
    )
