from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy

from .models import User


@admin.register(User)
class _UserAdmin(UserAdmin):
    hijack_success_url = reverse_lazy("root")
