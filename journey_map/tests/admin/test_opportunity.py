import sys

import pytest
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journey_map.admin.opportunity import OpportunityAdmin
from journey_map.models import Opportunity, JourneyAction
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestOpportunityAdmin:
    """
    Tests for the OpportunityAdmin class in the Django admin interface.

    This test class verifies the general functionality of the OpportunityAdmin,
    ensuring it is properly configured and behaves as expected in the Django admin
    interface, with a focus on configuration and permissions.

    """

    def test_admin_registered(self):
        """
        Test that the Opportunity model is registered with OpportunityAdmin in the admin site.

        Asserts:
        --------
            The admin site has Opportunity registered with an instance of OpportunityAdmin.
        """
        assert isinstance(admin.site._registry[Opportunity], OpportunityAdmin)

    def test_list_display_configured(self, opportunity_admin: OpportunityAdmin) -> None:
        """
        Test that the list_display attribute is defined and non-empty.

        Args:
            opportunity_admin (OpportunityAdmin): The admin class instance being tested.

        Asserts:
        --------
            list_display is a tuple or list and has at least one item.
        """
        assert isinstance(opportunity_admin.list_display, (tuple, list))
        assert len(opportunity_admin.list_display) > 0

    def test_truncated_description_short(self, opportunity_admin: OpportunityAdmin):
        """
        Test that truncated_description returns the full text when it's short.
        """
        short_desc = "Short description"
        obj = Opportunity(description=short_desc)

        result = opportunity_admin.truncated_description(obj)
        assert result == short_desc

    def test_truncated_description_long(self, opportunity_admin: OpportunityAdmin):
        """
        Test that truncated_description truncates long text properly.
        """
        long_desc = (
            "This is a very long description that should be truncated at 32 characters"
        )
        obj = Opportunity(description=long_desc)

        result = opportunity_admin.truncated_description(obj)
        assert result == "This is a very long description ..."
        assert len(result) == 35  # 32 chars + 3 dots

    def test_truncated_description_short_description(
        self, opportunity_admin: OpportunityAdmin
    ):
        """
        Test that the truncated_description method has the correct short_description attribute.
        """
        assert opportunity_admin.truncated_description.short_description == _(
            "Description"
        )

    def test_action_description(
        self, opportunity_admin: OpportunityAdmin, opportunity: Opportunity
    ):
        """
        Test that action_description correctly returns the truncated action description.
        """
        result = opportunity_admin.action_description(opportunity)
        expected = (
            opportunity.action.action_description[:32] + "..."
            if len(opportunity.action.action_description) > 32
            else opportunity.action.action_description
        )
        assert result == expected

    def test_action_description_short(
        self, opportunity_admin: OpportunityAdmin, journey_action: JourneyAction
    ):
        """
        Test action_description with a short action description.
        """
        obj = Opportunity(action=journey_action)

        result = opportunity_admin.action_description(obj)
        assert result is not None

    def test_journey_name(
        self, opportunity_admin: OpportunityAdmin, opportunity: Opportunity
    ):
        """
        Test that journey_name correctly returns the journey name.
        """
        result = opportunity_admin.journey_name(opportunity)
        assert result == opportunity.action.stage.journey.name

    def test_journey_name_short_description(self, opportunity_admin: OpportunityAdmin):
        """
        Test that the journey_name method has the correct short_description attribute.
        """
        assert opportunity_admin.journey_name.short_description == _("Journey")
