from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "sharing.utils"

    def ready(self):
        from . import checks  # noqa
