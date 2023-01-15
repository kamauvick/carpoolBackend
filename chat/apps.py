from django.apps import AppConfig

class WbbackendConfig(AppConfig):
    name = 'WBBackend'

    def ready(self):
        from . import signals
