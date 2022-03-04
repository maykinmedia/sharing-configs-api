import base64

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .factories import ClientConfigFactory
from .utils import TokenAuthMixin


class DownloadFileTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ClientConfigFactory.create(client_auth=self.client_auth)

    def test_download_file_debug(self):
        url = reverse(
            "file-download",
            kwargs={
                "slug": self.config.slug,
                "folder": "some/folder",
                "filename": "somefile.txt",
            },
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        self.assertEqual(response.content, b"example file")


class UploadFileTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ClientConfigFactory.create(client_auth=self.client_auth)

    def test_upload_file_debug(self):
        url = reverse(
            "file-list", kwargs={"slug": self.config.slug, "folder": "some/folder"}
        )
        data = {
            "filename": "somefile.txt",
            "content": base64.b64encode(b"example content").decode("utf-8"),
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        download_url = reverse(
            "file-download",
            kwargs={
                "slug": self.config.slug,
                "folder": "some/folder",
                "filename": "somefile.txt",
            },
        )
        self.assertEqual(
            response.json(),
            {
                "url": f"http://testserver{download_url}",
                "filename": "somefile.txt",
            },
        )


class ListFilesTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ClientConfigFactory.create(client_auth=self.client_auth)

    def test_list_files_debug(self):
        url = reverse(
            "file-list", kwargs={"slug": self.config.slug, "folder": "some/folder"}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        download_url = reverse(
            "file-download",
            kwargs={
                "slug": self.config.slug,
                "folder": "some/folder",
                "filename": "example_file.txt",
            },
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "url": f"http://testserver{download_url}",
                    "filename": "example_file.txt",
                }
            ],
        )
