from django.apps import AppConfig


class CloudconfigConfig(AppConfig):
    name = 'cloudconfig'

    def ready(self):
        import cloudconfig.signals
