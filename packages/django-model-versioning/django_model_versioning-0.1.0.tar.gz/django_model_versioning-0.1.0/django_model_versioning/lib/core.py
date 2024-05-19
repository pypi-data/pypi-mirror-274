from django.apps import apps
import importlib


def autodiscover_module(module):
    for app_name in apps.app_configs.keys():
        try:
            importlib.import_module('.'.join([app_name, module]))
        except ImportError:
            pass
