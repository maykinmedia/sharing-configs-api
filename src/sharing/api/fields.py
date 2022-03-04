from drf_extra_fields.fields import Base64FileField
from rest_framework.fields import Field
from rest_framework.reverse import reverse

from .data import FileData


class AnyFileType:
    def __contains__(self, item):
        return True


class AnyBase64FileField(Base64FileField):
    ALLOWED_TYPES = AnyFileType()


class DownloadUrlField(Field):
    view_name = "file-detail"

    def to_representation(self, file: FileData) -> str:
        assert "request" in self.context, (
            "`%s` requires the request in the serializer"
            " context. Add `context={'request': request}` when instantiating "
            "the serializer." % self.__class__.__name__
        )

        request = self.context["request"]

        url = reverse(
            self.view_name,
            kwargs={
                "slug": file.slug,
                "folder": file.folder,
                "filename": file.filename,
            },
            request=request,
        )
        return url
