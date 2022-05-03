from typing import List, Type

from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers

from .data import Folder
from .serializers import JsonSchemaSerializer

registry = {}


class BaseHandler:
    """
    Base class for Sharing Config handlers.
    A handler class is the combination of a handler callbacks and a set of options that
    are handler specific
    """

    configuration_options: Type[serializers.Serializer] = JsonSchemaSerializer
    """
    A serializer class describing the handler-specific configuration options.
    """

    def __init__(self, config):
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
