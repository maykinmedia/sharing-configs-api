from django.contrib import admin
from django.db import models

from .models import ClientAuth, Config, RootPathConfig
from .widgets import ConfigOptionsWidget


@admin.register(ClientAuth)
class ClientAuthAdmin(admin.ModelAdmin):
    list_display = ("organization", "token")
    readonly_fields = ("token",)
    autocomplete_fields = ("configs",)


class RootPathConfigInline(admin.TabularInline):
    model = RootPathConfig
    extra = 1


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    # list
    list_display = ("label", "type", "display_client_auths")
    list_filter = ("type",)
    search_fields = ("label",)

    # detail
    formfield_overrides = {models.JSONField: {"widget": ConfigOptionsWidget}}
    inlines = [RootPathConfigInline]

    def display_client_auths(self, obj):
        return ", ".join(c.organization for c in obj.client_auths.all())

    display_client_auths.short_description = "client_auths"
