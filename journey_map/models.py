from django.db import models

class UserJourney(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the user journey")
    description = models.TextField(blank=True, null=True, help_text="Description of the journey")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class JourneyStage(models.Model):
    journey = models.ForeignKey(UserJourney, related_name='stages', on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=255, help_text="Name of the stage (e.g., Consider, Explore, Compare, Test)")
    order = models.PositiveIntegerField(help_text="Order of the stage in the journey")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.journey.name} - {self.stage_name}"


class JourneyAction(models.Model):
    stage = models.ForeignKey(JourneyStage, related_name='actions', on_delete=models.CASCADE)
    action_description = models.TextField(help_text="Description of the action (e.g., Sees TV commercial, visits website)")
    order = models.PositiveIntegerField(help_text="Order of the action in the stage")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.stage.stage_name} - {self.action_description}"


class UserFeedback(models.Model):
    action = models.ForeignKey(JourneyAction, related_name='feedbacks', on_delete=models.CASCADE)
    feedback_text = models.TextField(help_text="User's feedback or emotion (e.g., 'I like that I can save cars')")
    is_positive = models.BooleanField(default=True, help_text="Is the feedback positive?")

    def __str__(self):
        return f"{self.action.action_description} - {self.feedback_text}"