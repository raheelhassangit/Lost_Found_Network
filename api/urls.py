from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from reports.api_views import ReportViewSet, CategoryViewSet, ReviewViewSet, MatchViewSet
from core.api_views import TestimonialViewSet

router = DefaultRouter()
router.register("reports", ReportViewSet, basename="report")
router.register("categories", CategoryViewSet, basename="category")
router.register("reviews", ReviewViewSet, basename="review")
router.register("matches", MatchViewSet, basename="match")
router.register("testimonials", TestimonialViewSet, basename="testimonial")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]