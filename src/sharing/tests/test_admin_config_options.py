import json
from unittest.mock import patch

from django.urls import reverse_lazy

from django_webtest import WebTest
from rest_framework import serializers

from sharing.accounts.tests.factories import SuperUserFactory
from sharing.core.models import Config
from sharing.core.serializers import JsonSchemaSerializer


class TestOptionsSerializer(JsonSchemaSerializer):
    foo = serializers.CharField(max_length=10)


class TestHandler:
    configuration_options = TestOptionsSerializer

    def __init__(self, config):
        self.config = config


class OtherTestOptionsSerializer(JsonSchemaSerializer):
    other = serializers.CharField(max_length=10)


class OtherTestHandler:
    configuration_options = OtherTestOptionsSerializer

    def __init__(self, config):
        self.config = config


test_registry = {"test": TestHandler, "other_test": OtherTestHandler}


class ConfigOptionsTests(WebTest):
    url = reverse_lazy("admin:core_config_add")

    def setUp(self) -> None:
        super().setUp()

        user = SuperUserFactory.create()
        self.app.set_user(user=user)

    @patch.dict("sharing.core.models.registry", test_registry)
    def test_options_not_valid(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["label"] = "some-config"
        form["type"] = "test"
        form["options"] = json.dumps({"not-foo": "some-value"})

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Config.objects.count(), 0)
        self.assertEqual(
            response.context["errors"].data, [["foo: Dit veld is vereist."]]
        )

    @patch.dict("sharing.core.models.registry", test_registry)
    def test_option_valid_for_other_type(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["label"] = "some-config"
        form["type"] = "other_test"
        form["options"] = json.dumps({"foo": "some-value"})

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Config.objects.count(), 0)
        self.assertEqual(
            response.context["errors"].data, [["other: Dit veld is vereist."]]
        )

    @patch.dict("sharing.core.models.registry", test_registry)
    def test_options_valid(self):
        get_response = self.app.get(self.url)

        form = get_response.form
        form["label"] = "some-config"
        form["type"] = "test"
        form["options"] = json.dumps({"foo": "some-value"})

        response = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Config.objects.count(), 1)

        config = Config.objects.get()
        self.assertEqual(config.type, "test")
        self.assertEqual(config.options, {"foo": "some-value"})
