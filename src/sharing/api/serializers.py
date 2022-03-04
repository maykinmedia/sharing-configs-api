from django.utils.translation import gettext_lazy as _

from rest_framework import fields, serializers

from .fields import AnyBase64FileField, DownloadUrlField


class FileSerializer(serializers.Serializer):
    url = DownloadUrlField(
        label=_("url"),
        help_text=_("Url of the file in the Sharing Configs API"),
        read_only=True,
    )
    filename = fields.CharField(
        label=_("filename"), max_length=100, help_text=_("Name of the file")
    )


class FileContentSerializer(FileSerializer):
    content = AnyBase64FileField(
        label=_("content"), help_text=_("File content with base64 encoding")
    )
