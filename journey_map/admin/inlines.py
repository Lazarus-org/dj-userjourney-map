from journey_map.mixins.admin.inlines import BaseTabularInline
from journey_map.models import (
    JourneyStage,
    JourneyAction,
    UserFeedback,
    Opportunity,
    PainPoint,
)


class JourneyStageInline(BaseTabularInline):
    model = JourneyStage
    fields = ("stage_name", "order")


class JourneyActionInline(BaseTabularInline):
    model = JourneyAction
    fields = ("action_description", "touchpoint", "order")


class UserFeedbackInline(BaseTabularInline):
    model = UserFeedback
    fields = ("feedback_text", "emotion", "intensity", "is_positive")


class PainPointInline(BaseTabularInline):
    model = PainPoint
    fields = ("description", "severity")


class OpportunityInline(BaseTabularInline):
    model = Opportunity
    fields = ("description",)
