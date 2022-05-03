from django import forms

from .handlers import registry


class ConfigOptionsWidget(forms.Widget):
    template_name = "admin/core/widgets/config_options_editor.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        json_schemas = {
            name: handler.configuration_options.display_as_jsonschema()
            for name, handler in registry.items()
        }
        context.update({"json_schemas": json_schemas, "type_field_id": "id_type"})
        return context
