import json

from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer


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

    def pretty_data(self):
        if not self.data:
            return ''
        try:
            points = json.dumps(
                json.loads(self.data), sort_keys=True,
                indent=2, ensure_ascii=False
            )
        except Exception:
            return ''
        formatter = HtmlFormatter(style='colorful')
        output = highlight(points, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + output)
    pretty_data.allow_tags = True
    pretty_data.short_description = 'Data'

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.created_at)


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
