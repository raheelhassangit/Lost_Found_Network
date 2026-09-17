from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_list_view, name="list"),
    path("mine/", views.my_reports_view, name="my_reports"),
    path("matches/", views.my_matches_view, name="my_matches"),
    path("new/<str:report_type>/", views.report_create_view, name="create"),
    path("<int:pk>/", views.report_detail_view, name="detail"),
    path("<int:pk>/edit/", views.report_update_view, name="update"),
    path("<int:pk>/delete/", views.report_delete_view, name="delete"),
    path("<int:pk>/close/", views.report_close_view, name="close"),
]