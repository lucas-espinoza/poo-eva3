from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls), path("", include("accounts.urls")),
    path("destinations/", include("destinations.urls")), path("packages/", include("packages.urls")),
    path("reservations/", include("reservations.urls")),
]
