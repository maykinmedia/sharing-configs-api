from django.db import migrations
from ..constants import ConfigTypes


def move_github_options_to_json(apps, _):
    Config = apps.get_model("core", "Config")

    for config in Config.objects.filter(type=ConfigTypes.github):
        config.options = {
            "access_token": config.access_token,
            "repo": config.repo,
            "branch": config.branch,
        }
        config.save()


def move_json_to_github_options(apps, _):
    Config = apps.get_model("core", "Config")

    for config in Config.objects.filter(type=ConfigTypes.github):
        config.access_token = config.options["access_token"]
        config.repo = config.options["repo"]
        config.branch = config.options.get("branch", "")
        config.save()


class Migration(migrations.Migration):

    dependencies = [("core", "0003_config_options")]

    operations = [
        migrations.RunPython(move_github_options_to_json, move_json_to_github_options)
    ]
