import json

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from finances.models import Transaction, Wallet
from .models import ConfigRequest, ConfigRequestResult, Formula, CloudStatusHistory, LaunchHistory
from core.utils.db_api import process_config_request

import logging
from functools import wraps


logger = logging.getLogger(__name__)



def skip_signal():
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_signal


@receiver(post_save, sender=LaunchHistory)
@skip_signal()
def on_new_launch(sender, instance, **kwargs):
    print(instance.changed_fields)
    if kwargs['created']:
        CloudStatusHistory.objects.create(
            status='starting',
            launch=instance,
            created_at=timezone.now()
        )
    else:
        if 'status' in instance.changed_fields:
            CloudStatusHistory.objects.create(
                status=instance.status,
                launch=instance,
                created_at=timezone.now()
            )


@receiver(post_save, sender=CloudStatusHistory)
def on_new_status(sender, instance, **kwargs):
    if kwargs['created']:
        if instance.status in ['finished', 'killed', 'error']:
            launch = instance.launch
            launch.finished_at = instance.created_at
            launch.total_price = launch.current_price()
            launch.skip_signal  = True
            launch.save()
            Transaction.objects.create(
                from_wallet=instance.launch.user.wallet,
                to_wallet=Wallet.objects.get(user__username='admin'),
                amount=launch.total_price,
                reason=Transaction.REASON_PURCHASE,
                created_at=instance.created_at
            )



@receiver(post_save, sender=ConfigRequest)
def on_new_config_request(sender, instance, **kwargs):
    storage_types = {
        'ssd': 'storage_ssd_price',
        'hdd': 'storage_hdd_price',
        'glusterfs': 'storage_glusterfs_price'
    }
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

                cores = data[0].get('cores')
                ram = data[0].get('ram_size')
                storage_size = data[0].get('hdd_size')
                storage_type = 'ssd'
                hourly_price = \
                    formula.provider._meta.get_field(storage_types.get(storage_type)).value_from_object(formula.provider) * float(storage_size) + \
                    formula.provider.core_price * float(cores) + \
                    formula.provider.mem_price * float(ram)
                result = ConfigRequestResult.objects.create(
                    user = instance.user,
                    config_request=instance,
                    provider=formula.provider,
                    cores=cores,
                    ram_memory=ram,
                    storage_size=storage_size,
                    storage_type=storage_type,
                    price_per_hour=hourly_price
                )
                result.save()
                return result
