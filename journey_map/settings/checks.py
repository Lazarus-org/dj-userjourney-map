from typing import Any, List

from django.core.checks import Error, register

from journey_map.settings.conf import config
from journey_map.validators.config_validators import (
    validate_boolean_setting,
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
    validate_throttle_rate,
)


@register()
def check_journey_map_settings(app_configs: Any, **kwargs: Any) -> List[Error]:
    """Check and validate project settings in the Django configuration.

    This function performs validation of various project-related settings
    defined in the Django settings. It returns a list of errors if any issues are found.

    Parameters:
    -----------
    app_configs : Any
        Passed by Django during checks (not used here).

    kwargs : Any
        Additional keyword arguments for flexibility.

    Returns:
    --------
    List[Error]
        A list of `Error` objects for any detected configuration issues.

    """
    errors: List[Error] = []

    # Validate global admin settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}ADMIN_SITE_CLASS", None),
            f"{config.prefix}ADMIN_SITE_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_add_permission,
            f"{config.prefix}ADMIN_HAS_ADD_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_change_permission,
            f"{config.prefix}ADMIN_HAS_CHANGE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_delete_permission,
            f"{config.prefix}ADMIN_HAS_DELETE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_has_module_permission,
            f"{config.prefix}ADMIN_HAS_MODULE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_include_inlines,
            f"{config.prefix}ADMIN_INCLUDE_INLINES",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_inline_has_add_permission,
            f"{config.prefix}ADMIN_INLINE_HAS_ADD_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_inline_has_change_permission,
            f"{config.prefix}ADMIN_INLINE_HAS_CHANGE_PERMISSION",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.admin_inline_has_delete_permission,
            f"{config.prefix}ADMIN_INLINE_HAS_DELETE_PERMISSION",
        )
    )

    # Validate global API settings
    errors.extend(
        validate_throttle_rate(
            config.base_user_throttle_rate,
            f"{config.prefix}BASE_USER_THROTTLE_RATE",
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.staff_user_throttle_rate,
            f"{config.prefix}STAFF_USER_THROTTLE_RATE",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_THROTTLE_CLASSES", None),
            f"{config.prefix}API_THROTTLE_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGINATION_CLASS", None),
            f"{config.prefix}API_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_PARSER_CLASSES", []),
            f"{config.prefix}API_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_EXTRA_PERMISSION_CLASS", None),
            f"{config.prefix}API_EXTRA_PERMISSION_CLASS",
        )
    )

    # Validate UserJourney-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_JOURNEY_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_USER_JOURNEY_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_journey_ordering_fields,
            f"{config.prefix}API_USER_JOURNEY_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_journey_search_fields,
            f"{config.prefix}API_USER_JOURNEY_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_JOURNEY_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_USER_JOURNEY_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_journey_allow_list,
            f"{config.prefix}API_USER_JOURNEY_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_journey_allow_retrieve,
            f"{config.prefix}API_USER_JOURNEY_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_journey_allow_create,
            f"{config.prefix}API_USER_JOURNEY_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_journey_allow_update,
            f"{config.prefix}API_USER_JOURNEY_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_journey_allow_delete,
            f"{config.prefix}API_USER_JOURNEY_ALLOW_DELETE",
        )
    )

    # Validate JourneyStage-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_JOURNEY_STAGE_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_JOURNEY_STAGE_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_journey_stage_ordering_fields,
            f"{config.prefix}API_JOURNEY_STAGE_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_journey_stage_search_fields,
            f"{config.prefix}API_JOURNEY_STAGE_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_JOURNEY_STAGE_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_JOURNEY_STAGE_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_stage_allow_list,
            f"{config.prefix}API_JOURNEY_STAGE_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_stage_allow_retrieve,
            f"{config.prefix}API_JOURNEY_STAGE_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_stage_allow_create,
            f"{config.prefix}API_JOURNEY_STAGE_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_stage_allow_update,
            f"{config.prefix}API_JOURNEY_STAGE_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_stage_allow_delete,
            f"{config.prefix}API_JOURNEY_STAGE_ALLOW_DELETE",
        )
    )

    # Validate JourneyAction-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_JOURNEY_ACTION_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_JOURNEY_ACTION_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_journey_action_ordering_fields,
            f"{config.prefix}API_JOURNEY_ACTION_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_journey_action_search_fields,
            f"{config.prefix}API_JOURNEY_ACTION_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_JOURNEY_ACTION_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_JOURNEY_ACTION_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_action_allow_list,
            f"{config.prefix}API_JOURNEY_ACTION_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_action_allow_retrieve,
            f"{config.prefix}API_JOURNEY_ACTION_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_action_allow_create,
            f"{config.prefix}API_JOURNEY_ACTION_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_action_allow_update,
            f"{config.prefix}API_JOURNEY_ACTION_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_journey_action_allow_delete,
            f"{config.prefix}API_JOURNEY_ACTION_ALLOW_DELETE",
        )
    )

    # Validate UserFeedback-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_FEEDBACK_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_USER_FEEDBACK_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_feedback_ordering_fields,
            f"{config.prefix}API_USER_FEEDBACK_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_user_feedback_search_fields,
            f"{config.prefix}API_USER_FEEDBACK_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_USER_FEEDBACK_FILTERSET_CLASS", None
            ),
            f"{config.prefix}API_USER_FEEDBACK_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_feedback_allow_list,
            f"{config.prefix}API_USER_FEEDBACK_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_feedback_allow_retrieve,
            f"{config.prefix}API_USER_FEEDBACK_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_feedback_allow_create,
            f"{config.prefix}API_USER_FEEDBACK_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_feedback_allow_update,
            f"{config.prefix}API_USER_FEEDBACK_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_user_feedback_allow_delete,
            f"{config.prefix}API_USER_FEEDBACK_ALLOW_DELETE",
        )
    )

    # Validate PainPoint-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAIN_POINT_SERIALIZER_CLASS", None),
            f"{config.prefix}API_PAIN_POINT_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_pain_point_ordering_fields,
            f"{config.prefix}API_PAIN_POINT_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_pain_point_search_fields,
            f"{config.prefix}API_PAIN_POINT_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAIN_POINT_FILTERSET_CLASS", None),
            f"{config.prefix}API_PAIN_POINT_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_pain_point_allow_list,
            f"{config.prefix}API_PAIN_POINT_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_pain_point_allow_retrieve,
            f"{config.prefix}API_PAIN_POINT_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_pain_point_allow_create,
            f"{config.prefix}API_PAIN_POINT_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_pain_point_allow_update,
            f"{config.prefix}API_PAIN_POINT_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_pain_point_allow_delete,
            f"{config.prefix}API_PAIN_POINT_ALLOW_DELETE",
        )
    )

    # Validate Opportunity-specific API settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_OPPORTUNITY_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_OPPORTUNITY_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_opportunity_ordering_fields,
            f"{config.prefix}API_OPPORTUNITY_ORDERING_FIELDS",
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_opportunity_search_fields,
            f"{config.prefix}API_OPPORTUNITY_SEARCH_FIELDS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_OPPORTUNITY_FILTERSET_CLASS", None),
            f"{config.prefix}API_OPPORTUNITY_FILTERSET_CLASS",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_opportunity_allow_list,
            f"{config.prefix}API_OPPORTUNITY_ALLOW_LIST",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_opportunity_allow_retrieve,
            f"{config.prefix}API_OPPORTUNITY_ALLOW_RETRIEVE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_opportunity_allow_create,
            f"{config.prefix}API_OPPORTUNITY_ALLOW_CREATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_opportunity_allow_update,
            f"{config.prefix}API_OPPORTUNITY_ALLOW_UPDATE",
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_opportunity_allow_delete,
            f"{config.prefix}API_OPPORTUNITY_ALLOW_DELETE",
        )
    )

    # Validate Template View settings
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}VIEW_PERMISSION_CLASS", None),
            f"{config.prefix}VIEW_PERMISSION_CLASS",
        )
    )

    return errors
