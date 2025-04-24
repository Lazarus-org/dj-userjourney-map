from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import JourneyAction, JourneyStage, UserJourney
from .settings.conf import config


class BaseView:
    """Base view class for views that handles common authentication logic."""

    permission_classes = [config.view_permission_class]

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view
        requires."""
        return [permission() for permission in self.permission_classes if permission]

    def check_permissions(self, request):
        """Check if the request should be permitted, raising PermissionDenied
        if not."""
        for permission in self.get_permissions():
            if not hasattr(
                permission, "has_permission"
            ) or not permission.has_permission(request, self):
                raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        """Handle request dispatch with permission checks."""
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)


class JourneyMapListView(BaseView, ListView):
    """A class-based view to list all user journeys.

    This view displays a list of UserJourney instances, allowing users
    to select one to view its detailed journey map. Permission checks
    are applied to restrict access.

    """

    model = UserJourney
    template_name = "journey_map_list.html"
    context_object_name = "journeys"

    def get_queryset(self):
        """Return the queryset of UserJourney instances, ordered by name."""
        return UserJourney.objects.select_related("persona").order_by("name")


class JourneyMapDetailView(BaseView, DetailView):
    """A class-based view to display a detailed user journey map with persona,
    feedback, pain points, and opportunities.

    This view retrieves a UserJourney by ID, prefetches related stages,
    actions, feedbacks, pain points, and opportunities, and renders them
    in a template with a timeline view. Permission checks are applied to
    restrict access.

    """

    model = UserJourney
    template_name = "journey_map_detail.html"
    context_object_name = "journey_data"

    def get_object(self, queryset=None):
        """Retrieve the UserJourney with all related data prefetched in a
        single query."""
        journey_id = self.kwargs.get("journey_id")
        return get_object_or_404(
            UserJourney.objects.select_related("persona").prefetch_related(
                Prefetch(
                    "stages",
                    queryset=JourneyStage.objects.order_by("order").prefetch_related(
                        Prefetch(
                            "actions",
                            queryset=JourneyAction.objects.order_by(
                                "order"
                            ).prefetch_related(
                                "feedbacks",
                                "pain_points",
                                "opportunities",
                            ),
                        )
                    ),
                )
            ),
            id=journey_id,
        )

    def get_context_data(self, **kwargs):
        """Prepare context data for the template using prefetched data to avoid
        extra queries."""
        context = super().get_context_data(**kwargs)
        journey = self.object
        journey_data = {
            "journey": journey,
            "persona": journey.persona,
            "stages": [],
        }

        # Access prefetched stages and actions directly
        for stage in journey.stages.all():  # Already ordered by Prefetch
            stage_data = {"stage": stage, "actions": []}
            for action in stage.actions.all():  # Already ordered by Prefetch
                # Use prefetched related objects directly
                action_data = {
                    "action": action,
                    "feedbacks": getattr(action, "_prefetched_objects_cache", {}).get(
                        "feedbacks", []
                    ),
                    "pain_points": getattr(action, "_prefetched_objects_cache", {}).get(
                        "pain_points", []
                    ),
                    "opportunities": getattr(
                        action, "_prefetched_objects_cache", {}
                    ).get("opportunities", []),
                }
                stage_data["actions"].append(action_data)
            journey_data["stages"].append(stage_data)

        context["journey_data"] = journey_data
        return context
