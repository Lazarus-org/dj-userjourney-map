import sys

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from journey_map.models import UserFeedback, JourneyAction
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


class TestUserFeedbackViewSet:
    """
    Tests for the UserFeedbackViewSet API endpoints.

    This test class verifies the behavior of the UserFeedbackViewSet,
    ensuring that the list, retrieve, create, update, and destroy methods function correctly
    under various configurations and permissions, including serializer validation.
    The endpoints are accessible at /api/user-feedbacks/.

    Tests:
    -------
    - test_list_user_feedback: Verifies the list endpoint returns 200 OK and includes feedback.
    - test_retrieve_user_feedback: Checks the retrieve endpoint returns 200 OK and correct data.
    - test_create_user_feedback: Tests the create endpoint returns 201 Created with valid data.
    - test_update_user_feedback: Tests the update endpoint returns 200 OK.
    - test_destroy_user_feedback: Tests the destroy endpoint returns 204 No Content.
    - test_list_user_feedback_disabled: Tests the list endpoint returns 405 when disabled.
    - test_retrieve_user_feedback_disabled: Tests the retrieve endpoint returns 405 when disabled.
    - test_create_user_feedback_invalid_action: Tests validation failure for non-existent action_id.
    """

    def test_list_user_feedback(
        self,
        api_client: APIClient,
        user_feedback: UserFeedback,
        admin_user: User,
    ):
        """
        Test the list endpoint for UserFeedback.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_feedback (UserFeedback): A sample UserFeedback instance.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains a 'results' key with feedback, including action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_list = True  # Enable list method
        config.api_user_feedback_extra_permission_class = None

        url = reverse("user-feedback-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."
        assert (
            response.data["results"][0]["id"] == user_feedback.id
        ), f"Expected ID {user_feedback.id}, got {response.data['results'][0]['id']}."
        assert response.data["results"][0]["action"] == str(
            user_feedback.action
        ), f"Expected action {str(user_feedback.action)}, got {response.data['results'][0]['action']}."
        assert (
            "action_id" not in response.data["results"][0]
        ), "Expected 'action_id' to be absent in response."

    def test_retrieve_user_feedback(
        self,
        api_client: APIClient,
        user_feedback: UserFeedback,
        admin_user: User,
    ):
        """
        Test the retrieve endpoint for UserFeedback.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_feedback (UserFeedback): The UserFeedback instance to retrieve.
            admin_user (User): The admin user for authentication.

        Asserts:
            The response status code is 200.
            The response data contains the correct UserFeedback ID, feedback_text, and action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_retrieve = True  # Enable retrieve method

        url = reverse("user-feedback-detail", kwargs={"pk": user_feedback.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == user_feedback.id
        ), f"Expected ID {user_feedback.id}, got {response.data['id']}."
        assert (
            response.data["feedback_text"] == user_feedback.feedback_text
        ), f"Expected feedback_text {user_feedback.feedback_text}, got {response.data['feedback_text']}."
        assert response.data["action"] == str(
            user_feedback.action
        ), f"Expected action {str(user_feedback.action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_create_user_feedback(
        self,
        api_client: APIClient,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the create endpoint for UserFeedback.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            journey_action (JourneyAction): The action to associate with the feedback.
            admin_user (User): The admin user creating the feedback.

        Asserts:
            The response status code is 201.
            The created feedback has the correct data, including action string.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_create = True  # Enable create method

        url = reverse("user-feedback-list")
        payload = {
            "feedback_text": "Great experience!",
            "emotion": "happy",
            "intensity": 4,
            "is_positive": True,
            "action_id": journey_action.id,
        }
        response = api_client.post(url, payload, format="json")

        assert (
            response.status_code == 201
        ), f"Expected 201 Created, got {response.status_code}."
        assert (
            response.data["feedback_text"] == payload["feedback_text"]
        ), f"Expected feedback_text {payload['feedback_text']}, got {response.data['feedback_text']}."
        assert response.data["action"] == str(
            journey_action
        ), f"Expected action {str(journey_action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_update_user_feedback(
        self,
        api_client: APIClient,
        user_feedback: UserFeedback,
        journey_action: JourneyAction,
        admin_user: User,
    ):
        """
        Test the update endpoint for UserFeedback.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_feedback (UserFeedback): The UserFeedback instance to update.
            journey_action (JourneyAction): A different action to update to.
            admin_user (User): The admin user updating the feedback.

        Asserts:
            The response status code is 200.
            The updated feedback reflects the new data, including new action.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_update = True  # Enable update method

        url = reverse("user-feedback-detail", kwargs={"pk": user_feedback.pk})
        payload = {"feedback_text": "Updated feedback", "action_id": journey_action.id}
        response = api_client.patch(url, payload, format="json")

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["feedback_text"] == payload["feedback_text"]
        ), f"Expected feedback_text {payload['feedback_text']}, got {response.data['feedback_text']}."
        assert response.data["action"] == str(
            journey_action
        ), f"Expected action {str(journey_action)}, got {response.data['action']}."
        assert (
            "action_id" not in response.data
        ), "Expected 'action_id' to be absent in response."

    def test_destroy_user_feedback(
        self,
        api_client: APIClient,
        user_feedback: UserFeedback,
        admin_user: User,
    ):
        """
        Test the destroy endpoint for UserFeedback.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            user_feedback (UserFeedback): The UserFeedback instance to delete.
            admin_user (User): The admin user deleting the feedback.

        Asserts:
            The response status code is 204.
            The feedback is removed from the database.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_delete = True  # Enable destroy method

        url = reverse("user-feedback-detail", kwargs={"pk": user_feedback.pk})
        response = api_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Expected 204 No Content, got {response.status_code}."
        assert not UserFeedback.objects.filter(
            pk=user_feedback.pk
        ).exists(), "Feedback was not deleted."

    def test_list_user_feedback_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user_feedback: UserFeedback,
    ):
        """
        Test the list view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_feedback (UserFeedback): A sample UserFeedback instance.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_list = False  # Disable list method

        url = reverse("user-feedback-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_user_feedback_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user_feedback: UserFeedback,
    ):
        """
        Test the retrieve view when disabled via configuration.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.
            user_feedback (UserFeedback): The UserFeedback instance to retrieve.

        Asserts:
            The response status code is 405.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_retrieve = False  # Disable retrieve method

        url = reverse("user-feedback-detail", kwargs={"pk": user_feedback.pk})
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_create_user_feedback_invalid_action(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the create endpoint with an invalid action_id.

        Args:
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user creating the feedback.

        Asserts:
            The response status code is 400.
            The error message indicates an invalid action_id.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_user_feedback_allow_create = True  # Enable create method

        url = reverse("user-feedback-list")
        payload = {
            "feedback_text": "Invalid feedback",
            "emotion": "confused",
            "intensity": 3,
            "is_positive": False,
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
