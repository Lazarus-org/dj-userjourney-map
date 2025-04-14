from django.db import models
from django.utils.translation import gettext_lazy as _
from persona_manager.models import UserPersona


class UserJourney(models.Model):
    """
    Represents a user journey map, which outlines the overall path a user takes to achieve a goal
    within a software application. It serves as the root model for stages, actions, and feedback.

    Attributes:
        name (str): The name of the user journey.
        description (str, optional): A detailed description of the journey.
        persona (UserPersona, optional): The user persona associated with this journey.
        created_at (datetime): Timestamp when the journey was created.
        updated_at (datetime): Timestamp when the journey was last updated.

    Example:
        A journey named "New User Onboarding" might describe how a persona signs up and
        starts using a project management tool.
    """

    name = models.CharField(
        max_length=255,
        help_text=_("Name of the user journey (e.g., 'New User Onboarding')."),
        db_comment="The title or identifier of the user journey.",
        verbose_name=_("Journey Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("A detailed description of the journey's purpose and context."),
        db_comment="Optional description providing context for the user journey.",
        verbose_name=_("Description"),
    )
    persona = models.ForeignKey(
        UserPersona,
        related_name="journeys",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_(
            "The user persona this journey is designed for (e.g., 'Sarah the Project Manager')."
        ),
        db_comment="Links to a specific user persona, nullable for flexibility.",
        verbose_name=_("Persona"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp when the journey was created."),
        db_comment="Automatically set to the creation date and time.",
        verbose_name=_("Created At"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Timestamp when the journey was last updated."),
        db_comment="Automatically updated to the last modification date and time.",
        verbose_name=_("Updated At"),
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("User Journey")
        verbose_name_plural = _("User Journeys")

    def __str__(self):
        return self.name
