from django.apps import AppConfig


class GitHubConfig(AppConfig):
    name = "sharing.contrib.github"

    def ready(self):
        from . import handlers  # noqa
