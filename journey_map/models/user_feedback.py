from django.db import models
from django.utils.translation import gettext_lazy as _
from journey_map.models.helper.eums.emotion_choices import EmotionChoices
from journey_map.models.journey_action import JourneyAction


class UserFeedback(models.Model):
    """
    Captures user feedback or emotions associated with a specific action in the journey.
    Feedback includes the emotional state, intensity, and whether it’s positive or negative.

    Attributes:
        action (JourneyAction): The action this feedback is tied to.
        feedback_text (str): The user’s feedback or emotional description.
        emotion (str): The user’s emotional state (e.g., Happy, Frustrated).
        intensity (int): The strength of the emotion (1-5 scale).
        is_positive (bool): Indicates if the feedback is positive or negative.
        created_at (datetime): Timestamp when the feedback was created.

    Example:
        Feedback might be 'I like that I can save cars' with emotion 'Happy' and intensity 4.
    """

    action = models.ForeignKey(
        JourneyAction,
        related_name="feedbacks",
        on_delete=models.CASCADE,
        help_text=_("The action this feedback relates to."),
        db_comment="Foreign key linking to the parent journey action.",
        verbose_name=_("Action"),
    )
    feedback_text = models.TextField(
        help_text=_(
            "User's feedback or emotion (e.g., 'I like that I can save cars')."
        ),
        db_comment="The user’s feedback or emotional response.",
        verbose_name=_("Feedback Text"),
    )
    emotion = models.CharField(
        max_length=50,
        choices=EmotionChoices.choices,
        default=EmotionChoices.NEUTRAL,
        help_text=_("The user’s emotional state (e.g., 'Happy', 'Frustrated')."),
        db_comment="The emotional category of the feedback.",
        verbose_name=_("Emotion"),
    )
    intensity = models.PositiveSmallIntegerField(
        default=1,
        help_text=_(
            "Intensity of the emotion on a scale of 1 to 5 (1 = low, 5 = high)."
        ),
        choices=[(i, str(i)) for i in range(1, 6)],
        db_comment="The strength of the user’s emotional response.",
        verbose_name=_("Emotion Intensity"),
    )
    is_positive = models.BooleanField(
        default=True,
        help_text=_(
            "Indicates whether the feedback is positive (True) or negative (False)."
        ),
        db_comment="Flag to categorize feedback as positive or negative.",
        verbose_name=_("Is Positive"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp when the feedback was created."),
        db_comment="Automatically set to the creation date and time.",
        verbose_name=_("Created At"),
    )

    class Meta:
        verbose_name = _("User Feedback")
        verbose_name_plural = _("User Feedback")

    def __str__(self):
        return f"Action ({self.action_id}) - {self.feedback_text}"
