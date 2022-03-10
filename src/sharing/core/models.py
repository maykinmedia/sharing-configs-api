import binascii
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .constants import ConfigTypes


class ClientAuth(models.Model):
    token = models.CharField(_("token"), max_length=40, primary_key=True)
    organization = models.CharField(
        _("organization"),
        max_length=200,
        help_text=_("Organization which has access to the API"),
    )
    email = models.EmailField(
        _("email"), help_text=_("Email to contact the organization")
    )
    created_on = models.DateTimeField(
        _("created on"),
        auto_now_add=True,
        help_text=_("Date when the token was created"),
    )
    updated_on = models.DateTimeField(
        _("updated on"),
        auto_now=True,
        help_text=_("Date when the token was last changed"),
    )
    configs = models.ManyToManyField(
        "core.Config", related_name="client_auths", blank=True
    )

    class Meta:
        verbose_name = _("Client authorization")
        verbose_name_plural = _("Client authorizations")

    def __str__(self):
        return self.organization

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def get_comment(self, author=None) -> str:
        """comment for exported files"""

        if author:
            return f"Automatically created by {author} for {self.organization} using {settings.PROJECT_NAME}"

        return f"Automatically created by {self.organization} using {settings.PROJECT_NAME}"


class Config(models.Model):
    label = models.CharField(
        _("label"),
        max_length=100,
        unique=True,
        help_text=_("Name of the config to define which file storage backend to use"),
    )
    type = models.CharField(
        _("type"),
        max_length=50,
        choices=ConfigTypes.choices,
        default=ConfigTypes.github,
        help_text=_("Type of the config"),
    )
    access_token = models.CharField(
        _("access token"),
        max_length=250,
        blank=True,
        help_text=_(
            "Access token for GitHub authorization. Can be generated at https://github.com/settings/tokens"
        ),
    )
    repo = models.CharField(
        _("repo"),
        max_length=250,
        blank=True,
        help_text=_("GitHub repository in the format {owner}/{name}"),
    )
    branch = models.CharField(
        _("branch"),
        max_length=250,
        blank=True,
        help_text=_("GitHub branch to use, if empty the default branch is used"),
    )

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    def __str__(self):
        return f"{self.label}"

    def save(self, **kwargs):
        self.label = slugify(self.label)

        super().save(**kwargs)

    def clean(self):
        super().clean()

        if self.type == ConfigTypes.github:
            if not self.access_token:
                raise ValidationError(
                    {"access_token": "This field is required for GitHub config"}
                )

            if not self.repo:
                raise ValidationError(
                    {"repo": "This field is required for GitHub config"}
                )
