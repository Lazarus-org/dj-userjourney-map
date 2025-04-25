import django_filters
from django.utils.translation import gettext_lazy as _

from journey_map.models import UserJourney


class UserJourneyFilter(django_filters.FilterSet):
    """FilterSet for the UserJourney model, allowing filtering by name,
    description, and persona."""

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by journey name (case-insensitive)."),
    )
    description = django_filters.CharFilter(
        lookup_expr="icontains",
        help_text=_("Filter by journey description (case-insensitive)."),
    )
    persona = django_filters.CharFilter(
        field_name="persona__persona_name",
        lookup_expr="icontains",
        help_text=_("Filter by persona name (case-insensitive)."),
    )
    created_at = django_filters.DateTimeFilter(
        lookup_expr="exact", help_text=_("Filter by exact creation date.")
    )
    created_at__gte = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        help_text=_("Filter by creation date greater than or equal to."),
    )
    created_at__lte = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        help_text=_("Filter by creation date less than or equal to."),
    )

    class Meta:
        model = UserJourney
        fields = ["name", "description", "persona", "created_at"]
