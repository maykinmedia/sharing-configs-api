import logging
from typing import List

from django.core.exceptions import ImproperlyConfigured

from sharing.core.constants import ConfigTypes
from sharing.core.models import Config

from .data import Folder

logger = logging.getLogger(__name__)

registry = {}


class BaseHandler:
    """
    Base class for Sharing Config handlers.
    """

    def __init__(self, config: Config):
        self.config = config

    def __init_subclass__(cls, /, type: str, **kwargs):
        super().__init_subclass__(**kwargs)

        registry[type] = cls

    def download(self, folder: str, filename: str) -> bytes:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :return: The content of the file
        :raise: HandlerException or HandlerObjectNotFound
        """
        raise ImproperlyConfigured("'download_content' method should be defined")

    def upload(
        self,
        folder: str,
        filename: str,
        content: bytes,
        comment: str,
        overwrite: bool = False,
    ) -> None:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :raise: HandlerException or HandlerObjectNotFound
        """
        raise ImproperlyConfigured("'upload_content' method should be defined")

    def list_files(self, folder: str) -> List[str]:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :return: The list of filenames in the folder.
        :raise: HandlerException or HandlerObjectNotFound
        """
        raise ImproperlyConfigured("'list_files' method should be defined")

    def list_folders(self) -> List[Folder]:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :return: The list of folders for the config. Each folder can have related subfolders
        :raise: HandlerException
        """
        raise ImproperlyConfigured("'list_folders' method should be defined")


class DebugHandler(BaseHandler, type=ConfigTypes.debug):
    """handler used for testing, It downloads the example file and uploads file into stdout"""

    def download(self, folder: str, filename: str):
        return b"example file"

    def upload(
        self,
        folder: str,
        filename: str,
        content: bytes,
        comment: str,
        overwrite: bool = False,
    ):
        logger.info(f"DebugHandler: {comment}")

    def list_files(self, folder: str):
        return ["example_file.txt"]

    def list_folders(self):
        return [
            Folder(name="example_folder", children=[Folder(name="example_subfolder")])
        ]
