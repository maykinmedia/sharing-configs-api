import binascii
import os

from django.db import models
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


class ClientConfig(models.Model):
    client_auth = models.ForeignKey(
        ClientAuth, related_name="configs", on_delete=models.CASCADE
    )
    label = models.CharField(
        _("label"), max_length=100, help_text=_("label to name the config")
    )
    slug = models.SlugField(
        _("slug"), max_length=100, help_text=_("Slug of the config. Used in the API")
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
        verbose_name = _("Client configuration")
        verbose_name_plural = _("Client configurations")
        unique_together = ("client_auth", "slug")

    def __str__(self):
        return f"{self.client_auth} ({self.label})"
