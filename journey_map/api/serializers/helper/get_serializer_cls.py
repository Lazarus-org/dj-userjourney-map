from typing import Type
from rest_framework.serializers import BaseSerializer
from journey_map.settings.conf import config


def user_journey_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the UserJourney model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default UserJourneySerializer.
    """
    from journey_map.api.serializers.user_journey import UserJourneySerializer

    return config.api_user_journey_serializer_class or UserJourneySerializer


def journey_stage_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the JourneyStage model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default JourneyStageSerializer.
    """
    from journey_map.api.serializers.journey_stage import JourneyStageSerializer

    return config.api_journey_stage_serializer_class or JourneyStageSerializer


def journey_action_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the JourneyAction model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default JourneyActionSerializer.
    """
    from journey_map.api.serializers.journey_action import JourneyActionSerializer

    return config.api_journey_action_serializer_class or JourneyActionSerializer


def user_feedback_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the UserFeedback model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default UserFeedbackSerializer.
    """
    from journey_map.api.serializers.user_feedback import UserFeedbackSerializer

    return config.api_user_feedback_serializer_class or UserFeedbackSerializer


def pain_point_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the PainPoint model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default PainPointSerializer.
    """
    from journey_map.api.serializers.pain_point import PainPointSerializer

    return config.api_pain_point_serializer_class or PainPointSerializer


def opportunity_serializer_class() -> Type[BaseSerializer]:
    """Get the serializer class for the Opportunity model, either from config or the default.

    Returns:
        The configured serializer class from settings or the default OpportunitySerializer.
    """
    from journey_map.api.serializers.opportunity import OpportunitySerializer

    return config.api_opportunity_serializer_class or OpportunitySerializer
