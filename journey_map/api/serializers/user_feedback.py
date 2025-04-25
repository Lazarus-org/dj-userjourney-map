from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from journey_map.models import JourneyAction, UserFeedback


class UserFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the UserFeedback model."""

    action_id = serializers.IntegerField(
        write_only=True,
        label=_("Action ID"),
        help_text=_("The action this feedback relates to."),
    )
    action = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserFeedback
        fields = [
            "id",
            "action_id",
            "action",
            "feedback_text",
            "emotion",
            "intensity",
            "is_positive",
        ]
        read_only_fields = ["id", "action"]

    def validate_action_id(self, value):
        """Validate that the action_id corresponds to an existing
        JourneyAction."""
        try:
            JourneyAction.objects.get(id=value)
        except JourneyAction.DoesNotExist:
            raise serializers.ValidationError(
                {"action_id": _("JourneyAction with the given ID was not found.")}
            )
        return value

    def create(self, validated_data):
        """Create a UserFeedback instance, mapping action_id to action."""
        action_id = validated_data.pop("action_id")
        validated_data["action"] = JourneyAction.objects.get(id=action_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update a UserFeedback instance, mapping action_id to action if
        provided."""
        action_id = validated_data.pop("action_id", None)
        if action_id is not None:
            validated_data["action"] = JourneyAction.objects.get(id=action_id)
        return super().update(instance, validated_data)
