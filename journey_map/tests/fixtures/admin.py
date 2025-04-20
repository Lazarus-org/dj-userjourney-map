import pytest
from django.contrib.admin import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory


from journey_map.admin import (
    UserJourneyAdmin,
    JourneyActionAdmin,
    UserFeedbackAdmin,
    OpportunityAdmin,
    PainPointAdmin,
)
from journey_map.models import (
    UserJourney,
    JourneyAction,
    UserFeedback,
    PainPoint,
    Opportunity,
)


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to provide an instance of RequestFactory.

    Returns:
    -------
        RequestFactory: An instance of Django's RequestFactory.
    """
    return RequestFactory()


@pytest.fixture
def mock_request():
    """
    Fixture to provide a mock HttpRequest object with messages support.

    Returns:
        HttpRequest: A Django HttpRequest object with messages middleware support.
    """
    request = RequestFactory().get("/")
    setattr(request, "session", "session")
    messages_storage = FallbackStorage(request)
    setattr(request, "_messages", messages_storage)
    return request


@pytest.fixture
def admin_site() -> AdminSite:
    """
    Fixture to provide an instance of AdminSite.

    Returns:
    -------
        AdminSite: An instance of Django's AdminSite.
    """
    return AdminSite()


@pytest.fixture
def user_journey_admin(admin_site: AdminSite) -> UserJourneyAdmin:
    """
    Fixture to provide an instance of UserJourneyAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        UserJourneyAdmin: An instance of UserJourneyAdmin.
    """
    return UserJourneyAdmin(UserJourney, admin_site)


@pytest.fixture
def journey_action_admin(admin_site: AdminSite) -> JourneyActionAdmin:
    """
    Fixture to provide an instance of JourneyActionAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        JourneyActionAdmin: An instance of JourneyActionAdmin.
    """
    return JourneyActionAdmin(JourneyAction, admin_site)


@pytest.fixture
def user_feedback_admin(admin_site: AdminSite) -> UserFeedbackAdmin:
    """
    Fixture to provide an instance of UserFeedbackAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        UserFeedbackAdmin: An instance of UserFeedbackAdmin.
    """
    return UserFeedbackAdmin(UserFeedback, admin_site)


@pytest.fixture
def pain_point_admin(admin_site: AdminSite) -> PainPointAdmin:
    """
    Fixture to provide an instance of PainPointAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        PainPointAdmin: An instance of PainPointAdmin.
    """
    return PainPointAdmin(PainPoint, admin_site)


@pytest.fixture
def opportunity_admin(admin_site: AdminSite) -> OpportunityAdmin:
    """
    Fixture to provide an instance of OpportunityAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        OpportunityAdmin: An instance of OpportunityAdmin.
    """
    return OpportunityAdmin(Opportunity, admin_site)
