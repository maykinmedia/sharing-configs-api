from django.test import TestCase

import requests_mock

from sharing.core.exceptions import HandlerException, HandlerObjectNotFound
from sharing.tests.factories import ConfigFactory, ConfigTypes

from ..handlers import GitHubHandler
from .utils import mock_github_file, mock_github_repo, mock_github_update_file

GITHUB_BASE_URL = "https://api.github.com:443/"


@requests_mock.Mocker()
class GitHubHandlerTests(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.config = ConfigFactory.create(
            type=ConfigTypes.github, access_token="12345", repo="some/repo"
        )
        self.handler = GitHubHandler(config=self.config)
        self.folder = "some/folder"
        self.filename = "somefile.txt"

    def test_download_file(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            json=mock_github_repo(name=self.config.repo),
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}/{self.filename}",
            json=mock_github_file(self.folder, self.filename, repo=self.config.repo),
        )

        file_content = self.handler.download(self.folder, self.filename)

        self.assertEqual(file_content, b"example content")

    def test_download_file_not_found(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=404,
            json={"message": "Not Found"},
        )
        with self.assertRaises(HandlerObjectNotFound):
            self.handler.download(self.folder, self.filename)

    def test_download_file_error(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=400,
            json={"message": "Client Error"},
        )
        with self.assertRaises(HandlerException):
            self.handler.download(self.folder, self.filename)

    def test_list_files(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            json=mock_github_repo(name=self.config.repo),
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}",
            json=[mock_github_file(self.folder, "somefile.txt", repo=self.config.repo)],
        )

        files = self.handler.list_files(self.folder)

        self.assertEqual(files, ["somefile.txt"])

    def test_list_files_not_found(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=404,
            json={"message": "Not Found"},
        )
        with self.assertRaises(HandlerObjectNotFound):
            self.handler.list_files(self.folder)

    def test_list_files_error(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=400,
            json={"message": "Client Error"},
        )
        with self.assertRaises(HandlerException):
            self.handler.list_files(self.folder)

    def test_upload_file(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            json=mock_github_repo(name=self.config.repo),
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}",
            json=[
                mock_github_file(self.folder, "otherfile.txt", repo=self.config.repo)
            ],
        )
        m.put(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}/{self.filename}",
            json=mock_github_update_file(
                self.folder, self.filename, repo=self.config.repo
            ),
        )
        self.handler.upload(
            self.folder,
            self.filename,
            content=b"example content",
            comment="some comment",
        )

    def test_upload_file_not_found(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=404,
            json={"message": "Not Found"},
        )
        with self.assertRaises(HandlerObjectNotFound):
            self.handler.upload(
                self.folder,
                self.filename,
                content=b"example content",
                comment="some comment",
            )

    def test_upload_file_error(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            status_code=400,
            json={"message": "Client Error"},
        )
        with self.assertRaises(HandlerException):
            self.handler.upload(
                self.folder,
                self.filename,
                content=b"example content",
                comment="some comment",
            )

    def test_upload_file_overwrite_existed(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            json=mock_github_repo(name=self.config.repo),
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}",
            json=[mock_github_file(self.folder, "somefile.txt", repo=self.config.repo)],
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}/{self.filename}",
            json=mock_github_file(self.folder, "somefile.txt", repo=self.config.repo),
        )
        m.put(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}/{self.filename}",
            json=mock_github_update_file(
                self.folder, self.filename, repo=self.config.repo
            ),
        )

        self.handler.upload(
            self.folder,
            self.filename,
            content=b"example content",
            comment="some comment",
            overwrite=True,
        )

    def test_upload_file_not_overwrite_existed(self, m):
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}",
            json=mock_github_repo(name=self.config.repo),
        )
        m.get(
            f"{GITHUB_BASE_URL}repos/{self.config.repo}/contents/{self.folder}",
            json=[mock_github_file(self.folder, "somefile.txt", repo=self.config.repo)],
        )
        with self.assertRaises(HandlerException):
            self.handler.upload(
                self.folder,
                self.filename,
                content=b"example content",
                comment="some comment",
            )
