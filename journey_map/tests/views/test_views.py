import pytest
import sys
from django.urls import reverse
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestJourneyMapViews:
    """Test suite for JourneyMapListView and JourneyMapDetailView."""

    def test_list_view_renders_correctly(self, client, user, user_journey, persona):
        """Test that JourneyMapListView renders correctly with journey and persona data."""
        client.force_login(user)
        response = client.get(reverse("journey_map_list"))
        assert response.status_code == 200
        assert "journeys" in response.context
        assert len(response.context["journeys"]) == 1
        assert response.context["journeys"][0].name == user_journey.name
        assert (
            response.context["journeys"][0].persona.persona_name == persona.persona_name
        )
        assert user_journey.name in str(response.content)
        assert persona.persona_name in str(response.content)
        assert response.template_name == [
            "journey_map_list.html",
            "journey_map/userjourney_list.html",
        ]

    def test_list_view_empty_queryset(self, client, user):
        """Test that JourneyMapListView handles an empty queryset."""
        client.force_login(user)
        response = client.get(reverse("journey_map_list"))
        assert response.status_code == 200
        assert "journeys" in response.context
        assert len(response.context["journeys"]) == 0
        assert "No user journeys available" in str(response.content)

    def test_list_view_permission_denied(self, client, user_journey):
        """Test that JourneyMapListView denies access to anonymous users."""
        response = client.get(reverse("journey_map_list"))
        assert response.status_code == 403

    def test_list_view_permission_allowed(self, client, admin_user, user_journey):
        """Test that JourneyMapListView allows access to authorized users."""
        client.force_login(admin_user)
        response = client.get(reverse("journey_map_list"))
        assert response.status_code == 200

    def test_detail_view_renders_correctly(
        self,
        client,
        user,
        user_journey,
        persona,
        journey_stage,
        journey_action,
        user_feedback,
        pain_point,
        opportunity,
    ):
        """Test that JourneyMapDetailView renders correctly with all related data."""
        client.force_login(user)
        response = client.get(
            reverse("journey_map_detail", kwargs={"journey_id": user_journey.id})
        )
        assert response.status_code == 200
        assert "journey_data" in response.context
        journey_data = response.context["journey_data"]
        assert journey_data["journey"].name == user_journey.name
        assert journey_data["persona"].persona_name == persona.persona_name
        assert len(journey_data["stages"]) == 1
        assert journey_data["stages"][0]["stage"].stage_name == journey_stage.stage_name
        assert len(journey_data["stages"][0]["actions"]) == 1
        assert (
            journey_data["stages"][0]["actions"][0]["action"].action_description
            == journey_action.action_description
        )
        assert len(journey_data["stages"][0]["actions"][0]["feedbacks"]) == 1
        assert (
            journey_data["stages"][0]["actions"][0]["feedbacks"][0].feedback_text
            == user_feedback.feedback_text
        )
        assert len(journey_data["stages"][0]["actions"][0]["pain_points"]) == 1
        assert (
            journey_data["stages"][0]["actions"][0]["pain_points"][0].description
            == pain_point.description
        )
        assert len(journey_data["stages"][0]["actions"][0]["opportunities"]) == 1
        assert (
            journey_data["stages"][0]["actions"][0]["opportunities"][0].description
            == opportunity.description
        )
        assert user_journey.name in str(response.content)
        assert persona.persona_name in str(response.content)
        assert journey_stage.stage_name in str(response.content)
        assert journey_action.action_description in str(response.content)
        assert user_feedback.feedback_text in str(response.content)
        assert pain_point.description in str(response.content)
        assert opportunity.description in str(response.content)
        assert response.template_name == ["journey_map_detail.html"]

    def test_detail_view_empty_stages(self, client, user, user_journey, persona):
        """Test that JourneyMapDetailView handles a journey with no stages."""
        client.force_login(user)
        response = client.get(
            reverse("journey_map_detail", kwargs={"journey_id": user_journey.id})
        )
        assert response.status_code == 200
        assert "journey_data" in response.context
        assert len(response.context["journey_data"]["stages"]) == 0
        assert user_journey.name in str(response.content)
        assert persona.persona_name in str(response.content)

    def test_detail_view_404(self, client, user):
        """Test that JourneyMapDetailView returns 404 for non-existent journey."""
        client.force_login(user)
        response = client.get(reverse("journey_map_detail", kwargs={"journey_id": 999}))
        assert response.status_code == 404

    def test_detail_view_permission_denied(self, client, user_journey):
        """Test that JourneyMapDetailView denies access to anonymous users."""
        response = client.get(
            reverse("journey_map_detail", kwargs={"journey_id": user_journey.id})
        )
        assert response.status_code == 403
