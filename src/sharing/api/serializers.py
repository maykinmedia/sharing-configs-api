from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from rest_framework import fields, serializers
from rest_framework.reverse import reverse

from sharing.core.models import Config

from .fields import AnyBase64FileField


class FileSerializer(serializers.Serializer):
    download_url = serializers.SerializerMethodField(
        label=_("download url"),
        help_text=_(
            "Url to download the content of the file in the Sharing Configs API"
        ),
    )
    filename = fields.CharField(
        label=_("filename"), max_length=100, help_text=_("Name of the file")
    )
    content = AnyBase64FileField(
        label=_("content"),
        write_only=True,
        help_text=_("File content with base64 encoding"),
    )
    author = serializers.CharField(
        label=_("author"),
        write_only=True,
        required=False,
        help_text=_("Person who uploads the file"),
    )
    overwrite = serializers.BooleanField(
        label=_("overwrite"),
        write_only=True,
        default=False,
        help_text=_(
            "Boolean if the uploaded file should overwrite the existing file in the folder"
        ),
    )

    @extend_schema_field(OpenApiTypes.URI)
    def get_download_url(self, data) -> str:
        request = self.context["request"]
        view = self.context["view"]

        url = reverse(
            "file-download",
            kwargs={
                "label": view.kwargs["label"],
                "folder": view.kwargs["folder"],
                "filename": data["filename"],
            },
            request=request,
        )
        return url


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ("label", "type")
