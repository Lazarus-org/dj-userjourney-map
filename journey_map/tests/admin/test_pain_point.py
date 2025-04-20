import sys

import pytest
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.admin.pain_point import PainPointAdmin
from journey_map.models import PainPoint, JourneyAction

from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestPainPointAdmin:
    """
    Tests for the PainPointAdmin class in the Django admin interface.

    This test class verifies the general functionality of the PainPointAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface, with a focus on configuration and permissions.

    """

    def test_admin_registered(self):
        """
        Test that the PainPoint model is registered with PainPointAdmin in the admin site.

        Asserts:
        --------
            The admin site has PainPoint registered with an instance of PainPointAdmin.
        """
        assert isinstance(admin.site._registry[PainPoint], PainPointAdmin)

    def test_list_display_configured(self, pain_point_admin: PainPointAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        Args:
            pain_point_admin (PainPointAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(pain_point_admin.list_display, (tuple, list))
        assert len(pain_point_admin.list_display) > 0

    def test_truncated_description_short(self, pain_point_admin: PainPointAdmin):
        """
        Test that truncated_description returns the full text when it's short.
        """
        short_desc = "Short description"
        obj = PainPoint(description=short_desc)

        result = pain_point_admin.truncated_description(obj)
        assert result == short_desc

    def test_truncated_description_long(self, pain_point_admin: PainPointAdmin):
        """
        Test that truncated_description truncates long text properly.
        """
        long_desc = (
            "This is a very long description that should be truncated at 32 characters"
        )
        obj = PainPoint(description=long_desc)

        result = pain_point_admin.truncated_description(obj)
        assert result == "This is a very long description ..."
        assert len(result) == 35  # 32 chars + 3 dots

    def test_truncated_description_short_description(
        self, pain_point_admin: PainPointAdmin
    ):
        """
        Test that the truncated_description method has the correct short_description attribute.
        """
        assert pain_point_admin.truncated_description.short_description == _(
            "Description"
        )

    def test_action_description(
        self, pain_point_admin: PainPointAdmin, pain_point: PainPoint
    ):
        """
        Test that action_description correctly returns the truncated action description.
        """
        result = pain_point_admin.action_description(pain_point)
        expected = (
            pain_point.action.action_description[:32] + "..."
            if len(pain_point.action.action_description) > 32
            else pain_point.action.action_description
        )
        assert result == expected

    def test_action_description_short(
        self, pain_point_admin: PainPointAdmin, journey_action: JourneyAction
    ):
        """
        Test action_description with a short action description.
        """
        obj = PainPoint(action=journey_action)

        result = pain_point_admin.action_description(obj)
        assert result == journey_action.action_description

    def test_action_description_short_description(
        self, pain_point_admin: PainPointAdmin
    ):
        """
        Test that the action_description method has the correct short_description attribute.
        """
        assert pain_point_admin.action_description.short_description == _("Action")

    def test_journey_name(
        self, pain_point_admin: PainPointAdmin, pain_point: PainPoint
    ):
        """
        Test that journey_name correctly returns the journey name.
        """
        result = pain_point_admin.journey_name(pain_point)
        assert result == pain_point.action.stage.journey.name

    def test_journey_name_short_description(self, pain_point_admin: PainPointAdmin):
        """
        Test that the journey_name method has the correct short_description attribute.
        """
        assert pain_point_admin.journey_name.short_description == _("Journey")
