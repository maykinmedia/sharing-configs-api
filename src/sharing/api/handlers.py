import logging

from django.core.exceptions import ImproperlyConfigured
from django.core.files.uploadedfile import SimpleUploadedFile

from sharing.core.constants import ConfigTypes
from sharing.core.models import ClientConfig

from .data import FileData

logger = logging.getLogger(__name__)


class BaseHandler:
    config: ClientConfig

    def download(self, folder: str, filename: str) -> FileData:
        """This method is used in the Download API endpoint"""
        file_content = self.download_content(folder, filename)
        file = FileData(
            slug=self.config.slug,
            folder=folder,
            filename=filename,
            content=file_content,
        )
        return file

    def upload(self, folder: str, filename: str, content: bytes) -> FileData:
        """This method is used in the Upload API endpoint"""
        self.upload_content(folder, filename, content)

        file = FileData(
            slug=self.config.slug,
            folder=folder,
            filename=filename,
            content=content,
        )
        return file

    def download_content(self, folder: str, filename: str) -> bytes:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :return: The content of the file
        """
        raise ImproperlyConfigured("'download_content' method should be defined")

    def upload_content(self, folder: str, filename: str, content: bytes) -> None:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        """
        raise ImproperlyConfigured("'upload_content' method should be defined")


class DebugHandler(BaseHandler):
    """handler used for testing, It downloads the example file and uploads file into stdout"""

    def download_content(self, folder: str, filename: str):
        return SimpleUploadedFile(name=filename, content=b"example file")

    def upload_content(self, folder: str, filename: str, content: bytes):
        logger.info(f"file {filename} is uploaded with DebugHandler to stdout")


HANDLER_REGISTRY = {ConfigTypes.debug: DebugHandler}
