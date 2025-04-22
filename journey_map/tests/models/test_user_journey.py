import sys

import pytest

from journey_map.models import UserJourney
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserJourneyModel:
    """
    Test suite for the UserJourney model.
    """

    def test_str_method(self, user_journey: UserJourney) -> None:
        """
        Test that the __str__ method returns the correct string representation of a User Journey.

        Asserts:
        -------
            - The string representation includes the correct structure.
        """
        expected_str = user_journey.name
        assert (
            str(user_journey) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(user_journey)}'."
