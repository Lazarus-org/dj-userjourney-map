from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from journey_map.models import JourneyStage, UserJourney
from journey_map.api.serializers.journey_action import JourneyActionSerializer


class JourneyStageSerializer(serializers.ModelSerializer):
    """Serializer for the JourneyStage model, including nested actions."""

    journey_id = serializers.IntegerField(
        write_only=True,
        label=_("Journey ID"),
        help_text=_("The user journey this stage is part of."),
    )
    journey = serializers.StringRelatedField(read_only=True)
    actions = JourneyActionSerializer(many=True, read_only=True)

    class Meta:
        model = JourneyStage
        fields = [
            "id",
            "journey_id",
            "journey",
            "stage_name",
            "order",
            "actions",
        ]
        read_only_fields = ["id", "journey", "actions"]

    def validate_journey_id(self, value):
        """Validate that the journey_id corresponds to an existing UserJourney."""
        try:
            UserJourney.objects.get(id=value)
        except UserJourney.DoesNotExist:
            raise serializers.ValidationError(
                {"journey_id": _("UserJourney with the given ID was not found.")}
            )
        return value

    def create(self, validated_data):
        """Create a JourneyStage instance, mapping journey_id to journey."""
        journey_id = validated_data.pop("journey_id")
        validated_data["journey"] = UserJourney.objects.get(id=journey_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update a JourneyStage instance, mapping journey_id to journey if provided."""
        journey_id = validated_data.pop("journey_id", None)
        if journey_id is not None:
            validated_data["journey"] = UserJourney.objects.get(id=journey_id)
        return super().update(instance, validated_data)
