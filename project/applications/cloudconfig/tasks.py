import time

from core.utils.mails import send_machine_credentials_mail
from celery.task import task
from .models import LaunchHistory
from core.utils import jenkins_api


@task
def build_machine(launch_pk):
    time.sleep(3)
    LaunchHistory.objects.all()
    launch = LaunchHistory.objects.get(hashed_id=launch_pk)
    single_id, ip_data, key_data = jenkins_api.build_machine()
    launch.jenkins_single_id = single_id
    launch.machine_ip = ip_data
    launch.machine_key = key_data
    launch.status = 'running'
    launch.save()
    try:
        send_machine_credentials_mail(launch.user.email, ip_data, key_data, single_id)
    finally:
        pass


@task
def kill_machine(single_id):
    jenkins_api.kill_machine(single_id)

