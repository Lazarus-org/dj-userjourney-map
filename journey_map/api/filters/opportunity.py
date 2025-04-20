import django_filters
from journey_map.models import Opportunity
from django.utils.translation import gettext_lazy as _


class OpportunityFilter(django_filters.FilterSet):
    """FilterSet for the Opportunity model, allowing filtering by description and action."""

    description = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by opportunity description (case-insensitive)."),
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
        model = Opportunity
        fields = ["description", "action"]
