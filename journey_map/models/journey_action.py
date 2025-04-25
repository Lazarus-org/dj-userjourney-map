from django.db import models
from django.utils.translation import gettext_lazy as _

from journey_map.models.journey_stage import JourneyStage


class JourneyAction(models.Model):
    """Represents a specific action a user takes within a journey stage, such
    as clicking a button or submitting a form. Actions are tied to touchpoints
    and ordered within their stage.

    Attributes:
        stage (JourneyStage): The stage this action belongs to.
        action_description (str): A description of what the user does.
        touchpoint (str, optional): The point of interaction (e.g., a button or link).
        order (int): The position of the action in the stage sequence.

    Example:
        An action might be 'Clicks the Sign Up button' with a touchpoint of 'Sign-up button'.

    """

    stage = models.ForeignKey(
        JourneyStage,
        related_name="actions",
        on_delete=models.CASCADE,
        help_text=_("The stage this action occurs within."),
        db_comment="Foreign key linking to the parent journey stage.",
        verbose_name=_("Stage"),
    )
    action_description = models.TextField(
        help_text=_(
            "Description of the action (e.g., 'Sees TV commercial', 'Visits website')."
        ),
        db_comment="Details what the user does during this action.",
        verbose_name=_("Action Description"),
    )
    touchpoint = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Point of interaction (e.g., 'Sign-up button', 'Email link')."),
        db_comment="Optional field for the specific interaction point.",
        verbose_name=_("Touchpoint"),
    )
    order = models.PositiveIntegerField(
        help_text=_("Order of the action within the stage (e.g., 1 for first action)."),
        db_comment="Determines the sequence of the action within the stage.",
        verbose_name=_("Order"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("Journey Action")
        verbose_name_plural = _("Journey Actions")

    def __str__(self):
        return f"Stage ({self.stage_id}) - {self.action_description}"
