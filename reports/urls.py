from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("new/<str:report_type>/", views.report_create_view, name="create"),
]