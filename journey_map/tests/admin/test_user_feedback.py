import sys

import pytest
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.admin.user_feedback import UserFeedbackAdmin
from journey_map.models import UserFeedback, JourneyAction
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserFeedbackAdmin:
    """
    Tests for the UserFeedbackAdmin class in the Django admin interface.

    This test class verifies the general functionality of the UserFeedbackAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface, with a focus on configuration and permissions.

    """

    def test_admin_registered(self):
        """
        Test that the UserFeedback model is registered with UserFeedbackAdmin in the admin site.

        Asserts:
        --------
            The admin site has UserFeedback registered with an instance of UserFeedbackAdmin.
        """
        assert isinstance(admin.site._registry[UserFeedback], UserFeedbackAdmin)

    def test_truncated_feedback_short(self, user_feedback_admin: UserFeedbackAdmin):
        """
        Test that truncated_feedback returns the full text when it's short.
        """
        short_feedback = "Short feedback"
        obj = UserFeedback(feedback_text=short_feedback)

        result = user_feedback_admin.truncated_feedback(obj)
        assert result == short_feedback

    def test_truncated_feedback_long(self, user_feedback_admin: UserFeedbackAdmin):
        """
        Test that truncated_feedback truncates long text properly.
        """
        long_feedback = "This is a very long feedback text that should be truncated at 32 characters"
        obj = UserFeedback(feedback_text=long_feedback)

        result = user_feedback_admin.truncated_feedback(obj)
        assert result == "This is a very long feedback tex..."
        assert len(result) == 35  # 32 chars + 3 dots

    def test_truncated_feedback_short_description(
        self, user_feedback_admin: UserFeedbackAdmin
    ):
        """
        Test that the truncated_feedback method has the correct short_description attribute.
        """
        assert user_feedback_admin.truncated_feedback.short_description == _("Feedback")

    def test_action_description(
        self, user_feedback_admin: UserFeedbackAdmin, user_feedback: UserFeedback
    ):
        """
        Test that action_description correctly returns the truncated action description.
        """
        result = user_feedback_admin.action_description(user_feedback)
        expected = (
            user_feedback.action.action_description[:32] + "..."
            if len(user_feedback.action.action_description) > 32
            else user_feedback.action.action_description
        )
        assert result == expected

    def test_action_description_short(
        self, user_feedback_admin: UserFeedbackAdmin, journey_action: JourneyAction
    ):
        """
        Test action_description with a short action description.
        """
        obj = UserFeedback(action=journey_action)

        result = user_feedback_admin.action_description(obj)
        assert result is not None

    def test_action_description_short_description(
        self, user_feedback_admin: UserFeedbackAdmin
    ):
        """
        Test that the action_description method has the correct short_description attribute.
        """
        assert user_feedback_admin.action_description.short_description == _("Action")
