from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("new/<str:report_type>/", views.report_create_view, name="create"),
    path("<int:pk>/edit/", views.report_update_view, name="update"),
    path("<int:pk>/delete/", views.report_delete_view, name="delete"),
    path("<int:pk>/", views.report_detail_view, name="detail"),
]