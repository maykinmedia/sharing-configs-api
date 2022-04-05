from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing.core.handlers import BaseHandler, registry
from sharing.core.models import Config
from sharing.utils.mixins import PaginationMixin

from .exceptions import handler_errors_for_api
from .renders import BinaryFileRenderer
from .serializers import ConfigSerializer, FileSerializer, FolderSerializer


class ConfigMixin:
    def get_config(self) -> Config:
        label = self.kwargs["label"]
        return get_object_or_404(Config, label=label, client_auths=self.request.auth)

    def get_handler(self) -> BaseHandler:
        config = self.get_config()
        return registry[config.type](config)


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
        tags=["files"],
    )
    def get(self, request, **kwargs):
        """Download configuration file"""
        content = self.download_file()
        return Response(content)

    @handler_errors_for_api
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
    tags=["files"],
)
class FileListView(ConfigMixin, PaginationMixin, APIView):
    serializer_class = FileSerializer
    pagination_class = PageNumberPagination

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
            overwrite=serializer.validated_data.get("overwrite", False),
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

        page = self.paginate_objects(files)
        serializer = self.get_serializer(instance=page)
        return self.get_paginated_response(serializer.data)

    def get_serializer(self, **kwargs):
        if self.request.method == "GET":
            kwargs["many"] = True

        return self.serializer_class(
            context={"request": self.request, "view": self},
            **kwargs,
        )

    @handler_errors_for_api
    def upload_file(self, filename, content, author=None, overwrite=False):
        handler = self.get_handler()
        folder = self.kwargs["folder"]
        comment = self.request.auth.get_comment(author)

        handler.upload(
            folder=folder,
            filename=filename,
            content=content,
            comment=comment,
            overwrite=overwrite,
        )

    @handler_errors_for_api
    def get_files_in_folder(self):
        handler = self.get_handler()
        folder = self.kwargs["folder"]

        return handler.list_files(folder=folder)


@extend_schema_view(
    get=extend_schema(
        operation_id="config_list",
        summary=_("List configs"),
        description=_("List all available configs"),
    )
)
class ConfigListView(ListAPIView):
    serializer_class = ConfigSerializer
    queryset = Config.objects.order_by("label")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(client_auths=self.request.auth).distinct()


class FolderView(ConfigMixin, APIView):
    serializer_class = FolderSerializer

    def get(self, request, **kwargs):
        """List all folders recursively"""
        folders = self.get_folders()

        serializer = self.serializer_class(instance=folders, many=True)
        return Response(serializer.data)

    @handler_errors_for_api
    def get_folders(self):
        handler = self.get_handler()
        folders = handler.list_folders()

        # todo add permissions to folders and serialziers
        # todo add pagination
        return folders
