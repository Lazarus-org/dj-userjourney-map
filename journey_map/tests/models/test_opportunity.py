import sys

import pytest

from journey_map.models import Opportunity
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestOpportunityModel:
    """
    Test suite for the Opportunity model.
    """

    def test_str_method(self, opportunity: Opportunity) -> None:
        """
        Test that the __str__ method returns the correct string representation of an Opportunity.

        Asserts:
        -------
            - The string representation includes the correct structure.
        """
        expected_str = f"Action ({opportunity.action_id}) - {opportunity.description}"
        assert (
            str(opportunity) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(opportunity)}'."
