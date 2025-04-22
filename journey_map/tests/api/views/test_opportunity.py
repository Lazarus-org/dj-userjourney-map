import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from journey_map.models import Opportunity, JourneyAction
from journey_map.settings.conf import config
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestOpportunityViewSet:
    """
    Tests for the OpportunityViewSet API endpoints.

    This test class verifies the behavior of the OpportunityViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and permissions, including serializer validation.
    The endpoints are accessible at /api/opportunities/.

    Tests:
    -------
    - test_list_opportunity: Verifies the list endpoint returns 200 OK and includes opportunities.
    - test_retrieve_opportunity: Checks the retrieve endpoint returns 200 OK and correct data.
    - test_create_opportunity: Tests the create endpoint returns 201 Created with valid data.
    - test_update_opportunity: Tests the update endpoint returns 200 OK.
    - test_destroy_opportunity: Tests the destroy endpoint returns 204 No Content.
    - test_list_opportunity_disabled: Tests the list endpoint returns 405 when disabled.
    - test_retrieve_opportunity_disabled: Tests the retrieve endpoint returns 405 when disabled.
    - test_create_opportunity_invalid_action: Tests validation failure for non-existent action_id.
    - test_create_opportunity_long_description: Tests validation failure for overly long description.
    """

    def test_list_opportunity(
        self,
        api_client: APIClient,
        opportunity: Opportunity,
        admin_user: User,
    ):
        """
        Test the list endpoint for Opportunity.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            opportunity (Opportunity): A sample Opportunity instance.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains a 'results' key with opportunities, including action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_list = True  # Enable list method
        config.api_opportunity_extra_permission_class = None

        url = reverse("opportunity-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["id"] == opportunity.id
        ), f"Expected ID {opportunity.id}, got {response.data['results'][0]['id']}."
        assert response.data["results"][0]["action"] == str(
            opportunity.action
        ), f"Expected action {str(opportunity.action)}, got {response.data['results'][0]['action']}."
        assert (
            "action_id" not in response.data["results"][0]
        ), "Expected 'action_id' to be absent in response."

    def test_retrieve_opportunity(
        self,
        api_client: APIClient,
        opportunity: Opportunity,
        admin_user: User,
    ):
        """
        Test the retrieve endpoint for Opportunity.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            opportunity (Opportunity): The Opportunity instance to retrieve.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains the correct Opportunity ID, description, and action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_retrieve = True  # Enable retrieve method

        url = reverse("opportunity-detail", kwargs={"pk": opportunity.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == opportunity.id
        ), f"Expected ID {opportunity.id}, got {response.data['id']}."
        assert (
            response.data["description"] == opportunity.description
        ), f"Expected description {opportunity.description}, got {response.data['description']}."
        assert response.data["action"] == str(
            opportunity.action
        ), f"Expected action {str(opportunity.action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_create_opportunity(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the create endpoint for Opportunity.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): The action to associate with the opportunity.
            admin_user (User): The admin user creating the opportunity.

        Asserts:
            The response status code is 201.
            The created opportunity has the correct data, including action string.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_create = True  # Enable create method

        url = reverse("opportunity-list")
        payload = {
            "description": "Improve website speed",
            "action_id": journey_action.id,
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["description"] == payload["description"]
        ), f"Expected description {payload['description']}, got {response.data['description']}."
        assert response.data["action"] == str(
            journey_action
        ), f"Expected action {str(journey_action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_update_opportunity(
        self,
        api_client: APIClient,
        opportunity: Opportunity,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the update endpoint for Opportunity.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            opportunity (Opportunity): The Opportunity instance to update.
            journey_action (JourneyAction): A different action to update to.
            admin_user (User): The admin user updating the opportunity.

        Asserts:
            The response status code is 200.
            The updated opportunity reflects the new data, including new action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_update = True  # Enable update method

        url = reverse("opportunity-detail", kwargs={"pk": opportunity.pk})
        payload = {"description": "Updated opportunity", "action_id": journey_action.id}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["description"] == payload["description"]
        ), f"Expected description {payload['description']}, got {response.data['description']}."
        assert response.data["action"] == str(
            journey_action
        ), f"Expected action {str(journey_action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_destroy_opportunity(
        self,
        api_client: APIClient,
        opportunity: Opportunity,
        admin_user: User,
    ):
        """
        Test the destroy endpoint for Opportunity.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            opportunity (Opportunity): The Opportunity instance to delete.
            admin_user (User): The admin user deleting the opportunity.

        Asserts:
            The response status code is 204.
            The opportunity is removed from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_delete = True  # Enable destroy method

        url = reverse("opportunity-detail", kwargs={"pk": opportunity.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not Opportunity.objects.filter(
            pk=opportunity.pk
        ).exists(), "Opportunity was not deleted."

    def test_list_opportunity_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        opportunity: Opportunity,
    ):
        """
        Test the list view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            opportunity (Opportunity): A sample Opportunity instance.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_list = False  # Disable list method

        url = reverse("opportunity-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_opportunity_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        opportunity: Opportunity,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            opportunity (Opportunity): The Opportunity instance to retrieve.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_retrieve = False  # Disable retrieve method

        url = reverse("opportunity-detail", kwargs={"pk": opportunity.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_create_opportunity_invalid_action(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid action_id.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user creating the opportunity.

        Asserts:
            The response status code is 400.
            The error message indicates an invalid action_id.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_opportunity_allow_create = True  # Enable create method

        url = reverse("opportunity-list")
        payload = {
            "description": "Invalid opportunity",
            "action_id": 999,  # Non-existent action ID
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert "action_id" in response.data, "Expected error for invalid action_id."
        assert "JourneyAction with the given ID was not found" in str(
            response.data["action_id"]
        ), "Unexpected error message."
