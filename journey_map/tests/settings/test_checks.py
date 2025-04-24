import sys
from unittest.mock import MagicMock, patch

import pytest

from journey_map.settings.checks import check_journey_map_settings
from journey_map.tests.constants import (
    PYTHON_VERSION,
    PYTHON_VERSION_REASON,
)

pytestmark = [
    pytest.mark.settings,
    pytest.mark.settings_checks,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestJourneyMapSettings:
    @patch("journey_map.settings.checks.config")
    def test_valid_settings(self, mock_config: MagicMock) -> None:
        """
        Test that valid settings produce no errors.

        Args:
            mock_config (MagicMock): Mocked configuration object with valid settings.

        Asserts:
            No errors are returned when all settings are valid.
        """
        # Mock all config values to be valid
        # Admin settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.admin_inline_has_add_permission = True
        mock_config.admin_inline_has_change_permission = False
        mock_config.admin_inline_has_delete_permission = True
        mock_config.admin_include_inlines = True

        # Global API settings
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.api_throttle_classes = None
        mock_config.api_pagination_class = None
        mock_config.api_parser_classes = []
        mock_config.api_extra_permission_class = None
        mock_config.admin_site_class = None

        # UserJourney API settings
        mock_config.api_user_journey_serializer_class = None
        mock_config.api_user_journey_ordering_fields = ["name", "created_at"]
        mock_config.api_user_journey_search_fields = ["name", "description"]
        mock_config.api_user_journey_filterset_class = None
        mock_config.api_user_journey_allow_list = True
        mock_config.api_user_journey_allow_retrieve = False
        mock_config.api_user_journey_allow_create = True
        mock_config.api_user_journey_allow_update = False
        mock_config.api_user_journey_allow_delete = True

        # JourneyStage API settings
        mock_config.api_journey_stage_serializer_class = None
        mock_config.api_journey_stage_ordering_fields = ["stage_name", "order"]
        mock_config.api_journey_stage_search_fields = ["stage_name"]
        mock_config.api_journey_stage_filterset_class = None
        mock_config.api_journey_stage_allow_list = True
        mock_config.api_journey_stage_allow_retrieve = False
        mock_config.api_journey_stage_allow_create = True
        mock_config.api_journey_stage_allow_update = False
        mock_config.api_journey_stage_allow_delete = True

        # JourneyAction API settings
        mock_config.api_journey_action_serializer_class = None
        mock_config.api_journey_action_ordering_fields = ["action_description", "order"]
        mock_config.api_journey_action_search_fields = [
            "action_description",
            "touchpoint",
        ]
        mock_config.api_journey_action_filterset_class = None
        mock_config.api_journey_action_allow_list = True
        mock_config.api_journey_action_allow_retrieve = False
        mock_config.api_journey_action_allow_create = True
        mock_config.api_journey_action_allow_update = False
        mock_config.api_journey_action_allow_delete = True

        # UserFeedback API settings
        mock_config.api_user_feedback_serializer_class = None
        mock_config.api_user_feedback_ordering_fields = ["intensity", "is_positive"]
        mock_config.api_user_feedback_search_fields = ["feedback_text"]
        mock_config.api_user_feedback_filterset_class = None
        mock_config.api_user_feedback_allow_list = True
        mock_config.api_user_feedback_allow_retrieve = False
        mock_config.api_user_feedback_allow_create = True
        mock_config.api_user_feedback_allow_update = False
        mock_config.api_user_feedback_allow_delete = True

        # PainPoint API settings
        mock_config.api_pain_point_serializer_class = None
        mock_config.api_pain_point_ordering_fields = ["severity", "description"]
        mock_config.api_pain_point_search_fields = ["description"]
        mock_config.api_pain_point_filterset_class = None
        mock_config.api_pain_point_allow_list = True
        mock_config.api_pain_point_allow_retrieve = False
        mock_config.api_pain_point_allow_create = True
        mock_config.api_pain_point_allow_update = False
        mock_config.api_pain_point_allow_delete = True

        # Opportunity API settings
        mock_config.api_opportunity_serializer_class = None
        mock_config.api_opportunity_ordering_fields = ["description"]
        mock_config.api_opportunity_search_fields = ["description"]
        mock_config.api_opportunity_filterset_class = None
        mock_config.api_opportunity_allow_list = True
        mock_config.api_opportunity_allow_retrieve = False
        mock_config.api_opportunity_allow_create = True
        mock_config.api_opportunity_allow_update = False
        mock_config.api_opportunity_allow_delete = True

        mock_config.get_setting.side_effect = lambda name, default: default
        mock_config.prefix = "JOURNEY_MAP_"

        errors = check_journey_map_settings(None)
        assert not errors, f"Expected no errors for valid settings, but got {errors}"

    @patch("journey_map.settings.checks.config")
    def test_invalid_boolean_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid boolean settings return errors.

        Args:
            mock_config (MagicMock): Mocked configuration object with invalid boolean settings.

        Asserts:
            Errors are returned for invalid boolean values in settings.
        """
        # Set valid defaults for non-boolean settings
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.api_throttle_classes = None
        mock_config.api_pagination_class = None
        mock_config.api_parser_classes = []
        mock_config.api_extra_permission_class = None
        mock_config.admin_site_class = None
        mock_config.api_user_journey_serializer_class = None
        mock_config.api_user_journey_ordering_fields = ["name", "created_at"]
        mock_config.api_user_journey_search_fields = ["name", "description"]
        mock_config.api_user_journey_filterset_class = None
        mock_config.api_journey_stage_serializer_class = None
        mock_config.api_journey_stage_ordering_fields = ["stage_name", "order"]
        mock_config.api_journey_stage_search_fields = ["stage_name"]
        mock_config.api_journey_stage_filterset_class = None
        mock_config.api_journey_action_serializer_class = None
        mock_config.api_journey_action_ordering_fields = ["action_description", "order"]
        mock_config.api_journey_action_search_fields = [
            "action_description",
            "touchpoint",
        ]
        mock_config.api_journey_action_filterset_class = None
        mock_config.api_user_feedback_serializer_class = None
        mock_config.api_user_feedback_ordering_fields = ["intensity", "is_positive"]
        mock_config.api_user_feedback_search_fields = ["feedback_text"]
        mock_config.api_user_feedback_filterset_class = None
        mock_config.api_pain_point_serializer_class = None
        mock_config.api_pain_point_ordering_fields = ["severity", "description"]
        mock_config.api_pain_point_search_fields = ["description"]
        mock_config.api_pain_point_filterset_class = None
        mock_config.api_opportunity_serializer_class = None
        mock_config.api_opportunity_ordering_fields = ["description"]
        mock_config.api_opportunity_search_fields = ["description"]
        mock_config.api_opportunity_filterset_class = None

        # Invalid boolean settings
        mock_config.admin_has_add_permission = "not_boolean"
        mock_config.admin_has_change_permission = "not_boolean"
        mock_config.admin_has_delete_permission = "not_boolean"
        mock_config.admin_has_module_permission = "not_boolean"
        mock_config.admin_inline_has_add_permission = "not_boolean"
        mock_config.admin_inline_has_change_permission = "not_boolean"
        mock_config.admin_inline_has_delete_permission = "not_boolean"
        mock_config.admin_include_inlines = "not_boolean"
        mock_config.api_user_journey_allow_list = "not_boolean"
        mock_config.api_user_journey_allow_retrieve = "not_boolean"
        mock_config.api_user_journey_allow_create = "not_boolean"
        mock_config.api_user_journey_allow_update = "not_boolean"
        mock_config.api_user_journey_allow_delete = "not_boolean"
        mock_config.api_journey_stage_allow_list = "not_boolean"
        mock_config.api_journey_stage_allow_retrieve = "not_boolean"
        mock_config.api_journey_stage_allow_create = "not_boolean"
        mock_config.api_journey_stage_allow_update = "not_boolean"
        mock_config.api_journey_stage_allow_delete = "not_boolean"
        mock_config.api_journey_action_allow_list = "not_boolean"
        mock_config.api_journey_action_allow_retrieve = "not_boolean"
        mock_config.api_journey_action_allow_create = "not_boolean"
        mock_config.api_journey_action_allow_update = "not_boolean"
        mock_config.api_journey_action_allow_delete = "not_boolean"
        mock_config.api_user_feedback_allow_list = "not_boolean"
        mock_config.api_user_feedback_allow_retrieve = "not_boolean"
        mock_config.api_user_feedback_allow_create = "not_boolean"
        mock_config.api_user_feedback_allow_update = "not_boolean"
        mock_config.api_user_feedback_allow_delete = "not_boolean"
        mock_config.api_pain_point_allow_list = "not_boolean"
        mock_config.api_pain_point_allow_retrieve = "not_boolean"
        mock_config.api_pain_point_allow_create = "not_boolean"
        mock_config.api_pain_point_allow_update = "not_boolean"
        mock_config.api_pain_point_allow_delete = "not_boolean"
        mock_config.api_opportunity_allow_list = "not_boolean"
        mock_config.api_opportunity_allow_retrieve = "not_boolean"
        mock_config.api_opportunity_allow_create = "not_boolean"
        mock_config.api_opportunity_allow_update = "not_boolean"
        mock_config.api_opportunity_allow_delete = "not_boolean"

        mock_config.get_setting.side_effect = lambda name, default: default
        mock_config.prefix = "JOURNEY_MAP_"

        errors = check_journey_map_settings(None)
        assert (
            len(errors) == 38
        ), f"Expected 38 errors for invalid booleans, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"journey_map.E001_{mock_config.prefix}ADMIN_HAS_ADD_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_HAS_DELETE_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_HAS_MODULE_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_INLINE_HAS_ADD_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_INLINE_HAS_CHANGE_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_INLINE_HAS_DELETE_PERMISSION",
            f"journey_map.E001_{mock_config.prefix}ADMIN_INCLUDE_INLINES",
            f"journey_map.E001_{mock_config.prefix}API_USER_JOURNEY_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_USER_JOURNEY_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_USER_JOURNEY_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_USER_JOURNEY_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_USER_JOURNEY_ALLOW_DELETE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_STAGE_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_STAGE_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_STAGE_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_STAGE_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_STAGE_ALLOW_DELETE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_ACTION_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_ACTION_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_ACTION_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_ACTION_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_JOURNEY_ACTION_ALLOW_DELETE",
            f"journey_map.E001_{mock_config.prefix}API_USER_FEEDBACK_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_USER_FEEDBACK_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_USER_FEEDBACK_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_USER_FEEDBACK_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_USER_FEEDBACK_ALLOW_DELETE",
            f"journey_map.E001_{mock_config.prefix}API_PAIN_POINT_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_PAIN_POINT_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_PAIN_POINT_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_PAIN_POINT_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_PAIN_POINT_ALLOW_DELETE",
            f"journey_map.E001_{mock_config.prefix}API_OPPORTUNITY_ALLOW_LIST",
            f"journey_map.E001_{mock_config.prefix}API_OPPORTUNITY_ALLOW_RETRIEVE",
            f"journey_map.E001_{mock_config.prefix}API_OPPORTUNITY_ALLOW_CREATE",
            f"journey_map.E001_{mock_config.prefix}API_OPPORTUNITY_ALLOW_UPDATE",
            f"journey_map.E001_{mock_config.prefix}API_OPPORTUNITY_ALLOW_DELETE",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("journey_map.settings.checks.config")
    def test_invalid_list_settings(self, mock_config: MagicMock) -> None:
        """
        Test that invalid list settings return errors.

        Args:
            mock_config (MagicMock): Mocked configuration object with invalid list settings.

        Asserts:
            Errors are returned for invalid list values in settings.
        """
        # Valid boolean and throttle settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.admin_inline_has_add_permission = True
        mock_config.admin_inline_has_change_permission = False
        mock_config.admin_inline_has_delete_permission = True
        mock_config.admin_include_inlines = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.api_throttle_classes = None
        mock_config.api_pagination_class = None
        mock_config.api_parser_classes = []
        mock_config.api_extra_permission_class = None
        mock_config.admin_site_class = None
        mock_config.api_user_journey_serializer_class = None
        mock_config.api_user_journey_allow_list = True
        mock_config.api_user_journey_allow_retrieve = False
        mock_config.api_user_journey_allow_create = True
        mock_config.api_user_journey_allow_update = False
        mock_config.api_user_journey_allow_delete = True
        mock_config.api_journey_stage_serializer_class = None
        mock_config.api_journey_stage_allow_list = True
        mock_config.api_journey_stage_allow_retrieve = False
        mock_config.api_journey_stage_allow_create = True
        mock_config.api_journey_stage_allow_update = False
        mock_config.api_journey_stage_allow_delete = True
        mock_config.api_journey_action_serializer_class = None
        mock_config.api_journey_action_allow_list = True
        mock_config.api_journey_action_allow_retrieve = False
        mock_config.api_journey_action_allow_create = True
        mock_config.api_journey_action_allow_update = False
        mock_config.api_journey_action_allow_delete = True
        mock_config.api_user_feedback_serializer_class = None
        mock_config.api_user_feedback_allow_list = True
        mock_config.api_user_feedback_allow_retrieve = False
        mock_config.api_user_feedback_allow_create = True
        mock_config.api_user_feedback_allow_update = False
        mock_config.api_user_feedback_allow_delete = True
        mock_config.api_pain_point_serializer_class = None
        mock_config.api_pain_point_allow_list = True
        mock_config.api_pain_point_allow_retrieve = False
        mock_config.api_pain_point_allow_create = True
        mock_config.api_pain_point_allow_update = False
        mock_config.api_pain_point_allow_delete = True
        mock_config.api_opportunity_serializer_class = None
        mock_config.api_opportunity_allow_list = True
        mock_config.api_opportunity_allow_retrieve = False
        mock_config.api_opportunity_allow_create = True
        mock_config.api_opportunity_allow_update = False
        mock_config.api_opportunity_allow_delete = True

        # Invalid list settings
        mock_config.api_user_journey_ordering_fields = []  # Empty list
        mock_config.api_user_journey_search_fields = [123]  # Invalid type
        mock_config.api_journey_stage_ordering_fields = []  # Empty list
        mock_config.api_journey_stage_search_fields = [456]  # Invalid type
        mock_config.api_journey_action_ordering_fields = []  # Empty list
        mock_config.api_journey_action_search_fields = [789]  # Invalid type
        mock_config.api_user_feedback_ordering_fields = []  # Empty list
        mock_config.api_user_feedback_search_fields = [101]  # Invalid type
        mock_config.api_pain_point_ordering_fields = []  # Empty list
        mock_config.api_pain_point_search_fields = [112]  # Invalid type
        mock_config.api_opportunity_ordering_fields = []  # Empty list
        mock_config.api_opportunity_search_fields = [131]  # Invalid type

        mock_config.get_setting.side_effect = lambda name, default: default
        mock_config.prefix = "JOURNEY_MAP_"

        errors = check_journey_map_settings(None)
        assert (
            len(errors) == 12
        ), f"Expected 12 errors for invalid lists, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"journey_map.E003_{mock_config.prefix}API_USER_JOURNEY_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_USER_JOURNEY_SEARCH_FIELDS",
            f"journey_map.E003_{mock_config.prefix}API_JOURNEY_STAGE_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_JOURNEY_STAGE_SEARCH_FIELDS",
            f"journey_map.E003_{mock_config.prefix}API_JOURNEY_ACTION_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_JOURNEY_ACTION_SEARCH_FIELDS",
            f"journey_map.E003_{mock_config.prefix}API_USER_FEEDBACK_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_USER_FEEDBACK_SEARCH_FIELDS",
            f"journey_map.E003_{mock_config.prefix}API_PAIN_POINT_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_PAIN_POINT_SEARCH_FIELDS",
            f"journey_map.E003_{mock_config.prefix}API_OPPORTUNITY_ORDERING_FIELDS",
            f"journey_map.E004_{mock_config.prefix}API_OPPORTUNITY_SEARCH_FIELDS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("journey_map.settings.checks.config")
    def test_invalid_throttle_rate(self, mock_config: MagicMock) -> None:
        """
        Test that invalid throttle rates return errors.

        Args:
            mock_config (MagicMock): Mocked configuration object with invalid throttle rates.

        Asserts:
            Errors are returned for invalid throttle rates.
        """
        # Valid boolean and list settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.admin_inline_has_add_permission = True
        mock_config.admin_inline_has_change_permission = False
        mock_config.admin_inline_has_delete_permission = True
        mock_config.admin_include_inlines = True
        mock_config.api_pagination_class = None
        mock_config.api_parser_classes = []
        mock_config.api_extra_permission_class = None
        mock_config.admin_site_class = None
        mock_config.api_user_journey_serializer_class = None
        mock_config.api_user_journey_ordering_fields = ["name", "created_at"]
        mock_config.api_user_journey_search_fields = ["name", "description"]
        mock_config.api_user_journey_filterset_class = None
        mock_config.api_user_journey_allow_list = True
        mock_config.api_user_journey_allow_retrieve = False
        mock_config.api_user_journey_allow_create = True
        mock_config.api_user_journey_allow_update = False
        mock_config.api_user_journey_allow_delete = True
        mock_config.api_journey_stage_serializer_class = None
        mock_config.api_journey_stage_ordering_fields = ["stage_name", "order"]
        mock_config.api_journey_stage_search_fields = ["stage_name"]
        mock_config.api_journey_stage_filterset_class = None
        mock_config.api_journey_stage_allow_list = True
        mock_config.api_journey_stage_allow_retrieve = False
        mock_config.api_journey_stage_allow_create = True
        mock_config.api_journey_stage_allow_update = False
        mock_config.api_journey_stage_allow_delete = True
        mock_config.api_journey_action_serializer_class = None
        mock_config.api_journey_action_ordering_fields = ["action_description", "order"]
        mock_config.api_journey_action_search_fields = [
            "action_description",
            "touchpoint",
        ]
        mock_config.api_journey_action_filterset_class = None
        mock_config.api_journey_action_allow_list = True
        mock_config.api_journey_action_allow_retrieve = False
        mock_config.api_journey_action_allow_create = True
        mock_config.api_journey_action_allow_update = False
        mock_config.api_journey_action_allow_delete = True
        mock_config.api_user_feedback_serializer_class = None
        mock_config.api_user_feedback_ordering_fields = ["intensity", "is_positive"]
        mock_config.api_user_feedback_search_fields = ["feedback_text"]
        mock_config.api_user_feedback_filterset_class = None
        mock_config.api_user_feedback_allow_list = True
        mock_config.api_user_feedback_allow_retrieve = False
        mock_config.api_user_feedback_allow_create = True
        mock_config.api_user_feedback_allow_update = False
        mock_config.api_user_feedback_allow_delete = True
        mock_config.api_pain_point_serializer_class = None
        mock_config.api_pain_point_ordering_fields = ["severity", "description"]
        mock_config.api_pain_point_search_fields = ["description"]
        mock_config.api_pain_point_filterset_class = None
        mock_config.api_pain_point_allow_list = True
        mock_config.api_pain_point_allow_retrieve = False
        mock_config.api_pain_point_allow_create = True
        mock_config.api_pain_point_allow_update = False
        mock_config.api_pain_point_allow_delete = True
        mock_config.api_opportunity_serializer_class = None
        mock_config.api_opportunity_ordering_fields = ["description"]
        mock_config.api_opportunity_search_fields = ["description"]
        mock_config.api_opportunity_filterset_class = None
        mock_config.api_opportunity_allow_list = True
        mock_config.api_opportunity_allow_retrieve = False
        mock_config.api_opportunity_allow_create = True
        mock_config.api_opportunity_allow_update = False
        mock_config.api_opportunity_allow_delete = True

        # Invalid throttle rates
        mock_config.base_user_throttle_rate = "invalid_rate"
        mock_config.staff_user_throttle_rate = "abc/hour"

        mock_config.get_setting.side_effect = lambda name, default: default
        mock_config.prefix = "JOURNEY_MAP_"

        errors = check_journey_map_settings(None)
        assert (
            len(errors) == 2
        ), f"Expected 2 errors for invalid throttle rates, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"journey_map.E005_{mock_config.prefix}BASE_USER_THROTTLE_RATE",
            f"journey_map.E007_{mock_config.prefix}STAFF_USER_THROTTLE_RATE",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"

    @patch("journey_map.settings.checks.config")
    def test_invalid_path_import(self, mock_config: MagicMock) -> None:
        """
        Test that invalid path import settings return errors.

        Args:
            mock_config (MagicMock): Mocked configuration object with invalid paths.

        Asserts:
            Errors are returned for invalid path imports.
        """
        # Valid boolean, list, and throttle settings
        mock_config.admin_has_add_permission = True
        mock_config.admin_has_change_permission = False
        mock_config.admin_has_delete_permission = True
        mock_config.admin_has_module_permission = False
        mock_config.admin_inline_has_add_permission = True
        mock_config.admin_inline_has_change_permission = False
        mock_config.admin_inline_has_delete_permission = True
        mock_config.admin_include_inlines = True
        mock_config.base_user_throttle_rate = "100/day"
        mock_config.staff_user_throttle_rate = "200/hour"
        mock_config.api_user_journey_ordering_fields = ["name", "created_at"]
        mock_config.api_user_journey_search_fields = ["name", "description"]
        mock_config.api_user_journey_allow_list = True
        mock_config.api_user_journey_allow_retrieve = False
        mock_config.api_user_journey_allow_create = True
        mock_config.api_user_journey_allow_update = False
        mock_config.api_user_journey_allow_delete = True
        mock_config.api_journey_stage_ordering_fields = ["stage_name", "order"]
        mock_config.api_journey_stage_search_fields = ["stage_name"]
        mock_config.api_journey_stage_allow_list = True
        mock_config.api_journey_stage_allow_retrieve = False
        mock_config.api_journey_stage_allow_create = True
        mock_config.api_journey_stage_allow_update = False
        mock_config.api_journey_stage_allow_delete = True
        mock_config.api_journey_action_ordering_fields = ["action_description", "order"]
        mock_config.api_journey_action_search_fields = [
            "action_description",
            "touchpoint",
        ]
        mock_config.api_journey_action_allow_list = True
        mock_config.api_journey_action_allow_retrieve = False
        mock_config.api_journey_action_allow_create = True
        mock_config.api_journey_action_allow_update = False
        mock_config.api_journey_action_allow_delete = True
        mock_config.api_user_feedback_ordering_fields = ["intensity", "is_positive"]
        mock_config.api_user_feedback_search_fields = ["feedback_text"]
        mock_config.api_user_feedback_allow_list = True
        mock_config.api_user_feedback_allow_retrieve = False
        mock_config.api_user_feedback_allow_create = True
        mock_config.api_user_feedback_allow_update = False
        mock_config.api_user_feedback_allow_delete = True
        mock_config.api_pain_point_ordering_fields = ["severity", "description"]
        mock_config.api_pain_point_search_fields = ["description"]
        mock_config.api_pain_point_allow_list = True
        mock_config.api_pain_point_allow_retrieve = False
        mock_config.api_pain_point_allow_create = True
        mock_config.api_pain_point_allow_update = False
        mock_config.api_pain_point_allow_delete = True
        mock_config.api_opportunity_ordering_fields = ["description"]
        mock_config.api_opportunity_search_fields = ["description"]
        mock_config.api_opportunity_allow_list = True
        mock_config.api_opportunity_allow_retrieve = False
        mock_config.api_opportunity_allow_create = True
        mock_config.api_opportunity_allow_update = False
        mock_config.api_opportunity_allow_delete = True

        # Invalid path imports
        mock_config.get_setting.side_effect = (
            lambda name, default: "invalid.path.ClassName"
        )

        mock_config.prefix = "JOURNEY_MAP_"

        errors = check_journey_map_settings(None)
        assert (
            len(errors) == 18
        ), f"Expected 18 errors for invalid paths, but got {len(errors)}"
        error_ids = [error.id for error in errors]
        expected_ids = [
            f"journey_map.E011_{mock_config.prefix}API_THROTTLE_CLASSES",
            f"journey_map.E010_{mock_config.prefix}API_PAGINATION_CLASS",
            f"journey_map.E011_{mock_config.prefix}API_PARSER_CLASSES",
            f"journey_map.E010_{mock_config.prefix}API_EXTRA_PERMISSION_CLASS",
            f"journey_map.E010_{mock_config.prefix}ADMIN_SITE_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_USER_JOURNEY_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_USER_JOURNEY_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_JOURNEY_STAGE_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_JOURNEY_STAGE_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_JOURNEY_ACTION_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_JOURNEY_ACTION_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_USER_FEEDBACK_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_USER_FEEDBACK_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_PAIN_POINT_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_PAIN_POINT_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_OPPORTUNITY_SERIALIZER_CLASS",
            f"journey_map.E010_{mock_config.prefix}API_OPPORTUNITY_FILTERSET_CLASS",
            f"journey_map.E010_{mock_config.prefix}VIEW_PERMISSION_CLASS",
        ]
        assert all(
            eid in error_ids for eid in expected_ids
        ), f"Expected error IDs {expected_ids}, got {error_ids}"
