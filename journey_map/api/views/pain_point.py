from rest_framework.viewsets import ModelViewSet
from journey_map.api.serializers.helper.get_serializer_cls import (
    pain_point_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import PainPoint


class PainPointViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "pain_point"
    queryset = PainPoint.objects.select_related("action").all()
    serializer_class = pain_point_serializer_class()
