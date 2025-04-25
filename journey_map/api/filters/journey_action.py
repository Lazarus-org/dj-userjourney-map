import django_filters
from django.utils.translation import gettext_lazy as _

from journey_map.models import JourneyAction


class JourneyActionFilter(django_filters.FilterSet):
    """FilterSet for the JourneyAction model, allowing filtering by action
    description, touchpoint, stage, and order."""

    action_description = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by action description (case-insensitive)."),
    )
    touchpoint = django_filters.CharFilter(
        lookup_expr="icontains", help_text=_("Filter by touchpoint (case-insensitive).")
    )
    stage = django_filters.CharFilter(
        field_name="stage__stage_name",
        lookup_expr="icontains",
        help_text=_("Filter by stage name (case-insensitive)."),
    )
    stage_id = django_filters.NumberFilter(
        field_name="stage__id",
        lookup_expr="exact",
        help_text=_("Filter by exact stage ID."),
    )
    journey = django_filters.CharFilter(
        field_name="stage__journey__name",
        lookup_expr="icontains",
        help_text=_("Filter by journey name (case-insensitive)."),
    )
    order = django_filters.NumberFilter(
        lookup_expr="exact", help_text=_("Filter by exact order.")
    )
    order__gte = django_filters.NumberFilter(
        field_name="order",
        lookup_expr="gte",
        help_text=_("Filter by order greater than or equal to."),
    )
    order__lte = django_filters.NumberFilter(
        field_name="order",
        lookup_expr="lte",
        help_text=_("Filter by order less than or equal to."),
    )

    class Meta:
        model = JourneyAction
        fields = ["action_description", "touchpoint", "stage", "order"]
