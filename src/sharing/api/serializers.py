from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from rest_framework import fields, serializers
from rest_framework.reverse import reverse

from .fields import AnyBase64FileField


class FileSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField(
        label=_("url"),
        help_text=_("Url of the file in the Sharing Configs API"),
    )
    filename = fields.CharField(
        label=_("filename"), max_length=100, help_text=_("Name of the file")
    )
    content = AnyBase64FileField(
        label=_("content"),
        write_only=True,
        help_text=_("File content with base64 encoding"),
    )

    @extend_schema_field(OpenApiTypes.URI)
    def get_url(self, data) -> str:
        request = self.context["request"]
        view = self.context["view"]

        url = reverse(
            "file-download",
            kwargs={
                "slug": view.kwargs["slug"],
                "folder": view.kwargs["folder"],
                "filename": data["filename"],
            },
            request=request,
        )
        return url
