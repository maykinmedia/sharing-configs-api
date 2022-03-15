from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ConfigFactory
from .utils import TokenAuthMixin


class ConfigAPITests(TokenAuthMixin, APITestCase):
    url = reverse_lazy("config-list")

    def test_list_configs(self):
        config = ConfigFactory.create(client_auth=self.client_auth)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"label": config.label, "type": config.type}],
            },
        )

    def test_list_configs_empty(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 0,
                "next": None,
                "previous": None,
                "results": [],
            },
        )
