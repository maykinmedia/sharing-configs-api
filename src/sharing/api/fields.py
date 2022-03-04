from drf_extra_fields.fields import Base64FileField


class AnyFileType:
    def __contains__(self, item):
        return True


class AnyBase64FileField(Base64FileField):
    ALLOWED_TYPES = AnyFileType()
