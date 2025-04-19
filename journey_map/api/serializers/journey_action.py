from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from journey_map.models import JourneyAction, JourneyStage
from journey_map.api.serializers.user_feedback import UserFeedbackSerializer
from journey_map.api.serializers.pain_point import PainPointSerializer
from journey_map.api.serializers.opportunity import OpportunitySerializer


class JourneyActionSerializer(serializers.ModelSerializer):
    """Serializer for the JourneyAction model, including nested feedback, pain points, and opportunities."""

    stage_id = serializers.IntegerField(
        write_only=True,
        label=_("Stage ID"),
        help_text=_("The stage this action occurs within."),
    )
    stage = serializers.StringRelatedField(read_only=True)
    feedbacks = UserFeedbackSerializer(many=True, read_only=True)
    pain_points = PainPointSerializer(many=True, read_only=True)
    opportunities = OpportunitySerializer(many=True, read_only=True)

    class Meta:
        model = JourneyAction
        fields = [
            "id",
            "stage_id",
            "stage",
            "action_description",
            "touchpoint",
            "order",
            "feedbacks",
            "pain_points",
            "opportunities",
        ]
        read_only_fields = ["id", "stage", "feedbacks", "pain_points", "opportunities"]

    def validate_stage_id(self, value):
        """Validate that the stage_id corresponds to an existing JourneyStage."""
        try:
            JourneyStage.objects.get(id=value)
        except JourneyStage.DoesNotExist:
            raise serializers.ValidationError(
                {"stage_id": _("JourneyStage with the given ID was not found.")}
            )
        return value

    def create(self, validated_data):
        """Create a JourneyAction instance, mapping stage_id to stage."""
        stage_id = validated_data.pop("stage_id")
        validated_data["stage"] = JourneyStage.objects.get(id=stage_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update a JourneyAction instance, mapping stage_id to stage if provided."""
        stage_id = validated_data.pop("stage_id", None)
        if stage_id is not None:
            validated_data["stage"] = JourneyStage.objects.get(id=stage_id)
        return super().update(instance, validated_data)
