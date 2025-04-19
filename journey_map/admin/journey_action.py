from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.admin.inlines import (
    UserFeedbackInline,
    PainPointInline,
    OpportunityInline,
)
from journey_map.mixins.admin.base import BaseModelAdmin
from journey_map.models import JourneyAction
from journey_map.settings.conf import config


@admin.register(JourneyAction, site=config.admin_site_class)
class JourneyActionAdmin(BaseModelAdmin):
    list_display = ("truncated_description", "stage_name", "stage__journey", "order")
    list_filter = ("stage", "stage__journey")
    list_select_related = ("stage__journey",)
    search_fields = ("action_description", "touchpoint", "stage__stage_name")
    autocomplete_fields = ("stage",)
    inlines = [UserFeedbackInline, PainPointInline, OpportunityInline] if config.admin_include_inlines else []

    def truncated_description(self, obj):
        return (
            obj.action_description[:32] + "..."
            if len(obj.action_description) > 32
            else obj.action_description
        )

    truncated_description.short_description = _("Action Description")

    def stage_name(self, obj):
        return obj.stage.stage_name

    stage_name.short_description = _("Stage")
