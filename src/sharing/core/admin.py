from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ClientAuth, ClientConfig


@admin.register(ClientAuth)
class ClientAuthAdmin(admin.ModelAdmin):
    list_display = ("organization", "token")
    readonly_fields = ("token",)


@admin.register(ClientConfig)
class ClientConfigAdmin(admin.ModelAdmin):
    # list
    list_display = ("client_auth", "label", "type")
    list_filter = ("client_auth__organization",)

    # detail
    prepopulated_fields = {"slug": ("label",)}
    fieldsets = (
        (None, {"fields": ("client_auth", "label", "slug", "type")}),
        (_("Github"), {"fields": ("access_token", "repo", "branch")}),
    )
