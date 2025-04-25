import django_filters
from django.utils.translation import gettext_lazy as _

from journey_map.models import UserFeedback


class UserFeedbackFilter(django_filters.FilterSet):
    """FilterSet for the UserFeedback model, allowing filtering by feedback
    text, emotion, intensity, and action."""

    feedback_text = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by feedback text (case-insensitive)."),
    )
    emotion = django_filters.CharFilter(
        lookup_expr="exact", help_text=_("Filter by exact emotion.")
    )
    intensity = django_filters.NumberFilter(
        lookup_expr="exact", help_text=_("Filter by exact intensity.")
    )
    intensity__gte = django_filters.NumberFilter(
        field_name="intensity",
        lookup_expr="gte",
        help_text=_("Filter by intensity greater than or equal to."),
    )
    intensity__lte = django_filters.NumberFilter(
        field_name="intensity",
        lookup_expr="lte",
        help_text=_("Filter by intensity less than or equal to."),
    )
    is_positive = django_filters.BooleanFilter(
        lookup_expr="exact", help_text=_("Filter by positive/negative feedback.")
    )
    action = django_filters.CharFilter(
        field_name="action__action_description",
        lookup_expr="icontains",
        help_text=_("Filter by action description (case-insensitive)."),
    )
    action_id = django_filters.NumberFilter(
        field_name="action__id",
        lookup_expr="exact",
        help_text=_("Filter by exact action ID."),
    )
    journey = django_filters.CharFilter(
        field_name="action__stage__journey__name",
        lookup_expr="icontains",
        help_text=_("Filter by journey name (case-insensitive)."),
    )

    class Meta:
        model = UserFeedback
        fields = ["feedback_text", "emotion", "intensity", "is_positive", "action"]
