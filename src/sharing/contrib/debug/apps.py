from django.apps import AppConfig


class GitHubConfig(AppConfig):
    name = "sharing.contrib.debug"

    def ready(self):
        from . import handlers  # noqa
