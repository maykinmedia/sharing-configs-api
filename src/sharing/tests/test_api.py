import base64
from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from sharing.core.constants import ConfigTypes, PermissionModes
from sharing.core.exceptions import HandlerException, HandlerObjectNotFound

from .factories import ConfigFactory, RootPathConfigFactory
from .utils import TokenAuthMixin


class NotFoundHandler:
    """mock handler to test catching exceptions"""

    def __init__(self, config):
        self.config = config

    def download(self, folder, filename):
        raise HandlerObjectNotFound("not found")

    def upload(self, folder, filename, content, comment, overwrite):
        raise HandlerObjectNotFound("not found")

    def list_files(self, folder):
        raise HandlerObjectNotFound("not found")


class OtherErrorHandler:
    """mock handler to test catching exceptions"""

    def __init__(self, config):
        self.config = config

    def download(self, folder, filename):
        raise HandlerException("other error")

    def upload(self, folder, filename, content, comment, overwrite):
        raise HandlerException("other error")

    def list_files(self, folder):
        raise HandlerException("other error")

    def list_folders(self):
        raise HandlerException("other error")


not_found_registry = {ConfigTypes.debug: NotFoundHandler}
other_error_registry = {ConfigTypes.debug: OtherErrorHandler}


class DownloadFileTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ConfigFactory.create(client_auth=self.client_auth)
        RootPathConfigFactory.create(config=self.config, folder="some")

        self.url = reverse(
            "file-download",
            kwargs={
                "label": self.config.label,
                "folder": "some/folder",
                "filename": "somefile.txt",
            },
        )

    def test_download_file(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        self.assertEqual(response.content, b"example file")

    @patch.dict("sharing.api.views.registry", not_found_registry)
    def test_download_file_not_found(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.dict("sharing.api.views.registry", other_error_registry)
    def test_download_file_error(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b"other error")


class UploadFileTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ConfigFactory.create(client_auth=self.client_auth)
        RootPathConfigFactory.create(config=self.config, folder="some")
        self.url = reverse(
            "file-list", kwargs={"label": self.config.label, "folder": "some/folder"}
        )

    def test_upload_file(self):
        data = {
            "filename": "somefile.txt",
            "content": base64.b64encode(b"example content").decode("utf-8"),
            "author": "some author",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        download_url = reverse(
            "file-download",
            kwargs={
                "label": self.config.label,
                "folder": "some/folder",
                "filename": "somefile.txt",
            },
        )
        self.assertEqual(
            response.json(),
            {
                "download_url": f"http://testserver{download_url}",
                "filename": "somefile.txt",
            },
        )

    @patch.dict("sharing.api.views.registry", not_found_registry)
    def test_upload_file_not_found(self):
        data = {
            "filename": "somefile.txt",
            "content": base64.b64encode(b"example content").decode("utf-8"),
            "author": "some author",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.dict("sharing.api.views.registry", other_error_registry)
    def test_upload_file_error(self):
        data = {
            "filename": "somefile.txt",
            "content": base64.b64encode(b"example content").decode("utf-8"),
            "author": "some author",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ["other error"])


class ListFilesTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ConfigFactory.create(client_auth=self.client_auth)
        RootPathConfigFactory.create(config=self.config, folder="some")
        self.url = reverse(
            "file-list", kwargs={"label": self.config.label, "folder": "some/folder"}
        )

    def test_list_files(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        download_url = reverse(
            "file-download",
            kwargs={
                "label": self.config.label,
                "folder": "some/folder",
                "filename": "example_file.txt",
            },
        )
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "download_url": f"http://testserver{download_url}",
                        "filename": "example_file.txt",
                    }
                ],
            },
        )

    @patch.dict("sharing.api.views.registry", not_found_registry)
    def test_list_files_not_found(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.dict("sharing.api.views.registry", other_error_registry)
    def test_list_files_error(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListFoldersTests(TokenAuthMixin, APITestCase):
    def setUp(self):
        super().setUp()

        self.config = ConfigFactory.create(client_auth=self.client_auth)
        self.url = reverse("folder-list", kwargs={"label": self.config.label})

    def test_list_folders(self):
        RootPathConfigFactory.create(config=self.config, folder="example_folder")
        RootPathConfigFactory.create(config=self.config, folder="example_other_folder")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "example_folder",
                        "children": [{"name": "example_subfolder", "children": []}],
                        "permission": "write",
                    },
                    {
                        "name": "example_other_folder",
                        "children": [],
                        "permission": "write",
                    },
                ],
            },
        )

    @patch.dict("sharing.api.views.registry", other_error_registry)
    def test_list_folders_error(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_folders_no_root_path_config(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )

    def test_list_folders_only_in_root_path_config(self):
        RootPathConfigFactory.create(config=self.config, folder="example_folder")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "example_folder",
                        "children": [{"name": "example_subfolder", "children": []}],
                        "permission": "write",
                    },
                ],
            },
        )

    def test_list_folders_filter_on_permission(self):
        RootPathConfigFactory.create(
            config=self.config,
            folder="example_folder",
            permission=PermissionModes.write,
        )
        RootPathConfigFactory.create(
            config=self.config,
            folder="example_other_folder",
            permission=PermissionModes.read,
        )

        response = self.client.get(self.url, {"permission": PermissionModes.write})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "example_folder",
                        "children": [{"name": "example_subfolder", "children": []}],
                        "permission": "write",
                    },
                ],
            },
        )
