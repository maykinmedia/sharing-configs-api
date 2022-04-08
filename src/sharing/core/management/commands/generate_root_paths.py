from django.core.management import BaseCommand

from ...constants import PermissionModes
from ...handlers import registry
from ...models import Config, RootPathConfig


class Command(BaseCommand):
    help = "Generate root path configs for all available configs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--write",
            action="store_true",
            help="Generate 'write' permission for all new root paths",
        )
        parser.set_defaults(write=False)

    def handle(self, *args, **options):
        permission = PermissionModes.write if options["write"] else PermissionModes.read
        generated = 0

        for config in Config.objects.all():
            handler = registry[config.type](config)
            folders = handler.list_folders()
            for folder in folders:
                root_path_config, created = RootPathConfig.objects.update_or_create(
                    config=config,
                    folder=folder.name,
                    defaults={"permission": permission},
                )
                if created:
                    generated += 1

        self.stdout.write(f"{generated} root path configs were generated")
