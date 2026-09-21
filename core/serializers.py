from rest_framework import serializers
from .models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Testimonial
        fields = ["id", "user", "rating", "comment", "created_at"]
        read_only_fields = ["user"]