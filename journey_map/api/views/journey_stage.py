from rest_framework.viewsets import ModelViewSet

from journey_map.api.serializers.helper.get_serializer_cls import (
    journey_stage_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import JourneyStage


class JourneyStageViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "journey_stage"
    queryset = (
        JourneyStage.objects.select_related("journey")
        .prefetch_related(
            "actions__feedbacks",
            "actions__pain_points",
            "actions__opportunities",
        )
        .all()
    )
    serializer_class = journey_stage_serializer_class()
