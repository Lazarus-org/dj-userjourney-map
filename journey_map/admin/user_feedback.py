from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.mixins.admin.base import BaseModelAdmin
from journey_map.models import UserFeedback
from journey_map.settings.conf import config


@admin.register(UserFeedback, site=config.admin_site_class)
class UserFeedbackAdmin(BaseModelAdmin):
    list_display = (
        "truncated_feedback",
        "action_description",
        "emotion",
        "intensity",
        "is_positive",
    )
    list_filter = ("is_positive", "emotion", "action__stage__journey")
    list_select_related = ("action",)
    autocomplete_fields = ("action",)
    search_fields = ("feedback_text", "action__action_description")

    def truncated_feedback(self, obj):
        return (
            obj.feedback_text[:32] + "..."
            if len(obj.feedback_text) > 32
            else obj.feedback_text
        )

    truncated_feedback.short_description = _("Feedback")

    def action_description(self, obj):
        return (
            obj.action.action_description[:32] + "..."
            if len(obj.action.action_description) > 32
            else obj.action.action_description
        )

    action_description.short_description = _("Action")
