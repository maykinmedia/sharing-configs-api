import binascii
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .constants import PermissionModes
from .handlers import registry


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
            return f"Automatically uploaded by {author} for {self.organization} using {settings.PROJECT_NAME}"

        return f"Automatically uploaded by {self.organization} using {settings.PROJECT_NAME}"


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
        help_text=_("Type of the config"),
    )
    options = models.JSONField(
        _("options"),
        default=dict,
        blank=True,
        null=True,
        help_text=_(
            "Configuration-specific options. The shape of the field is described "
            "in the `handler.configuration_options` "
        ),
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

        handler = self.get_handler()
        options_serializer = handler.configuration_options(data=self.options)
        if not options_serializer.is_valid():
            raise ValidationError({"options": options_serializer.errors})

    def get_handler(self):
        return registry[self.type](self)


class RootPathConfig(models.Model):
    config = models.ForeignKey(
        Config,
        on_delete=models.CASCADE,
        related_name="root_paths",
        help_text=_("Config for which the root path is defined"),
    )
    folder = models.CharField(
        _("folder"), max_length=200, help_text=_("Folder in the root")
    )
    permission = models.CharField(
        _("permission"),
        choices=PermissionModes.choices,
        max_length=20,
        help_text=_("Permission for the folder"),
    )

    class Meta:
        verbose_name = _("Root path configuration")
        verbose_name_plural = _("Root path configurations")

    def __str__(self):
        return f"{self.config}: {self.folder}"
