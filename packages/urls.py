from django.urls import path
from . import views
app_name = "packages"
urlpatterns = [path("", views.catalog, name="catalog"), path("staff/", views.package_list, name="list"), path("staff/new/", views.package_create, name="create"), path("staff/<int:pk>/", views.staff_detail, name="staff_detail"), path("staff/<int:pk>/edit/", views.package_edit, name="edit"), path("staff/<int:pk>/publish/", views.publish, name="publish"), path("staff/<int:pk>/toggle/", views.toggle_enabled, name="toggle"), path("<int:pk>/", views.customer_detail, name="detail")]
