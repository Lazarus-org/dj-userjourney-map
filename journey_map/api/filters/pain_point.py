import django_filters
from django.utils.translation import gettext_lazy as _

from journey_map.models import PainPoint


class PainPointFilter(django_filters.FilterSet):
    """FilterSet for the PainPoint model, allowing filtering by description,
    severity, and action."""

    description = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by pain point description (case-insensitive)."),
    )
    severity = django_filters.NumberFilter(
        lookup_expr="exact", help_text=_("Filter by exact severity (1-5).")
    )
    severity__gte = django_filters.NumberFilter(
        field_name="severity",
        lookup_expr="gte",
        help_text=_("Filter by severity greater than or equal to."),
    )
    severity__lte = django_filters.NumberFilter(
        field_name="severity",
        lookup_expr="lte",
        help_text=_("Filter by severity less than or equal to."),
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
        model = PainPoint
        fields = ["description", "severity", "action"]
