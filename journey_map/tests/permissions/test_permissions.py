import pytest
import sys
from django.http import HttpRequest
from django.views.generic import View
from journey_map.permissions import (
    BasePermission,
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsSuperUser,
)
from journey_map.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON
from django.contrib.auth.models import User

pytestmark = [
    pytest.mark.permissions,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestPermissions:
    """Test suite for permission classes in the journey_map application.

    This class contains tests for all permission classes to ensure they correctly
    enforce access control rules for different types of users.
    """

    def test_base_perm(self, request_factory: pytest.fixture, view: View) -> None:
        """Test that BasePermission raises NotImplementedError.

        Args:
            request_factory: Pytest fixture for creating request objects
            view: A generic Django view instance for testing

        Raises:
            pytest.raises: Expects NotImplementedError for both permission methods
        """
        request: HttpRequest = request_factory.get("/")
        request.user = None
        with pytest.raises(NotImplementedError):
            BasePermission().has_permission(request, view)

        with pytest.raises(NotImplementedError):
            BasePermission().has_object_permission(request, view, object())

    def test_allow_any(self, request_factory: pytest.fixture, view: View) -> None:
        """Test that AllowAny permission always grants access.

        Args:
            request_factory: Pytest fixture for creating request objects
            view: A generic Django view instance for testing
        """
        request: HttpRequest = request_factory.get("/")
        request.user = None
        assert AllowAny().has_permission(request, view), "AllowAny failed"
        assert AllowAny().has_object_permission(
            request, view, object()
        ), "AllowAny object permission failed"

    def test_is_authenticated(
        self,
        request_factory: pytest.fixture,
        user: User,
        admin_user: User,
        view: View,
    ) -> None:
        """Test IsAuthenticated permission with different user types.

        Args:
            request_factory: Pytest fixture for creating request objects
            user: Regular user fixture
            admin_user: Admin user fixture
            view: A generic Django view instance for testing
        """
        request: HttpRequest = request_factory.get("/")
        request.user = None
        assert not IsAuthenticated().has_permission(
            request, view
        ), "IsAuthenticated passed for anonymous user"

        for test_user in [user, admin_user]:
            request.user = test_user
            assert IsAuthenticated().has_permission(
                request, view
            ), f"IsAuthenticated failed for {test_user}"
            assert IsAuthenticated().has_object_permission(
                request, view, object()
            ), f"IsAuthenticated object permission failed for {test_user}"

    def test_is_admin_user(
        self,
        request_factory: pytest.fixture,
        user: User,
        admin_user: User,
        view: View,
    ) -> None:
        """Test IsAdminUser permission with different user types.

        Args:
            request_factory: Pytest fixture for creating request objects
            user: Regular user fixture
            admin_user: Admin user fixture
            view: A generic Django view instance for testing
        """
        request: HttpRequest = request_factory.get("/")
        for test_user in [None, user]:
            request.user = test_user
            assert not IsAdminUser().has_permission(
                request, view
            ), f"IsAdminUser passed for {test_user}"

        request.user = admin_user
        assert IsAdminUser().has_permission(
            request, view
        ), "IsAdminUser failed for admin user"
        assert IsAdminUser().has_object_permission(
            request, view, object()
        ), "IsAdminUser object permission failed for admin user"

    def test_is_superuser(
        self,
        request_factory: pytest.fixture,
        user: User,
        admin_user: User,
        view: View,
    ) -> None:
        """Test IsSuperUser permission with different user types.

        Args:
            request_factory: Pytest fixture for creating request objects
            user: Regular user fixture
            admin_user: Admin user fixture (must be a superuser)
            view: A generic Django view instance for testing
        """
        request: HttpRequest = request_factory.get("/")
        request.user = user
        assert not IsSuperUser().has_permission(
            request, view
        ), f"IsSuperUser passed for regular user {user}"

        request.user = admin_user
        assert IsSuperUser().has_permission(
            request, view
        ), "IsSuperUser failed for superuser"
        assert IsSuperUser().has_object_permission(
            request, view, object()
        ), "IsSuperUser object permission failed for superuser"
