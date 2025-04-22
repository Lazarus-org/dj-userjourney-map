import sys

import pytest

from journey_map.models import PainPoint
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestPainPointModel:
    """
    Test suite for the PainPoint model.
    """

    def test_str_method(self, pain_point: PainPoint) -> None:
        """
        Test that the __str__ method returns the correct string representation of a PainPoint.

        Asserts:
        -------
            - The string representation includes the correct structure.
        """
        expected_str = f"Action ({pain_point.action_id}) - {pain_point.description}"
        assert (
            str(pain_point) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(pain_point)}'."
