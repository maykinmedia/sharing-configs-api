from django.utils.translation import gettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class ConfigTypes(DjangoChoices):
    github = ChoiceItem("github", _("Github"))
    debug = ChoiceItem("debug", _("Testing"))


class PermissionModes(DjangoChoices):
    read = ChoiceItem("read", _("Read-only"))
    write = ChoiceItem("write", _("Read and write"))
