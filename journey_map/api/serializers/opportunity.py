from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from journey_map.models import Opportunity, JourneyAction


class OpportunitySerializer(serializers.ModelSerializer):
    """Serializer for the Opportunity model."""

    action_id = serializers.IntegerField(
        write_only=True,
        label=_("Action ID"),
        help_text=_("The action this opportunity is associated with."),
    )
    action = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            "id",
            "action_id",
            "action",
            "description",
        ]
        read_only_fields = ["id", "action"]

    def validate_action_id(self, value):
        """Validate that the action_id corresponds to an existing JourneyAction."""
        try:
            JourneyAction.objects.get(id=value)
        except JourneyAction.DoesNotExist:
            raise serializers.ValidationError(
                {"action_id": _("JourneyAction with the given ID was not found.")}
            )
        return value

    def create(self, validated_data):
        """Create an Opportunity instance, mapping action_id to action."""
        action_id = validated_data.pop("action_id")
        validated_data["action"] = JourneyAction.objects.get(id=action_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an Opportunity instance, mapping action_id to action if provided."""
        action_id = validated_data.pop("action_id", None)
        if action_id is not None:
            validated_data["action"] = JourneyAction.objects.get(id=action_id)
        return super().update(instance, validated_data)
