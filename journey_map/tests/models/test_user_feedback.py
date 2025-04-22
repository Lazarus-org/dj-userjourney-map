import sys

import pytest

from journey_map.models import UserFeedback
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserFeedbackModel:
    """
    Test suite for the UserFeedback model.
    """

    def test_str_method(self, user_feedback: UserFeedback) -> None:
        """
        Test that the __str__ method returns the correct string representation of a UserFeedback.

        Asserts:
        -------
            - The string representation includes the correct structure.
        """
        expected_str = (
            f"Action ({user_feedback.action_id}) - {user_feedback.feedback_text}"
        )
        assert (
            str(user_feedback) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(user_feedback)}'."
