from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JourneyMapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "journey_map"
    verbose_name = _("Django Journey Map")
