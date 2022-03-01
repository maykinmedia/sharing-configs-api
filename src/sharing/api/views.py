from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView

from sharing.core.models import ClientConfig

from .handlers import HANDLER_REGISTRY, BaseHandler
from .serializers import FileSerializer


class ConfigMixin:
    def get_config(self) -> ClientConfig:
        slug = self.kwargs["slug"]
        return get_object_or_404(ClientConfig, client_auth=self.request.auth, slug=slug)

    def get_handler(self) -> BaseHandler:
        config = self.get_config()
        return HANDLER_REGISTRY[config.type](config)


class FileDetailView(APIView):
    serializer_class = FileSerializer

    def get(self, request, **kwargs):
        file = self.download_file()
        serializer = self.serializer_class(file)
        return Response(serializer.data)

    def download_file(self):
        handler = get_handler()
        folder = self.kwargs["folder"]
        file = self.kwargs["file"]

        return handler.download(folder, file)


class FileListView(APIView):
    serializer_class = FileSerializer

    def post(self, request, **kwargs):
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = self.upload_file(
            filename=serializer.data["filename"], content=serializer.data["content"]
        )

        serializer.instance = file
        return Response(serializer.data)

    def upload_file(self, filename, content):
        handler = get_handler()
        folder = self.kwargs["folder"]

        return handler.upload(folder=folder, filename=filename, content=content)
