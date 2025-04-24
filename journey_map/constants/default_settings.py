from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None
    admin_has_add_permission: bool = True
    admin_has_change_permission: bool = True
    admin_has_delete_permission: bool = True
    admin_has_module_permission: bool = True
    include_inlines: bool = True
    admin_inline_has_add_permission: bool = True
    admin_inline_has_change_permission: bool = True
    admin_inline_has_delete_permission: bool = True


@dataclass(frozen=True)
class DefaultSerializerSettings:
    user_journey_serializer_class: Optional[str] = None
    journey_stage_serializer_class: Optional[str] = None
    journey_action_serializer_class: Optional[str] = None
    user_feedback_serializer_class: Optional[str] = None
    pain_point_serializer_class: Optional[str] = None
    opportunity_serializer_class: Optional[str] = None


@dataclass(frozen=True)
class DefaultThrottleSettings:
    base_user_throttle_rate: str = "30/minute"
    staff_user_throttle_rate: str = "100/minute"
    throttle_class: str = "journey_map.api.throttlings.RoleBasedUserRateThrottle"


@dataclass(frozen=True)
class DefaultAPISettings:
    allow_list: bool = True
    allow_retrieve: bool = True
    allow_create: bool = True
    allow_update: bool = True
    allow_delete: bool = True
    pagination_class: str = "journey_map.api.paginations.DefaultLimitOffSetPagination"
    extra_permission_class: Optional[str] = None
    parser_classes: List[str] = field(
        default_factory=lambda: [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.MultiPartParser",
            "rest_framework.parsers.FormParser",
        ]
    )


@dataclass(frozen=True)
class DefaultUserJourneyAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(
        default_factory=lambda: ["created_at", "updated_at"]
    )
    search_fields: List[str] = field(default_factory=lambda: ["name", "description"])


@dataclass(frozen=True)
class DefaultJourneyStageAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["order"])
    search_fields: List[str] = field(
        default_factory=lambda: ["stage_name", "journey__name"]
    )


@dataclass(frozen=True)
class DefaultJourneyActionAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["order"])
    search_fields: List[str] = field(
        default_factory=lambda: ["action_description", "touchpoint"]
    )


@dataclass(frozen=True)
class DefaultUserFeedbackAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(
        default_factory=lambda: ["created_at", "intensity", "is_positive"]
    )
    search_fields: List[str] = field(default_factory=lambda: ["feedback_text"])


@dataclass(frozen=True)
class DefaultPainPointAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["severity"])
    search_fields: List[str] = field(default_factory=lambda: ["description"])


@dataclass(frozen=True)
class DefaultOpportunityAPISettings:
    filterset_class: Optional[str] = None
    ordering_fields: List[str] = field(default_factory=lambda: ["action__order"])
    search_fields: List[str] = field(default_factory=lambda: ["description"])


@dataclass(frozen=True)
class DefaultViewSettings:
    permission_class: Optional[str] = "journey_map.permissions.IsAuthenticated"


admin_settings: DefaultAdminSettings = DefaultAdminSettings()
serializer_settings = DefaultSerializerSettings()
throttle_settings = DefaultThrottleSettings()
api_settings = DefaultAPISettings()
user_journey_api_settings = DefaultUserJourneyAPISettings()
journey_stage_api_settings = DefaultJourneyStageAPISettings()
journey_action_api_settings = DefaultJourneyActionAPISettings()
pain_point_api_settings = DefaultPainPointAPISettings()
opportunity_api_settings = DefaultOpportunityAPISettings()
user_feedback_api_settings = DefaultUserFeedbackAPISettings()
view_settings = DefaultViewSettings()
