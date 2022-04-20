import factory

from sharing.core.constants import PermissionModes


class ClientAuthFactory(factory.django.DjangoModelFactory):
    organization = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = "core.ClientAuth"


class ConfigFactory(factory.django.DjangoModelFactory):
    label = factory.Faker("word")
    type = "debug"

    class Meta:
        model = "core.Config"

    @factory.post_generation
    def client_auth(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.client_auths.add(extracted)


class RootPathConfigFactory(factory.django.DjangoModelFactory):
    config = factory.SubFactory(ConfigFactory)
    folder = factory.Faker("word")
    permission = PermissionModes.write

    class Meta:
        model = "core.RootPathConfig"
