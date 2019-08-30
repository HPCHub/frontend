import json

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ConfigRequest, ConfigRequestResult, Formula
from core.utils.db_api import process_config_request

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ConfigRequest)
def on_new_config_request(sender, instance, **kwargs):
    if kwargs['created']:
        data = json.loads(instance.data)
        software_type = data.get('software_type')
        solver_type = data.get('solver_type')
        formulas = Formula.objects.filter(software_type=software_type, provider__is_active=True)
        if solver_type:
            formulas = formulas.filter(solver_type=solver_type)
        for formula in formulas:
            if formula.provider.name == 'Google':
                data = process_config_request(instance, formula.formula)
                result = json.loads(formula.provider.template)
                result['machineType'] = data[0].get('machine_type')
                result['disks'][0]['initializeParams']['diskSizeGb'] = data[0].get('hdd_size')
                result = ConfigRequestResult.objects.create(
                    user = instance.user,
                    config_request=instance,
                    data=json.dumps(result),
                    provider=formula.provider
                )
                result.save()
                return result
