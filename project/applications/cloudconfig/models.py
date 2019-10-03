import json
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# Create your models here.
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from core.mixins.model_mixins import ModelDiffMixin

STATUSES = (
    ('unknown', 'Unknown'),
    ('starting', 'Starting'),
    ('running', 'Running'),
    ('finished', 'Finished'),
    ('killed', 'Killed'),
    ('error', 'Error')
)



class CloudProvider(models.Model):
    name = models.CharField(
        max_length=80,
        null=True, blank=True,
    )
    template = models.TextField(
        null=True, blank=True,
    )
    other_price = models.FloatField(
        null=True, blank=True,
    )
    core_price = models.FloatField(
        null=True, blank=True
    )
    mem_price = models.FloatField(
        null=True, blank=True
    )
    storage_ssd_price = models.FloatField(
        null=True, blank=True
    )
    storage_hdd_price = models.FloatField(
        null=True, blank=True
    )
    storage_glusterfs_price = models.FloatField(
        null=True, blank=True
    )
    is_active = models.BooleanField(
        default=True,
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
    provider = models.ForeignKey(
        CloudProvider, models.PROTECT,
        null=True, blank=True,
    )

    formula = models.TextField(
        null=True, blank=True,
        help_text="""
            Select {formula} from cloudconfig_configrequest 
            where id={request_id}
            
            So you need to write formula
        """
    )

    def clean(self):
        if ';' in self.formula:
            raise ValidationError('You can not use ";" symbol')

    def __str__(self):
        return '{} - {} - {}'.format(self.provider, self.software_type, self.solver_type)


class ConfigRequest(models.Model):
    hashed_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=80, null=True, blank=True
    )
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


    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.hashed_id,))


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
        if self.name:
            return '{} - {} - {}'.format(self.name, self.user.username, self.created_at)
        return '{} - {}'.format(self.user.username, self.created_at)


class ConfigRequestResult(models.Model):
    TYPES = (
        ('optimal', 'Optimal'),
        ('speed', 'Speed'),
        ('price', 'Price'),
    )

    hashed_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True
    )
    config_type = models.CharField(
        choices=TYPES, max_length=30,
        default='optimal'
    )
    cores = models.IntegerField(
        null=True, blank=True,
    )
    ram_memory = models.IntegerField(
        null=True, blank=True,
    )
    storage_type = models.CharField(
        max_length=30,
        null=True, blank=True,
    )
    storage_size = models.IntegerField(
        null=True, blank=True,
    )
    price_per_hour = models.FloatField(
        null=True, blank=True,
    )
    provider = models.ForeignKey(
        CloudProvider, models.PROTECT,
        null=True, blank=True
    )
    config_request = models.ForeignKey(
        ConfigRequest, models.PROTECT,
        null=True, blank=True
    )


    def __str__(self):
        return '{} - {}'.format(self.config_request, self.provider.name)



class LaunchHistory(models.Model, ModelDiffMixin):
    hashed_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True
    )
    provider = models.ForeignKey(
        CloudProvider, models.PROTECT,
        null=True, blank=True
    )
    config_request = models.ForeignKey(
        ConfigRequest, models.PROTECT,
        null=True, blank=True
    )
    config_request_result = models.ForeignKey(
        ConfigRequestResult, models.PROTECT,
        null=True, blank=True
    )
    started_at = models.DateTimeField(
        auto_created=True
    )
    finished_at = models.DateTimeField(
        null=True, blank=True
    )
    total_price = models.FloatField(
        null=True, blank=True,
    )
    status = models.CharField(
        choices=STATUSES, max_length=30,
        default='unknown'
    )

    def current_price(self):
        start_datetime = CloudStatusHistory.objects.filter(launch=self, status='starting').first().created_at
        finish_datetime = CloudStatusHistory.objects.filter(launch=self, status__in=['finished', 'killed', 'error']).order_by('-created_at').first()
        if finish_datetime:
            finish_datetime = finish_datetime.created_at
        if not finish_datetime:
            finish_datetime = timezone.now()
        return round((finish_datetime-start_datetime).total_seconds() * self.config_request_result.price_per_hour / 60 / 60, 2)


    def colored_status(self):
        STATUS_COLORS = {
            'unknown': 'gray',
            'starting': 'blue',
            'running': 'blue',
            'finished': 'green',
            'killed': 'red',
            'error': 'red'
        }
        color = STATUS_COLORS.get(self.status, 'gray')
        return format_html(
            '<b><span style="color: {0};">{1}</span></b>', color, self.status.capitalize()
        )

    colored_status.allow_tags = True
    colored_status.short_description = 'Cloud status'

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.hashed_id,))



class CloudStatusHistory(models.Model):
    hashed_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False
    )
    status = models.CharField(
        choices=STATUSES, max_length=30,
        default='unknown'
    )
    launch = models.ForeignKey(
        LaunchHistory, models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_created=True
    )