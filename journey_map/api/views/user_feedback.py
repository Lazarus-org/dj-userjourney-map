from rest_framework.viewsets import ModelViewSet
from journey_map.api.serializers.helper.get_serializer_cls import (
    user_feedback_serializer_class,
)
from journey_map.api.views.base import BaseViewSet
from journey_map.models import UserFeedback


class UserFeedbackViewSet(BaseViewSet, ModelViewSet):
    config_prefix = "user_feedback"
    queryset = UserFeedback.objects.select_related("action").all()
    serializer_class = user_feedback_serializer_class()
