from rest_framework.viewsets import ModelViewSet

from journey_map.api.serializers.helper.get_serializer_cls import (
    journey_action_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import JourneyAction


class JourneyActionViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "journey_action"
    queryset = (
        JourneyAction.objects.select_related("stage")
        .prefetch_related(
            "feedbacks",
            "pain_points",
            "opportunities",
        )
        .all()
    )
    serializer_class = journey_action_serializer_class()
