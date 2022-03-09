import logging
from dataclasses import dataclass
from typing import List

from django.core.exceptions import ImproperlyConfigured

from sharing.core.constants import ConfigTypes
from sharing.core.models import Config

logger = logging.getLogger(__name__)


@dataclass
class BaseHandler:
    config: Config

    def download(self, folder: str, filename: str) -> bytes:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        :return: The content of the file
        """
        raise ImproperlyConfigured("'download_content' method should be defined")

    def upload(self, folder: str, filename: str, content: bytes, comment: str) -> None:
        """
        Hook to overwrite. Should include interaction with underlying file storage

        """
        raise ImproperlyConfigured("'upload_content' method should be defined")

    def list_files(self, folder: str) -> List[str]:
        raise ImproperlyConfigured("'list_files' method should be defined")


class DebugHandler(BaseHandler):
    """handler used for testing, It downloads the example file and uploads file into stdout"""

    def download(self, folder: str, filename: str):
        return b"example file"

    def upload(
        self,
        folder: str,
        filename: str,
        content: bytes,
        comment: str,
    ):
        logger.info(f"DebugHandler: {comment}")

    def list_files(self, folder: str):
        return ["example_file.txt"]


HANDLER_REGISTRY = {ConfigTypes.debug: DebugHandler}
