from django.urls import path
from . import views
app_name = "reservations"
urlpatterns = [path("history/", views.history, name="history"), path("admin/", views.admin_list, name="admin_list"), path("admin/<int:pk>/<str:state>/", views.transition, name="transition"), path("package/<int:package_pk>/", views.create, name="create"), path("<int:pk>/", views.detail, name="detail")]
