import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from journey_map.models.user_journey import UserJourney, UserPersona
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


class TestUserJourneyViewSet:
    """
    Tests for the UserJourneyViewSet API endpoints.

    This test class verifies the behavior of the UserJourneyViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and permissions, including serializer validation.
    The endpoints are accessible at /api/user-journeys/.

    Tests:
    -------
    - test_list_user_journey: Verifies the list endpoint returns 200 OK and includes journeys.
    - test_retrieve_user_journey: Checks the retrieve endpoint returns 200 OK and correct data when allowed.
    - test_create_user_journey: Tests the create endpoint returns 201 Created with valid data when allowed.
    - test_update_user_journey: Tests the update endpoint returns 200 OK when allowed.
    - test_destroy_user_journey: Tests the destroy endpoint returns 204 No Content when allowed.
    - test_list_user_journey_disabled: Tests the list endpoint returns 405 when disabled.
    - test_retrieve_user_journey_disabled: Tests the retrieve endpoint returns 405 when disabled.
    - test_create_user_journey_invalid_persona: Tests validation failure for non-existent persona.
    """

    def test_list_user_journey(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the list endpoint for UserJourney.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): A sample UserJourney instance.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains a 'results' key with journeys.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_list = True  # Enable list method
        config.api_user_journey_extra_permission_class = None

        url = reverse("user-journey-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["id"] == user_journey.id
        ), f"Expected ID {user_journey.id}, got {response.data['results'][0]['id']}."

    def test_retrieve_user_journey(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the retrieve endpoint for UserJourney.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): The UserJourney instance to retrieve.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains the correct UserJourney ID and name.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_retrieve = True  # Enable retrieve method

        url = reverse("user-journey-detail", kwargs={"pk": user_journey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == user_journey.id
        ), f"Expected ID {user_journey.id}, got {response.data['id']}."
        assert (
            response.data["name"] == user_journey.name
        ), f"Expected name {user_journey.name}, got {response.data['name']}."

    def test_create_user_journey(
        self,
        api_client: APIClient,
        persona: UserPersona,
        admin_user: User,
    ):
        """
        Test the create endpoint for UserJourney.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            persona (UserPersona): The persona to associate with the journey.
            admin_user (User): The admin user creating the journey.

        Asserts:
            The response status code is 201.
            The created journey has the correct data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_create = True  # Enable create method

        url = reverse("user-journey-list")
        payload = {
            "name": "New Journey",
            "description": "A new user journey",
            "persona_id": persona.id,
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["name"] == payload["name"]
        ), f"Expected name {payload['name']}, got {response.data['name']}."
        assert response.data["persona"] == str(
            persona
        ), f"Expected persona {persona}, got {response.data['persona']}."

    def test_update_user_journey(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the update endpoint for UserJourney.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): The UserJourney instance to update.
            admin_user (User): The admin user updating the journey.

        Asserts:
            The response status code is 200.
            The updated journey reflects the new data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_update = True  # Enable update method

        url = reverse("user-journey-detail", kwargs={"pk": user_journey.pk})
        payload = {"name": "Updated Journey"}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["name"] == payload["name"]
        ), f"Expected name {payload['name']}, got {response.data['name']}."

    def test_destroy_user_journey(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        admin_user: User,
    ):
        """
        Test the destroy endpoint for UserJourney.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): The UserJourney instance to delete.
            admin_user (User): The admin user deleting the journey.

        Asserts:
            The response status code is 204.
            The journey is removed from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_delete = True  # Enable destroy method

        url = reverse("user-journey-detail", kwargs={"pk": user_journey.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not UserJourney.objects.filter(
            pk=user_journey.pk
        ).exists(), "Journey was not deleted."

    def test_list_user_journey_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user_journey: UserJourney,
    ):
        """
        Test the list view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_journey (UserJourney): A sample UserJourney instance.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_list = False  # Disable list method

        url = reverse("user-journey-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_user_journey_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user_journey: UserJourney,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_journey (UserJourney): The UserJourney instance to retrieve.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_retrieve = False  # Disable retrieve method

        url = reverse("user-journey-detail", kwargs={"pk": user_journey.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_create_user_journey_invalid_persona(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid persona ID.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user creating the journey.

        Asserts:
            The response status code is 400.
            The error message indicates an invalid persona ID.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_create = True  # Enable create method

        url = reverse("user-journey-list")
        payload = {
            "name": "Unique Journey",
            "description": "A new journey",
            "persona_id": 999,  # Non-existent persona ID
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 400
        ), f"Expected 400 Bad Request, got {response.status_code}."
        assert "persona_id" in response.data, "Expected error for invalid persona ID."

    def test_update_user_journey_with_persona(
        self,
        api_client: APIClient,
        user_journey: UserJourney,
        persona: UserPersona,
        admin_user: User,
    ):
        """
        Test the update endpoint for UserJourney with a new persona.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_journey (UserJourney): The UserJourney instance to update.
            persona (UserPersona): The persona to associate with the journey.
            admin_user (User): The admin user updating the journey.

        Asserts:
            The response status code is 200.
            The updated journey reflects the new data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_journey_allow_update = True  # Enable update method

        url = reverse("user-journey-detail", kwargs={"pk": user_journey.pk})
        payload = {"persona_id": persona.id}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert response.data["persona"] == str(
            persona
        ), f"Expected persona {persona}, got {response.data['persona']}."
