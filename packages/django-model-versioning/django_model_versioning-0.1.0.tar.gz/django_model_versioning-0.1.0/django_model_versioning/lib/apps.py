from django.apps import AppConfig


class ModelVersioningConfig(AppConfig):
    name = 'django_model_versioning'
    verbose_name = 'DjangoModelVersioning'

    def ready(self):
        from lib.core import autodiscover_module

        autodiscover_module('versioning')
