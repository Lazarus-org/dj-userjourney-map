import pytest
from django.contrib.auth import get_user_model
from journey_map.models import (
    UserJourney,
    JourneyStage,
    JourneyAction,
    UserFeedback,
    PainPoint,
    Opportunity,
)
from persona_manager.models import UserPersona

User = get_user_model()


@pytest.fixture
def persona(db) -> UserPersona:
    """
    Fixture to create a UserPersona instance.

    Creates a Persona with a default name and description, useful for associating
    with UserJourney instances.

    Args:
        db: Pytest fixture to enable database access.

    Returns:
        UserPersona: The created UserPersona instance.
    """
    persona = UserPersona.objects.create(
        persona_name="Test Persona",
        description="A sample persona for testing",
    )
    return persona


@pytest.fixture
def user_journey(db, persona) -> UserJourney:
    """
    Fixture to create a UserJourney instance linked to a Persona.

    Creates a UserJourney with a default name and description, associated with the
    provided persona.

    Args:
        db: Pytest fixture to enable database access.
        persona: The Persona fixture to associate with the journey.

    Returns:
        UserJourney: The created UserJourney instance.
    """
    return UserJourney.objects.create(
        name="Test Journey",
        description="A sample user journey for testing",
        persona=persona,
    )


@pytest.fixture
def journey_stage(db, user_journey) -> JourneyStage:
    """
    Fixture to create a JourneyStage instance linked to a UserJourney.

    Creates a JourneyStage with a default name and order, associated with the
    provided user journey.

    Args:
        db: Pytest fixture to enable database access.
        user_journey: The UserJourney fixture to associate with the stage.

    Returns:
        JourneyStage: The created JourneyStage instance.
    """
    return JourneyStage.objects.create(
        journey=user_journey,
        stage_name="Discovery",
        order=1,
    )


@pytest.fixture
def journey_action(db, journey_stage) -> JourneyAction:
    """
    Fixture to create a JourneyAction instance linked to a JourneyStage.

    Creates a JourneyAction with a default description, touchpoint, and order,
    associated with the provided journey stage.

    Args:
        db: Pytest fixture to enable database access.
        journey_stage: The JourneyStage fixture to associate with the action.

    Returns:
        JourneyAction: The created JourneyAction instance.
    """
    return JourneyAction.objects.create(
        stage=journey_stage,
        action_description="Click on signup button",
        touchpoint="Website homepage",
        order=1,
    )


@pytest.fixture
def user_feedback(db, journey_action) -> UserFeedback:
    """
    Fixture to create a UserFeedback instance linked to a JourneyAction.

    Creates a UserFeedback with default text, emotion, intensity, and positivity,
    associated with the provided journey action.

    Args:
        db: Pytest fixture to enable database access.
        journey_action: The JourneyAction fixture to associate with the feedback.

    Returns:
        UserFeedback: The created UserFeedback instance.
    """
    return UserFeedback.objects.create(
        action=journey_action,
        feedback_text="The button was hard to find",
        emotion="Frustration",
        intensity=3,
        is_positive=False,
    )


@pytest.fixture
def pain_point(db, journey_action) -> PainPoint:
    """
    Fixture to create a PainPoint instance linked to a JourneyAction.

    Creates a PainPoint with a default description and severity,
    associated with the provided journey action.

    Args:
        db: Pytest fixture to enable database access.
        journey_action: The JourneyAction fixture to associate with the pain point.

    Returns:
        PainPoint: The created PainPoint instance.
    """
    return PainPoint.objects.create(
        action=journey_action,
        description="Confusing button placement",
        severity=4,
    )


@pytest.fixture
def opportunity(db, journey_action) -> Opportunity:
    """
    Fixture to create an Opportunity instance linked to a JourneyAction.

    Creates an Opportunity with a default description,
    associated with the provided journey action.

    Args:
        db: Pytest fixture to enable database access.
        journey_action: The JourneyAction fixture to associate with the opportunity.

    Returns:
        Opportunity: The created Opportunity instance.
    """
    return Opportunity.objects.create(
        action=journey_action,
        description="Add a tooltip for the signup button",
    )