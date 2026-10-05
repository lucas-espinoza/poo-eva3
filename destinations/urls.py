from django.urls import path
from . import views

app_name = "destinations"
urlpatterns = [path("", views.destination_list, name="list"), path("new/", views.destination_create, name="create"), path("<int:pk>/edit/", views.destination_edit, name="edit"), path("<int:pk>/remove/", views.destination_remove, name="remove")]
