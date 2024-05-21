# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InseeSirene(AppConfig):
    name = "insee_sirene"
    verbose_name = _("INSEE Sirene")
