from drf_jsonschema import to_jsonschema
from rest_framework import serializers


class JsonSchemaSerializerMixin:
    """ "
    add method to show serializer fields in the form of JSON schema
    """

    @classmethod
    def display_as_jsonschema(cls):
        json_schema = to_jsonschema(cls())
        return json_schema


class JsonSchemaSerializer(JsonSchemaSerializerMixin, serializers.Serializer):
    pass
