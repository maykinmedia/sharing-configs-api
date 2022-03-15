from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ClientAuthFactory, ConfigFactory


class TokenAuthTests(APITestCase):
    def setUp(self) -> None:
        self.file_urls = [
            reverse(
                "file-download",
                kwargs={
                    "label": "some-label",
                    "folder": "some/folder",
                    "filename": "somefile.txt",
                },
            ),
            reverse(
                "file-list", kwargs={"label": "some-label", "folder": "some/folder"}
            ),
        ]
        self.config_url = reverse("config-list")
        self.urls = self.file_urls + [self.config_url]

    def test_non_auth(self):
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        ClientAuthFactory.create()
        ConfigFactory.create()
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(url, HTTP_AUTHORIZATION="Token 12345")
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_slug(self):
        client_auth = ClientAuthFactory.create()
        config = ConfigFactory.create()
        for url in self.file_urls:
            with self.subTest(url=url):
                response = self.client.get(
                    url, HTTP_AUTHORIZATION=f"Token {client_auth.token}"
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
