from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from journey_map.api.serializers.journey_stage import JourneyStageSerializer
from journey_map.models.user_journey import UserJourney, UserPersona


class UserJourneySerializer(serializers.ModelSerializer):
    """Serializer for the UserJourney model, including nested stages."""

    persona_id = serializers.IntegerField(
        write_only=True,
        label=_("Persona ID"),
        help_text=_("The ID of the user persona this journey is designed for"),
    )
    persona = serializers.StringRelatedField(read_only=True)
    stages = JourneyStageSerializer(many=True, read_only=True)

    class Meta:
        model = UserJourney
        fields = [
            "id",
            "name",
            "description",
            "persona_id",
            "persona",
            "stages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_persona_id(self, value):
        """Validate that the persona_id corresponds to an existing
        UserPersona."""
        try:
            UserPersona.objects.get(id=value)
        except UserPersona.DoesNotExist:
            raise serializers.ValidationError(
                {"persona_id": _("Persona with the given ID was not found.")}
            )
        return value

    def create(self, validated_data):
        """Create a UserJourney instance, mapping persona_id to persona."""
        persona_id = validated_data.pop("persona_id")
        validated_data["persona"] = UserPersona.objects.get(id=persona_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update a UserJourney instance, mapping persona_id to persona if
        provided."""
        persona_id = validated_data.pop("persona_id", None)
        if persona_id is not None:
            validated_data["persona"] = UserPersona.objects.get(id=persona_id)
        return super().update(instance, validated_data)
