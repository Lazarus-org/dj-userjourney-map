from typing import Any, List

from django.conf import settings
from django.utils.module_loading import import_string

from journey_map.constants.default_settings import (
    admin_settings,
    serializer_settings,
    throttle_settings,
    api_settings,
    user_journey_api_settings,
    opportunity_api_settings,
    pain_point_api_settings,
    user_feedback_api_settings,
    journey_stage_api_settings,
    journey_action_api_settings,
)
from journey_map.constants.types import DefaultPath, OptionalPaths


class JourneyMapConfig:
    """A configuration handler for the Django UserJourney Map, allowing
    settings to be dynamically loaded from Django settings with defaults
    provided through Default Settings.

    """

    prefix = "JOURNEY_MAP_"

    def __init__(self) -> None:
        """Initialize the Config, loading values from Django
        settings or falling back to the default settings."""

        # Admin settings (global)
        self.admin_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_ADD_PERMISSION",
            admin_settings.admin_has_add_permission,
        )
        self.admin_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_CHANGE_PERMISSION",
            admin_settings.admin_has_change_permission,
        )
        self.admin_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_DELETE_PERMISSION",
            admin_settings.admin_has_delete_permission,
        )
        self.admin_has_module_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_HAS_MODULE_PERMISSION",
            admin_settings.admin_has_module_permission,
        )
        self.admin_include_inlines: bool = self.get_setting(
            f"{self.prefix}ADMIN_INCLUDE_INLINES", admin_settings.include_inlines
        )
        self.admin_inline_has_add_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_ADD_PERMISSION",
            admin_settings.admin_inline_has_add_permission,
        )
        self.admin_inline_has_change_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_CHANGE_PERMISSION",
            admin_settings.admin_inline_has_change_permission,
        )
        self.admin_inline_has_delete_permission: bool = self.get_setting(
            f"{self.prefix}ADMIN_INLINE_HAS_DELETE_PERMISSION",
            admin_settings.admin_inline_has_delete_permission,
        )
        self.admin_site_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}ADMIN_SITE_CLASS",
            admin_settings.admin_site_class,
        )

        # Global API settings
        self.base_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}BASE_USER_THROTTLE_RATE",
            throttle_settings.base_user_throttle_rate,
        )
        self.staff_user_throttle_rate: str = self.get_setting(
            f"{self.prefix}STAFF_USER_THROTTLE_RATE",
            throttle_settings.staff_user_throttle_rate,
        )
        self.api_throttle_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_THROTTLE_CLASSES",
            throttle_settings.throttle_class,
        )
        self.api_pagination_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAGINATION_CLASS",
            api_settings.pagination_class,
        )
        self.api_extra_permission_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_EXTRA_PERMISSION_CLASS",
            api_settings.extra_permission_class,
        )
        self.api_parser_classes: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PARSER_CLASSES",
            api_settings.parser_classes,
        )

        # UserJourney-specific API settings
        self.api_user_journey_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_JOURNEY_SERIALIZER_CLASS",
            serializer_settings.user_journey_serializer_class,
        )
        self.api_user_journey_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ORDERING_FIELDS",
            user_journey_api_settings.ordering_fields,
        )
        self.api_user_journey_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_SEARCH_FIELDS",
            user_journey_api_settings.search_fields,
        )
        self.api_user_journey_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_JOURNEY_FILTERSET_CLASS",
            user_journey_api_settings.filterset_class,
        )
        self.api_user_journey_allow_list: bool = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_user_journey_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_user_journey_allow_create: bool = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_user_journey_allow_update: bool = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_user_journey_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_USER_JOURNEY_ALLOW_DELETE",
            api_settings.allow_delete,
        )

        # JourneyStage-specific API settings
        self.api_journey_stage_serializer_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_JOURNEY_STAGE_SERIALIZER_CLASS",
                serializer_settings.journey_stage_serializer_class,
            )
        )
        self.api_journey_stage_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ORDERING_FIELDS",
            journey_stage_api_settings.ordering_fields,
        )
        self.api_journey_stage_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_SEARCH_FIELDS",
            journey_stage_api_settings.search_fields,
        )
        self.api_journey_stage_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_JOURNEY_STAGE_FILTERSET_CLASS",
            journey_stage_api_settings.filterset_class,
        )
        self.api_journey_stage_allow_list: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_journey_stage_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_journey_stage_allow_create: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_journey_stage_allow_update: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_journey_stage_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_STAGE_ALLOW_DELETE",
            api_settings.allow_delete,
        )

        # JourneyAction-specific API settings
        self.api_journey_action_serializer_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_JOURNEY_ACTION_SERIALIZER_CLASS",
                serializer_settings.journey_action_serializer_class,
            )
        )
        self.api_journey_action_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ORDERING_FIELDS",
            journey_action_api_settings.ordering_fields,
        )
        self.api_journey_action_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_SEARCH_FIELDS",
            journey_action_api_settings.search_fields,
        )
        self.api_journey_action_filterset_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_JOURNEY_ACTION_FILTERSET_CLASS",
                journey_action_api_settings.filterset_class,
            )
        )
        self.api_journey_action_allow_list: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_journey_action_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_journey_action_allow_create: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_journey_action_allow_update: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_journey_action_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_JOURNEY_ACTION_ALLOW_DELETE",
            api_settings.allow_delete,
        )

        # UserFeedback-specific API settings
        self.api_user_feedback_serializer_class: OptionalPaths = (
            self.get_optional_paths(
                f"{self.prefix}API_USER_FEEDBACK_SERIALIZER_CLASS",
                serializer_settings.user_feedback_serializer_class,
            )
        )
        self.api_user_feedback_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ORDERING_FIELDS",
            user_feedback_api_settings.ordering_fields,
        )
        self.api_user_feedback_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_SEARCH_FIELDS",
            user_feedback_api_settings.search_fields,
        )
        self.api_user_feedback_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_USER_FEEDBACK_FILTERSET_CLASS",
            user_feedback_api_settings.filterset_class,
        )
        self.api_user_feedback_allow_list: bool = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_user_feedback_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_user_feedback_allow_create: bool = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_user_feedback_allow_update: bool = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_user_feedback_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_USER_FEEDBACK_ALLOW_DELETE",
            api_settings.allow_delete,
        )

        # PainPoint-specific API settings
        self.api_pain_point_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAIN_POINT_SERIALIZER_CLASS",
            serializer_settings.pain_point_serializer_class,
        )
        self.api_pain_point_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ORDERING_FIELDS",
            pain_point_api_settings.ordering_fields,
        )
        self.api_pain_point_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_SEARCH_FIELDS",
            pain_point_api_settings.search_fields,
        )
        self.api_pain_point_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_PAIN_POINT_FILTERSET_CLASS",
            pain_point_api_settings.filterset_class,
        )
        self.api_pain_point_allow_list: bool = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_pain_point_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_pain_point_allow_create: bool = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_pain_point_allow_update: bool = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_pain_point_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_PAIN_POINT_ALLOW_DELETE",
            api_settings.allow_delete,
        )

        # Opportunity-specific API settings
        self.api_opportunity_serializer_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_OPPORTUNITY_SERIALIZER_CLASS",
            serializer_settings.opportunity_serializer_class,
        )
        self.api_opportunity_ordering_fields: List[str] = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ORDERING_FIELDS",
            opportunity_api_settings.ordering_fields,
        )
        self.api_opportunity_search_fields: List[str] = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_SEARCH_FIELDS",
            opportunity_api_settings.search_fields,
        )
        self.api_opportunity_filterset_class: OptionalPaths = self.get_optional_paths(
            f"{self.prefix}API_OPPORTUNITY_FILTERSET_CLASS",
            opportunity_api_settings.filterset_class,
        )
        self.api_opportunity_allow_list: bool = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ALLOW_LIST",
            api_settings.allow_list,
        )
        self.api_opportunity_allow_retrieve: bool = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ALLOW_RETRIEVE",
            api_settings.allow_retrieve,
        )
        self.api_opportunity_allow_create: bool = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ALLOW_CREATE",
            api_settings.allow_create,
        )
        self.api_opportunity_allow_update: bool = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ALLOW_UPDATE",
            api_settings.allow_update,
        )
        self.api_opportunity_allow_delete: bool = self.get_setting(
            f"{self.prefix}API_OPPORTUNITY_ALLOW_DELETE",
            api_settings.allow_delete,
        )

    def get_setting(self, setting_name: str, default_value: Any) -> Any:
        """Retrieve a setting from Django settings with a default fallback.

        Args:
            setting_name (str): The name of the setting to retrieve.
            default_value (Any): The default value to return if the setting is not found.

        Returns:
            Any: The value of the setting or the default value if not found.

        """
        return getattr(settings, setting_name, default_value)

    def get_optional_paths(
        self,
        setting_name: str,
        default_path: DefaultPath,
    ) -> OptionalPaths:
        """Dynamically load a method or class path on a setting, or return None
        if the setting is None or invalid.

        Args:
            setting_name (str): The name of the setting for the method or class path.
            default_path (Optional[Union[str, List[str]]): The default import path for the method or class.

        Returns:
            Optional[Union[Type[Any], List[Type[Any]]]]: The imported method or class or None
             if import fails or the path is invalid.

        """
        _path: DefaultPath = self.get_setting(setting_name, default_path)

        if _path and isinstance(_path, str):
            try:
                return import_string(_path)
            except ImportError:
                return None
        elif _path and isinstance(_path, list):
            try:
                return [import_string(path) for path in _path if isinstance(path, str)]
            except ImportError:
                return []

        return None


config: JourneyMapConfig = JourneyMapConfig()
