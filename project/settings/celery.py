from __future__ import absolute_import, unicode_literals

from .secret import RABBIT_LOGIN, RABBIT_PASSWORD

broker_url = 'amqp://{}:{}@localhost:5672'.format(RABBIT_LOGIN, RABBIT_PASSWORD)
accept_content = ['json']
enable_utc = False
task_serializer = 'json'
result_backend = 'django-db'
timezone = 'UTC'
task_track_started = True
worker_hijack_root_logger = False
worker_redirect_stdouts_level = 'ERROR'
beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
result_expires = 60 * 10
