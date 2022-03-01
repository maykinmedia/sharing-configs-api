from django.utils.translation import gettext_lazy as _

from drf_extra_fields.fields import Base64FileField
from rest_framework import fields, serializers


class FileSerializer(serializers.Serializer):
    url = fields.URLField(
        label=_("url"),
        help_text=_("Url of the file in the Sharing Configs API"),
        read_only=True,
    )
    filename = fields.CharField(
        label=_("filename"), max_length=100, help_text=_("Name of the file")
    )
    content = Base64FileField(
        label=_("content"), help_text=_("File content with base64 encoding")
    )
