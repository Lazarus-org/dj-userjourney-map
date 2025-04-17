from django.contrib import admin

from journey_map.admin.inlines import JourneyStageInline
from journey_map.mixins.admin.base import BaseModelAdmin
from journey_map.models import UserJourney
from django.utils.translation import gettext_lazy as _

from journey_map.settings.conf import config


@admin.register(UserJourney, site=config.admin_site_class)
class UserJourneyAdmin(BaseModelAdmin):
    list_display = ("name", "persona", "created_at", "updated_at")
    list_filter = ("persona", "created_at")
    search_fields = ("name", "description")
    list_select_related = ("persona",)
    inlines = [JourneyStageInline] if config.admin_include_inlines else []
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (_("Details"), {"fields": ("name", "description", "persona")}),
        (_("Metadata"), {"fields": ("created_at", "updated_at")}),
    )
