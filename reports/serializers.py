from rest_framework import serializers
from .models import Report, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Report
        fields = [
            "id", "report_type", "item_name", "description", "category", "category_name",
            "color", "location", "date", "image", "status", "user", "created_at", "updated_at",
        ]
        read_only_fields = ["status", "user"]