import logging
import random

from django.forms import fields
from django.conf import settings
from django.db import models
from .validators import ExtendedUrlValidator
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


class ExtendedUrlFormField(fields.URLField):
    default_validators = [ExtendedUrlValidator()]


class ExtendedUrlField(models.URLField):
    default_validators = [ExtendedUrlValidator()]

    def formfield(self, **kwargs):
        defaults = {'form_class': ExtendedUrlFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class ShortUrl(models.Model):
    short_id = models.SlugField(
        max_length=10,
        null=True,
        verbose_name='Short ID')
    description = models.CharField(
        max_length=80,
        null=True,
        verbose_name='Description')
    basic_url = ExtendedUrlField(
        max_length=200,
        verbose_name='Main url')
    pub_date = models.DateTimeField(
        null=True,
        verbose_name='Created')
    last_click = models.DateTimeField(
        null=True,
        verbose_name='Last click')
    count = models.IntegerField(
        default=0,
        verbose_name='Clicks count')

    def save(self, force_insert=False, force_update=False, **kwargs):
        """
        Saves the url. If insert, generate surl unique token (alias)
        """
        if not self.id:
            self.short_id = None
            while 1:
                url_id = self.gen_token()
                try:
                    ShortUrl.objects.get(short_id=url_id)
                except ShortUrl.DoesNotExist:
                    break
            self.short_id = url_id

        super(ShortUrl, self).save(force_insert, force_update)

    @staticmethod
    def gen_token():
        symbols = 'ab1cd2ef3gh4ij5kl6mn7op8qr9stuvwxyz'
        url_id = ''.join([random.choice(symbols) for i in range(6)])
        return url_id

    def compile(self):
        context = (settings.HOST_PROTO, settings.HOST_URL, self.short_id)
        short_url = "%s://%s/%s" % context
        return short_url

    @property
    def qr_code(self):
        url = 'https://api.qrserver.com/v1/create-qr-code/?data={}/&size=1000x1000&ecc=H'
        if self.short_id:
            return url.format(self.compile())
        else:
            return None

    def show_qr_url(self):
        return mark_safe('<a href="%s">Fullsize</a>' % self.qr_code)
    show_qr_url.allow_tags = True
    show_qr_url.short_description = 'QR url'

    def show_qr_as_pic(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.qr_code)
    show_qr_as_pic.allow_tags = True
    show_qr_as_pic.short_description = 'QR'

    def __str__(self):
        return self.short_id + ' ' + self.description

    class Meta:
        verbose_name = 'Short url'
        verbose_name_plural = 'Short urls'


class UserData(models.Model):
    click_time = models.DateTimeField(
        null=True,
        verbose_name='Click')
    user_data = models.TextField(
        default='[]',
        null=True,
        verbose_name='User agent')
    user_ip = models.CharField(
        null=True,
        max_length=15,
        default='',
        verbose_name='IP'
    )
    short_url = models.ForeignKey(
        ShortUrl,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Short url'
    )

    def __str__(self):
        return str(self.click_time)

    class Meta:
        verbose_name = 'Useragent'
        verbose_name_plural = 'Useragents'
