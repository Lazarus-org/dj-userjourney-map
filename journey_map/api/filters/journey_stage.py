import django_filters
from journey_map.models import JourneyStage
from django.utils.translation import gettext_lazy as _


class JourneyStageFilter(django_filters.FilterSet):
    """FilterSet for the JourneyStage model, allowing filtering by stage name, journey, and order."""

    stage_name = django_filters.CharFilter(
        lookup_expr="icontains", help_text=_("Filter by stage name (case-insensitive).")
    )
    journey = django_filters.CharFilter(
        field_name="journey__name",
        lookup_expr="icontains",
        help_text=_("Filter by journey name (case-insensitive)."),
    )
    journey_id = django_filters.NumberFilter(
        field_name="journey__id",
        lookup_expr="exact",
        help_text=_("Filter by exact journey ID."),
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
        model = JourneyStage
        fields = ["stage_name", "journey", "order"]
