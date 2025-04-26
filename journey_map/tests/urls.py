from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('journey_map/', include("journey_map.urls")),
    path('journey_map/', include("journey_map.api.routers"))
]
