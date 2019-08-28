import json
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer


class HPCProvider(models.Model):
    name = models.CharField(
        max_length=80,
        null=True, blank=True,
        verbose_name='Provider name'
    )

    def __str__(self):
        return self.name



class Formula(models.Model):
    software_type = models.CharField(
        max_length=80,
        null=True, blank=True,
        verbose_name='Software type'
    )
    solver_type = models.CharField(
        max_length=80,
        null=True, blank=True,
        verbose_name='Solver type'
    )
    formula = models.TextField(
        null=True, blank=True,
        verbose_name='Formula'
    )

    def __str__(self):
        return '{} - {}'.format(self.software_type, self.solver_type)


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

    def software_type(self):
        if not self.data:
            return ''
        return str(json.loads(self.data).get('software_type'))

    def solver_type(self):
        if not self.data:
            return ''
        return str(json.loads(self.data).get('solver_type'))

    def request_config(self):
        return mark_safe('<a href="https://ptchk.typeform.com/to/To9Fp9?id={}">'
                         'Request another configuration</a>'.format(self.user.id))
    request_config.allow_tags = True
    request_config.short_description = 'Request URL'

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


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
