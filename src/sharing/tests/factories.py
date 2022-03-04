from django.utils.text import slugify

import factory

from sharing.core.constants import ConfigTypes


class ClientAuthFactory(factory.django.DjangoModelFactory):
    organization = factory.Faker("name")
    email = factory.Faker("email")

    class Meta:
        model = "core.ClientAuth"


class ClientConfigFactory(factory.django.DjangoModelFactory):
    client_auth = factory.SubFactory(ClientAuthFactory)
    label = factory.Faker("name")
    slug = factory.LazyAttribute(lambda a: slugify(a.label))
    type = ConfigTypes.debug

    class Meta:
        model = "core.ClientConfig"
