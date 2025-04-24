from rest_framework.routers import DefaultRouter

from journey_map.api.views import (
    JourneyActionViewSet,
    JourneyStageViewSet,
    OpportunityViewSet,
    PainPointViewSet,
    UserFeedbackViewSet,
    UserJourneyViewSet,
)

router = DefaultRouter()
router.register(r"user-journeys", UserJourneyViewSet, basename="user-journey")
router.register(r"journey-stages", JourneyStageViewSet, basename="journey-stage")
router.register(r"journey-actions", JourneyActionViewSet, basename="journey-action")
router.register(r"user-feedback", UserFeedbackViewSet, basename="user-feedback")
router.register(r"pain-points", PainPointViewSet, basename="pain-point")
router.register(r"opportunities", OpportunityViewSet, basename="opportunity")
