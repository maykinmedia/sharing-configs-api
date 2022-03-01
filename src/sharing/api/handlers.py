import logging
from dataclasses import dataclass

from django.core.files.uploadedfile import SimpleUploadedFile

from sharing.core.constants import ConfigTypes
from sharing.core.models import ClientConfig

logger = logging.getLogger(__name__)


class BaseHandler:
    config: ClientConfig

    def __post_init__(self):
        type = self.config.type
        if type in handler_registry:
            raise ImproperlyConfigured(
                "Handler with type '%s' already exists" % self.name
            )
        handler_registry[type] = self

    def download(self, folder: str, filename: str) -> bytes:
        raise ImproperlyConfigured("'download' method should be defined")

    def upload(self, folder: str, filename: str, content: bytes):
        raise ImproperlyConfigured("'upload' method should be defined")


class DebugHandler(BaseHandler):
    """handler used for testing, It downloads the example file and uploads file into stdout"""

    def download(self, folder: str, filename: str):
        return SimpleUploadedFile(name=filename, content=b"example file")

    def upload(self, folder: str, filename: str, content: bytes):
        logger.info(f"file {filename} is uploaded with DebugHandler to stdout")


HANDLER_REGISTRY = {ConfigTypes.debug: DebugHandler}
