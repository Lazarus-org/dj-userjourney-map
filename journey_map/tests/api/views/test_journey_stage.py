import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from journey_map.models import JourneyStage, UserJourney
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


class TestJourneyStageViewSet:
    """
    Tests for the JourneyStageViewSet API endpoints.

    This test class verifies the behavior of the JourneyStageViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and permissions, including serializer validation.
    The endpoints are accessible at /api/journey-stages/.

    Tests:
    -------
    - test_list_journey_stage: Verifies the list endpoint returns 200 OK and includes stages.
    - test_retrieve_journey_stage: Checks the retrieve endpoint returns 200 OK and correct data.
    - test_create_journey_stage: Tests the create endpoint returns 201 Created with valid data.
    - test_update_journey_stage: Tests the update endpoint returns 200 OK.
    - test_destroy_journey_stage: Tests the destroy endpoint returns 204 No Content.
    - test_list_journey_stage_disabled: Tests the list endpoint returns 405 when disabled.
    - test_retrieve_journey_stage_disabled: Tests the retrieve endpoint returns 405 when disabled.
    - test_create_journey_stage_invalid_journey: Tests validation failure for non-existent journey_id.
    """

    def test_list_journey_stage(
        self,
        api_client: APIClient,
        journey_stage: JourneyStage,
        admin_user: User,
    ):
        """
        Test the list endpoint for JourneyStage.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_stage (JourneyStage): A sample JourneyStage instance.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains a 'results' key with stages, including journey and actions.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_list = True  # Enable list method
        config.api_journey_stage_extra_permission_class = None

        url = reverse("journey-stage-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["id"] == journey_stage.id
        ), f"Expected ID {journey_stage.id}, got {response.data['results'][0]['id']}."
        assert response.data["results"][0]["journey"] == str(
            journey_stage.journey
        ), f"Expected journey {str(journey_stage.journey)}, got {response.data['results'][0]['journey']}."
        assert (
            "actions" in response.data["results"][0]
        ), "Expected 'actions' in response data."
        assert (
            "journey_id" not in response.data["results"][0]
        ), "Expected 'journey_id' to be absent in response."

    def test_retrieve_journey_stage(
        self,
        api_client: APIClient,
        journey_stage: JourneyStage,
        admin_user: User,
    ):
        """
        Test the retrieve endpoint for JourneyStage.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_stage (JourneyStage): The JourneyStage instance to retrieve.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains the correct JourneyStage ID, stage_name, and journey.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_retrieve = True  # Enable retrieve method

        url = reverse("journey-stage-detail", kwargs={"pk": journey_stage.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == journey_stage.id
        ), f"Expected ID {journey_stage.id}, got {response.data['id']}."
        assert (
            response.data["stage_name"] == journey_stage.stage_name
        ), f"Expected stage_name {journey_stage.stage_name}, got {response.data['stage_name']}."
        assert response.data["journey"] == str(
            journey_stage.journey
        ), f"Expected journey {str(journey_stage.journey)}, got {response.data['journey']}."
        assert "actions" in response.data, "Expected 'actions' in response data."
        assert (
            "journey_id" not in response.data
        ), "Expected 'journey_id' to be absent in response."

    def test_create_journey_stage(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the create endpoint for JourneyStage.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): The journey to associate with the stage.
            admin_user (User): The admin user creating the stage.

        Asserts:
            The response status code is 201.
            The created stage has the correct data, including journey string.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_create = True  # Enable create method

        url = reverse("journey-stage-list")
        payload = {
            "stage_name": "New Stage",
            "order": 2,
            "journey_id": user_journey.id,
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["stage_name"] == payload["stage_name"]
        ), f"Expected stage_name {payload['stage_name']}, got {response.data['stage_name']}."
        assert response.data["journey"] == str(
            user_journey
        ), f"Expected journey {str(user_journey)}, got {response.data['journey']}."
        assert (
            response.data["actions"] == []
        ), "Expected empty 'actions' list for new stage."
        assert (
            "journey_id" not in response.data
        ), "Expected 'journey_id' to be absent in response."

    def test_update_journey_stage(
        self,
        api_client: APIClient,
        journey_stage: JourneyStage,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the update endpoint for JourneyStage.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_stage (JourneyStage): The JourneyStage instance to update.
            user_journey (UserJourney): A different journey to update to.
            admin_user (User): The admin user updating the stage.

        Asserts:
            The response status code is 200.
            The updated stage reflects the new data, including new journey.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_update = True  # Enable update method

        url = reverse("journey-stage-detail", kwargs={"pk": journey_stage.pk})
        payload = {"stage_name": "Updated Stage", "journey_id": user_journey.id}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["stage_name"] == payload["stage_name"]
        ), f"Expected stage_name {payload['stage_name']}, got {response.data['stage_name']}."
        assert response.data["journey"] == str(
            user_journey
        ), f"Expected journey {str(user_journey)}, got {response.data['journey']}."
        assert (
            "journey_id" not in response.data
        ), "Expected 'journey_id' to be absent in response."

    def test_destroy_journey_stage(
        self,
        api_client: APIClient,
        journey_stage: JourneyStage,
        admin_user: User,
    ):
        """
        Test the destroy endpoint for JourneyStage.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_stage (JourneyStage): The JourneyStage instance to delete.
            admin_user (User): The admin user deleting the stage.

        Asserts:
            The response status code is 204.
            The stage is removed from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_delete = True  # Enable destroy method

        url = reverse("journey-stage-detail", kwargs={"pk": journey_stage.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not JourneyStage.objects.filter(
            pk=journey_stage.pk
        ).exists(), "Stage was not deleted."

    def test_list_journey_stage_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        journey_stage: JourneyStage,
    ):
        """
        Test the list view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            journey_stage (JourneyStage): A sample JourneyStage instance.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_list = False  # Disable list method

        url = reverse("journey-stage-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_journey_stage_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        journey_stage: JourneyStage,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            journey_stage (JourneyStage): The JourneyStage instance to retrieve.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_retrieve = False  # Disable retrieve method

        url = reverse("journey-stage-detail", kwargs={"pk": journey_stage.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_create_journey_stage_invalid_journey(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid journey_id.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user creating the stage.

        Asserts:
            The response status code is 400.
            The error message indicates an invalid journey_id.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_journey_stage_allow_create = True  # Enable create method

        url = reverse("journey-stage-list")
        payload = {
            "stage_name": "New Stage",
            "order": 1,
            "journey_id": 999,  # Non-existent journey ID
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert "journey_id" in response.data, "Expected error for invalid journey_id."
        assert "UserJourney with the given ID was not found" in str(
            response.data["journey_id"]
        ), "Unexpected error message."
