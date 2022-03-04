from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing.core.models import ClientConfig

from .handlers import HANDLER_REGISTRY, BaseHandler
from .serializers import FileContentSerializer


class ConfigMixin:
    def get_config(self) -> ClientConfig:
        slug = self.kwargs["slug"]
        return get_object_or_404(ClientConfig, client_auth=self.request.auth, slug=slug)

    def get_handler(self) -> BaseHandler:
        config = self.get_config()
        return HANDLER_REGISTRY[config.type](config)


class FileDetailView(ConfigMixin, APIView):
    serializer_class = FileContentSerializer

    @extend_schema(
        operation_id="file_download",
        summary=_("File download"),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_(
                    "Slug label of the client configuration. Used to define the type of backend"
                ),
            ),
            OpenApiParameter(
                name="folder",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_(
                    "Path to the folder where the configuration file is located"
                ),
            ),
            OpenApiParameter(
                name="filename",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_("Name of the configuration file"),
            ),
        ],
    )
    def get(self, request, **kwargs):
        """Download configuration file"""
        file = self.download_file()
        serializer = self.serializer_class(file)
        return Response(serializer.data)

    def download_file(self):
        handler = self.get_handler()
        folder = self.kwargs["folder"]
        filename = self.kwargs["filename"]

        return handler.download(folder, filename)


class FileListView(ConfigMixin, APIView):
    serializer_class = FileContentSerializer

    @extend_schema(
        operation_id="file_upload",
        summary=_("File upload"),
        parameters=[
            OpenApiParameter(
                name="slug",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_(
                    "Slug label of the client configuration. Used to define the type of backend"
                ),
            ),
            OpenApiParameter(
                name="folder",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_(
                    "Path to the folder where the configuration file is located"
                ),
            ),
        ],
    )
    def post(self, request, **kwargs):
        """Upload configuration file"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = self.upload_file(
            filename=serializer.data["filename"], content=serializer.data["content"]
        )

        serializer.instance = file
        return Response(serializer.data)

    def upload_file(self, filename, content):
        handler = self.get_handler()
        folder = self.kwargs["folder"]

        return handler.upload(folder=folder, filename=filename, content=content)
