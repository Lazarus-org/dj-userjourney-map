import sys

import pytest
from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from journey_map.admin.journey_action import JourneyActionAdmin
from journey_map.models import JourneyAction
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestJourneyActionAdmin:
    """
    Tests for the JourneyActionAdmin class in the Django admin interface.

    This test class verifies the general functionality of the JourneyActionAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface, with a focus on configuration and permissions.

    """

    def test_admin_registered(self):
        """
        Test that the JourneyAction model is registered with JourneyActionAdmin in the admin site.

        Asserts:
        --------
            The admin site has JourneyAction registered with an instance of JourneyActionAdmin.
        """
        assert isinstance(admin.site._registry[JourneyAction], JourneyActionAdmin)

    def test_list_display_configured(
        self, journey_action_admin: JourneyActionAdmin
    ) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        Args:
            journey_action_admin (JourneyActionAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(journey_action_admin.list_display, (tuple, list))
        assert len(journey_action_admin.list_display) > 0

    def test_list_filter_configured(
        self, journey_action_admin: JourneyActionAdmin
    ) -> None:
        """
        Test that the list_filter attribute is defined and non-empty.

        Args:
            journey_action_admin (JourneyActionAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_filter is a tuple or list and has at least one item.
        """
        assert isinstance(journey_action_admin.list_filter, (tuple, list))
        assert len(journey_action_admin.list_filter) > 0

    def test_search_fields_configured(
        self, journey_action_admin: JourneyActionAdmin
    ) -> None:
        """
        Test that the search_fields attribute is defined and non-empty.

        Args:
            journey_action_admin (JourneyActionAdmin): The admin class instance being tested.

        Asserts:
        --------
            search_fields is a tuple or list and has at least one item.
        """
        assert isinstance(journey_action_admin.search_fields, (tuple, list))
        assert len(journey_action_admin.search_fields) > 0

    def test_journey_action_display(
        self,
        journey_action_admin: JourneyActionAdmin,
        journey_action: JourneyAction,
        mock_request: HttpRequest,
    ):
        """
        Test that JourneyAction fields are correctly displayed in the admin list view.

        Args:
            journey_action_admin (JourneyActionAdmin): The admin class instance being tested.
            journey_action (JourneyAction): The JourneyAction fixture for testing.
            mock_request (HttpRequest): A mock request object for context.

        Asserts:
        --------
            The list view displays expected field values for a JourneyAction instance.
        """
        response = journey_action_admin.get_changelist_instance(
            mock_request
        ).get_queryset(mock_request)
        assert response.count() == 1
        assert response[0].action_description == journey_action.action_description
        assert response[0].stage.stage_name == journey_action.stage.stage_name

    def test_truncated_description_short(
        self, journey_action_admin: JourneyActionAdmin
    ):
        """
        Test that truncated_description returns the full description when it's short.
        """
        short_desc = "Short description"
        obj = JourneyAction(action_description=short_desc)

        result = journey_action_admin.truncated_description(obj)
        assert result == short_desc

    def test_truncated_description_long(self, journey_action_admin: JourneyActionAdmin):
        """
        Test that truncated_description truncates long descriptions properly.
        """
        long_desc = (
            "This is a very long description that should be truncated at 32 characters"
        )
        obj = JourneyAction(action_description=long_desc)

        result = journey_action_admin.truncated_description(obj)
        assert result == "This is a very long description ..."
        assert len(result) == 35  # 32 chars + 3 dots

    def test_truncated_description_short_description(
        self, journey_action_admin: JourneyActionAdmin
    ):
        """
        Test that the truncated_description method has the correct short_description attribute.
        """
        assert journey_action_admin.truncated_description.short_description == _(
            "Action Description"
        )

    def test_stage_name(
        self, journey_action_admin: JourneyActionAdmin, journey_action: JourneyAction
    ):
        """
        Test that stage_name correctly returns the stage's name.
        """
        result = journey_action_admin.stage_name(journey_action)
        assert result == journey_action.stage.stage_name

    def test_stage_name_short_description(
        self, journey_action_admin: JourneyActionAdmin
    ):
        """
        Test that the stage_name method has the correct short_description attribute.
        """
        assert journey_action_admin.stage_name.short_description == _("Stage")
