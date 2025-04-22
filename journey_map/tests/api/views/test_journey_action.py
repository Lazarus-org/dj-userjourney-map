import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from journey_map.models import JourneyAction, JourneyStage
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


class TestJourneyActionViewSet:
    """
    Tests for the JourneyActionViewSet API endpoints.

    This test class verifies the behavior of the JourneyActionViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and permissions, including serializer validation.
    The endpoints are accessible at /api/journey-actions/.

    Tests:
    -------
    - test_list_journey_action: Verifies the list endpoint returns 200 OK and includes actions.
    - test_retrieve_journey_action: Checks the retrieve endpoint returns 200 OK and correct data.
    - test_create_journey_action: Tests the create endpoint returns 201 Created with valid data.
    - test_update_journey_action: Tests the update endpoint returns 200 OK.
    - test_destroy_journey_action: Tests the destroy endpoint returns 204 No Content.
    - test_list_journey_action_disabled: Tests the list endpoint returns 405 when disabled.
    - test_retrieve_journey_action_disabled: Tests the retrieve endpoint returns 405 when disabled.
    - test_create_journey_action_invalid_stage: Tests validation failure for non-existent stage_id.
    """

    def test_list_journey_action(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the list endpoint for JourneyAction.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): A sample JourneyAction instance.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains a 'results' key with actions, including stage and nested fields.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_list = True  # Enable list method
        config.api_journey_action_extra_permission_class = None

        url = reverse("journey-action-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["id"] == journey_action.id
        ), f"Expected ID {journey_action.id}, got {response.data['results'][0]['id']}."
        assert response.data["results"][0]["stage"] == str(
            journey_action.stage
        ), f"Expected stage {str(journey_action.stage)}, got {response.data['results'][0]['stage']}."
        assert (
            "feedbacks" in response.data["results"][0]
        ), "Expected 'feedbacks' in response data."
        assert (
            "pain_points" in response.data["results"][0]
        ), "Expected 'pain_points' in response data."
        assert (
            "opportunities" in response.data["results"][0]
        ), "Expected 'opportunities' in response data."
        assert (
            "stage_id" not in response.data["results"][0]
        ), "Expected 'stage_id' to be absent in response."

    def test_retrieve_journey_action(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the retrieve endpoint for JourneyAction.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): The JourneyAction instance to retrieve.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains the correct JourneyAction ID, action_description, and stage.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_retrieve = True  # Enable retrieve method

        url = reverse("journey-action-detail", kwargs={"pk": journey_action.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == journey_action.id
        ), f"Expected ID {journey_action.id}, got {response.data['id']}."
        assert (
            response.data["action_description"] == journey_action.action_description
        ), f"Expected action_description {journey_action.action_description}, got {response.data['action_description']}."
        assert response.data["stage"] == str(
            journey_action.stage
        ), f"Expected stage {str(journey_action.stage)}, got {response.data['stage']}."
        assert "feedbacks" in response.data, "Expected 'feedbacks' in response data."
        assert (
            "pain_points" in response.data
        ), "Expected 'pain_points' in response data."
        assert (
            "opportunities" in response.data
        ), "Expected 'opportunities' in response data."
        assert (
            "stage_id" not in response.data
        ), "Expected 'stage_id' to be absent in response."

    def test_create_journey_action(
        self,
        api_client: APIClient,
        journey_stage: JourneyStage,
        admin_user: User,
    ):
        """
        Test the create endpoint for JourneyAction.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_stage (JourneyStage): The stage to associate with the action.
            admin_user (User): The admin user creating the action.

        Asserts:
            The response status code is 201.
            The created action has the correct data, including stage string.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_create = True  # Enable create method

        url = reverse("journey-action-list")
        payload = {
            "action_description": "New Action",
            "touchpoint": "Website",
            "order": 2,
            "stage_id": journey_stage.id,
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["action_description"] == payload["action_description"]
        ), f"Expected action_description {payload['action_description']}, got {response.data['action_description']}."
        assert response.data["stage"] == str(
            journey_stage
        ), f"Expected stage {str(journey_stage)}, got {response.data['stage']}."
        assert (
            response.data["feedbacks"] == []
        ), "Expected empty 'feedbacks' list for new action."
        assert (
            response.data["pain_points"] == []
        ), "Expected empty 'pain_points' list for new action."
        assert (
            response.data["opportunities"] == []
        ), "Expected empty 'opportunities' list for new action."
        assert (
            "stage_id" not in response.data
        ), "Expected 'stage_id' to be absent in response."

    def test_update_journey_action(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        journey_stage: JourneyStage,
        admin_user: User,
    ):
        """
        Test the update endpoint for JourneyAction.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): The JourneyAction instance to update.
            journey_stage (JourneyStage): A different stage to update to.
            admin_user (User): The admin user updating the action.

        Asserts:
            The response status code is 200.
            The updated action reflects the new data, including new stage.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_update = True  # Enable update method

        url = reverse("journey-action-detail", kwargs={"pk": journey_action.pk})
        payload = {"action_description": "Updated Action", "stage_id": journey_stage.id}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["action_description"] == payload["action_description"]
        ), f"Expected action_description {payload['action_description']}, got {response.data['action_description']}."
        assert response.data["stage"] == str(
            journey_stage
        ), f"Expected stage {str(journey_stage)}, got {response.data['stage']}."
        assert (
            "stage_id" not in response.data
        ), "Expected 'stage_id' to be absent in response."

    def test_destroy_journey_action(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the destroy endpoint for JourneyAction.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): The JourneyAction instance to delete.
            admin_user (User): The admin user deleting the action.

        Asserts:
            The response status code is 204.
            The action is removed from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_delete = True  # Enable destroy method

        url = reverse("journey-action-detail", kwargs={"pk": journey_action.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not JourneyAction.objects.filter(
            pk=journey_action.pk
        ).exists(), "Action was not deleted."

    def test_list_journey_action_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        journey_action: JourneyAction,
    ):
        """
        Test the list view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            journey_action (JourneyAction): A sample JourneyAction instance.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_list = False  # Disable list method

        url = reverse("journey-action-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_journey_action_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        journey_action: JourneyAction,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            journey_action (JourneyAction): The JourneyAction instance to retrieve.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_retrieve = False  # Disable retrieve method

        url = reverse("journey-action-detail", kwargs={"pk": journey_action.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_create_journey_action_invalid_stage(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid stage_id.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user creating the action.

        Asserts:
            The response status code is 400.
            The error message indicates an invalid stage_id.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_action_allow_create = True  # Enable create method

        url = reverse("journey-action-list")
        payload = {
            "action_description": "New Action",
            "touchpoint": "Website",
            "order": 1,
            "stage_id": 999,  # Non-existent stage ID
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert "stage_id" in response.data, "Expected error for invalid stage_id."
        assert "JourneyStage with the given ID was not found" in str(
            response.data["stage_id"]
        ), "Unexpected error message."
