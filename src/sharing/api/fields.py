from drf_extra_fields.fields import Base64FileField
from drf_spectacular.utils import OpenApiTypes, extend_schema_field


class AnyFileType:
    def __contains__(self, item):
        return True


@extend_schema_field(OpenApiTypes.STR)
class AnyBase64FileField(Base64FileField):
    ALLOWED_TYPES = AnyFileType()

    def get_file_extension(self, filename, decoded_file):
        return self.parent.initial_data["filename"].rsplit(".", 1)[1]

    def get_file_name(self, decoded_file):
        return self.parent.initial_data["filename"].rsplit(".", 1)[0]
