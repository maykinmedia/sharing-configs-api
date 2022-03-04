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
        assert "request" in self.context, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )
        request = self.context["request"]

        url = reverse(
            "file-download",
            kwargs={
                "slug": request.kwargs["slug"],
                "folder": request.kwargs["folder"],
                "filename": data["filename"],
            },
            request=request,
        )
        return "url"
