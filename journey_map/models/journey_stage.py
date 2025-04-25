from django.db import models
from django.utils.translation import gettext_lazy as _

from journey_map.models.user_journey import UserJourney


class JourneyStage(models.Model):
    """Represents a stage within a user journey, defining a distinct phase in
    the user's experience, such as 'Awareness' or 'Decision'. Stages are
    ordered to reflect the sequence of the journey.

    Attributes:
        journey (UserJourney): The user journey this stage belongs to.
        stage_name (str): The name of the stage.
        order (int): The position of the stage in the journey sequence.

    Example:
        In a journey for purchasing a product, stages might include 'Explore', 'Compare', and 'Purchase'.

    """

    journey = models.ForeignKey(
        UserJourney,
        related_name="stages",
        on_delete=models.CASCADE,
        help_text=_("The user journey this stage is part of."),
        db_comment="Foreign key linking to the parent user journey.",
        verbose_name=_("Journey"),
    )
    stage_name = models.CharField(
        max_length=255,
        help_text=_(
            "Name of the stage (e.g., 'Consider', 'Explore', 'Compare', 'Test')."
        ),
        db_comment="The title of the stage in the user journey.",
        verbose_name=_("Stage Name"),
    )
    order = models.PositiveIntegerField(
        help_text=_(
            "Order of the stage in the journey (e.g., 1 for first stage, 2 for second)."
        ),
        db_comment="Determines the sequence of the stage within the journey.",
        verbose_name=_("Order"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("Journey Stage")
        verbose_name_plural = _("Journey Stages")

    def __str__(self):
        return f"Journey ({self.journey_id}) - {self.stage_name}"
