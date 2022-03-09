from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing.core.models import Config

from .handlers import HANDLER_REGISTRY, BaseHandler
from .renders import BinaryFileRenderer
from .serializers import FileSerializer


class ConfigMixin:
    def get_config(self) -> Config:
        label = self.kwargs["label"]
        return get_object_or_404(Config, label=label, client_auths=self.request.auth)

    def get_handler(self) -> BaseHandler:
        config = self.get_config()
        return HANDLER_REGISTRY[config.type](config)


class FileDetailView(ConfigMixin, APIView):
    renderer_classes = [BinaryFileRenderer]

    @extend_schema(
        operation_id="file_download",
        summary=_("File download"),
        responses={(200, "application/octet-stream"): OpenApiTypes.BINARY},
        parameters=[
            OpenApiParameter(
                name="label",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                required=True,
                description=_(
                    "Name of the configuration. Used to define the parameters for file storage backend"
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
        content = self.download_file()
        return Response(content)

    def download_file(self):
        handler = self.get_handler()
        folder = self.kwargs["folder"]
        filename = self.kwargs["filename"]

        return handler.download(folder, filename)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="label",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
            description=_(
                "Name of the configuration Used to define the parameters for file storage backend"
            ),
        ),
        OpenApiParameter(
            name="folder",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
            description=_("Path to the folder where the configuration file is located"),
        ),
    ],
)
class FileListView(ConfigMixin, APIView):
    serializer_class = FileSerializer

    @extend_schema(
        operation_id="file_upload",
        summary=_("File upload"),
    )
    def post(self, request, **kwargs):
        """Upload configuration file"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.upload_file(
            filename=serializer.validated_data["filename"],
            content=serializer.validated_data["content"].read(),
            author=serializer.validated_data.get("author"),
        )

        return Response(serializer.data)

    @extend_schema(
        operation_id="file_list",
        summary=_("List files"),
    )
    def get(self, request, **kwargs):
        """List all files in the folder"""
        filenames = self.get_files_in_folder()
        files = [{"filename": filename} for filename in filenames]
        serializer = self.get_serializer(instance=files)
        return Response(serializer.data)

    def get_serializer(self, **kwargs):
        if self.request.method == "GET":
            kwargs["many"] = True

        return self.serializer_class(
            context={"request": self.request, "view": self},
            **kwargs,
        )

    def upload_file(self, filename, content, author=None):
        handler = self.get_handler()
        folder = self.kwargs["folder"]
        comment = self.request.auth.get_comment(author)

        return handler.upload(
            folder=folder,
            filename=filename,
            content=content,
            comment=comment,
        )

    def get_files_in_folder(self):
        handler = self.get_handler()
        folder = self.kwargs["folder"]

        return handler.list_files(folder=folder)
