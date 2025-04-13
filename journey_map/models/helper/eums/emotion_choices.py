from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EmotionChoices(TextChoices):
    HAPPY = "happy", _("Happy")
    FRUSTRATED = "frustrated", _("Frustrated")
    CONFUSED = "confused", _("Confused")
    NEUTRAL = "neutral", _("Neutral")
    EXCITED = "excited", _("Excited")
