from django.urls import path

from journey_map.views import JourneyMapDetailView, JourneyMapListView


urlpatterns = [
    path("journeys/", JourneyMapListView.as_view(), name="journey_map_list"),
    path(
        "journeys/<int:journey_id>/",
        JourneyMapDetailView.as_view(),
        name="journey_map_detail",
    ),
]
