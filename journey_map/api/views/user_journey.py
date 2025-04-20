from rest_framework.viewsets import ModelViewSet
from journey_map.api.serializers.helper.get_serializer_cls import (
    user_journey_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import UserJourney


class UserJourneyViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "user_journey"
    queryset = (
        UserJourney.objects.select_related("persona")
        .prefetch_related(
            "stages__actions__feedbacks",
            "stages__actions__pain_points",
            "stages__actions__opportunities",
        )
        .all()
    )
    serializer_class = user_journey_serializer_class()
