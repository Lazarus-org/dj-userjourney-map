import sys

import pytest
from django.contrib import admin
from django.http import HttpRequest

from journey_map.admin.user_journey import UserJourneyAdmin
from journey_map.models import UserJourney
from journey_map.settings.conf import config
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestUserJourneyAdmin:
    """
    Tests for the UserJourneyAdmin class in the Django admin interface.

    This test class verifies the general functionality of the UserJourneyAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface, with a focus on configuration and permissions.

    Tests:
    -------
    - test_admin_registered: Verifies UserJourney is registered with UserJourneyAdmin.
    - test_list_display_configured: Ensures list_display is properly set.
    - test_list_filter_configured: Ensures list_filter is properly set.
    - test_search_fields_configured: Ensures search_fields is properly set.
    - test_admin_permissions: Verifies permission settings via config.
    - test_user_journey_display: Tests display of UserJourney fields in list view.
    """

    def test_admin_registered(self):
        """
        Test that the UserJourney model is registered with UserJourneyAdmin in the admin site.

        Asserts:
        --------
            The admin site has UserJourney registered with an instance of UserJourneyAdmin.
        """
        assert isinstance(admin.site._registry[UserJourney], UserJourneyAdmin)

    def test_list_display_configured(
        self, user_journey_admin: UserJourneyAdmin
    ) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        Args:
            user_journey_admin (UserJourneyAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(user_journey_admin.list_display, (tuple, list))
        assert len(user_journey_admin.list_display) > 0

    def test_list_filter_configured(self, user_journey_admin: UserJourneyAdmin) -> None:
        """
        Test that the list_filter attribute is defined and non-empty.

        Args:
            user_journey_admin (UserJourneyAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_filter is a tuple or list and has at least one item.
        """
        assert isinstance(user_journey_admin.list_filter, (tuple, list))
        assert len(user_journey_admin.list_filter) > 0

    def test_search_fields_configured(
        self, user_journey_admin: UserJourneyAdmin
    ) -> None:
        """
        Test that the search_fields attribute is defined and non-empty.

        Args:
            user_journey_admin (UserJourneyAdmin): The admin class instance being tested.

        Asserts:
        --------
            search_fields is a tuple or list and has at least one item.
        """
        assert isinstance(user_journey_admin.search_fields, (tuple, list))
        assert len(user_journey_admin.search_fields) > 0

    def test_admin_permissions(
        self, user_journey_admin: UserJourneyAdmin, mock_request: HttpRequest
    ):
        """
        Test that admin permissions reflect the config settings.

        Args:
            user_journey_admin (UserJourneyAdmin): The admin class instance being tested.
            mock_request (HttpRequest): A mock request object for permission checks.

        Asserts:
        --------
            has_add_permission, has_change_permission, has_delete_permission, and
            has_module_permission reflect config settings.
        """
        # Test with config permissions denied
        config.admin_has_add_permission = False
        config.admin_has_change_permission = False
        config.admin_has_delete_permission = False
        config.admin_has_module_permission = False
        assert user_journey_admin.has_add_permission(mock_request) is False
        assert user_journey_admin.has_change_permission(mock_request) is False
        assert user_journey_admin.has_delete_permission(mock_request) is False
        assert user_journey_admin.has_module_permission(mock_request) is False

        # Test with config permissions granted
        config.admin_has_add_permission = True
        config.admin_has_change_permission = True
        config.admin_has_delete_permission = True
        config.admin_has_module_permission = True
        assert user_journey_admin.has_add_permission(mock_request) is True
        assert user_journey_admin.has_change_permission(mock_request) is True
        assert user_journey_admin.has_delete_permission(mock_request) is True
        assert user_journey_admin.has_module_permission(mock_request) is True

    def test_user_journey_display(
        self,
        user_journey_admin: UserJourneyAdmin,
        user_journey: UserJourney,
        mock_request: HttpRequest,
    ):
        """
        Test that UserJourney fields are correctly displayed in the admin list view.

        Args:
            user_journey_admin (UserJourneyAdmin): The admin class instance being tested.
            user_journey (UserJourney): The UserJourney fixture for testing.
            mock_request (HttpRequest): A mock request object for context.

        Asserts:
        --------
            The list view displays expected field values for a UserJourney instance.
        """
        response = user_journey_admin.get_changelist_instance(
            mock_request
        ).get_queryset(mock_request)
        assert response.count() == 1
        assert response[0].name == user_journey.name
        assert response[0].persona.persona_name == user_journey.persona.persona_name
