from django.urls import path
from .views import journey_map

urlpatterns = [
    path('journey/<int:journey_id>/', journey_map, name='journey_map'),
]