from django.apps import AppConfig


class HpcconfigConfig(AppConfig):
    name = 'hpcconfig'

    def ready(self):
        import hpcconfig.signals
