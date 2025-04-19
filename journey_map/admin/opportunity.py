from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.mixins.admin.base import BaseModelAdmin
from journey_map.models import Opportunity
from journey_map.settings.conf import config


@admin.register(Opportunity, site=config.admin_site_class)
class OpportunityAdmin(BaseModelAdmin):
    list_display = ("truncated_description", "action_description", "journey_name")
    list_select_related = ("action__stage__journey",)
    list_filter = ("action__order",)
    search_fields = ("description", "action__action_description")

    def truncated_description(self, obj):
        return (
            obj.description[:32] + "..."
            if len(obj.description) > 32
            else obj.description
        )

    truncated_description.short_description = _("Description")

    def action_description(self, obj):
        return (
            obj.action.action_description[:32] + "..."
            if len(obj.action.action_description) > 32
            else obj.action.action_description
        )

    action_description.short_description = _("Action")

    def journey_name(self, obj):
        return obj.action.stage.journey.name

    journey_name.short_description = _("Journey")
