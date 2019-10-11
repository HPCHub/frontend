import time

import re

from django.utils import timezone
from core.utils.mails import send_machine_credentials_mail
from celery.task import task
from .models import LaunchHistory
from core.utils import jenkins_api


@task
def build_machine(launch_pk):
    time.sleep(3)
    LaunchHistory.objects.all()
    launch = LaunchHistory.objects.get(hashed_id=launch_pk)
    if launch.provider.name == 'Google':
        single_id, ip_data, key_data = jenkins_api.build_default_gcp()
    else:
        single_id, ip_data, key_data = jenkins_api.build_default_oci()
    launch.jenkins_single_id = single_id
    launch.machine_ip = ip_data
    launch.machine_key = key_data
    launch.status = 'running'
    launch.save()
    if launch.config_request.name:
        cleared_name = re.sub('[^A-Za-z0-9]+', '_', launch.config_request.name)
        filename = 'SSHkey_{}_{}'.format(
            cleared_name,
            (timezone.now()-timezone.timedelta(hours=7)).strftime('%Y_%m_%d_%H_%M')
        )
    else:
        filename = 'SSHkey_{}'.format(
            (timezone.now() - timezone.timedelta(hours=7)).strftime('%Y_%m_%d_%H_%M')
        )
    try:
        if launch.config_request.name:
            send_machine_credentials_mail(launch.user.email, ip_data, key_data, filename, config_name=launch.config_request.name)
        else:
            send_machine_credentials_mail(launch.user.email, ip_data, key_data, filename)
    finally:
        pass


@task
def kill_machine(provider, single_id):
    if provider == 'Google':
        jenkins_api.kill_machine_gcp(single_id)
    else:
        jenkins_api.kill_machine_oci(single_id)


@task
def process_balance():
    running_instances = LaunchHistory.objects.filter(status='running')
    for instance in running_instances:
        pass