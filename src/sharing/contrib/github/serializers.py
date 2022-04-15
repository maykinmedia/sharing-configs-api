from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from sharing.core.serializers import JsonSchemaSerializer


class GitHubOptionsSerializer(JsonSchemaSerializer):
    access_token = serializers.CharField(
        label=_("access token"),
        max_length=250,
        help_text=_(
            "Access token for GitHub authorization. Can be generated at https://github.com/settings/tokens"
        ),
    )
    repo = serializers.CharField(
        label=_("repo"),
        max_length=250,
        help_text=_("GitHub repository in the format {owner}/{name}"),
    )
    branch = serializers.CharField(
        label=_("branch"),
        max_length=250,
        required=False,
        help_text=_("GitHub branch to use, if empty the default branch is used"),
    )
