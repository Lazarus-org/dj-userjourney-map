from rest_framework.viewsets import ModelViewSet
from journey_map.api.serializers.helper.get_serializer_cls import (
    opportunity_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import Opportunity


class OpportunityViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "opportunity"
    queryset = Opportunity.objects.select_related("action").all()
    serializer_class = opportunity_serializer_class()
