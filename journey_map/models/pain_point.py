from django.db import models
from django.utils.translation import gettext_lazy as _

from journey_map.models.journey_action import JourneyAction


class PainPoint(models.Model):
    """Represents a pain point or issue encountered by the user during a
    specific action. Pain points are used to identify areas for improvement in
    the user journey.

    Attributes:
        action (JourneyAction): The action where the pain point occurs.
        description (str): A description of the issue.
        severity (int): The severity of the pain point (1-5 scale).

    Example:
        A pain point might be 'Unclear error message' with severity 3.

    """

    action = models.ForeignKey(
        JourneyAction,
        related_name="pain_points",
        on_delete=models.CASCADE,
        help_text=_("The action where this pain point occurs."),
        db_comment="Foreign key linking to the parent journey action.",
        verbose_name=_("Action"),
    )
    description = models.TextField(
        help_text=_("Description of the pain point (e.g., 'Unclear error message')."),
        db_comment="Details the issue or frustration encountered.",
        verbose_name=_("Description"),
    )
    severity = models.PositiveSmallIntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text=_(
            "Severity of the pain point on a scale of 1 to 5 (1 = minor, 5 = critical)."
        ),
        db_comment="The impact level of the pain point.",
        verbose_name=_("Severity"),
    )

    class Meta:
        verbose_name = _("Pain Point")
        verbose_name_plural = _("Pain Points")

    def __str__(self):
        return f"Action ({self.action_id}) - {self.description}"
