from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from sharing.core.constants import PermissionModes

from .factories import ClientAuthFactory, ConfigFactory, RootPathConfigFactory


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
        self.folder_url = reverse("folder-list", kwargs={"label": "some-label"})
        self.config_url = reverse("config-list")
        self.urls = self.file_urls + [self.folder_url, self.config_url]

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

    def test_invalid_label(self):
        client_auth = ClientAuthFactory.create()
        config = ConfigFactory.create()
        for url in self.file_urls:
            with self.subTest(url=url):
                response = self.client.get(
                    url, HTTP_AUTHORIZATION=f"Token {client_auth.token}"
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_root_path_config(self):
        client_auth = ClientAuthFactory.create()
        config = ConfigFactory.create(label="some-label", client_auth=client_auth)
        for url in self.file_urls:
            with self.subTest(url=url):
                response = self.client.get(
                    url, HTTP_AUTHORIZATION=f"Token {client_auth.token}"
                )
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_insufficient_permission_in_root_config(self):
        client_auth = ClientAuthFactory.create()
        config = ConfigFactory.create(label="some-label", client_auth=client_auth)
        RootPathConfigFactory.create(
            config=config, folder="some", permission=PermissionModes.read
        )
        upload_url = reverse(
            "file-list", kwargs={"label": "some-label", "folder": "some/folder"}
        )

        response = self.client.post(
            upload_url, HTTP_AUTHORIZATION=f"Token {client_auth.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
