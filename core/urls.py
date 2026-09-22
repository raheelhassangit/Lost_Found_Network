from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("testimonials/add/", views.add_testimonial_view, name="add_testimonial"),
    path("support/", views.support_view, name="support"),
    path("get-api/", views.get_api_view, name="get_api"),
    path("terms/", views.terms_view, name="terms"),
    path("privacy/", views.privacy_view, name="privacy"),
]