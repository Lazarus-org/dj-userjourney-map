from django.contrib import admin

from journey_map.admin.inlines import JourneyActionInline
from journey_map.mixins.admin.base import BaseModelAdmin
from journey_map.models import JourneyStage

from journey_map.settings.conf import config


@admin.register(JourneyStage, site=config.admin_site_class)
class JourneyStageAdmin(BaseModelAdmin):
    list_display = ("stage_name", "journey", "order")
    list_filter = ("journey",)
    search_fields = ("stage_name", "journey__name")
    inlines = [JourneyActionInline] if config.admin_include_inlines else []
