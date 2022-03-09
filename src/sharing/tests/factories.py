import factory

from sharing.core.constants import ConfigTypes


class ClientAuthFactory(factory.django.DjangoModelFactory):
    organization = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = "core.ClientAuth"


class ConfigFactory(factory.django.DjangoModelFactory):
    label = factory.Faker("word")
    type = ConfigTypes.debug

    class Meta:
        model = "core.Config"

    @factory.post_generation
    def client_auth(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.client_auths.add(extracted)
