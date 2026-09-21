from rest_framework import viewsets, permissions
from .models import Testimonial
from .serializers import TestimonialSerializer

from accounts.permissions import HasAPIKeyScope
from accounts.models import APIKey

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.select_related("user").order_by("-created_at")
    serializer_class = TestimonialSerializer
    required_scope = APIKey.Scope.TESTIMONIALS
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, HasAPIKeyScope]
    http_method_names = ["get", "post", "head", "options"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)