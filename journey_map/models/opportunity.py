from django.db import models
from django.utils.translation import gettext_lazy as _

from journey_map.models.journey_action import JourneyAction


class Opportunity(models.Model):
    """Represents an opportunity for improvement tied to a specific action in
    the user journey. Opportunities suggest ways to enhance the user
    experience.

    Attributes:
        action (JourneyAction): The action this opportunity relates to.
        description (str): A description of the suggested improvement.

    Example:
        An opportunity might be 'Add a tooltip to clarify the form field'.

    """

    action = models.ForeignKey(
        JourneyAction,
        related_name="opportunities",
        on_delete=models.CASCADE,
        help_text=_("The action this opportunity is associated with."),
        db_comment="Foreign key linking to the parent journey action.",
        verbose_name=_("Action"),
    )
    description = models.TextField(
        help_text=_(
            "Suggested improvement or opportunity (e.g., 'Add a tooltip to clarify')."
        ),
        db_comment="Details the proposed enhancement for the user experience.",
        verbose_name=_("Description"),
    )

    class Meta:
        verbose_name = _("Opportunity")
        verbose_name_plural = _("Opportunities")

    def __str__(self):
        return f"Action ({self.action_id}) - {self.description}"
